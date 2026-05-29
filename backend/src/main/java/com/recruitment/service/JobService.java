package com.recruitment.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.recruitment.dto.*;
import com.recruitment.entity.JobListing;
import com.recruitment.repository.JobListingMapper;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class JobService {

    private final JobListingMapper jobMapper;

    public JobService(JobListingMapper jobMapper) {
        this.jobMapper = jobMapper;
    }

    /** 分页搜索招聘数据 */
    public Page<JobListing> search(JobQueryRequest req) {
        LambdaQueryWrapper<JobListing> qw = new LambdaQueryWrapper<>();
        if (req.getKeyword() != null && !req.getKeyword().isBlank()) {
            qw.and(w -> w.like(JobListing::getJobTitle, req.getKeyword())
                    .or().like(JobListing::getSkillsRaw, req.getKeyword()));
        }
        if (req.getCity() != null && !req.getCity().isBlank()) {
            qw.eq(JobListing::getCity, req.getCity());
        }
        if (req.getExperience() != null && !req.getExperience().isBlank()) {
            qw.eq(JobListing::getExperience, req.getExperience());
        }
        if (req.getEducation() != null && !req.getEducation().isBlank()) {
            qw.eq(JobListing::getEducation, req.getEducation());
        }
        if (req.getIndustry() != null && !req.getIndustry().isBlank()) {
            qw.eq(JobListing::getIndustry, req.getIndustry());
        }
        if (req.getSalaryMin() != null) {
            qw.ge(JobListing::getSalaryAvg, req.getSalaryMin());
        }
        if (req.getSalaryMax() != null) {
            qw.le(JobListing::getSalaryAvg, req.getSalaryMax());
        }

        Page<JobListing> page = new Page<>(req.getPage(), req.getSize());
        return jobMapper.selectPage(page, qw);
    }

    /** 薪资统计 — 使用数据库聚合 */
    public SalaryStats getSalaryStats() {
        List<JobListing> all = jobMapper.selectList(null);
        List<Integer> salaries = all.stream()
                .map(JobListing::getSalaryAvg)
                .filter(Objects::nonNull)
                .sorted()
                .collect(Collectors.toList());

        if (salaries.isEmpty()) return new SalaryStats();

        SalaryStats stats = new SalaryStats();
        stats.setCount(salaries.size());
        stats.setAvgSalary(salaries.stream().mapToInt(Integer::intValue).average().orElse(0));
        stats.setMinSalary(salaries.get(0));
        stats.setMaxSalary(salaries.get(salaries.size() - 1));

        int mid = salaries.size() / 2;
        stats.setMedianSalary(salaries.size() % 2 == 0
                ? (salaries.get(mid - 1) + salaries.get(mid)) / 2.0
                : salaries.get(mid));
        return stats;
    }

    /** 城市岗位分布 */
    public List<CityStats> getCityDistribution() {
        return jobMapper.selectList(null).stream()
                .filter(j -> j.getCity() != null)
                .collect(Collectors.groupingBy(JobListing::getCity, Collectors.counting()))
                .entrySet().stream()
                .map(e -> { CityStats s = new CityStats(); s.setCity(e.getKey()); s.setCount(e.getValue()); return s; })
                .sorted((a, b) -> Long.compare(b.getCount(), a.getCount()))
                .limit(20)
                .collect(Collectors.toList());
    }

    /** 学历薪资统计 */
    public List<EducationStats> getEducationStats() {
        return jobMapper.selectList(null).stream()
                .filter(j -> j.getEducation() != null)
                .collect(Collectors.groupingBy(JobListing::getEducation))
                .entrySet().stream()
                .map(e -> {
                    EducationStats s = new EducationStats();
                    s.setEducation(e.getKey());
                    s.setCount(e.getValue().size());
                    s.setAvgSalary(e.getValue().stream()
                            .map(JobListing::getSalaryAvg)
                            .filter(Objects::nonNull)
                            .mapToInt(Integer::intValue)
                            .average().orElse(0));
                    return s;
                })
                .collect(Collectors.toList());
    }

    /** 经验分布 */
    public List<ExperienceStats> getExperienceDistribution() {
        return jobMapper.selectList(null).stream()
                .filter(j -> j.getExperience() != null)
                .collect(Collectors.groupingBy(JobListing::getExperience, Collectors.counting()))
                .entrySet().stream()
                .map(e -> { ExperienceStats s = new ExperienceStats(); s.setExperience(e.getKey()); s.setCount(e.getValue()); return s; })
                .sorted((a, b) -> Long.compare(b.getCount(), a.getCount()))
                .collect(Collectors.toList());
    }

    /** 公司类型分布 */
    public Map<String, Long> getCompanyTypeDistribution() {
        return jobMapper.selectList(null).stream()
                .filter(j -> j.getCompanyType() != null)
                .collect(Collectors.groupingBy(JobListing::getCompanyType, Collectors.counting()));
    }

    /** 行业分布 */
    public Map<String, Long> getIndustryDistribution() {
        return jobMapper.selectList(null).stream()
                .filter(j -> j.getIndustry() != null)
                .collect(Collectors.groupingBy(JobListing::getIndustry, Collectors.counting()));
    }

    /** 获取所有城市列表 */
    public List<String> getCities() {
        return jobMapper.selectList(null).stream()
                .map(JobListing::getCity)
                .filter(Objects::nonNull)
                .distinct()
                .sorted()
                .collect(Collectors.toList());
    }
}
