-- ============================================================
-- 招聘数据智能系统 — MySQL 数据库建表脚本
-- ============================================================

CREATE DATABASE IF NOT EXISTS recruitment_ai
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE recruitment_ai;

-- ============================================================
-- 1. 系统用户表
-- ============================================================
CREATE TABLE sys_user (
    id              BIGINT          AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)     NOT NULL UNIQUE COMMENT '用户名',
    password        VARCHAR(255)    NOT NULL COMMENT '加密后的密码',
    email           VARCHAR(100)    DEFAULT NULL COMMENT '邮箱',
    role            VARCHAR(20)     NOT NULL DEFAULT 'user' COMMENT '角色: user / admin',
    status          TINYINT         NOT NULL DEFAULT 1 COMMENT '1=启用 0=禁用',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB COMMENT='系统用户表';


-- ============================================================
-- 2. 招聘数据主表
-- ============================================================
CREATE TABLE job_listing (
    id              BIGINT          AUTO_INCREMENT PRIMARY KEY,
    source_url      VARCHAR(500)    DEFAULT NULL COMMENT '信息_链接',
    job_title       VARCHAR(200)    NOT NULL COMMENT '岗位名称',
    salary_raw      VARCHAR(100)    DEFAULT NULL COMMENT '原始薪水文本',
    skills_raw      TEXT            DEFAULT NULL COMMENT '技能关键词(原始)',
    tag             VARCHAR(100)    DEFAULT NULL COMMENT '标签',
    experience      VARCHAR(20)     DEFAULT NULL COMMENT '工作经验',
    education       VARCHAR(20)     DEFAULT NULL COMMENT '学历要求',
    work_location   VARCHAR(200)    DEFAULT NULL COMMENT '工作地点(原始)',
    company_name    VARCHAR(200)    DEFAULT NULL COMMENT '公司名称',
    company_info    VARCHAR(500)    DEFAULT NULL COMMENT '公司信息(原始)',
    company_tag     VARCHAR(300)    DEFAULT NULL COMMENT '公司标签',
    extra_info      VARCHAR(300)    DEFAULT NULL COMMENT '其它信息',

    -- 派生字段
    salary_min      INT             DEFAULT NULL COMMENT '最低薪资(元/月)',
    salary_max      INT             DEFAULT NULL COMMENT '最高薪资(元/月)',
    salary_unit     VARCHAR(10)     DEFAULT NULL COMMENT '薪资单位: 万/元',
    salary_months   DECIMAL(4,1)    DEFAULT 12.0 COMMENT '年薪月数',
    salary_avg      INT             DEFAULT NULL COMMENT '平均月薪',
    company_type    VARCHAR(50)     DEFAULT NULL COMMENT '公司类型',
    company_size    VARCHAR(50)     DEFAULT NULL COMMENT '公司规模',
    industry        VARCHAR(100)    DEFAULT NULL COMMENT '所属行业',
    city            VARCHAR(50)     DEFAULT NULL COMMENT '城市',
    district        VARCHAR(50)     DEFAULT NULL COMMENT '区域',

    -- 元数据
    source          VARCHAR(50)     DEFAULT '智联招聘' COMMENT '数据来源',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_job_title (job_title),
    INDEX idx_city (city),
    INDEX idx_experience (experience),
    INDEX idx_education (education),
    INDEX idx_salary_avg (salary_avg),
    INDEX idx_company_type (company_type),
    INDEX idx_industry (industry)
) ENGINE=InnoDB COMMENT='招聘岗位数据表';


-- ============================================================
-- 3. KMeans 聚类结果表
-- ============================================================
CREATE TABLE cluster_result (
    id              BIGINT          AUTO_INCREMENT PRIMARY KEY,
    job_id          BIGINT          NOT NULL COMMENT '关联 job_listing.id',
    cluster_label   INT             NOT NULL COMMENT '聚类标签(0..k-1)',
    cluster_name    VARCHAR(100)    DEFAULT NULL COMMENT '聚类名称(如: 初级开发/高级架构/数据方向)',
    feature_vector  TEXT            DEFAULT NULL COMMENT '特征向量 JSON',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_cluster_label (cluster_label),
    FOREIGN KEY (job_id) REFERENCES job_listing(id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='KMeans 聚类结果';


-- ============================================================
-- 4. AI 对话记录表
-- ============================================================
CREATE TABLE chat_history (
    id              BIGINT          AUTO_INCREMENT PRIMARY KEY,
    user_id         BIGINT          NOT NULL COMMENT '用户ID',
    session_id      VARCHAR(64)     NOT NULL COMMENT '会话标识',
    role            VARCHAR(20)     NOT NULL COMMENT 'user / assistant',
    content         TEXT            NOT NULL COMMENT '消息内容',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='AI 对话记录';
