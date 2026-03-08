# 测试知识库功能
import requests
import json

class TestKnowledgeBase:
    """知识库测试类"""
    
    def __init__(self):
        """初始化测试类"""
        self.base_url = "http://localhost:8000"
    
    def test_list_databases(self):
        """测试列出所有数据库"""
        url = f"{self.base_url}/databases"
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            print("=== 测试列出所有数据库 ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def test_create_database(self):
        """测试创建数据库"""
        url = f"{self.base_url}/databases/create"
        try:
            response = requests.post(url)
            response.raise_for_status()
            result = response.json()
            print("\n=== 测试创建数据库 ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def test_create_knowledge_base(self):
        """测试创建知识库"""
        url = f"{self.base_url}/knowledge-base/create"
        try:
            response = requests.post(url)
            response.raise_for_status()
            result = response.json()
            print("\n=== 测试创建知识库 ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def test_check_knowledge_base_status(self):
        """测试检查知识库状态"""
        url = f"{self.base_url}/knowledge-base/status"
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            print("\n=== 测试检查知识库状态 ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def test_add_documents(self):
        """测试添加文档"""
        url = f"{self.base_url}/knowledge-base/add-documents"
        test_data = {
            "documents": [
                {
                    "question": "什么是向量数据库？",
                    "answer": "向量数据库是一种专门用于存储和检索向量数据的数据库系统。",
                    "category": "数据库"
                },
                {
                    "question": "Ollama 是什么？",
                    "answer": "Ollama 是一个轻量级的本地大语言模型运行框架。",
                    "category": "AI 工具"
                }
            ]
        }
        try:
            response = requests.post(url, json=test_data)
            response.raise_for_status()
            result = response.json()
            print("\n=== 测试添加文档 ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"响应状态码: {e.response.status_code}")
                try:
                    print(f"响应内容: {e.response.json()}")
                except:
                    print(f"响应内容: {e.response.text}")
            return None

if __name__ == "__main__":
    # 初始化测试类
    test = TestKnowledgeBase()
    
    # 运行所有测试
    test.test_list_databases()
    test.test_create_database()
    test.test_create_knowledge_base()
    test.test_check_knowledge_base_status()
    test.test_add_documents()
