# 嵌入存储库
import requests
import json
from typing import List, Optional
from core.configs.settings import OLLAMA_CONFIG
from core.exceptions.custom_exceptions import EmbeddingError
from core.interfaces.embedding_interface import EmbeddingInterface


class EmbeddingRepository(EmbeddingInterface):
    """嵌入存储库"""
    
    def __init__(self):
        """初始化嵌入存储库"""
        # 禁用代理，直接连接 Ollama 服务器
        self.session = requests.Session()
        self.session.trust_env = False
    
    def get_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """获取文本的向量表示"""
        url = OLLAMA_CONFIG["api_url"]
        if model is None:
            model = OLLAMA_CONFIG["model"]
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "prompt": text
        }
        
        try:
            response = self.session.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # 检查请求是否成功
            result = response.json()
            embedding = result.get("embedding", [])
            if not embedding:
                raise EmbeddingError("获取的嵌入向量为空")
            return embedding
        except requests.RequestException as e:
            print(f"Error getting embedding: {e}")
            print("建议检查：")
            print("1. Ollama 服务器是否在运行")
            print("2. 服务器地址和端口是否正确")
            print("3. 网络连接是否正常")
            raise EmbeddingError(f"获取嵌入向量失败：{e}")

if __name__ == "__main__":
    emb = EmbeddingRepository()
    print(emb.get_embedding("Hello world"))