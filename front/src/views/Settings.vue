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
        <router-link to="/documents" class="sidebar-item">
          <i class="fa fa-file-text w-5 text-center"></i>
          <span>文档管理</span>
        </router-link>
        <router-link to="/settings" class="sidebar-item active">
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
          <h2 class="text-2xl font-bold text-dark">设置</h2>
          <p class="text-gray-500">配置系统参数</p>
        </div>
        <div class="flex space-x-3">
          <button @click="saveSettings" class="btn btn-primary">
            <i class="fa fa-save"></i>
            <span>保存设置</span>
          </button>
        </div>
      </div>

      <!-- 服务器设置 -->
      <div class="card mb-8">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-semibold text-dark">服务器设置</h3>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">服务器端口</label>
            <input type="number" v-model="settings.server.port" class="input-field" min="1" max="65535">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">主机地址</label>
            <input type="text" v-model="settings.server.host" class="input-field">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">调试模式</label>
            <div class="flex items-center space-x-2">
              <input type="radio" id="debug-true" name="debug" v-model="settings.server.debug" :value="true">
              <label for="debug-true">开启</label>
              <input type="radio" id="debug-false" name="debug" v-model="settings.server.debug" :value="false">
              <label for="debug-false">关闭</label>
            </div>
          </div>
        </div>
      </div>

      <!-- Milvus 设置 -->
      <div class="card mb-8">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-semibold text-dark">Milvus 设置</h3>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Milvus 主机</label>
            <input type="text" v-model="settings.milvus.host" class="input-field">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Milvus 端口</label>
            <input type="number" v-model="settings.milvus.port" class="input-field" min="1" max="65535">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">默认向量维度</label>
            <input type="number" v-model="settings.milvus.dimension" class="input-field" min="1">
          </div>
        </div>
      </div>

      <!-- Ollama 设置 -->
      <div class="card mb-8">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-semibold text-dark">Ollama 设置</h3>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Ollama 主机</label>
            <input type="text" v-model="settings.ollama.host" class="input-field">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Ollama 端口</label>
            <input type="number" v-model="settings.ollama.port" class="input-field" min="1" max="65535">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">默认模型</label>
            <input type="text" v-model="settings.ollama.model" class="input-field">
          </div>
        </div>
      </div>

      <!-- 系统信息 -->
      <div class="card">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-semibold text-dark">系统信息</h3>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">系统版本</label>
            <input type="text" v-model="systemInfo.version" class="input-field" readonly>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Python 版本</label>
            <input type="text" v-model="systemInfo.pythonVersion" class="input-field" readonly>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Milvus 版本</label>
            <input type="text" v-model="systemInfo.milvusVersion" class="input-field" readonly>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Ollama 版本</label>
            <input type="text" v-model="systemInfo.ollamaVersion" class="input-field" readonly>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'AppSettings',
  data() {
    return {
      settings: {
        server: {
          port: 8000,
          host: '0.0.0.0',
          debug: true
        },
        milvus: {
          host: 'localhost',
          port: 19530,
          dimension: 1024
        },
        ollama: {
          host: 'localhost',
          port: 11434,
          model: 'llama3'
        }
      },
      systemInfo: {
        version: '1.0.0',
        pythonVersion: '3.9.13',
        milvusVersion: '2.6.9',
        ollamaVersion: '0.1.30'
      }
    }
  },
  methods: {
    saveSettings() {
      console.log('保存设置...')
      // 这里可以添加保存设置的逻辑
      alert('设置保存成功！')
    }
  }
}
</script>

<style scoped>
/* 组件特定样式 */
</style>