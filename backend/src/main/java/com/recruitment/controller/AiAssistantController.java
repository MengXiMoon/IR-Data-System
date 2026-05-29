package com.recruitment.controller;

import com.recruitment.common.Result;
import com.recruitment.dto.ChatRequest;
import com.recruitment.dto.ChatResponse;
import com.recruitment.entity.ChatHistory;
import com.recruitment.service.AiService;
import jakarta.validation.Valid;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/ai")
public class AiAssistantController {

    private final AiService aiService;

    public AiAssistantController(AiService aiService) {
        this.aiService = aiService;
    }

    @PostMapping("/chat")
    public Result<ChatResponse> chat(@Valid @RequestBody ChatRequest req) {
        Long userId = getCurrentUserId();
        return Result.ok(aiService.chat(userId, req.getSessionId(), req.getMessage()));
    }

    @GetMapping("/history/{sessionId}")
    public Result<List<ChatHistory>> history(@PathVariable String sessionId) {
        Long userId = getCurrentUserId();
        return Result.ok(aiService.getHistory(userId, sessionId));
    }

    private Long getCurrentUserId() {
        return (Long) SecurityContextHolder.getContext()
                .getAuthentication().getDetails();
    }
}
