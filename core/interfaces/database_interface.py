# 数据库接口定义
from abc import ABC, abstractmethod
from typing import List


class DatabaseInterface(ABC):
    """数据库接口"""
    
    @abstractmethod
    def create_database(self) -> bool:
        """创建数据库"""
        pass
    
    @abstractmethod
    def delete_database(self) -> bool:
        """删除数据库"""
        pass
    
    @abstractmethod
    def list_databases(self) -> List[str]:
        """列出所有数据库"""
        pass
