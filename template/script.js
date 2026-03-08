// API 基础 URL
const API_BASE_URL = 'http://localhost:8000';

// 操作日志
const logElement = document.getElementById('operation-log');

// 日志记录函数
function addLog(message, type = 'info') {
    const logEntry = document.createElement('div');
    logEntry.className = `mb-2 ${type === 'success' ? 'text-green-600' : type === 'error' ? 'text-red-600' : 'text-gray-600'}`;
    logEntry.innerHTML = `<i class="fa ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'} mr-2"></i>${new Date().toLocaleString()} - ${message}`;
    logElement.appendChild(logEntry);
    logElement.scrollTop = logElement.scrollHeight;
}

// API 调用函数
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call error:', error);
        addLog(`API 调用失败: ${error.message}`, 'error');
        throw error;
    }
}

// 加载数据库列表
async function loadDatabaseList() {
    try {
        addLog('加载数据库列表...');
        const data = await apiCall('/databases');
        const databaseList = document.querySelector('#database-list tbody');
        
        databaseList.innerHTML = '';
        
        if (data.databases && data.databases.length > 0) {
            data.databases.forEach(db => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-900">${db}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            存在
                        </span>
                    </td>
                `;
                databaseList.appendChild(row);
            });
        } else {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="2" class="px-6 py-4 text-center text-gray-500">
                    暂无数据库
                </td>
            `;
            databaseList.appendChild(row);
        }
        
        addLog('数据库列表加载成功', 'success');
    } catch (error) {
        addLog('加载数据库列表失败', 'error');
    }
}

// 加载数据库状态
async function loadDatabaseStatus() {
    try {
        const data = await apiCall('/databases');
        const databaseStatus = document.getElementById('database-status');
        
        if (data.databases && data.databases.includes('ollama_rag_db')) {
            databaseStatus.innerHTML = `
                <p class="font-medium text-green-600">✓ 数据库存在</p>
                <p class="text-sm">数据库名称: ollama_rag_db</p>
            `;
        } else {
            databaseStatus.innerHTML = `
                <p class="font-medium text-red-600">✗ 数据库不存在</p>
                <p class="text-sm">请点击创建按钮创建数据库</p>
            `;
        }
    } catch (error) {
        document.getElementById('database-status').innerHTML = `
            <p class="font-medium text-red-600">✗ 加载失败</p>
            <p class="text-sm">${error.message}</p>
        `;
    }
}

// 加载知识库状态
async function loadKnowledgeBaseStatus() {
    try {
        const data = await apiCall('/knowledge-base/status');
        const knowledgeBaseStatus = document.getElementById('knowledge-base-status');
        
        if (data.exists) {
            knowledgeBaseStatus.innerHTML = `
                <p class="font-medium text-green-600">✓ 知识库存在</p>
                <p class="text-sm">集合名称: ollama_rag</p>
            `;
        } else {
            knowledgeBaseStatus.innerHTML = `
                <p class="font-medium text-red-600">✗ 知识库不存在</p>
                <p class="text-sm">请点击创建按钮创建知识库</p>
            `;
        }
    } catch (error) {
        document.getElementById('knowledge-base-status').innerHTML = `
            <p class="font-medium text-red-600">✗ 加载失败</p>
            <p class="text-sm">${error.message}</p>
        `;
    }
}

// 加载文档统计
function loadDocumentStats() {
    // 这里可以添加文档统计逻辑
    const documentStats = document.getElementById('document-stats');
    documentStats.innerHTML = `
        <p class="font-medium">文档数量: 未知</p>
        <p class="text-sm">请添加文档</p>
    `;
}

// 加载集合列表
async function loadCollectionList() {
    try {
        addLog('加载集合列表...');
        const data = await apiCall('/collections');
        const collectionList = document.querySelector('#collection-list tbody');
        
        if (collectionList) {
            collectionList.innerHTML = '';
            
            if (data.collections && data.collections.length > 0) {
                data.collections.forEach(collection => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="text-sm font-medium text-gray-900">${collection}</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <button class="btn btn-primary btn-sm" onclick="describeCollection('${collection}')">
                                <i class="fa fa-info-circle mr-1"></i> 详情
                            </button>
                        </td>
                    `;
                    collectionList.appendChild(row);
                });
            } else {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td colspan="2" class="px-6 py-4 text-center text-gray-500">
                        暂无集合
                    </td>
                `;
                collectionList.appendChild(row);
            }
        }
        
        addLog('集合列表加载成功', 'success');
    } catch (error) {
        addLog('加载集合列表失败', 'error');
    }
}

// 获取集合详细信息
async function describeCollection(collectionName) {
    try {
        addLog(`获取集合 ${collectionName} 详细信息...`);
        const data = await apiCall(`/collections/${collectionName}`);
        
        // 显示集合详细信息
        let infoHtml = `<h3 class="font-medium text-dark mb-2">集合 ${collectionName} 详细信息</h3>`;
        
        if (data.exists === false) {
            infoHtml += `<p class="text-red-600">${data.message}</p>`;
        } else {
            infoHtml += `
                <div class="space-y-2 text-sm">
                    <p><strong>集合名称:</strong> ${data.collection_name}</p>
                    <p><strong>自动 ID:</strong> ${data.auto_id}</p>
                    <p><strong>分片数:</strong> ${data.num_shards}</p>
                    <p><strong>描述:</strong> ${data.description || '无'}</p>
                    <p><strong>集合 ID:</strong> ${data.collection_id}</p>
                    <p><strong>一致性级别:</strong> ${data.consistency_level}</p>
                    <p><strong>分区数:</strong> ${data.num_partitions}</p>
                    <p><strong>启用动态字段:</strong> ${data.enable_dynamic_field}</p>
                    <p><strong>字段:</strong></p>
                    <ul class="list-disc pl-4">
                        ${data.fields.map(field => `
                            <li>
                                <strong>${field.name}</strong> (${field.type})
                                ${field.is_primary ? ' [主键]' : ''}
                                ${field.params.dim ? ` - 维度: ${field.params.dim}` : ''}
                            </li>
                        `).join('')}
                    </ul>
                </div>
            `;
        }
        
        // 创建模态框
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4">
                <div class="p-4 border-b flex justify-between items-center">
                    <h2 class="text-lg font-semibold text-dark">集合详细信息</h2>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700">
                        <i class="fa fa-times text-xl"></i>
                    </button>
                </div>
                <div class="p-6">
                    ${infoHtml}
                </div>
                <div class="p-4 border-t flex justify-end">
                    <button onclick="this.closest('.fixed').remove()" class="btn bg-gray-200 text-gray-700 hover:bg-gray-300">
                        关闭
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        addLog(`获取集合 ${collectionName} 详细信息成功`, 'success');
    } catch (error) {
        addLog(`获取集合 ${collectionName} 详细信息失败`, 'error');
    }
}

// 刷新所有状态
async function refreshAllStatus() {
    addLog('刷新所有状态...');
    await Promise.all([
        loadDatabaseList(),
        loadCollectionList(),
        loadDatabaseStatus(),
        loadKnowledgeBaseStatus(),
        loadDocumentStats()
    ]);
    addLog('状态刷新完成', 'success');
}

// 创建数据库
async function createDatabase() {
    try {
        addLog('创建数据库...');
        const data = await apiCall('/databases/create', 'POST');
        if (data.success) {
            addLog('数据库创建成功', 'success');
            await loadDatabaseStatus();
            await loadDatabaseList();
        } else {
            addLog('数据库创建失败', 'error');
        }
    } catch (error) {
        addLog('创建数据库失败', 'error');
    }
}

// 删除数据库
async function deleteDatabase() {
    if (!confirm('确定要删除数据库吗？这将删除所有数据！')) {
        return;
    }
    
    try {
        addLog('删除数据库...');
        const data = await apiCall('/databases/delete', 'DELETE');
        if (data.success) {
            addLog('数据库删除成功', 'success');
            await loadDatabaseStatus();
            await loadDatabaseList();
        } else {
            addLog('数据库删除失败', 'error');
        }
    } catch (error) {
        addLog('删除数据库失败', 'error');
    }
}

// 创建知识库
async function createKnowledgeBase() {
    try {
        addLog('创建知识库...');
        const data = await apiCall('/knowledge-base/create', 'POST');
        if (data.success) {
            addLog('知识库创建成功', 'success');
            await loadKnowledgeBaseStatus();
        } else {
            addLog('知识库创建失败', 'error');
        }
    } catch (error) {
        addLog('创建知识库失败', 'error');
    }
}

// 删除知识库
async function deleteKnowledgeBase() {
    if (!confirm('确定要删除知识库吗？这将删除所有文档！')) {
        return;
    }
    
    try {
        addLog('删除知识库...');
        const data = await apiCall('/knowledge-base/delete', 'DELETE');
        if (data.success) {
            addLog('知识库删除成功', 'success');
            await loadKnowledgeBaseStatus();
        } else {
            addLog('知识库删除失败', 'error');
        }
    } catch (error) {
        addLog('删除知识库失败', 'error');
    }
}

// 添加文档
async function addDocuments() {
    const forms = document.querySelectorAll('.document-form');
    const documents = [];
    
    // 收集文档数据
    forms.forEach((form, index) => {
        const question = form.querySelector('input[name="question"]').value.trim();
        const answer = form.querySelector('textarea[name="answer"]').value.trim();
        const category = form.querySelector('input[name="category"]').value.trim();
        
        if (question && answer && category) {
            documents.push({
                question,
                answer,
                category
            });
        } else {
            alert(`文档 ${index + 1} 填写不完整，请检查！`);
            return;
        }
    });
    
    if (documents.length === 0) {
        alert('请填写至少一个文档！');
        return;
    }
    
    try {
        addLog('添加文档...');
        const data = await apiCall('/knowledge-base/add-documents', 'POST', { documents });
        if (data.success) {
            addLog(`成功添加 ${data.count} 个文档`, 'success');
            // 清空表单
            forms.forEach(form => {
                form.querySelector('input[name="question"]').value = '';
                form.querySelector('textarea[name="answer"]').value = '';
                form.querySelector('input[name="category"]').value = '';
            });
            // 关闭模态框
            document.getElementById('add-docs-modal').classList.add('hidden');
        } else {
            addLog('添加文档失败', 'error');
        }
    } catch (error) {
        addLog('添加文档失败', 'error');
    }
}

// 动态添加文档表单
function addDocumentForm() {
    const formsContainer = document.getElementById('document-forms');
    const formCount = formsContainer.querySelectorAll('.document-form').length + 1;
    
    const newForm = document.createElement('div');
    newForm.className = 'document-form';
    newForm.innerHTML = `
        <h3 class="font-medium text-dark mb-2">文档 ${formCount}</h3>
        <div class="space-y-2">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">问题</label>
                <input type="text" class="input-field" name="question" placeholder="请输入问题">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">回答</label>
                <textarea class="textarea-field" rows="3" name="answer" placeholder="请输入回答"></textarea>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">分类</label>
                <input type="text" class="input-field" name="category" placeholder="请输入分类">
            </div>
        </div>
    `;
    
    formsContainer.appendChild(newForm);
}

// 移除文档表单
function removeDocumentForm() {
    const formsContainer = document.getElementById('document-forms');
    const forms = formsContainer.querySelectorAll('.document-form');
    
    if (forms.length > 1) {
        forms[forms.length - 1].remove();
    } else {
        alert('至少需要一个文档！');
    }
}

// 初始化页面
async function initPage() {
    addLog('初始化页面...');
    await refreshAllStatus();
    addLog('页面初始化完成', 'success');
}

// 事件监听器
document.addEventListener('DOMContentLoaded', function() {
    // 初始化页面
    initPage();
    
    // 刷新按钮
    document.getElementById('refresh-btn').addEventListener('click', refreshAllStatus);
    
    // 数据库操作
    document.getElementById('create-db-btn').addEventListener('click', createDatabase);
    document.getElementById('delete-db-btn').addEventListener('click', deleteDatabase);
    
    // 知识库操作
    document.getElementById('create-kb-btn').addEventListener('click', createKnowledgeBase);
    document.getElementById('delete-kb-btn').addEventListener('click', deleteKnowledgeBase);
    
    // 添加文档模态框
    document.getElementById('add-docs-btn').addEventListener('click', function() {
        document.getElementById('add-docs-modal').classList.remove('hidden');
    });
    
    document.getElementById('close-modal-btn').addEventListener('click', function() {
        document.getElementById('add-docs-modal').classList.add('hidden');
    });
    
    document.getElementById('cancel-add-docs-btn').addEventListener('click', function() {
        document.getElementById('add-docs-modal').classList.add('hidden');
    });
    
    // 动态添加/移除文档表单
    document.getElementById('add-form-btn').addEventListener('click', addDocumentForm);
    document.getElementById('remove-form-btn').addEventListener('click', removeDocumentForm);
    
    // 提交文档
    document.getElementById('submit-docs-btn').addEventListener('click', addDocuments);
});
