package com.recruitment.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;
import java.util.List;
import java.util.Map;

@Service
public class MlClientService {

    private final RestTemplate restTemplate;
    private final String mlServiceUrl;

    public MlClientService(@Value("${ml.service.url}") String mlServiceUrl) {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(5000);
        factory.setReadTimeout(60000);
        this.restTemplate = new RestTemplate(factory);
        this.mlServiceUrl = mlServiceUrl;
    }

    /** 调用 Python KMeans 聚类服务 */
    @SuppressWarnings("unchecked")
    public List<Integer> predictCluster(List<List<Double>> features) {
        try {
            String url = mlServiceUrl + "/cluster/predict";
            Map<String, Object> body = Map.of("features", features);
            Map<String, Object> resp = restTemplate.postForObject(url, body, Map.class);
            if (resp != null && resp.containsKey("labels")) {
                return (List<Integer>) resp.get("labels");
            }
            return Collections.emptyList();
        } catch (Exception e) {
            throw new RuntimeException("ML 聚类服务调用失败: " + e.getMessage());
        }
    }

    /** 调用 Python 神经网络分类服务 */
    @SuppressWarnings("unchecked")
    public Map<String, Object> predictClassify(List<List<Double>> features) {
        try {
            String url = mlServiceUrl + "/classify/predict";
            Map<String, Object> body = Map.of("features", features);
            return restTemplate.postForObject(url, body, Map.class);
        } catch (Exception e) {
            throw new RuntimeException("ML 分类服务调用失败: " + e.getMessage());
        }
    }
}
