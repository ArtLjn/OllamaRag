# 自定义异常类

class KnowledgeBaseError(Exception):
    """知识库相关错误"""
    pass

class EmbeddingError(Exception):
    """嵌入相关错误"""
    pass

class DatabaseError(Exception):
    """数据库相关错误"""
    pass
