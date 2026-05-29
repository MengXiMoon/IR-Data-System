package com.recruitment.config;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class LlmConfig {

    @Value("${llm.provider}")
    private String provider;

    // OpenAI
    @Value("${llm.openai.api-key}")
    private String openAiKey;
    @Value("${llm.openai.base-url}")
    private String openAiBaseUrl;
    @Value("${llm.openai.model}")
    private String openAiModel;

    // 火山引擎
    @Value("${llm.volcengine.api-key}")
    private String volcKey;
    @Value("${llm.volcengine.base-url}")
    private String volcBaseUrl;
    @Value("${llm.volcengine.endpoint-id}")
    private String volcEndpointId;

    // 阿里百炼
    @Value("${llm.bailian.api-key}")
    private String bailianKey;
    @Value("${llm.bailian.base-url}")
    private String bailianBaseUrl;
    @Value("${llm.bailian.model}")
    private String bailianModel;

    @Bean
    public ChatLanguageModel chatLanguageModel() {
        return switch (provider) {
            case "volcengine" -> OpenAiChatModel.builder()
                    .apiKey(volcKey)
                    .baseUrl(volcBaseUrl)
                    .modelName(volcEndpointId)
                    .temperature(0.7)
                    .maxTokens(1024)
                    .build();

            case "bailian" -> OpenAiChatModel.builder()
                    .apiKey(bailianKey)
                    .baseUrl(bailianBaseUrl)
                    .modelName(bailianModel)
                    .temperature(0.7)
                    .maxTokens(1024)
                    .build();

            default -> OpenAiChatModel.builder()
                    .apiKey(openAiKey)
                    .baseUrl(openAiBaseUrl)
                    .modelName(openAiModel)
                    .temperature(0.7)
                    .maxTokens(1024)
                    .build();
        };
    }
}
