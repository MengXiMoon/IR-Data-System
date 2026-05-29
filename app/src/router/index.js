import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
  },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        meta: { title: '仪表盘' },
        component: () => import('../views/DashboardView.vue'),
      },
      {
        path: 'charts',
        name: 'charts',
        meta: { title: '数据可视化' },
        component: () => import('../views/ChartsView.vue'),
      },
      {
        path: 'jobs',
        name: 'jobs',
        meta: { title: '岗位搜索' },
        component: () => import('../views/JobsView.vue'),
      },
      {
        path: 'ai-chat',
        name: 'aiChat',
        meta: { title: 'AI 助手' },
        component: () => import('../views/AiChatView.vue'),
      },
      {
        path: 'ml',
        name: 'ml',
        meta: { title: '机器学习' },
        component: () => import('../views/MlView.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
