# 测试集合查看方法
import requests
import json

class TestCollections:
    """集合测试类"""
    
    def __init__(self):
        """初始化测试类"""
        self.base_url = "http://localhost:8000"
    
    def test_list_collections(self):
        """测试列出所有集合"""
        url = f"{self.base_url}/collections"
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            print("=== 测试列出所有集合 ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def test_describe_collection(self, collection_name):
        """测试获取集合详细信息"""
        url = f"{self.base_url}/collections/{collection_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            print(f"\n=== 测试获取集合 {collection_name} 详细信息 ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

if __name__ == "__main__":
    # 初始化测试类
    test = TestCollections()
    
    # 运行测试
    collections = test.test_list_collections()
    
    # 如果有集合，测试获取详细信息
    if collections and collections.get('collections'):
        for collection in collections['collections']:
            test.test_describe_collection(collection)
