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
