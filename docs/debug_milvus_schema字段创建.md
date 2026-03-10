你的观察非常敏锐！问题出在 client.create_collection 的调用方式上。

❌ 问题根源

你使用的代码：
client.create_collection(
    collection_name=collection_name,
    dimension=1024,
    primary_field_name="id",
    vector_field_name="embedding",
    metric_type="L2"
)

这种写法是 PyMilvus 的 “快捷模式” (Auto Schema)。
当你只指定 id 和 embedding 时，Milvus 会认为：“除了这两个字段，其他所有传入的数据都塞进一个默认的 JSON 字段里吧！”
这个默认的 JSON 字段通常就叫 meta 或者 dynamic_field。
所以，你传入的 content, file_id, chunk_index 等字段，全被它当成“动态字段”打包存进 JSON 了，而不是独立的列。

✅ 解决方案

你需要使用 “显式 Schema 模式”，手动定义每一个字段的类型和属性。这样 Milvus 才会为它们创建独立的列，而不是扔进 JSON。

请使用 milvus_client.CreateCollectionParams 和 FieldSchema 来重构创建部分的代码。

🛠️ 修改后的代码

请将你的 test_create_collection_with_schema 函数中 创建集合 的部分替换为以下代码：

from pymilvus import MilvusClient, DataType, FieldSchema, CreateCollectionParams

... (前面的代码保持不变) ...

        # --- 修改开始：显式定义 Schema ---
        print("正在定义 Schema...")
        
        # 1. 定义主键
        pk_field = FieldSchema(
            name="id", 
            dtype=DataType.INT64, 
            is_primary=True, 
            auto_id=False  # 这里我们手动指定 ID，所以设为 False
        )
        
        # 2. 定义向量字段
        vector_field = FieldSchema(
            name="embedding", 
            dtype=DataType.FLOAT_VECTOR, 
            dim=1024
        )
        
        # 3. 定义普通标量字段 (这才是关键！)
        content_field = FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535)
        file_id_field = FieldSchema(name="file_id", dtype=DataType.VARCHAR, max_length=128)
        file_name_field = FieldSchema(name="file_name", dtype=DataType.VARCHAR, max_length=256)
        chunk_index_field = FieldSchema(name="chunk_index", dtype=DataType.INT64)
        
        # 4. 定义 JSON 字段 (只存真正的动态元数据)
        meta_field = FieldSchema(name="metadata", dtype=DataType.JSON)

        # 5. 组装 Schema
        schema = [pk_field, vector_field, content_field, file_id_field, file_name_field, chunk_index_field, meta_field]

        # 6. 创建集合参数对象
        params = CreateCollectionParams(
            collection_name=collection_name,
            schema=schema,
            index_params=[
                {
                    "field_name": "embedding",
                    "index_type": "AUTOINDEX",
                    "metric_type": "L2"
                }
            ]
        )
        
        print("正在创建集合 (显式 Schema)...")
        client.create_collection(params=params)
        # --- 修改结束 ---

        print("集合创建成功！")
        
        # ... (后面的插入和查询代码保持不变) ...

🔍 修改点详解

引入必要类：导入了 DataType, FieldSchema, CreateCollectionParams。
逐个定义字段：
    content, file_id, file_name: 定义为 VARCHAR (字符串)。
    chunk_index: 定义为 INT64 (整数)，这样以后就可以做排序和范围查询了。
    metadata: 专门留一个 JSON 字段给你存那些不固定的键值对（如 key1, key2）。
使用 CreateCollectionParams：不再直接传 dimension 等参数给 create_collection，而是把定义好的 schema 列表传进去。

💡 预期结果

运行修改后的代码，再去 Milvus 界面查看 Schema，你会发现：

之前：只有 id, embedding, meta (里面塞了一堆东西)。
现在：会有清晰的独立列：
  # id (Int64)
  ~ embedding (FloatVector)
  content (VarChar)  <-- ✅ 独立列
  file_id (VarChar)   <-- ✅ 独立列
  file_name (VarChar) <-- ✅ 独立列
  chunk_index (Int64) <-- ✅ 独立列
  metadata (JSON)     <-- ✅ 只存真正的动态数据

这样设计后，你就可以针对 file_id 或 chunk_index 建立索引，实现高效的过滤和排序了！