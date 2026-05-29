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

> 以下命令均以**项目根目录**（`IR-Data-System/`）为工作目录执行。

### 1. 环境准备

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| JDK | 17+ | 后端运行环境 |
| Maven | 3.9+ | 后端构建工具 |
| Node.js | 20+ | 前端运行环境（npm 自带） |
| Python | 3.12+ | ML 推理服务 |
| MySQL | 8.0 | 数据库，需提前安装并启动 |

**克隆项目后，进入项目根目录：**
```bash
cd IR-Data-System
```

---

**Python 虚拟环境（首次）**：

在 `python_ml/` 下创建虚拟环境并安装 ML 服务依赖：

```bash
cd python_ml

# 创建虚拟环境
python -m venv nlp_env

# 激活虚拟环境
# Windows CMD / PowerShell:
nlp_env\Scripts\activate
# Linux / Mac:
source nlp_env/bin/activate

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

cd ..
```

> 如还需运行数据清洗、可视化或 Jupyter Notebook，额外安装完整依赖(根目录下执行以下命令)：
> ```bash
> pip install -r ../requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

---

**前端依赖（首次）**：

```bash
cd app
npm install
cd ..
```

---

**建库（首次）**：

```bash
# 执行建表 SQL（git bash中执行）
mysql -u root -p < database/schema.sql

# 激活 Python 虚拟环境后导入清洗数据
cd python_ml
nlp_env\Scripts\activate          # Windows
# source nlp_env/bin/activate     # Linux / Mac
set DB_PASSWORD=你的MySQL密码
python ../database/import_data.py
cd ..
```

---

### 2. 启动 MySQL

```bash
# Windows
net start MySQL80

# Linux / Mac
sudo systemctl start mysql
```

---

### 3. 启动 Python ML 推理服务

```bash
cd python_ml

# 激活虚拟环境
nlp_env\Scripts\activate          # Windows
# source nlp_env/bin/activate     # Linux / Mac

# 启动 FastAPI 服务（默认 8000 端口）
uvicorn main:app --host 127.0.0.1 --port 8000

cd ..
```

---

### 4. 启动 Java 后端

**Windows（CMD / PowerShell）：**
```cmd
cd backend
set DB_PASSWORD=你的MySQL密码
set JWT_SECRET=一个至少32字符的随机密钥
set OPENAI_API_KEY=你的大模型API_KEY

mvn clean package -DskipTests
java -jar target\recruitment-ai-1.0.0.jar
```

**Linux / Mac / Git Bash：**
```bash
cd backend
export DB_PASSWORD=你的MySQL密码
export JWT_SECRET=一个至少32字符的随机密钥
export OPENAI_API_KEY=你的大模型API_KEY    # 可选，不用 AI 客服可不设

mvn clean package -DskipTests
java -jar target/recruitment-ai-1.0.0.jar
```

> **环境变量说明**：
> | 变量 | 必填 | 说明 |
> |------|------|------|
> | `DB_PASSWORD` | 是 | MySQL root 密码 |
> | `JWT_SECRET` | 是 | JWT 签名密钥，不少于 32 字符 |
> | `OPENAI_API_KEY` | 否 | 不填则跳过 AI 客服模块，系统其余功能正常 |

---

### 5. 启动 Vue 前端

```bash
cd app
npx vite --host 0.0.0.0 --port 5173
```

---

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
