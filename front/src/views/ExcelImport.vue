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
        <router-link to="/excel-import" class="sidebar-item active">
          <i class="fa fa-file-excel-o w-5 text-center"></i>
          <span>Excel导入</span>
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
          <h2 class="text-2xl font-bold text-dark">Excel 知识库导入</h2>
          <p class="text-gray-500">上传 Excel 文件并导入到知识库</p>
        </div>
      </div>

      <!-- 步骤导航 -->
      <div class="card mb-6">
        <div class="p-6">
          <div class="flex items-center justify-center space-x-8">
            <div class="flex flex-col items-center">
              <div class="w-10 h-10 rounded-full flex items-center justify-center mb-2" :class="currentStep >= 1 ? 'bg-primary text-white' : 'bg-gray-200 text-gray-500'">
                {{ currentStep >= 1 ? '✓' : '1' }}
              </div>
              <span class="text-sm font-medium" :class="currentStep >= 1 ? 'text-primary' : 'text-gray-500'">上传</span>
            </div>
            <div class="h-0.5 flex-1" :class="currentStep >= 2 ? 'bg-primary' : 'bg-gray-200'"></div>
            <div class="flex flex-col items-center">
              <div class="w-10 h-10 rounded-full flex items-center justify-center mb-2" :class="currentStep >= 2 ? 'bg-primary text-white' : 'bg-gray-200 text-gray-500'">
                {{ currentStep >= 2 ? '✓' : '2' }}
              </div>
              <span class="text-sm font-medium" :class="currentStep >= 2 ? 'text-primary' : 'text-gray-500'">表结构配置</span>
            </div>
            <div class="h-0.5 flex-1" :class="currentStep >= 3 ? 'bg-primary' : 'bg-gray-200'"></div>
            <div class="flex flex-col items-center">
              <div class="w-10 h-10 rounded-full flex items-center justify-center mb-2" :class="currentStep >= 3 ? 'bg-primary text-white' : 'bg-gray-200 text-gray-500'">
                {{ currentStep >= 3 ? '✓' : '3' }}
              </div>
              <span class="text-sm font-medium" :class="currentStep >= 3 ? 'text-primary' : 'text-gray-500'">预览</span>
            </div>
            <div class="h-0.5 flex-1" :class="currentStep >= 4 ? 'bg-primary' : 'bg-gray-200'"></div>
            <div class="flex flex-col items-center">
              <div class="w-10 h-10 rounded-full flex items-center justify-center mb-2" :class="currentStep >= 4 ? 'bg-primary text-white' : 'bg-gray-200 text-gray-500'">
                {{ currentStep >= 4 ? '✓' : '4' }}
              </div>
              <span class="text-sm font-medium" :class="currentStep >= 4 ? 'text-primary' : 'text-gray-500'">数据处理</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 步骤内容 -->
      <div class="card">
        <!-- 步骤 1: 文件上传 -->
        <div v-if="currentStep === 1" class="p-6">
          <h3 class="text-lg font-semibold text-dark mb-6">上传 Excel 文件</h3>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <input 
              type="file" 
              accept=".xlsx,.xls" 
              class="hidden" 
              id="excel-file" 
              @change="handleFileUpload"
            />
            <label for="excel-file" class="cursor-pointer">
              <div class="flex flex-col items-center">
                <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                  <i class="fa fa-file-excel-o text-blue-500 text-2xl"></i>
                </div>
                <p class="text-gray-600">点击或拖拽文件到此处上传</p>
                <p class="text-sm text-gray-400 mt-1">支持 .xlsx 和 .xls 格式</p>
              </div>
            </label>
          </div>
          <div v-if="selectedFile" class="mt-4 p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <i class="fa fa-file-excel-o text-green-500 mr-2"></i>
                <span>{{ selectedFile.name }}</span>
              </div>
              <button 
                @click="selectedFile = null" 
                class="text-red-500 hover:text-red-700"
              >
                移除
              </button>
            </div>
          </div>
          <div class="mt-6 flex justify-end">
            <button 
              @click="nextStep" 
              :disabled="!selectedFile" 
              class="btn btn-primary disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              下一步
            </button>
          </div>
        </div>

        <!-- 步骤 2: 表结构配置 -->
        <div v-if="currentStep === 2" class="p-6">
          <h3 class="text-lg font-semibold text-dark mb-6">表结构配置</h3>
          
          <div v-if="isParsing" class="flex justify-center items-center py-10">
            <div class="flex flex-col items-center">
              <div class="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4"></div>
              <p class="text-gray-600">正在解析 Excel 文件...</p>
            </div>
          </div>
          
          <div v-else-if="tableStructure" class="space-y-6">
            <!-- 数据表和表头配置 -->
            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">数据表</label>
                <select v-model="tableConfig.sheet" class="input-field">
                  <option v-for="sheet in tableStructure.sheets" :key="sheet" :value="sheet">
                    {{ sheet }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">表头</label>
                <select v-model="tableConfig.headerRow" class="input-field">
                  <option v-for="i in 10" :key="i" :value="i">
                    第{{ i }}行
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">数据起始行</label>
                <select v-model="tableConfig.dataStartRow" class="input-field">
                  <option v-for="i in 10" :key="i" :value="i">
                    第{{ i }}行
                  </option>
                </select>
              </div>
            </div>

            <!-- 表结构配置 -->
            <div>
              <h4 class="text-md font-medium text-gray-700 mb-3">表结构</h4>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <input 
                          type="checkbox" 
                          @change="toggleAllColumns"
                          :checked="isAllSelected"
                          class="h-4 w-4 text-blue-600 rounded"
                        />
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        索引
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        列名 <span class="text-red-500">*</span>
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        描述
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        数据类型 <span class="text-red-500">*</span>
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        操作
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="(field, index) in tableStructure.fields" :key="index">
                      <td class="px-4 py-3 whitespace-nowrap">
                        <input 
                          type="checkbox" 
                          :value="field.name" 
                          v-model="selectedColumns"
                          class="h-4 w-4 text-blue-600 rounded"
                        />
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap">
                        <div class="text-sm text-gray-900">{{ index + 1 }}</div>
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap">
                        <input 
                          type="text" 
                          v-model="field.name" 
                          class="input-field"
                          placeholder="请输入列名"
                        />
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap">
                        <input 
                          type="text" 
                          v-model="field.description" 
                          class="input-field"
                          placeholder="请输入描述"
                        />
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap">
                        <select v-model="field.type" class="input-field">
                          <option value="String">String</option>
                          <option value="Integer">Integer</option>
                          <option value="Float">Float</option>
                          <option value="Boolean">Boolean</option>
                        </select>
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-sm font-medium">
                        <button class="text-red-500 hover:text-red-700">
                          <i class="fa fa-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex justify-between">
              <button @click="prevStep" class="btn btn-outline">
                上一步
              </button>
              <button @click="nextStep" class="btn btn-primary">
                下一步
              </button>
            </div>
          </div>
          
          <div v-else class="flex justify-center items-center py-10">
            <p class="text-gray-500">请先上传 Excel 文件</p>
          </div>
        </div>

        <!-- 步骤 3: 预览 -->
        <div v-if="currentStep === 3" class="p-6">
          <h3 class="text-lg font-semibold text-dark mb-6">数据预览</h3>
          
          <div v-if="previewData" class="space-y-6">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th v-for="field in tableStructure.fields" :key="field.name" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {{ field.name }}
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(row, index) in previewData" :key="index">
                    <td v-for="field in tableStructure.fields" :key="field.name" class="px-4 py-3 whitespace-nowrap">
                      <div class="text-sm text-gray-900">{{ row[field.name] || '' }}</div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="flex justify-between">
              <button @click="prevStep" class="btn btn-outline">
                上一步
              </button>
              <button @click="nextStep" class="btn btn-primary">
                下一步
              </button>
            </div>
          </div>
          
          <div v-else class="flex justify-center items-center py-10">
            <p class="text-gray-500">请先配置表结构</p>
          </div>
        </div>

        <!-- 步骤 4: 数据处理 -->
        <div v-if="currentStep === 4" class="p-6">
          <h3 class="text-lg font-semibold text-dark mb-6">数据处理</h3>
          
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">知识库名称</label>
              <input 
                type="text" 
                v-model="formData.knowledgeBaseName" 
                class="input-field"
                placeholder="请输入知识库名称"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">向量维度</label>
              <select v-model="formData.dimension" class="input-field">
                <option value="1024">1024</option>
                <option value="2048">2048</option>
                <option value="768">768</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">用于生成向量的字段</label>
              <div class="p-3 bg-gray-50 rounded border border-gray-200">
                <div v-if="selectedColumns.length > 0" class="flex flex-wrap gap-2">
                  <span v-for="(column, index) in selectedColumns" :key="index" class="inline-block px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                    {{ column }}
                  </span>
                </div>
                <div v-else class="text-gray-500 text-sm">
                  请在步骤 2 中选择要用于生成向量的字段
                </div>
              </div>
            </div>
            
            <div class="flex justify-between">
              <button @click="prevStep" class="btn btn-outline">
                上一步
              </button>
              <button 
                @click="importExcel" 
                :disabled="!formData.knowledgeBaseName" 
                class="btn btn-primary disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {{ isImporting ? '导入中...' : '开始导入' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 导入结果 -->
      <div v-if="importResult" class="mt-6 p-4 rounded-lg" :class="importResult.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'">
        <div class="flex items-start">
          <i v-if="importResult.success" class="fa fa-check-circle text-xl mr-2 mt-0.5"></i>
          <i v-else class="fa fa-times-circle text-xl mr-2 mt-0.5"></i>
          <div>
            <h3 class="font-semibold">{{ importResult.success ? '导入成功' : '导入失败' }}</h3>
            <p>{{ importResult.message }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'ExcelImport',
  data() {
    return {
      currentStep: 1,
      selectedFile: null,
      isParsing: false,
      isImporting: false,
      importResult: null,
      tableStructure: null,
      selectedColumns: [],
      tableConfig: {
        sheet: 'Sheet1',
        headerRow: 1,
        dataStartRow: 2
      },
      previewData: null,
      formData: {
        knowledgeBaseName: '',
        dimension: '1024'
      }
    }
  },
  computed: {
    isAllSelected() {
      if (!this.tableStructure || !this.tableStructure.fields) return false
      return this.tableStructure.fields.length > 0 && 
             this.selectedColumns.length === this.tableStructure.fields.length
    }
  },
  mounted() {
    // 从路由参数中获取知识库名称
    if (this.$route.query.collection_name) {
      this.formData.knowledgeBaseName = this.$route.query.collection_name
    }
  },
  methods: {
    handleFileUpload(e) {
      const file = e.target.files[0]
      if (file) {
        this.selectedFile = file
      }
    },
    async nextStep() {
      if (this.currentStep === 1 && this.selectedFile) {
        // 解析 Excel 文件
        this.isParsing = true
        try {
          const formData = new FormData()
          formData.append('file', this.selectedFile)
          
          const response = await fetch('http://localhost:8000/excel/parse', {
            method: 'POST',
            body: formData
          })
          
          const result = await response.json()
          
          if (response.ok) {
            // 清空之前的选择
            this.selectedColumns = []
            // 构建表结构
            const typeMap = {
              'string': 'String',
              'integer': 'Integer',
              'float': 'Float',
              'boolean': 'Boolean'
            }
            this.tableStructure = {
              sheets: ['Sheet1'], // 简化处理，实际应该从 API 返回
              fields: result.data.field_names.map(name => ({
                name: name,
                description: '',
                type: typeMap[result.data.field_types[name]] || 'String'
              }))
            }
            // 生成预览数据
            this.previewData = result.data.data.slice(0, 5) // 只显示前 5 行
            
            this.currentStep = 2
          } else {
            alert('解析 Excel 文件失败: ' + result.detail)
          }
        } catch (error) {
          alert('网络错误，请确保后端服务正在运行')
        } finally {
          this.isParsing = false
        }
      } else if (this.currentStep < 4) {
        this.currentStep++
      }
    },
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--
      }
    },
    toggleAllColumns(event) {
      if (event.target.checked) {
        this.selectedColumns = this.tableStructure.fields.map(f => f.name)
      } else {
        this.selectedColumns = []
      }
    },
    async importExcel() {
      if (!this.formData.knowledgeBaseName) {
        return
      }

      this.isImporting = true
      this.importResult = null

      try {
        const formData = new FormData()
        formData.append('file', this.selectedFile)
        formData.append('collection_name', this.formData.knowledgeBaseName)
        formData.append('fields', this.selectedColumns.join(','))

        const response = await fetch('http://localhost:8000/excel/import', {
          method: 'POST',
          body: formData
        })

        const result = await response.json()

        if (response.ok) {
          this.importResult = {
            success: true,
            message: `成功导入 ${result.count} 条数据到知识库 '${this.formData.knowledgeBaseName}'`
          }
          // 重置表单
          this.resetForm()
        } else {
          this.importResult = {
            success: false,
            message: result.detail || '导入失败，请检查服务器日志'
          }
        }
      } catch (error) {
        this.importResult = {
          success: false,
          message: '网络错误，请确保后端服务正在运行'
        }
      } finally {
        this.isImporting = false
      }
    },
    resetForm() {
      this.currentStep = 1
      this.selectedFile = null
      this.tableStructure = null
      this.previewData = null
      this.formData = {
        knowledgeBaseName: '',
        dimension: '1024'
      }
      this.importResult = null
    }
  }
}
</script>

<style scoped>
/* 组件特定样式 */
</style>