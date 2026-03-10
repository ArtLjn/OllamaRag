from pymilvus import MilvusClient, DataType
import random
import string
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 生成随机集合名称
def generate_random_collection_name():
    return 'test_schema_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# 测试创建带有指定 schema 的集合
def test_create_collection_with_schema():
    print("测试创建带有指定 schema 的集合")
    print("=" * 60)
    
    # 创建 Milvus 客户端
    from core.configs.settings import MILVUS_CONFIG
    client = MilvusClient(
        uri=f"http://{MILVUS_CONFIG['host']}:{MILVUS_CONFIG['port']}",
        db_name=MILVUS_CONFIG['database_name']
    )
    
    # 生成随机集合名称
    collection_name = generate_random_collection_name()
    print(f"集合名称: {collection_name}")
    
    try:
        # 检查集合是否存在，如果存在则删除
        if client.has_collection(collection_name=collection_name):
            client.drop_collection(collection_name=collection_name)
            print(f"已删除 existing collection: {collection_name}")
        
        # 创建 schema
        print("正在创建 schema...")
        schema = client.create_schema(
            auto_id=False,
            enable_dynamic_field=True,
        )
        
        # 添加字段
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=1024)
        schema.add_field(field_name="content", datatype=DataType.VARCHAR, max_length=65535)
        schema.add_field(field_name="file_id", datatype=DataType.VARCHAR, max_length=64)
        schema.add_field(field_name="file_name", datatype=DataType.VARCHAR, max_length=256)
        schema.add_field(field_name="chunk_index", datatype=DataType.INT32)
        
        # 准备索引参数
        print("正在准备索引参数...")
        index_params = client.prepare_index_params()
        
        # 添加索引
        index_params.add_index(
            field_name="id",
            index_type="AUTOINDEX"
        )
        
        index_params.add_index(
            field_name="embedding", 
            index_type="AUTOINDEX",
            metric_type="L2"
        )
        
        # 创建集合
        print("正在创建集合...")
        client.create_collection(
            collection_name=collection_name,
            schema=schema,
            index_params=index_params
        )
        print("集合创建成功！")
        
        # 测试插入数据
        print("\n测试插入数据...")
        test_data = [
            {
                "id": 1,
                "embedding": [0.1] * 1024,  # 简化的向量
                "content": "测试内容1",
                "file_id": "test_file_id_1",
                "file_name": "test_file1.xlsx",
                "chunk_index": 0,
                "metadata": {"key1": "value1", "key2": "value2"}
            },
            {
                "id": 2,
                "embedding": [0.2] * 1024,  # 简化的向量
                "content": "测试内容2",
                "file_id": "test_file_id_2",
                "file_name": "test_file2.xlsx",
                "chunk_index": 1,
                "metadata": {"key1": "value3", "key2": "value4"}
            }
        ]
        
        result = client.insert(collection_name=collection_name, data=test_data)
        print(f"插入成功，插入数量: {len(result)}")
        print(f"插入结果: {result}")
        
        # 等待一小段时间，确保数据已提交
        import time
        print("\n等待数据提交...")
        time.sleep(2)
        
        # 描述集合
        print("\n集合详情:")
        collection_info = client.describe_collection(collection_name=collection_name)
        print(f"集合名称: {collection_info['collection_name']}")
        print(f"字段数: {len(collection_info['fields'])}")
        
        # 打印所有字段
        print("\n字段信息:")
        for field in collection_info['fields']:
            print(f"  - {field['name']}: {field['type']}")
            if 'params' in field:
                print(f"    参数: {field['params']}")
        
        # 加载集合
        print("\n正在加载集合...")
        client.load_collection(collection_name=collection_name)
        print("集合加载成功！")
        
        # 测试查询
        print("\n测试查询数据...")
        results = client.query(
            collection_name=collection_name,
            filter="",
            output_fields=["*"],
            limit=10
        )
        print(f"查询结果数量: {len(results)}")
        if results:
            for i, result in enumerate(results):
                print(f"\n结果 {i+1}:")
                for field, value in result.items():
                    if field != "embedding":  # 不打印向量
                        print(f"  {field}: {value}")
        
        # 保留集合，不删除
        print(f"\n集合 '{collection_name}' 已创建并插入数据，可在 Milvus 中查看")
        print("测试完成！")
        
    except Exception as e:
        print(f"测试失败: {e}")
        # 清理
        if client.has_collection(collection_name=collection_name):
            client.drop_collection(collection_name=collection_name)

if __name__ == "__main__":
    test_create_collection_with_schema()
