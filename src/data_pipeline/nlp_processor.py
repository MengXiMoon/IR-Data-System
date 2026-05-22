"""文本分词、去停用词、特征向量化（TF-IDF / 词向量）"""

import jieba


def segment(text: str) -> list[str]:
    """Jieba 分词"""
    return list(jieba.cut(text))


def remove_stopwords(words: list[str], stopwords_path: str | None = None) -> list[str]:
    """去除停用词"""
    pass


def build_tfidf(corpus: list[str]):
    """构建 TF-IDF 特征矩阵"""
    pass
