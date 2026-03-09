# Excel 导入服务
import pandas as pd
from jinja2 import Template
from typing import List, Dict, Any
from core.repositories.embedding_repository import EmbeddingRepository
from core.repositories.collection_repository import CollectionRepository
from core.exceptions.custom_exceptions import KnowledgeBaseError


class ExcelImportService:
    """Excel 导入服务"""
    
    def __init__(self):
        """初始化 Excel 导入服务"""
        self.embedding_repository = EmbeddingRepository()
        self.collection_repository = CollectionRepository()
    
    def parse_excel(self, file_path: str) -> Dict[str, Any]:
        """解析 Excel 文件"""
        try:
            # 读取 Excel 文件
            df = pd.read_excel(file_path)
            
            # 处理 NaN 和无穷大值
            df = df.fillna('')  # 将 NaN 替换为空字符串
            
            # 获取字段名
            field_names = list(df.columns)
            
            # 自动推断字段类型
            field_types = {}
            for field in field_names:
                dtype = str(df[field].dtype)
                if 'int' in dtype:
                    field_types[field] = 'integer'
                elif 'float' in dtype:
                    field_types[field] = 'float'
                elif 'bool' in dtype:
                    field_types[field] = 'boolean'
                else:
                    field_types[field] = 'string'
            
            # 生成数据 schema
            schema = {
                'fields': [
                    {'name': field, 'type': field_types[field]}
                    for field in field_names
                ]
            }
            
            # 转换数据为字典列表
            data = df.to_dict('records')
            
            # 进一步处理数据中的特殊值
            def clean_value(value):
                import math
                if isinstance(value, float):
                    if math.isnan(value) or math.isinf(value):
                        return ''
                return value
            
            for item in data:
                for key, value in item.items():
                    item[key] = clean_value(value)
            
            return {
                'field_names': field_names,
                'field_types': field_types,
                'schema': schema,
                'data': data
            }
        except Exception as e:
            print(f"解析 Excel 文件失败: {e}")
            raise KnowledgeBaseError(f"解析 Excel 文件失败: {e}")
    
    def generate_embedding_content(self, data: List[Dict], fields: List[str] = None, template: str = None) -> List[Dict]:
        """生成 embedding 内容"""
        try:
            result = []
            
            for item in data:
                if template:
                    # 使用模板生成内容
                    jinja_template = Template(template)
                    embedding_content = jinja_template.render(**item)
                elif fields:
                    # 使用指定字段生成内容
                    content_parts = []
                    for field in fields:
                        if field in item:
                            content_parts.append(str(item[field]))
                    embedding_content = ' '.join(content_parts)
                else:
                    # 使用所有字段生成内容
                    content_parts = []
                    for key, value in item.items():
                        content_parts.append(str(value))
                    embedding_content = ' '.join(content_parts)
                
                item_with_embedding = item.copy()
                item_with_embedding['embedding_content'] = embedding_content
                result.append(item_with_embedding)
            
            return result
        except Exception as e:
            print(f"生成 embedding 内容失败: {e}")
            raise KnowledgeBaseError(f"生成 embedding 内容失败: {e}")
    
    def generate_embeddings(self, data: List[Dict]) -> List[Dict]:
        """生成 embedding 向量"""
        try:
            result = []
            
            for item in data:
                if 'embedding_content' in item:
                    try:
                        embedding = self.embedding_repository.get_embedding(item['embedding_content'])
                        item_with_vector = item.copy()
                        item_with_vector['vector'] = embedding
                        result.append(item_with_vector)
                    except Exception as e:
                        print(f"生成 embedding 失败，跳过数据: {item['embedding_content']}")
                        print(f"错误信息: {e}")
                        continue
            
            return result
        except Exception as e:
            print(f"生成 embedding 向量失败: {e}")
            raise KnowledgeBaseError(f"生成 embedding 向量失败: {e}")
    
    def import_to_milvus(self, data: List[Dict], collection_name: str) -> int:
        """导入数据到 Milvus"""
        try:
            # 确保集合存在
            self.collection_repository.create_collection(collection_name)
            
            # 准备数据
            milvus_data = []
            for i, item in enumerate(data):
                milvus_item = {
                    'id': i + 1,
                    'embedding': item.get('vector', []),
                    'embedding_content': item.get('embedding_content', ''),
                    # 添加原始字段
                    **{k: v for k, v in item.items() if k not in ['vector', 'embedding_content']}
                }
                milvus_data.append(milvus_item)
            
            # 批量添加文档
            if milvus_data:
                count = self.collection_repository.add_documents(milvus_data, collection_name)
                return count
            else:
                return 0
        except Exception as e:
            print(f"导入数据到 Milvus 失败: {e}")
            raise KnowledgeBaseError(f"导入数据到 Milvus 失败: {e}")
    
    def search_similar(self, collection_name: str, query: str, top_k: int = 5) -> List[Dict]:
        """搜索相似文档"""
        try:
            # 生成查询向量
            query_vector = self.embedding_repository.get_embedding(query)
            
            # 调用集合存储库的搜索方法
            results = self.collection_repository.search_similar(
                collection_name=collection_name,
                query_vector=query_vector,
                top_k=top_k
            )
            
            return results
        except Exception as e:
            print(f"搜索相似文档失败: {e}")
            raise KnowledgeBaseError(f"搜索相似文档失败: {e}")