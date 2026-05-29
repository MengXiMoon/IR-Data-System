package com.recruitment.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@RestController
public class HomeController {

    @GetMapping("/")
    public Map<String, Object> home() {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("name", "招聘数据智能系统");
        result.put("version", "1.0.0");
        result.put("apis", List.of(
                Map.of("method", "POST", "path", "/api/auth/register", "desc", "用户注册"),
                Map.of("method", "POST", "path", "/api/auth/login", "desc", "用户登录"),
                Map.of("method", "POST", "path", "/api/jobs/search", "desc", "搜索招聘数据"),
                Map.of("method", "GET", "path", "/api/charts/dashboard", "desc", "可视化数据总览"),
                Map.of("method", "POST", "path", "/api/ai/chat", "desc", "AI 智能客服"),
                Map.of("method", "POST", "path", "/api/ml/cluster", "desc", "KMeans 聚类预测"),
                Map.of("method", "POST", "path", "/api/ml/classify", "desc", "神经网络分类预测")
        ));
        result.put("docs", "先 POST /api/auth/login 获取 token，其他接口需 Authorization: Bearer <token>");
        return result;
    }
}
