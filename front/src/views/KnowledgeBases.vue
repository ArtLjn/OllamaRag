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
        <router-link to="/knowledge-bases" class="sidebar-item active">
          <i class="fa fa-book w-5 text-center"></i>
          <span>知识库</span>
          <span class="badge badge-primary ml-auto">{{ knowledgeBases.length }}</span>
        </router-link>
        <router-link to="/documents" class="sidebar-item">
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
          <h2 class="text-2xl font-bold text-dark">知识库</h2>
          <p class="text-gray-500">管理您的知识库</p>
        </div>
        <div class="flex space-x-3">
          <div class="relative">
            <input type="text" v-model="searchKeyword" placeholder="搜索知识库" class="w-full px-4 py-2 pl-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
            <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
              <i class="fa fa-search"></i>
            </span>
          </div>
          <button @click="showCreateKbModal = true" class="btn btn-primary">
            <i class="fa fa-plus"></i>
            <span>创建知识库</span>
          </button>
        </div>
      </div>

      <!-- 知识库列表 -->
      <div class="card mb-8">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-semibold text-dark">知识库列表</h3>
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
                  名称
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  文档数
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  创建时间
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  状态
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="knowledgeBases.length === 0">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                  加载中...
                </td>
              </tr>
              <tr v-for="kb in knowledgeBases" :key="kb.collection_name">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="w-8 h-8 rounded-md bg-primary-light flex items-center justify-center mr-3">
                      <i class="fa fa-book text-primary"></i>
                    </div>
                    <div>
                      <router-link :to="`/knowledge-base/${kb.collection_name}`" class="text-sm font-medium text-primary hover:underline">{{ kb.collection_name }}</router-link>
                      <div class="text-xs text-gray-500">{{ kb.description || '无描述' }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ kb.document_count || 0 }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ kb.created_at || '未知' }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="badge badge-secondary">正常</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex space-x-2">
                    <button @click="editKnowledgeBase(kb.collection_name)" class="text-primary hover:text-primary/80">
                      <i class="fa fa-edit"></i>
                    </button>
                    <router-link :to="`/knowledge-base/${kb.collection_name}`" class="text-gray-600 hover:text-gray-900">
                      <i class="fa fa-eye"></i>
                    </router-link>
                    <button @click="deleteKnowledgeBase(kb.collection_name)" class="text-danger hover:text-danger/80">
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
            显示 1-{{ knowledgeBases.length }} 条，共 {{ knowledgeBases.length }} 条
          </div>
          <div class="flex space-x-1">
            <button class="px-3 py-1 rounded-md border border-gray-300 text-gray-500 hover:bg-gray-50">上一页</button>
            <button class="px-3 py-1 rounded-md border border-primary bg-primary text-white">1</button>
            <button class="px-3 py-1 rounded-md border border-gray-300 text-gray-500 hover:bg-gray-50">下一页</button>
          </div>
        </div>
      </div>

      <!-- 知识库详情 -->
      <div v-if="selectedKnowledgeBase" class="card">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-semibold text-dark">知识库详情</h3>
          <button @click="selectedKnowledgeBase = null" class="btn btn-outline">
            <i class="fa fa-times"></i>
            <span>关闭</span>
          </button>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">知识库名称</label>
            <input type="text" v-model="selectedKnowledgeBase.collection_name" class="input-field" readonly>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
            <textarea v-model="selectedKnowledgeBase.description" class="textarea-field" rows="3" readonly></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">创建时间</label>
            <input type="text" v-model="selectedKnowledgeBase.created_at" class="input-field" readonly>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">文档数</label>
            <input type="text" v-model="selectedKnowledgeBase.document_count" class="input-field" readonly>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">向量维度</label>
            <input type="text" v-model="selectedKnowledgeBase.dimension" class="input-field" readonly>
          </div>
        </div>
        <div class="mt-6 flex space-x-2">
          <button class="btn btn-primary flex-1">
            <i class="fa fa-edit mr-1"></i> 编辑
          </button>
          <router-link :to="{ path: '/documents' }" class="btn btn-outline flex-1">
            <i class="fa fa-file-text mr-1"></i> 管理文档
          </router-link>
          <button class="btn btn-danger flex-1">
            <i class="fa fa-trash mr-1"></i> 删除
          </button>
        </div>
      </div>
    </main>

    <!-- 创建知识库模态框 -->
    <div v-if="showCreateKbModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-4 border-b flex justify-between items-center">
          <h2 class="text-lg font-semibold text-dark">创建知识库</h2>
          <button @click="showCreateKbModal = false" class="text-gray-500 hover:text-gray-700">
            <i class="fa fa-times text-xl"></i>
          </button>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">知识库名称</label>
              <input type="text" v-model="newKnowledgeBase.name" class="input-field" placeholder="请输入知识库名称">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
              <textarea v-model="newKnowledgeBase.description" class="textarea-field" rows="3" placeholder="请输入知识库描述（可选）"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">默认向量维度</label>
              <select v-model="newKnowledgeBase.dimension" class="input-field">
                <option value="1024">1024</option>
                <option value="2048">2048</option>
                <option value="768">768</option>
              </select>
            </div>
          </div>
        </div>
        <div class="p-4 border-t flex justify-end space-x-2">
          <button @click="showCreateKbModal = false" class="btn btn-outline">
            取消
          </button>
          <button @click="createKnowledgeBase" class="btn btn-primary">
            创建
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AppKnowledgeBases',
  data() {
    return {
      knowledgeBases: [],
      selectedKnowledgeBase: null,
      searchKeyword: '',
      showCreateKbModal: false,
      newKnowledgeBase: {
        name: '',
        description: '',
        dimension: '1024'
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
        } else {
          console.log('获取知识库列表失败')
          this.knowledgeBases = []
        }
      } catch (error) {
        console.error('获取知识库列表失败:', error)
        this.knowledgeBases = []
      }
    },
    async getKnowledgeBaseDetail(collectionName) {
      try {
        console.log(`获取知识库 ${collectionName} 详情...`)
        const response = await axios.get('http://localhost:8000/knowledge-base/info', {
          params: {
            collection_name: collectionName
          }
        })
        if (response.data.success) {
          console.log('获取知识库详情成功')
          return response.data.data
        } else {
          console.log('获取知识库详情失败')
          return null
        }
      } catch (error) {
        console.error('获取知识库详情失败:', error)
        return null
      }
    },
    async createKnowledgeBase() {
      try {
        console.log('创建知识库...')
        const response = await axios.post('http://localhost:8000/knowledge-base/create', {}, {
          params: {
            collection_name: this.newKnowledgeBase.name || null
          }
        })
        if (response.data.success) {
          console.log('知识库创建成功')
          this.showCreateKbModal = false
          this.newKnowledgeBase = {
            name: '',
            description: '',
            dimension: '1024'
          }
          // 重新加载知识库列表
          this.loadKnowledgeBases()
        } else {
          console.log('知识库创建失败')
        }
      } catch (error) {
        console.error('创建知识库失败:', error)
      }
    },
    async viewKnowledgeBase(collectionName) {
      const detail = await this.getKnowledgeBaseDetail(collectionName)
      if (detail) {
        this.selectedKnowledgeBase = detail
      }
    },
    editKnowledgeBase(collectionName) {
      console.log(`编辑知识库 ${collectionName}`)
    },
    deleteKnowledgeBase(collectionName) {
      if (confirm(`确定要删除知识库 ${collectionName} 吗？`)) {
        console.log(`删除知识库 ${collectionName}`)
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