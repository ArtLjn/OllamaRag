# 项目配置文件

# 服务器配置
SERVER_IP = "10.217.163.18"
# SERVER_IP = "10.217.163.200"

# Ollama 配置
OLLAMA_CONFIG = {
    "api_url": f"http://{SERVER_IP}:11434/api/embeddings",
    "model": "qwen3-embedding:0.6b"
}

# Milvus 配置
MILVUS_CONFIG = {
    "host": SERVER_IP,
    "port": 19530,
    "database_name": "ollama_rag_db",
    "collection_name": "ollama_rag"
}

# 项目配置
PROJECT_CONFIG = {
    "name": "OllamaRag",
    "version": "1.0.0"
}
