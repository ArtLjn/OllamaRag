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
    
    def create_knowledge_base(self) -> bool:
        """创建知识库"""
        return self.collection_repository.create_collection()
    
    def delete_knowledge_base(self) -> bool:
        """删除知识库"""
        return self.collection_repository.delete_collection()
    
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
