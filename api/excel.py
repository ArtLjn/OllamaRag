from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from core.services.excel_import_service import ExcelImportService
from core.exceptions.custom_exceptions import KnowledgeBaseError
import os
import tempfile

router = APIRouter()

# 初始化 Excel 导入服务
excel_service = ExcelImportService()

# 上传并解析 Excel 文件
@router.post("/parse")
async def parse_excel(file: UploadFile = File(...)):
    """
    上传并解析 Excel 文件
    """
    try:
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # 解析 Excel 文件
        result = excel_service.parse_excel(temp_file_path)
        
        # 删除临时文件
        os.unlink(temp_file_path)
        
        return {"success": True, "data": result}
    except Exception as e:
        # 确保临时文件被删除
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

# 导入 Excel 数据到知识库
'''
前端返回一个embedding合并列表比如 ['名称','描述'] 字段进行数据合并，这时候我们处理
数据的时候需要将两个数据进行合并获得向量存入 content_embedding 向量字段
其余字段数据照常存储，只不过总价一个 content_embedding 向量字段
'''
@router.post("/import")
async def import_excel(
    file: UploadFile = File(...),
    collection_name: str = Form(...),
    fields: str = Form(None),
    template: str = Form(None)
):
    """
    导入 Excel 数据到知识库
    """
    try:
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # 解析 Excel 文件
        parse_result = excel_service.parse_excel(temp_file_path)
        
        # 生成 embedding 内容
        fields_list = None
        if fields:
            fields_list = fields.split(",")
        
        data_with_embedding_content = excel_service.generate_embedding_content(
            parse_result['data'],
            fields=fields_list,
            template=template
        )
        
        # 生成 embedding 向量
        data_with_vectors = excel_service.generate_embeddings(data_with_embedding_content)
        
        # 导入数据到 Milvus
        count = excel_service.import_to_milvus(data_with_vectors, collection_name, file.filename)
        
        # 删除临时文件
        os.unlink(temp_file_path)
        
        return {
            "success": True,
            "message": f"成功导入 {count} 条数据到知识库 '{collection_name}'",
            "count": count
        }
    except Exception as e:
        # 确保临时文件被删除
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

# 搜索相似文档
@router.get("/search")
async def search_similar(
    collection_name: str,
    query: str,
    top_k: int = 5
):
    """
    搜索相似文档
    """
    try:
        results = excel_service.search_similar(collection_name, query, top_k)
        return {"success": True, "data": results}
    except KnowledgeBaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
