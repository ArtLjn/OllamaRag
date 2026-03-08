from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from core.services.knowledge_base_service import KnowledgeBaseService
from core.models.document import Document, DocumentList
from core.exceptions.custom_exceptions import KnowledgeBaseError, DatabaseError
import uvicorn

# 初始化 FastAPI 应用
app = FastAPI(
    title="知识库管理 API",
    description="提供知识库的创建、删除、添加文档和检查状态等操作",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化知识库服务
kb_service = KnowledgeBaseService()

# 根路径
@app.get("/")
async def root():
    return {"message": "知识库管理 API 服务运行中"}

# 检查知识库状态
@app.get("/knowledge-base/status")
async def check_knowledge_base_status():
    """
    检查知识库状态
    """
    try:
        status = kb_service.check_knowledge_base()
        return status
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 创建知识库
@app.post("/knowledge-base/create")
async def create_knowledge_base():
    """
    创建知识库（集合）
    """
    try:
        result = kb_service.create_knowledge_base()
        if result:
            return {"success": True, "message": f"知识库创建成功"}
        else:
            raise HTTPException(status_code=500, detail="知识库创建失败")
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 删除知识库
@app.delete("/knowledge-base/delete")
async def delete_knowledge_base():
    """
    删除知识库（集合）
    """
    try:
        result = kb_service.delete_knowledge_base()
        if result:
            return {"success": True, "message": f"知识库删除成功"}
        else:
            raise HTTPException(status_code=500, detail="知识库删除失败")
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 向知识库添加文档
@app.post("/knowledge-base/add-documents")
async def add_documents(documents: DocumentList = Body(...)):
    """
    向知识库添加文档
    """
    try:
        # 转换为字典列表
        doc_list = []
        for doc in documents.documents:
            # 确保每个文档都能正确转换为字典
            doc_dict = doc.model_dump() if hasattr(doc, 'model_dump') else doc.dict()
            doc_list.append(doc_dict)
        count = kb_service.add_documents(doc_list)
        return {"success": True, "message": f"成功添加 {count} 个文档", "count": count}
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 列出所有数据库
@app.get("/databases")
async def list_databases():
    """
    列出所有数据库
    """
    try:
        databases = kb_service.list_databases()
        return {"databases": databases}
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 创建数据库
@app.post("/databases/create")
async def create_database():
    """
    创建数据库
    """
    try:
        result = kb_service.create_database()
        if result:
            return {"success": True, "message": f"数据库创建成功"}
        else:
            raise HTTPException(status_code=500, detail="数据库创建失败")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 删除数据库
@app.delete("/databases/delete")
async def delete_database():
    """
    删除数据库
    """
    try:
        result = kb_service.delete_database()
        if result:
            return {"success": True, "message": f"数据库删除成功"}
        else:
            raise HTTPException(status_code=500, detail="数据库删除失败")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 列出所有集合
@app.get("/collections")
async def list_collections():
    """
    列出所有集合
    """
    try:
        collections = kb_service.list_collections()
        return {"collections": collections}
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取集合详细信息
@app.get("/collections/{collection_name}")
async def describe_collection(collection_name: str):
    """
    获取集合详细信息
    """
    try:
        collection_info = kb_service.describe_collection(collection_name)
        return collection_info
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
