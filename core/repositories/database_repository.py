# 数据库存储库
from pymilvus import MilvusClient
from typing import List
from core.configs.settings import MILVUS_CONFIG
from core.exceptions.custom_exceptions import DatabaseError
from core.interfaces.database_interface import DatabaseInterface


class DatabaseRepository(DatabaseInterface):
    """数据库存储库"""
    
    def __init__(self):
        """初始化数据库存储库"""
        self.database_name = MILVUS_CONFIG['database_name']
        self.client = MilvusClient(
            uri=f"http://{MILVUS_CONFIG['host']}:{MILVUS_CONFIG['port']}",
            db_name=self.database_name
        )
    
    def create_database(self) -> bool:
        """创建数据库"""
        try:
            databases = self.client.list_databases()
            if self.database_name in databases:
                print(f"数据库 '{self.database_name}' 已存在")
                return True
            
            self.client.create_database(db_name=self.database_name)
            print(f"数据库 '{self.database_name}' 创建成功")
            return True
        except Exception as e:
            print(f"创建数据库失败：{e}")
            raise DatabaseError(f"创建数据库失败：{e}")
    
    def delete_database(self) -> bool:
        """删除数据库"""
        try:
            databases = self.client.list_databases()
            if self.database_name not in databases:
                print(f"数据库 '{self.database_name}' 不存在")
                return True
            
            self.client.drop_database(db_name=self.database_name)
            print(f"数据库 '{self.database_name}' 删除成功")
            return True
        except Exception as e:
            print(f"删除数据库失败：{e}")
            raise DatabaseError(f"删除数据库失败：{e}")
    
    def list_databases(self) -> List[str]:
        """列出所有数据库"""
        try:
            databases = self.client.list_databases()
            print(f"当前数据库列表：{databases}")
            return databases
        except Exception as e:
            print(f"列出数据库失败：{e}")
            raise DatabaseError(f"列出数据库失败：{e}")
