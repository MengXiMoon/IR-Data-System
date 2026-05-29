package com.recruitment.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.recruitment.common.Result;
import com.recruitment.dto.JobQueryRequest;
import com.recruitment.entity.JobListing;
import com.recruitment.service.JobService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/jobs")
public class JobController {

    private final JobService jobService;

    public JobController(JobService jobService) {
        this.jobService = jobService;
    }

    /** 分页搜索招聘岗位 */
    @PostMapping("/search")
    public Result<Page<JobListing>> search(@RequestBody JobQueryRequest req) {
        return Result.ok(jobService.search(req));
    }

    /** 获取城市列表 */
    @GetMapping("/cities")
    public Result<?> getCities() {
        return Result.ok(jobService.getCities());
    }
}
