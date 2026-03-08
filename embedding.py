import requests
import json
from config import OLLAMA_CONFIG

# 禁用代理，直接连接 Ollama 服务器
session = requests.Session()
session.trust_env = False

def get_embedding(text, model=None):
    """
    调用 Ollama API 获取文本的向量表示
    
    Args:
        text (str): 需要转为向量的文本
        model (str): 使用的嵌入模型，默认为配置文件中的模型
    
    Returns:
        list: 文本的向量表示
    """
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
        response = session.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()
        return result.get("embedding", [])
    except requests.RequestException as e:
        print(f"Error getting embedding: {e}")
        print("建议检查：")
        print("1. Ollama 服务器是否在运行")
        print("2. 服务器地址和端口是否正确")
        print("3. 网络连接是否正常")
        return []

# 测试示例
if __name__ == "__main__":
    test_text = "向量数据库有什么用"
    embedding = get_embedding(test_text)
    print(f"Text: {test_text}")
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
