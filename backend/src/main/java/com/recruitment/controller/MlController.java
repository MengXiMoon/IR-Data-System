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

    /** 调用 Python KMeans 聚类预测 */
    @PostMapping("/cluster")
    public Result<List<Integer>> cluster(@RequestBody List<List<Double>> features) {
        return Result.ok(mlClientService.predictCluster(features));
    }

    /** 调用 Python 神经网络分类预测 */
    @PostMapping("/classify")
    public Result<Map<String, Object>> classify(@RequestBody List<List<Double>> features) {
        return Result.ok(mlClientService.predictClassify(features));
    }
}
