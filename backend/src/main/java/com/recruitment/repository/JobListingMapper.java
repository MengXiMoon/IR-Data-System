package com.recruitment.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.recruitment.entity.JobListing;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface JobListingMapper extends BaseMapper<JobListing> {
}
