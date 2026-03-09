from fastapi import APIRouter, HTTPException
from core.services.knowledge_base_service import KnowledgeBaseService
from core.exceptions.custom_exceptions import DatabaseError

router = APIRouter()

# 初始化知识库服务
kb_service = KnowledgeBaseService()

# 列出所有数据库
@router.get("/")
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
@router.post("/create")
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
@router.delete("/delete")
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
