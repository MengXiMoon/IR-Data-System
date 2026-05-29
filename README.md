# 招聘数据智能系统

基于 NLP 与机器学习的招聘市场数据分析平台，支持数据爬取、清洗、可视化、KMeans 聚类、神经网络分类、AI 智能客服。

## 技术架构

```
Vue 3 前端 (Vite)  →  Java Spring Boot 后端  →  MySQL 数据库
                         ↓ HTTP 调用
                    Python FastAPI ML 推理服务
```

| 层 | 技术栈 | 端口 |
|------|------|------|
| 前端 | Vue 3 + Vue Router + Pinia + Axios | 5173 |
| 后端 | Spring Boot 3.3 + MyBatis-Plus + LangChain4j + JWT | 8080 |
| ML 推理 | Python FastAPI + scikit-learn + PyTorch | 8000 |
| 数据库 | MySQL 8.0 | 3306 |

## 快速启动

### 1. 环境准备

- JDK 17+
- Maven 3.9+
- Node.js 20+
- Python 3.12+
- MySQL 8.0（需先建库）

Python 虚拟环境（首次）：

```bash
python -m venv D:/编程程序/python/nlp_env
D:/编程程序/python/nlp_env/Scripts/pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

前端依赖（首次）：

```bash
cd app
npm install
```

建库（首次）：

```bash
mysql -u root -p < database/schema.sql
python database/import_data.py   # 导入清洗后的数据
```

### 2. 启动 MySQL

```bash
net start MySQL80    # 或确保服务已在运行
```

### 3. 启动 Python ML 推理服务

```bash
cd python_ml
D:/编程程序/python/nlp_env/Scripts/python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### 4. 启动 Java 后端

**Windows (Git Bash)：**

```bash
cd backend
export DB_PASSWORD=你的MySQL密码
export JWT_SECRET=一个至少32字符的随机密钥
export OPENAI_API_KEY=你的大模型API_KEY    # 可选，不用 AI 客服可不设

mvn clean package -DskipTests
java -jar target/recruitment-ai-1.0.0.jar
```

### 5. 启动 Vue 前端

```bash
cd app
npx vite --host 0.0.0.0 --port 5173
```

### 6. 打开浏览器

访问 `http://localhost:5173`，注册账号后即可使用。

> 组内其他成员访问 `http://你的局域网IP:5173`

## 项目目录

```
├── app/                  # Vue 3 前端
│   └── src/views/        # 仪表盘、可视化、岗位搜索、AI 助手、机器学习
├── backend/              # Java Spring Boot 后端
├── python_ml/            # Python FastAPI ML 推理服务
├── data/
│   ├── raw/              # 原始爬取数据
│   └── processed/        # 清洗后数据 + 图表
├── models/               # 训练好的模型文件
├── notebooks/            # Jupyter 训练脚本
├── database/             # 建表 SQL + 导入脚本
├── docs/                 # API 文档 + 训练指南
└── config/               # 配置文件
```

## 模型训练

大模型 AI 客服开箱即用。KMeans 聚类和神经网络分类需要先训练模型：

1. 运行 `notebooks/02_nlp_and_clustering.ipynb` → 生成 `models/kmeans_model.pkl`
2. 运行 `notebooks/03_nn_classification.ipynb` → 生成 `models/nn_classifier.pt`
3. 重启 Python ML 推理服务

详见 `docs/模型训练指南.md`。

## API 文档

前端对接接口见 `docs/API文档.md`，或启动后端后访问 `http://localhost:8080/` 查看 JSON 格式的接口目录。
