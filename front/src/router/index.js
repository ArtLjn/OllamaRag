import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import KnowledgeBases from '../views/KnowledgeBases.vue'
import KnowledgeBaseDetail from '../views/KnowledgeBaseDetail.vue'
import Documents from '../views/Documents.vue'
import Settings from '../views/Settings.vue'
import ExcelImport from '../views/ExcelImport.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/knowledge-bases',
    name: 'KnowledgeBases',
    component: KnowledgeBases
  },
  {
    path: '/knowledge-base/:name',
    name: 'KnowledgeBaseDetail',
    component: KnowledgeBaseDetail
  },
  {
    path: '/documents',
    name: 'Documents',
    component: Documents
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/excel-import',
    name: 'ExcelImport',
    component: ExcelImport
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router