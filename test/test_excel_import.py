import requests
import os
import random
import string

# 生成随机知识库名称
def generate_random_collection_name():
    return 'test_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# 测试 /excel/import 接口
def test_excel_import():
    url = 'http://localhost:8000/excel/import'
    file_path = '/Users/ljn/Documents/demo/OllamaRag/static/template2.xlsx'
    collection_name = generate_random_collection_name()
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    try:
        # 准备文件上传和表单数据
        with open(file_path, 'rb') as f:
            files = {'file': ('template2.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            data = {
                'collection_name': collection_name,
                'fields': '名称,描述'  # 测试字段合并功能
            }
            response = requests.post(url, files=files, data=data)
        
        # 打印响应结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        print(f"测试的知识库名称: {collection_name}")
        
        if response.status_code == 200:
            print("测试成功!")
        else:
            print("测试失败!")
    except Exception as e:
        print(f"测试过程中发生错误: {e}")


def test_excel_import2():
    url = 'http://localhost:8000/excel/import'
    file_path = '/Users/ljn/Documents/demo/OllamaRag/static/rag_test_dataset.xlsx'
    collection_name = "ollama_rag"

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return

    try:
        # 准备文件上传和表单数据
        with open(file_path, 'rb') as f:
            files = {'file': ('rag_test_dataset.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            data = {
                'collection_name': collection_name,
                'fields': 'question,category'  # 测试字段合并功能
            }
            response = requests.post(url, files=files, data=data)

        # 打印响应结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        print(f"测试的知识库名称: {collection_name}")

        if response.status_code == 200:
            print("测试成功!")
        else:
            print("测试失败!")
    except Exception as e:
        print(f"测试过程中发生错误: {e}")

# 测试 /excel/import 接口 - 不指定字段
def test_excel_import_no_fields():
    url = 'http://localhost:8000/excel/import'
    file_path = '/Users/ljn/Documents/demo/OllamaRag/static/template2.xlsx'
    collection_name = generate_random_collection_name()
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    try:
        # 准备文件上传和表单数据（不指定 fields）
        with open(file_path, 'rb') as f:
            files = {'file': ('template2.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            data = {
                'collection_name': collection_name
            }
            response = requests.post(url, files=files, data=data)
        
        # 打印响应结果
        print(f"\n测试不指定字段:")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        print(f"测试的知识库名称: {collection_name}")
        
        if response.status_code == 200:
            print("测试成功!")
        else:
            print("测试失败!")
    except Exception as e:
        print(f"测试过程中发生错误: {e}")

if __name__ == "__main__":
    print("测试 /excel/import 接口")
    print("=" * 50)
    test_excel_import()
    # test_excel_import2()
    print("\n" + "=" * 50)
    # test_excel_import_no_fields()
