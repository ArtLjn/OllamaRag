# 集合存储库
from pymilvus import MilvusClient
from typing import List, Dict
from core.configs.settings import MILVUS_CONFIG
from core.exceptions.custom_exceptions import KnowledgeBaseError
from core.interfaces.collection_interface import CollectionInterface
from core.repositories.database_repository import DatabaseRepository


class CollectionRepository(CollectionInterface):
    """集合存储库"""
    
    def __init__(self):
        """初始化集合存储库"""
        self.database_name = MILVUS_CONFIG['database_name']
        self.collection_name = MILVUS_CONFIG['collection_name']
        self.client = MilvusClient(
            uri=f"http://{MILVUS_CONFIG['host']}:{MILVUS_CONFIG['port']}",
            db_name=self.database_name
        )
        self.database_repository = DatabaseRepository()
    
    def create_collection(self) -> bool:
        """创建集合"""
        try:
            if not self.database_repository.create_database():
                return False
            
            if self.client.has_collection(collection_name=self.collection_name):
                print(f"集合 '{self.collection_name}' 已存在")
                return True
            
            self.client.create_collection(
                collection_name=self.collection_name,
                dimension=1024,  # 使用 Ollama 模型返回的实际维度 1024
                primary_field_name="id",
                vector_field_name="embedding",
                metric_type="L2"
            )
            
            print(f"集合 '{self.collection_name}' 创建成功")
            return True
        except Exception as e:
            print(f"创建集合失败：{e}")
            raise KnowledgeBaseError(f"创建集合失败：{e}")
    
    def delete_collection(self) -> bool:
        """删除集合"""
        try:
            if not self.client.has_collection(collection_name=self.collection_name):
                print(f"集合 '{self.collection_name}' 不存在")
                return True
            
            self.client.drop_collection(collection_name=self.collection_name)
            print(f"集合 '{self.collection_name}' 删除成功")
            return True
        except Exception as e:
            print(f"删除集合失败: {e}")
            raise KnowledgeBaseError(f"删除集合失败: {e}")
    
    def add_documents(self, documents: List[Dict]) -> int:
        """添加文档"""
        try:
            if not self.client.has_collection(collection_name=self.collection_name):
                print(f"集合 '{self.collection_name}' 不存在，请先创建")
                return 0
            
            data = []
            for doc in documents:
                data.append({
                    "id": len(data) + 1,  # 简单的 ID 生成
                    "question": doc['question'],
                    "answer": doc['answer'],
                    "category": doc['category'],
                    "embedding": doc.get('embedding', [])
                })
            
            if data:
                result = self.client.insert(
                    collection_name=self.collection_name,
                    data=data
                )
                print(f"成功添加 {len(result)} 个文档到集合")
                return len(result)
            else:
                print("没有有效文档可添加")
                return 0
        except Exception as e:
            print(f"添加文档失败: {e}")
            raise KnowledgeBaseError(f"添加文档失败: {e}")
    
    def check_collection(self) -> Dict:
        """检查集合状态"""
        try:
            if not self.client.has_collection(collection_name=self.collection_name):
                return {
                    "exists": False,
                    "message": f"集合 '{self.collection_name}' 不存在"
                }
            
            # 在 pymilvus 2.6.9 版本中，get_stats 方法不存在
            stats = "无法获取统计信息"
            
            return {
                "exists": True,
                "message": f"集合 '{self.collection_name}' 存在",
                "stats": stats
            }
        except Exception as e:
            print(f"检查集合状态失败: {e}")
            raise KnowledgeBaseError(f"检查集合状态失败: {e}")
