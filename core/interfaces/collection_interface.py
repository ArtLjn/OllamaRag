# 集合接口定义
from abc import ABC, abstractmethod
from typing import List, Dict


class CollectionInterface(ABC):
    """集合接口"""
    
    @abstractmethod
    def create_collection(self) -> bool:
        """创建集合"""
        pass
    
    @abstractmethod
    def delete_collection(self) -> bool:
        """删除集合"""
        pass
    
    @abstractmethod
    def add_documents(self, documents: List[Dict]) -> int:
        """添加文档"""
        pass
    
    @abstractmethod
    def check_collection(self) -> Dict:
        """检查集合状态"""
        pass
