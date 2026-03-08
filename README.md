# OllamaRag - 基于 Ollama 和 Milvus 的知识库管理系统

## 项目介绍

OllamaRag 是一个基于 Ollama 大语言模型和 Milvus 向量数据库的知识库管理系统，支持知识库的创建、文档管理、向量检索等功能。

### 核心功能

- **知识库管理**：创建、删除、查看知识库
- **文档管理**：添加、编辑、删除文档
- **向量检索**：基于向量相似度的智能检索
- **Web 界面**：直观的 Coze 风格管理界面
- **RESTful API**：完整的 API 接口支持

## 技术栈

### 后端
- Python 3.9+
- FastAPI
- Milvus 2.6.9
- Ollama

### 前端
- Vue 3
- Vue Router
- Tailwind CSS
- Axios

## 快速开始

### 前提条件

- Python 3.9 或更高版本
- Milvus 2.6.9 或更高版本
- Ollama

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/ArtLjn/OllamaRag.git
cd OllamaRag
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **启动 Milvus**

确保 Milvus 服务已经启动并运行在默认端口 19530。

4. **启动 Ollama**

确保 Ollama 服务已经启动并运行在默认端口 11434。

5. **启动后端服务**

```bash
python api.py
```

后端服务将运行在 `http://localhost:8000`。

6. **启动前端服务**

```bash
cd front
npm install
npm run serve
```

前端服务将运行在 `http://localhost:8080`。

## API 接口

### 知识库管理

- `GET /knowledge-base/status` - 检查知识库状态
- `POST /knowledge-base/create?collection_name={name}` - 创建知识库
- `DELETE /knowledge-base/delete` - 删除知识库
- `GET /knowledge-base/list` - 获取知识库列表
- `GET /knowledge-base/info?collection_name={name}` - 获取知识库信息

### 文档管理

- `POST /knowledge-base/add` - 添加单个文档
- `POST /knowledge-base/add-documents` - 批量添加文档

### 数据库管理

- `GET /databases` - 列出所有数据库
- `POST /databases/create` - 创建数据库
- `DELETE /databases/delete` - 删除数据库

### 集合管理

- `GET /collections` - 列出所有集合
- `GET /collections/{collection_name}` - 获取集合详细信息

## 项目结构

```
OllamaRag/
├── core/                  # 核心代码
│   ├── configs/         # 配置文件
│   ├── exceptions/      # 自定义异常
│   ├── interfaces/      # 抽象接口
│   ├── models/          # 数据模型
│   ├── repositories/    # 数据访问层
│   └── services/        # 业务逻辑层
├── front/               # 前端代码
│   ├── public/          # 静态资源
│   └── src/             # 源代码
├── test/                # 测试代码
├── api.py               # 后端入口
├── requirements.txt     # 依赖文件
└── README.md            # 项目说明
```

## 使用指南

### 1. 创建知识库

1. 打开前端界面 `http://localhost:8080`
2. 点击侧边栏的 "知识库" 选项
3. 点击 "创建知识库" 按钮
4. 输入知识库名称和描述
5. 点击 "创建" 按钮

### 2. 添加文档

1. 打开前端界面 `http://localhost:8080`
2. 点击侧边栏的 "文档管理" 选项
3. 选择要添加文档的知识库
4. 点击 "添加文档" 按钮
5. 输入问题、回答和分类
6. 点击 "添加" 按钮

### 3. 查看知识库

1. 打开前端界面 `http://localhost:8080`
2. 点击侧边栏的 "知识库" 选项
3. 点击知识库列表中的 "查看" 按钮
4. 查看知识库详细信息

## 配置说明

### Milvus 配置

在 `core/configs/settings.py` 文件中配置 Milvus 连接信息：

```python
MILVUS_CONFIG = {
    'host': 'localhost',
    'port': '19530',
    'database_name': 'ollama_rag_db',
    'collection_name': 'ollama_rag'
}
```

### Ollama 配置

在 `core/configs/settings.py` 文件中配置 Ollama 连接信息：

```python
OLLAMA_CONFIG = {
    'host': 'localhost',
    'port': '11434',
    'model': 'llama3'
}
```

## 故障排除

### 1. Milvus 连接失败

- 确保 Milvus 服务已经启动
- 检查 Milvus 配置中的主机和端口是否正确
- 确保网络连接正常

### 2. Ollama 连接失败

- 确保 Ollama 服务已经启动
- 检查 Ollama 配置中的主机和端口是否正确
- 确保网络连接正常

### 3. 文档添加失败

- 确保知识库已经创建
- 检查文档格式是否正确
- 查看后端日志获取详细错误信息

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

本项目采用 MIT 许可证。
