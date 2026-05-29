package com.recruitment.controller;

import com.recruitment.common.Result;
import com.recruitment.service.JobService;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/charts")
public class ChartController {

    private final JobService jobService;

    public ChartController(JobService jobService) {
        this.jobService = jobService;
    }

    /** 薪资统计 */
    @GetMapping("/salary")
    public Result<?> salaryStats() {
        return Result.ok(jobService.getSalaryStats());
    }

    /** 城市分布 */
    @GetMapping("/cities")
    public Result<?> cityDistribution() {
        return Result.ok(jobService.getCityDistribution());
    }

    /** 学历薪资统计 */
    @GetMapping("/education")
    public Result<?> educationStats() {
        return Result.ok(jobService.getEducationStats());
    }

    /** 经验分布 */
    @GetMapping("/experience")
    public Result<?> experienceDistribution() {
        return Result.ok(jobService.getExperienceDistribution());
    }

    /** 公司类型分布 */
    @GetMapping("/company-type")
    public Result<Map<String, Long>> companyTypeDistribution() {
        return Result.ok(jobService.getCompanyTypeDistribution());
    }

    /** 行业分布 */
    @GetMapping("/industry")
    public Result<Map<String, Long>> industryDistribution() {
        return Result.ok(jobService.getIndustryDistribution());
    }

    /** 仪表盘总览（一次性返回所有统计数据） */
    @GetMapping("/dashboard")
    public Result<Map<String, Object>> dashboard() {
        return Result.ok(Map.of(
            "salary", jobService.getSalaryStats(),
            "cities", jobService.getCityDistribution(),
            "education", jobService.getEducationStats(),
            "experience", jobService.getExperienceDistribution(),
            "companyType", jobService.getCompanyTypeDistribution(),
            "industry", jobService.getIndustryDistribution()
        ));
    }
}
