package com.recruitment.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.recruitment.dto.ChatResponse;
import com.recruitment.entity.ChatHistory;
import com.recruitment.repository.ChatHistoryMapper;
import dev.langchain4j.data.message.ChatMessage;
import dev.langchain4j.data.message.SystemMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.model.chat.ChatLanguageModel;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class AiService {

    private static final String SYSTEM_PROMPT = """
            你是一位专业的求职顾问 AI，帮助用户分析招聘信息并提供求职建议。
            你可以从技能匹配、薪资评估、职业发展等维度给出定制化建议。""";

    private final ChatLanguageModel chatModel;
    private final ChatHistoryMapper chatHistoryMapper;

    public AiService(ChatLanguageModel chatModel, ChatHistoryMapper chatHistoryMapper) {
        this.chatModel = chatModel;
        this.chatHistoryMapper = chatHistoryMapper;
    }

    public ChatResponse chat(Long userId, String sessionId, String message) {
        if (sessionId == null || sessionId.isBlank()) {
            sessionId = UUID.randomUUID().toString().substring(0, 8);
        }

        // 保存用户消息
        ChatHistory userMsg = new ChatHistory();
        userMsg.setUserId(userId);
        userMsg.setSessionId(sessionId);
        userMsg.setRole("user");
        userMsg.setContent(message);
        chatHistoryMapper.insert(userMsg);

        // 获取历史最近10轮对话作为上下文（正序）
        List<ChatHistory> history = chatHistoryMapper.selectList(
                new LambdaQueryWrapper<ChatHistory>()
                        .eq(ChatHistory::getSessionId, sessionId)
                        .orderByAsc(ChatHistory::getCreatedAt)
                        .last("LIMIT 20"));

        // 构建多轮对话消息
        List<ChatMessage> messages = new ArrayList<>();
        messages.add(new SystemMessage(SYSTEM_PROMPT));
        for (ChatHistory h : history) {
            if ("user".equals(h.getRole())) {
                messages.add(new UserMessage(h.getContent()));
            } else if ("assistant".equals(h.getRole())) {
                messages.add(new dev.langchain4j.data.message.AiMessage(h.getContent()));
            }
        }

        // 调用 LLM（多轮对话）
        String reply = chatModel.chat(messages).aiMessage().text();

        // 保存 AI 回复
        ChatHistory aiMsg = new ChatHistory();
        aiMsg.setUserId(userId);
        aiMsg.setSessionId(sessionId);
        aiMsg.setRole("assistant");
        aiMsg.setContent(reply);
        chatHistoryMapper.insert(aiMsg);

        ChatResponse resp = new ChatResponse();
        resp.setSessionId(sessionId);
        resp.setReply(reply);
        return resp;
    }

    public List<ChatHistory> getHistory(Long userId, String sessionId) {
        return chatHistoryMapper.selectList(
                new LambdaQueryWrapper<ChatHistory>()
                        .eq(ChatHistory::getUserId, userId)
                        .eq(ChatHistory::getSessionId, sessionId)
                        .orderByAsc(ChatHistory::getCreatedAt));
    }
}
