# 知识库服务
from typing import List, Dict
from core.repositories.database_repository import DatabaseRepository
from core.repositories.collection_repository import CollectionRepository
from core.repositories.embedding_repository import EmbeddingRepository
from core.exceptions.custom_exceptions import KnowledgeBaseError, EmbeddingError


class KnowledgeBaseService:
    """知识库服务"""
    
    def __init__(self):
        """初始化知识库服务"""
        self.database_repository = DatabaseRepository()
        self.collection_repository = CollectionRepository()
        self.embedding_repository = EmbeddingRepository()
    
    def create_database(self) -> bool:
        """创建数据库"""
        return self.database_repository.create_database()
    
    def delete_database(self) -> bool:
        """删除数据库"""
        return self.database_repository.delete_database()
    
    def list_databases(self) -> List[str]:
        """列出所有数据库"""
        return self.database_repository.list_databases()
    
    def create_knowledge_base(self, collection_name: str = None) -> bool:
        """创建知识库"""
        return self.collection_repository.create_collection(collection_name)
    
    def delete_knowledge_base(self, collection_name: str = None) -> bool:
        """删除知识库"""
        return self.collection_repository.delete_collection(collection_name)
    
    def add_documents(self, documents: List[Dict]) -> int:
        """添加文档"""
        try:
            # 为每个文档获取嵌入向量
            documents_with_embedding = []
            for doc in documents:
                try:
                    embedding = self.embedding_repository.get_embedding(doc['question'])
                    doc_with_embedding = doc.copy()
                    doc_with_embedding['embedding'] = embedding
                    documents_with_embedding.append(doc_with_embedding)
                except EmbeddingError as e:
                    print(f"获取嵌入向量失败，跳过文档: {doc['question']}")
                    print(f"错误信息: {e}")
                    continue
            
            # 添加文档到知识库
            return self.collection_repository.add_documents(documents_with_embedding)
        except Exception as e:
            print(f"添加文档失败: {e}")
            raise KnowledgeBaseError(f"添加文档失败: {e}")
    
    def check_knowledge_base(self) -> Dict:
        """检查知识库状态"""
        return self.collection_repository.check_collection()
    
    def list_collections(self) -> List[str]:
        """列出所有集合"""
        return self.collection_repository.list_collections()
    
    def describe_collection(self, collection_name: str) -> Dict:
        """获取集合详细信息"""
        return self.collection_repository.describe_collection(collection_name)
    
    def list_knowledge_bases(self) -> List[Dict]:
        """获取知识库列表"""
        collections = self.collection_repository.list_collections()
        knowledge_bases = []
        for collection_name in collections:
            try:
                info = self.collection_repository.describe_collection(collection_name)
                knowledge_bases.append({
                    "collection_name": collection_name,
                    "description": info.get("description", ""),
                    "document_count": info.get("document_count", 0),
                    "created_at": info.get("created_at", ""),
                    "dimension": info.get("dimension", 1024)
                })
            except Exception as e:
                print(f"获取知识库信息失败: {collection_name}")
                print(f"错误信息: {e}")
                continue
        return knowledge_bases
    
    def get_knowledge_base_info(self, collection_name: str) -> Dict:
        """获取知识库信息"""
        info = self.collection_repository.describe_collection(collection_name)
        return {
            "collection_name": collection_name,
            "description": info.get("description", ""),
            "document_count": info.get("document_count", 0),
            "created_at": info.get("created_at", ""),
            "dimension": info.get("dimension", 1024)
        }
