package com.recruitment.dto;

import lombok.Data;

@Data
public class SalaryStats {
    private long count;
    private double avgSalary;
    private double medianSalary;
    private int minSalary;
    private int maxSalary;
}
