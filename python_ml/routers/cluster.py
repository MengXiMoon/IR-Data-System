"""KMeans 聚类推理端点"""

import pickle
import os
from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np

router = APIRouter()

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "kmeans_model.pkl")

_model = None


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"模型文件不存在: {MODEL_PATH}")
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


from typing import List, Optional


class ClusterRequest(BaseModel):
    features: List[List[float]]  # [[f1, f2, ...], ...]


class ClusterResponse(BaseModel):
    labels: List[int]
    cluster_names: Optional[List[str]] = None


@router.post("/cluster/predict", response_model=ClusterResponse)
def predict_cluster(req: ClusterRequest):
    """对输入特征进行 KMeans 聚类标签预测"""
    model = get_model()
    X = np.array(req.features)
    labels = model.predict(X).tolist()
    return ClusterResponse(labels=labels)
