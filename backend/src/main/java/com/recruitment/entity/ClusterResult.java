package com.recruitment.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("cluster_result")
public class ClusterResult {

    @TableId(type = IdType.AUTO)
    private Long id;
    private Long jobId;
    private Integer clusterLabel;
    private String clusterName;
    private String featureVector;

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}
