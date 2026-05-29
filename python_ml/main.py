"""ML 推理微服务 — FastAPI 入口"""

import os
import sys

# 将 src 加入路径，复用已有的 NLP 处理模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi import FastAPI
from routers import cluster, classifier

app = FastAPI(
    title="招聘数据 ML 推理服务",
    version="1.0.0",
)

app.include_router(cluster.router, prefix="/api/ml", tags=["聚类"])
app.include_router(classifier.router, prefix="/api/ml", tags=["分类"])


@app.get("/health")
def health():
    return {"status": "ok"}
