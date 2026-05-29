package com.recruitment.config;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class LlmConfig {

    @Value("${llm.openai.api-key}")
    private String apiKey;

    @Value("${llm.openai.base-url}")
    private String baseUrl;

    @Value("${llm.openai.model}")
    private String model;

    @Bean
    public ChatLanguageModel chatLanguageModel() {
        return OpenAiChatModel.builder()
                .apiKey(apiKey)
                .baseUrl(baseUrl)
                .modelName(model)
                .temperature(0.7)
                .maxTokens(1024)
                .build();
    }
}
