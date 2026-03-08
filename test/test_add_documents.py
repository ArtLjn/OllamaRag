# 测试添加文档功能
import requests
import json

# API 端点
url = "http://localhost:8000/knowledge-base/add-documents"

# 测试文档数据
test_data = {
    "documents": [
        {
            "question": "什么是向量数据库？",
            "answer": "向量数据库是一种专门用于存储和检索向量数据的数据库系统。",
            "category": "数据库"
        }
    ]
}

# 发送请求
try:
    response = requests.post(url, json=test_data)
    response.raise_for_status()  # 检查请求是否成功
    result = response.json()
    print("添加文档结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
except requests.RequestException as e:
    print(f"请求失败: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"响应状态码: {e.response.status_code}")
        try:
            print(f"响应内容: {e.response.json()}")
        except:
            print(f"响应内容: {e.response.text}")
