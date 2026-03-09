import requests
import os

# 测试 /excel/parse 接口
def test_excel_parse():
    url = 'http://localhost:8000/excel/parse'
    file_path = '/Users/ljn/Documents/demo/OllamaRag/static/template2.xlsx'
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    try:
        # 准备文件上传
        with open(file_path, 'rb') as f:
            files = {'file': ('template2.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post(url, files=files)
        
        # 打印响应结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("测试成功!")
        else:
            print("测试失败!")
    except Exception as e:
        print(f"测试过程中发生错误: {e}")

if __name__ == "__main__":
    test_excel_parse()
