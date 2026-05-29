package com.recruitment.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class ChatRequest {
    @NotBlank(message = "消息不能为空")
    private String message;
    private String sessionId;
}

@Data
public class ChatResponse {
    private String sessionId;
    private String reply;
}

@Data
public class ClusterRequest {
    private String featureType;  // tfidf / embedding
}

@Data
public class ClassifyRequest {
    private String text;  // 岗位描述文本
}
