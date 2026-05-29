"""神经网络分类推理端点"""

import pickle
import os
import re
from typing import List

import jieba
import torch
import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

_model = None
_tfidf = None
_scaler = None


def _get_model():
    global _model
    if _model is not None:
        return _model
    path = os.path.join(MODEL_DIR, "nn_classifier.pt")
    if not os.path.exists(path):
        raise FileNotFoundError(f"模型不存在: {path}，请先运行 notebooks/03_nn_classification.ipynb")

    checkpoint = torch.load(path, map_location="cpu", weights_only=False)

    from ....src.ml_engine.classifier import RecruitmentClassifier
    input_dim = checkpoint["input_dim"]
    hidden_dim = checkpoint.get("hidden_dim", 256)
    num_classes = checkpoint["num_classes"]

    _model = RecruitmentClassifier(input_dim, hidden_dim, num_classes)
    _model.load_state_dict(checkpoint["state_dict"])
    _model.eval()
    return _model


def _get_tfidf():
    global _tfidf
    if _tfidf is None:
        path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
        if not os.path.exists(path):
            raise FileNotFoundError(f"向量器不存在: {path}")
        with open(path, "rb") as f:
            _tfidf = pickle.load(f)
    return _tfidf


def _get_scaler():
    global _scaler
    if _scaler is None:
        path = os.path.join(MODEL_DIR, "scaler.pkl")
        if not os.path.exists(path):
            raise FileNotFoundError(f"标准化器不存在: {path}")
        with open(path, "rb") as f:
            _scaler = pickle.load(f)
    return _scaler


def _preprocess(text: str) -> str:
    stopwords = {"的", "了", "和", "是", "就", "都", "而", "及", "与", "着", "或", "一个", "没有"}
    text = re.sub(r"[^一-龥a-zA-Z0-9\s]", " ", str(text))
    words = jieba.cut(text)
    return " ".join(w for w in words if len(w) > 1 and w not in stopwords)


class ClassifyByTextRequest(BaseModel):
    """通过原始文本进行分类"""
    texts: List[str]


class ClassifyByFeaturesRequest(BaseModel):
    """通过特征向量进行分类"""
    features: List[List[float]]


class ClassifyResponse(BaseModel):
    predictions: List[int]
    probabilities: List[List[float]]


@router.post("/classify/predict", response_model=ClassifyResponse)
def predict_classify(req: ClassifyByTextRequest):
    """输入岗位技能描述文本，返回分类标签和概率"""
    model = _get_model()
    tfidf = _get_tfidf()
    scaler = _get_scaler()

    cleaned = [_preprocess(t) for t in req.texts]
    X = tfidf.transform(cleaned).toarray()
    X = scaler.transform(X)
    X_t = torch.tensor(X, dtype=torch.float32)

    with torch.no_grad():
        logits = model(X_t)
        probs = torch.softmax(logits, dim=1).tolist()
        preds = logits.argmax(dim=1).tolist()

    return ClassifyResponse(predictions=preds, probabilities=probs)


@router.post("/classify/predict_features", response_model=ClassifyResponse)
def predict_classify_features(req: ClassifyByFeaturesRequest):
    """输入已提取的特征向量，返回分类标签（兼容旧版）"""
    model = _get_model()
    scaler = _get_scaler()
    X = np.array(req.features)
    X = scaler.transform(X)
    X_t = torch.tensor(X, dtype=torch.float32)

    with torch.no_grad():
        logits = model(X_t)
        probs = torch.softmax(logits, dim=1).tolist()
        preds = logits.argmax(dim=1).tolist()

    return ClassifyResponse(predictions=preds, probabilities=probs)
