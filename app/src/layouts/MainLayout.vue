<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <div class="brand-icon">IR</div>
        <div class="brand-text">
          <span class="brand-title">招聘数据智能系统</span>
          <span class="brand-sub">Recruitment Intelligence</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item" active-class="nav-item--active">
          <span class="nav-icon">📊</span>
          <span class="nav-label">仪表盘</span>
        </router-link>
        <router-link to="/charts" class="nav-item" active-class="nav-item--active">
          <span class="nav-icon">📈</span>
          <span class="nav-label">数据可视化</span>
        </router-link>
        <router-link to="/jobs" class="nav-item" active-class="nav-item--active">
          <span class="nav-icon">🔍</span>
          <span class="nav-label">岗位搜索</span>
        </router-link>
        <router-link to="/ai-chat" class="nav-item" active-class="nav-item--active">
          <span class="nav-icon">🤖</span>
          <span class="nav-label">AI 助手</span>
        </router-link>
        <router-link to="/ml" class="nav-item" active-class="nav-item--active">
          <span class="nav-icon">🧠</span>
          <span class="nav-label">机器学习</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <span class="user-avatar">{{ username.charAt(0) }}</span>
          <span class="user-name">{{ username }}</span>
        </div>
        <button class="btn-logout" @click="handleLogout">退出</button>
      </div>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const username = computed(() => auth.username)

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  user-select: none;
}

.sidebar-brand {
  padding: 24px 20px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--gold-gradient);
  color: #000;
  font-weight: 900;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--gold-primary);
  letter-spacing: 0.5px;
}

.brand-sub {
  font-size: 10px;
  color: var(--text-muted);
  letter-spacing: 1px;
}

.sidebar-nav {
  flex: 1;
  padding: 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.nav-item--active {
  background: rgba(201, 168, 76, 0.1);
  color: var(--gold-primary);
  border: 1px solid var(--border-gold);
}

.nav-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.nav-label {
  font-weight: 500;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--gold-gradient);
  color: #000;
  font-weight: 700;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-size: 13px;
  color: var(--text-secondary);
}

.btn-logout {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  border-color: #e15759;
  color: #e15759;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
  background: var(--bg-primary);
}
</style>
