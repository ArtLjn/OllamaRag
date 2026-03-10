from fastapi import APIRouter, HTTPException, Body
from core.services.knowledge_base_service import KnowledgeBaseService
from core.models.document import Document, DocumentList
from core.exceptions.custom_exceptions import KnowledgeBaseError

router = APIRouter()

# 初始化知识库服务
kb_service = KnowledgeBaseService()

# 检查知识库状态
@router.get("/status")
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
@router.post("/create")
async def create_knowledge_base(collection_name: str = None):
    """
    创建知识库（集合）
    """
    try:
        result = kb_service.create_knowledge_base(collection_name)
        if result:
            return {"success": True, "message": f"知识库创建成功"}
        else:
            raise HTTPException(status_code=500, detail="知识库创建失败")
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取知识库列表
@router.get("/list")
async def list_knowledge_bases():
    """
    获取知识库列表
    """
    try:
        knowledge_bases = kb_service.list_knowledge_bases()
        return {"success": True, "data": knowledge_bases}
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取知识库信息
@router.get("/info")
async def get_knowledge_base_info(collection_name: str):
    """
    获取知识库信息
    """
    try:
        knowledge_base_info = kb_service.get_knowledge_base_info(collection_name)
        return {"success": True, "data": knowledge_base_info}
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 向知识库添加单个文档
@router.post("/add")
async def add_document(question: str, answer: str, category: str):
    """
    向知识库添加单个文档
    """
    try:
        document = {"question": question, "answer": answer, "category": category}
        count = kb_service.add_documents([document])
        return {"success": True, "message": f"成功添加 {count} 个文档", "count": count}
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 删除知识库
@router.delete("/delete")
async def delete_knowledge_base(collection_name: str = None):
    """
    删除知识库（集合）
    """
    try:
        result = kb_service.delete_knowledge_base(collection_name)
        if result:
            return {"success": True, "message": f"知识库删除成功"}
        else:
            raise HTTPException(status_code=500, detail="知识库删除失败")
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# 向知识库添加文档
@router.post("/add-documents")
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

# 列出所有集合
@router.get("/collections")
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
@router.get("/collections/{collection_name}")
async def describe_collection(collection_name: str):
    """
    获取集合详细信息
    """
    try:
        collection_info = kb_service.describe_collection(collection_name)
        return collection_info
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
