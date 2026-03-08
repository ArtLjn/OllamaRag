# 文档模型
from pydantic import BaseModel


class Document(BaseModel):
    """文档模型"""
    question: str
    answer: str
    category: str


class DocumentList(BaseModel):
    """文档列表模型"""
    documents: list[Document]
