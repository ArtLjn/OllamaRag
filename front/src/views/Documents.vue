<template>
  <div class="flex">
    <!-- 侧边栏 -->
    <aside class="w-64 bg-white shadow-sm fixed h-full left-0 top-0 z-10">
      <div class="p-4 border-b">
        <div class="flex items-center space-x-2">
          <i class="fa fa-database text-primary text-2xl"></i>
          <h1 class="text-xl font-bold text-dark">知识库管理</h1>
        </div>
      </div>
      <nav class="mt-6 px-3">
        <router-link to="/" class="sidebar-item">
          <i class="fa fa-home w-5 text-center"></i>
          <span>控制台</span>
        </router-link>
        <router-link to="/knowledge-bases" class="sidebar-item">
          <i class="fa fa-book w-5 text-center"></i>
          <span>知识库</span>
          <span class="badge badge-primary ml-auto">3</span>
        </router-link>
        <router-link to="/documents" class="sidebar-item active">
          <i class="fa fa-file-text w-5 text-center"></i>
          <span>文档管理</span>
        </router-link>
        <router-link to="/settings" class="sidebar-item">
          <i class="fa fa-cog w-5 text-center"></i>
          <span>设置</span>
        </router-link>
      </nav>
      <div class="absolute bottom-0 left-0 right-0 p-4 border-t">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center">
            <i class="fa fa-user"></i>
          </div>
          <div>
            <p class="text-sm font-medium text-dark">管理员</p>
            <p class="text-xs text-gray-500">admin@example.com</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- 主内容 -->
    <main class="flex-1 ml-64 p-6">
      <!-- 顶部导航 -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h2 class="text-2xl font-bold text-dark">文档管理</h2>
          <p class="text-gray-500">管理知识库中的文档</p>
        </div>
        <div class="flex space-x-3">
          <div class="relative">
            <input type="text" v-model="searchKeyword" placeholder="搜索文档" class="w-48 px-4 py-2 pl-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
            <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
              <i class="fa fa-search"></i>
            </span>
          </div>
          <button @click="showAddDocModal = true" class="btn btn-primary">
            <i class="fa fa-plus"></i>
            <span>添加文档</span>
          </button>
        </div>
      </div>

      <!-- 知识库选择 -->
      <div class="card mb-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-dark">选择知识库</h3>
        </div>
        <div class="flex space-x-3">
          <select v-model="selectedKnowledgeBase" class="input-field flex-1">
            <option v-for="kb in knowledgeBases" :key="kb.collection_name" :value="kb.collection_name">
              {{ kb.collection_name }} ({{ kb.description || '无描述' }})
            </option>
          </select>
          <button @click="loadKnowledgeBases" class="btn btn-outline">
            <i class="fa fa-refresh"></i>
          </button>
        </div>
      </div>

      <!-- 文档列表 -->
      <div class="card mb-8">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-semibold text-dark">文档列表</h3>
          <div class="flex space-x-2">
            <button class="btn btn-outline">
              <i class="fa fa-filter"></i>
              <span>筛选</span>
            </button>
            <button class="btn btn-outline">
              <i class="fa fa-sort"></i>
              <span>排序</span>
            </button>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  问题
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  分类
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  创建时间
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="doc in documents" :key="doc.id">
                <td class="px-6 py-4">
                  <div class="text-sm font-medium text-gray-900">{{ doc.question }}</div>
                </td>
                <td class="px-6 py-4">
                  <span class="badge badge-secondary">{{ doc.category }}</span>
                </td>
                <td class="px-6 py-4">
                  <div class="text-sm text-gray-500">{{ doc.created_at || '2026-03-08 10:00' }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex space-x-2">
                    <button @click="editDocument(doc.id)" class="text-primary hover:text-primary/80">
                      <i class="fa fa-edit"></i>
                    </button>
                    <button @click="viewDocument(doc.id)" class="text-gray-600 hover:text-gray-900">
                      <i class="fa fa-eye"></i>
                    </button>
                    <button @click="deleteDocument(doc.id)" class="text-danger hover:text-danger/80">
                      <i class="fa fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="mt-6 flex justify-between items-center">
          <div class="text-sm text-gray-500">
            显示 1-{{ documents.length }} 条，共 {{ documents.length }} 条
          </div>
          <div class="flex space-x-1">
            <button class="px-3 py-1 rounded-md border border-gray-300 text-gray-500 hover:bg-gray-50">上一页</button>
            <button class="px-3 py-1 rounded-md border border-primary bg-primary text-white">1</button>
            <button class="px-3 py-1 rounded-md border border-gray-300 text-gray-500 hover:bg-gray-50">2</button>
            <button class="px-3 py-1 rounded-md border border-gray-300 text-gray-500 hover:bg-gray-50">下一页</button>
          </div>
        </div>
      </div>
    </main>

    <!-- 添加文档模态框 -->
    <div v-if="showAddDocModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4">
        <div class="p-4 border-b flex justify-between items-center">
          <h2 class="text-lg font-semibold text-dark">添加文档</h2>
          <button @click="showAddDocModal = false" class="text-gray-500 hover:text-gray-700">
            <i class="fa fa-times text-xl"></i>
          </button>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">问题</label>
              <input type="text" v-model="newDocument.question" class="input-field" placeholder="请输入问题">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">回答</label>
              <textarea v-model="newDocument.answer" class="textarea-field" rows="4" placeholder="请输入回答"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">分类</label>
              <input type="text" v-model="newDocument.category" class="input-field" placeholder="请输入分类">
            </div>
          </div>
        </div>
        <div class="p-4 border-t flex justify-end space-x-2">
          <button @click="showAddDocModal = false" class="btn btn-outline">
            取消
          </button>
          <button @click="addDocument" class="btn btn-primary">
            添加
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AppDocuments',
  data() {
    return {
      knowledgeBases: [],
      selectedKnowledgeBase: '',
      documents: [
        {
          id: 1,
          question: '什么是向量数据库？',
          answer: '向量数据库是一种专门用于存储和检索向量嵌入的数据库，它能够高效地处理相似性搜索和推荐系统等任务。',
          category: '数据库',
          created_at: '2026-03-08 10:00'
        },
        {
          id: 2,
          question: 'Ollama 是什么？',
          answer: 'Ollama 是一个用于本地运行大型语言模型的工具，它允许用户在自己的设备上部署和使用各种开源LLM。',
          category: 'AI 工具',
          created_at: '2026-03-08 10:05'
        },
        {
          id: 3,
          question: '如何使用 Milvus？',
          answer: 'Milvus 是一个开源的向量数据库，使用它需要先安装并启动服务，然后通过 SDK 或 API 进行操作。',
          category: '数据库',
          created_at: '2026-03-08 10:10'
        }
      ],
      searchKeyword: '',
      showAddDocModal: false,
      newDocument: {
        question: '',
        answer: '',
        category: ''
      }
    }
  },
  methods: {
    async loadKnowledgeBases() {
      try {
        console.log('获取知识库列表...')
        const response = await axios.get('http://localhost:8000/knowledge-base/list')
        if (response.data.success) {
          console.log('获取知识库列表成功')
          this.knowledgeBases = response.data.data
          if (this.knowledgeBases.length > 0 && !this.selectedKnowledgeBase) {
            this.selectedKnowledgeBase = this.knowledgeBases[0].collection_name
          }
        } else {
          console.log('获取知识库列表失败')
          this.knowledgeBases = []
        }
      } catch (error) {
        console.error('获取知识库列表失败:', error)
        this.knowledgeBases = []
      }
    },
    async addDocument() {
      try {
        console.log('添加文档...')
        const response = await axios.post('http://localhost:8000/knowledge-base/add', {
          question: this.newDocument.question,
          answer: this.newDocument.answer,
          category: this.newDocument.category
        })
        if (response.data.success) {
          console.log('文档添加成功')
          this.showAddDocModal = false
          this.newDocument = {
            question: '',
            answer: '',
            category: ''
          }
          // 重新加载文档列表
          this.loadDocuments()
        } else {
          console.log('文档添加失败')
        }
      } catch (error) {
        console.error('添加文档失败:', error)
      }
    },
    async loadDocuments() {
      // 这里可以添加加载文档列表的逻辑
      console.log('加载文档列表...')
    },
    editDocument(id) {
      console.log(`编辑文档 ${id}`)
    },
    viewDocument(id) {
      console.log(`查看文档 ${id}`)
    },
    deleteDocument(id) {
      if (confirm('确定要删除这个文档吗？')) {
        console.log(`删除文档 ${id}`)
      }
    }
  },
  mounted() {
    this.loadKnowledgeBases()
  }
}
</script>

<style scoped>
/* 组件特定样式 */
</style>