import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import KnowledgeBases from '../views/KnowledgeBases.vue'
import Documents from '../views/Documents.vue'
import Settings from '../views/Settings.vue'

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
    path: '/documents',
    name: 'Documents',
    component: Documents
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router