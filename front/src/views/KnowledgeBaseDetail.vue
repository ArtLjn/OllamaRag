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
          <div class="flex items-center space-x-2 mb-2">
            <router-link to="/knowledge-bases" class="text-gray-500 hover:underline">根目录</router-link>
            <span class="text-gray-500">/</span>
            <span class="text-primary font-medium">{{ knowledgeBaseName }}</span>
          </div>
          <div class="flex items-center space-x-4">
            <h2 class="text-xl font-bold text-dark">数据集</h2>
            <button class="text-primary hover:underline">搜索测试</button>
          </div>
        </div>
        <div class="flex space-x-3">
          <div class="relative">
            <input type="text" v-model="searchKeyword" placeholder="搜索" class="w-48 px-4 py-2 pl-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
            <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
              <i class="fa fa-search"></i>
            </span>
          </div>
          <div class="relative">
            <select v-model="filterLabel" class="w-32 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
              <option value="">标签</option>
              <option value="all">全部</option>
              <option value="excel">Excel</option>
              <option value="txt">文本</option>
            </select>
          </div>
          <router-link :to="{ path: '/excel-import', query: { collection_name: knowledgeBaseName } }" class="btn btn-primary">
            <i class="fa fa-plus"></i>
            <span>新建/导入</span>
          </router-link>
        </div>
      </div>

      <!-- 文件列表 -->
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <div class="flex items-center space-x-2">
            <i class="fa fa-folder text-gray-500"></i>
            <span class="font-medium">文件 ({{ files.length }})</span>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <div class="flex items-center">
                    <input type="checkbox" class="mr-2">
                    <span>名称</span>
                  </div>
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  处理模式
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  数量
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  创建/更新时间
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  状态
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  启用
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="file in files" :key="file.id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <input type="checkbox" class="mr-3">
                    <div class="flex items-center">
                      <div class="w-8 h-8 rounded-md bg-green-100 flex items-center justify-center mr-3">
                        <i class="fa fa-file-excel-o text-green-600"></i>
                      </div>
                      <div>
                        <div class="text-sm font-medium text-gray-900">{{ file.name }}</div>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ file.processingMode }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ file.count }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ file.timestamp }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="badge badge-success flex items-center">
                    <i class="fa fa-check-circle mr-1"></i>
                    {{ file.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" :checked="file.enabled" class="sr-only peer" @change="toggleFileStatus(file.id)">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                  </label>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button class="text-gray-600 hover:text-gray-900">
                    <i class="fa fa-ellipsis-v"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="files.length === 0">
                <td colspan="7" class="px-6 py-8 text-center text-gray-500">
                  <div class="flex flex-col items-center">
                    <i class="fa fa-folder-open text-4xl text-gray-300 mb-3"></i>
                    <p>暂无文件</p>
                    <p class="text-sm mt-1">点击「新建/导入」按钮添加文件</p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>


  </div>
</template>

<script>
export default {
  name: 'KnowledgeBaseDetail',
  data() {
    return {
      knowledgeBaseName: '',
      files: [],
      searchKeyword: '',
      filterLabel: ''
    }
  },
  mounted() {
    // 从路由参数中获取知识库名称
    this.knowledgeBaseName = this.$route.params.name || '知识库'
    this.loadFiles()
  },
  methods: {
    loadFiles() {
      // 模拟数据，实际应该从API获取
      this.files = [
        {
          id: 1,
          name: 'template2.xlsx',
          processingMode: '分块存储',
          count: 1,
          timestamp: '2026-03-09 10:45',
          status: '已就绪',
          enabled: true
        }
      ]
    },
    toggleFileStatus(fileId) {
      const file = this.files.find(f => f.id === fileId)
      if (file) {
        file.enabled = !file.enabled
      }
    }
  }
}
</script>

<style scoped>
/* 组件特定样式 */
</style>