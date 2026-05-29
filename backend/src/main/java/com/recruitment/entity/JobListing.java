package com.recruitment.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("job_listing")
public class JobListing {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String sourceUrl;
    private String jobTitle;
    private String salaryRaw;
    private String skillsRaw;
    private String tag;
    private String experience;
    private String education;
    private String workLocation;
    private String companyName;
    private String companyInfo;
    private String companyTag;
    private String extraInfo;

    private Integer salaryMin;
    private Integer salaryMax;
    private String salaryUnit;
    private BigDecimal salaryMonths;
    private Integer salaryAvg;
    private String companyType;
    private String companySize;
    private String industry;
    private String city;
    private String district;

    private String source;

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}
