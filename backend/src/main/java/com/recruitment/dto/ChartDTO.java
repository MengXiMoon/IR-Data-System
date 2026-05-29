package com.recruitment.dto;

import lombok.Data;

@Data
public class JobQueryRequest {
    private String keyword;
    private String city;
    private String experience;
    private String education;
    private String industry;
    private Integer salaryMin;
    private Integer salaryMax;
    private Integer page = 1;
    private Integer size = 20;
}

@Data
public class SalaryStats {
    private long count;
    private double avgSalary;
    private double medianSalary;
    private int minSalary;
    private int maxSalary;
}

@Data
public class CityStats {
    private String city;
    private long count;
}

@Data
public class EducationStats {
    private String education;
    private long count;
    private double avgSalary;
}

@Data
public class ExperienceStats {
    private String experience;
    private long count;
}
