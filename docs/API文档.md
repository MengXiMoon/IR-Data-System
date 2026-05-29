# 招聘数据智能系统 — 前端 API 文档

> Base URL: `http://localhost:8080`

---

## 1. 认证模块

### 1.1 登录

```
POST /api/auth/login
Content-Type: application/json
```

**请求体：**
```json
{
  "username": "admin",
  "password": "123456"
}
```

**成功响应 (200)：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiJ9...",
    "username": "admin",
    "role": "admin"
  }
}
```

**失败响应：**
```json
{
  "code": 500,
  "message": "用户名或密码错误",
  "data": null
}
```

---

### 1.2 注册

```
POST /api/auth/register
Content-Type: application/json
```

**请求体：**
```json
{
  "username": "newuser",
  "password": "123456",
  "email": "test@example.com"
}
```

**成功响应 (200)：**
```json
{
  "code": 200,
  "message": "success",
  "data": null
}
```

---

## 全局说明

**认证方式：** 除 `/api/auth/**` 外，所有接口需在 Header 中携带：
```
Authorization: Bearer <token>
```

---

## 2. 招聘数据模块

### 2.1 搜索招聘岗位

```
POST /api/jobs/search
Content-Type: application/json
Authorization: Bearer <token>
```

**请求体：**
```json
{
  "keyword": "Python",
  "city": "北京",
  "experience": "3-5年",
  "education": "本科",
  "industry": "互联网/IT服务",
  "salaryMin": 15000,
  "salaryMax": 30000,
  "page": 1,
  "size": 20
}
```

> 所有字段均可选，不传则不筛选。

**成功响应 (200)：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "records": [
      {
        "id": 1,
        "jobTitle": "Python后端开发工程师",
        "salaryRaw": "1.5-2.5万·13薪",
        "salaryMin": 15000,
        "salaryMax": 25000,
        "salaryAvg": 20000,
        "salaryUnit": "万",
        "salaryMonths": 13.0,
        "skillsRaw": "Python Django MySQL Redis Docker",
        "tag": "Python",
        "experience": "3-5年",
        "education": "本科",
        "workLocation": "北京·海淀·中关村",
        "companyName": "某科技有限公司",
        "companyType": "民营",
        "companySize": "100-299人",
        "industry": "互联网/IT服务",
        "city": "北京",
        "district": "海淀"
      }
    ],
    "total": 1345,
    "size": 20,
    "current": 1,
    "pages": 68
  }
}
```

---

### 2.2 获取城市列表

```
GET /api/jobs/cities
Authorization: Bearer <token>
```

**成功响应 (200)：**
```json
{
  "code": 200,
  "message": "success",
  "data": ["上海", "北京", "南京", "厦门", "成都", "杭州", "武汉", "深圳", "苏州", "西安", "长沙", "青岛"]
}
```

---

## 3. 可视化数据模块

### 3.1 仪表盘总览（一次性返回所有统计）

```
GET /api/charts/dashboard
Authorization: Bearer <token>
```

**成功响应 (200)：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "salary": {
      "count": 1345,
      "avgSalary": 15227.0,
      "medianSalary": 14000.0,
      "minSalary": 1000,
      "maxSalary": 60000
    },
    "cities": [
      { "city": "北京", "count": 99 },
      { "city": "深圳", "count": 99 },
      { "city": "南京", "count": 97 }
    ],
    "education": [
      { "education": "本科", "count": 1128, "avgSalary": 15200.0 },
      { "education": "大专", "count": 141, "avgSalary": 12000.0 },
      { "education": "硕士", "count": 33, "avgSalary": 21000.0 }
    ],
    "experience": [
      { "experience": "3-5年", "count": 448 },
      { "experience": "经验不限", "count": 379 },
      { "experience": "1-3年", "count": 340 }
    ],
    "companyType": {
      "民营": 498,
      "股份制": 287,
      "上市公司": 259
    },
    "industry": {
      "互联网/IT服务": 736,
      "企业数字化平台": 68,
      "咨询服务": 38
    }
  }
}
```

---

### 3.2 单项统计接口

| 端点 | 说明 | 返回格式 |
|------|------|----------|
| `GET /api/charts/salary` | 薪资统计 | `SalaryStats` |
| `GET /api/charts/cities` | 城市分布 | `List<CityStats>` |
| `GET /api/charts/education` | 学历薪资 | `List<EducationStats>` |
| `GET /api/charts/experience` | 经验分布 | `List<ExperienceStats>` |
| `GET /api/charts/company-type` | 公司类型 | `Map<String, Long>` |
| `GET /api/charts/industry` | 行业分布 | `Map<String, Long>` |

> 所有接口需 `Authorization: Bearer <token>`，返回结构均为 `{ code, message, data }`。

---

## 4. AI 智能客服模块

### 4.1 发送消息

```
POST /api/ai/chat
Content-Type: application/json
Authorization: Bearer <token>
```

**请求体：**
```json
{
  "message": "我有3年Python开发经验，在深圳找什么工作比较合适？",
  "sessionId": ""
}
```

> 首次对话 `sessionId` 为空，后端自动生成；后续传返回的 `sessionId` 以保持上下文。

**成功响应 (200)：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "sessionId": "a1b2c3d4",
    "reply": "根据你的3年Python开发经验和深圳市场情况..."
  }
}
```

---

### 4.2 获取对话历史

```
GET /api/ai/history/{sessionId}
Authorization: Bearer <token>
```

**成功响应 (200)：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    { "role": "user", "content": "你好", "createdAt": "2024-01-15T10:00:00" },
    { "role": "assistant", "content": "你好！我是求职助手...", "createdAt": "2024-01-15T10:00:02" }
  ]
}
```

---

## 5. 机器学习模块

### 5.1 KMeans 聚类预测

```
POST /api/ml/cluster
Content-Type: application/json
Authorization: Bearer <token>
```

**请求体：**
```json
["Python Django MySQL 后端开发", "Java Spring Boot 微服务"]
```

> 传入岗位技能描述文本列表，后端自动分词 → TF-IDF → 聚类

**成功响应 (200)：**
```json
{
  "code": 200,
  "message": "success",
  "data": [2, 0]
}
```

---

### 5.2 神经网络分类预测

```
POST /api/ml/classify
Content-Type: application/json
Authorization: Bearer <token>
```

**请求体：**
```json
["Python Django MySQL 后端开发"]
```

> 传入岗位技能描述文本列表，后端自动分词 → TF-IDF → 标准化 → 分类

**成功响应 (200)：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "predictions": [2],
    "probabilities": [[0.05, 0.12, 0.68, 0.10, 0.05]]
  }
}
```

> 注意：需先运行 notebook 训练模型，详见 docs/模型训练指南.md

---

## 附录：前端集成要点

### Axios 配置示例

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8080',
  timeout: 30000,
});

// 请求拦截：自动带 token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截：401 自动跳登录
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);
```

### Streamlit 调用示例（若保留 Python 端调试）

```python
import requests

resp = requests.post(
    "http://localhost:8080/api/jobs/search",
    json={"city": "北京", "page": 1, "size": 10},
    headers={"Authorization": f"Bearer {token}"}
)
data = resp.json()
```
