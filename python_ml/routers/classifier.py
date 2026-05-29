"""神经网络分类推理端点"""

import os
from fastapi import APIRouter
from pydantic import BaseModel
import torch
import numpy as np

router = APIRouter()

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "nn_classifier.pt")

_model = None
_input_dim = None
_num_classes = None


def get_model():
    global _model, _input_dim, _num_classes
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"模型文件不存在: {MODEL_PATH}")
        checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
        # 支持两种保存格式：完整模型 或 state_dict + config
        if isinstance(checkpoint, dict) and "state_dict" in checkpoint:
            _input_dim = checkpoint.get("input_dim", 5000)
            _num_classes = checkpoint.get("num_classes", 5)
            from src.ml_engine.classifier import RecruitmentClassifier
            _model = RecruitmentClassifier(_input_dim, _num_classes)
            _model.load_state_dict(checkpoint["state_dict"])
        else:
            _model = checkpoint
        _model.eval()
    return _model


from typing import List


class ClassifyRequest(BaseModel):
    features: List[List[float]]


class ClassifyResponse(BaseModel):
    predictions: List[int]
    probabilities: List[List[float]]


@router.post("/classify/predict", response_model=ClassifyResponse)
def predict_classify(req: ClassifyRequest):
    """对输入特征进行神经网络分类预测"""
    model = get_model()
    X = torch.tensor(req.features, dtype=torch.float32)
    with torch.no_grad():
        logits = model(X)
        probs = torch.softmax(logits, dim=1).tolist()
        preds = logits.argmax(dim=1).tolist()
    return ClassifyResponse(predictions=preds, probabilities=probs)
