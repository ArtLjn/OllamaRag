# 嵌入接口定义
from abc import ABC, abstractmethod
from typing import List, Optional


class EmbeddingInterface(ABC):
    """嵌入接口"""
    
    @abstractmethod
    def get_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """获取文本的向量表示"""
        pass
