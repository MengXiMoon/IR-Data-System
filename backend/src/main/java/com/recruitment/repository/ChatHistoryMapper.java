package com.recruitment.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.recruitment.entity.ChatHistory;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface ChatHistoryMapper extends BaseMapper<ChatHistory> {
}
