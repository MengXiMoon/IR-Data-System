package com.recruitment.controller;

import com.recruitment.common.Result;
import com.recruitment.service.MlClientService;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/ml")
public class MlController {

    private final MlClientService mlClientService;

    public MlController(MlClientService mlClientService) {
        this.mlClientService = mlClientService;
    }

    /** 通过岗位描述文本进行聚类预测 */
    @PostMapping("/cluster")
    public Result<List<Integer>> cluster(@RequestBody List<String> texts) {
        return Result.ok(mlClientService.predictClusterByText(texts));
    }

    /** 通过岗位描述文本进行分类预测 */
    @PostMapping("/classify")
    public Result<Map<String, Object>> classify(@RequestBody List<String> texts) {
        return Result.ok(mlClientService.predictClassifyByText(texts));
    }
}
