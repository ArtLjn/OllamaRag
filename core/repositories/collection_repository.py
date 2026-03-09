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
    
    def create_collection(self, collection_name: str = None) -> bool:
        """创建集合"""
        try:
            if not self.database_repository.create_database():
                return False
            
            target_collection_name = collection_name if collection_name else self.collection_name
            
            if self.client.has_collection(collection_name=target_collection_name):
                print(f"集合 '{target_collection_name}' 已存在")
                return True
            
            self.client.create_collection(
                collection_name=target_collection_name,
                dimension=1024,  # 使用 Ollama 模型返回的实际维度 1024
                primary_field_name="id",
                vector_field_name="embedding",
                metric_type="L2"
            )
            
            print(f"集合 '{target_collection_name}' 创建成功")
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
    
    def add_documents(self, documents: List[Dict], collection_name: str = None) -> int:
        """添加文档"""
        try:
            target_collection_name = collection_name if collection_name else self.collection_name
            
            if not self.client.has_collection(collection_name=target_collection_name):
                print(f"集合 '{target_collection_name}' 不存在，请先创建")
                return 0
            
            data = []
            for i, doc in enumerate(documents):
                # 构建文档数据，支持动态字段
                doc_data = {
                    "id": doc.get('id', i + 1),  # 使用文档中的 ID 或生成新 ID
                    "embedding": doc.get('embedding', [])
                }
                
                # 添加其他字段
                for key, value in doc.items():
                    if key not in ['id', 'embedding']:
                        doc_data[key] = value
                
                data.append(doc_data)
            
            if data:
                result = self.client.insert(
                    collection_name=target_collection_name,
                    data=data
                )
                print(f"成功添加 {len(result)} 个文档到集合 '{target_collection_name}'")
                return len(result)
            else:
                print("没有有效文档可添加")
                return 0
        except Exception as e:
            print(f"添加文档失败: {e}")
            raise KnowledgeBaseError(f"添加文档失败: {e}")
    
    def search_similar(self, collection_name: str, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """搜索相似文档"""
        try:
            if not self.client.has_collection(collection_name=collection_name):
                print(f"集合 '{collection_name}' 不存在")
                return []
            
            # 执行相似性搜索
            results = self.client.search(
                collection_name=collection_name,
                data=[query_vector],
                limit=top_k,
                output_fields=["*"]  # 返回所有字段
            )
            
            # 处理搜索结果
            search_results = []
            for result in results[0]:  # 只处理第一个查询的结果
                item = {
                    "id": result.id,
                    "distance": result.distance,
                    "score": 1 / (1 + result.distance)  # 转换为相似度分数
                }
                # 添加其他字段
                for field, value in result.entity.items():
                    item[field] = value
                search_results.append(item)
            
            return search_results
        except Exception as e:
            print(f"搜索相似文档失败: {e}")
            raise KnowledgeBaseError(f"搜索相似文档失败: {e}")
    
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
    
    def list_collections(self) -> List[str]:
        """列出所有集合"""
        try:
            collections = self.client.list_collections()
            print(f"当前集合列表：{collections}")
            return collections
        except Exception as e:
            print(f"列出集合失败: {e}")
            raise KnowledgeBaseError(f"列出集合失败: {e}")
    
    def describe_collection(self, collection_name: str) -> Dict:
        """获取集合详细信息"""
        try:
            if not self.client.has_collection(collection_name=collection_name):
                return {
                    "exists": False,
                    "message": f"集合 '{collection_name}' 不存在"
                }
            
            collection_info = self.client.describe_collection(collection_name=collection_name)
            print(f"集合 '{collection_name}' 详细信息: {collection_info}")
            return collection_info
        except Exception as e:
            print(f"获取集合详细信息失败: {e}")
            raise KnowledgeBaseError(f"获取集合详细信息失败: {e}")
