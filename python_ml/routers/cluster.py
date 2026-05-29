"""KMeans 聚类推理端点"""

import pickle
import os
import re
from typing import List, Optional

import jieba
import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

_kmeans = None
_tfidf = None
_stopwords = None


def _load_stopwords():
    global _stopwords
    if _stopwords is not None:
        return _stopwords
    sw_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "stopwords.txt")
    if os.path.exists(sw_path):
        with open(sw_path, encoding="utf-8") as f:
            _stopwords = set(f.read().splitlines())
    else:
        _stopwords = {"的", "了", "和", "是", "就", "都", "而", "及", "与", "着", "或", "一个", "没有"}
    return _stopwords


def _get_kmeans():
    global _kmeans
    if _kmeans is None:
        path = os.path.join(MODEL_DIR, "kmeans_model.pkl")
        if not os.path.exists(path):
            raise FileNotFoundError(f"模型不存在: {path}，请先运行 notebooks/02_nlp_and_clustering.ipynb")
        with open(path, "rb") as f:
            _kmeans = pickle.load(f)
    return _kmeans


def _get_tfidf():
    global _tfidf
    if _tfidf is None:
        path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
        if not os.path.exists(path):
            raise FileNotFoundError(f"向量器不存在: {path}，请先运行 notebooks/02_nlp_and_clustering.ipynb")
        with open(path, "rb") as f:
            _tfidf = pickle.load(f)
    return _tfidf


def _preprocess(text: str) -> str:
    """与训练 notebook 保持一致的文本预处理"""
    stopwords = _load_stopwords()
    text = re.sub(r"[^一-龥a-zA-Z0-9\s]", " ", str(text))
    words = jieba.cut(text)
    return " ".join(w for w in words if len(w) > 1 and w not in stopwords)


class ClusterByTextRequest(BaseModel):
    """通过原始文本进行聚类"""
    texts: List[str]  # 岗位技能描述文本列表


class ClusterByFeaturesRequest(BaseModel):
    """通过已提取的特征向量进行聚类"""
    features: List[List[float]]


class ClusterResponse(BaseModel):
    labels: List[int]


@router.post("/cluster/predict", response_model=ClusterResponse)
def predict_cluster(req: ClusterByTextRequest):
    """输入岗位技能描述文本，返回聚类标签"""
    kmeans = _get_kmeans()
    tfidf = _get_tfidf()

    cleaned = [_preprocess(t) for t in req.texts]
    X = tfidf.transform(cleaned).toarray()
    labels = kmeans.predict(X).tolist()
    return ClusterResponse(labels=labels)


@router.post("/cluster/predict_features", response_model=ClusterResponse)
def predict_cluster_features(req: ClusterByFeaturesRequest):
    """输入已提取的特征向量，返回聚类标签（兼容旧版）"""
    kmeans = _get_kmeans()
    X = np.array(req.features)
    labels = kmeans.predict(X).tolist()
    return ClusterResponse(labels=labels)
