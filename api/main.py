from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.knowledge_base import router as knowledge_base_router
from api.excel import router as excel_router
from api.database import router as database_router

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

# 根路径
@app.get("/")
async def root():
    return {"message": "知识库管理 API 服务运行中"}

# 注册路由
app.include_router(knowledge_base_router, prefix="/knowledge-base", tags=["knowledge-base"])
app.include_router(excel_router, prefix="/excel", tags=["excel"])
app.include_router(database_router, prefix="/databases", tags=["databases"])
