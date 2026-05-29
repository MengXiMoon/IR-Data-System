<template>
  <div class="dashboard">
    <h2 class="page-title">数据仪表盘</h2>
    <p class="page-desc">招聘数据全景概览</p>

    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-label">总岗位数</div>
        <div class="stat-value">{{ dashboard.salary?.count || '-' }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">平均月薪</div>
        <div class="stat-value gold">{{ fmtSalary(dashboard.salary?.avgSalary) }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">薪资中位数</div>
        <div class="stat-value">{{ fmtSalary(dashboard.salary?.medianSalary) }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">薪资区间</div>
        <div class="stat-value small">{{ fmtSalary(dashboard.salary?.minSalary) }} - {{ fmtSalary(dashboard.salary?.maxSalary) }}</div>
      </div>
    </div>

    <div class="section">
      <h3 class="section-title">功能导航</h3>
      <div class="nav-cards">
        <router-link to="/jobs" class="nav-card">
          <span class="nav-card-icon">🔍</span>
          <span class="nav-card-title">岗位搜索</span>
          <span class="nav-card-desc">多维度筛选招聘信息</span>
        </router-link>
        <router-link to="/charts" class="nav-card">
          <span class="nav-card-icon">📈</span>
          <span class="nav-card-title">数据可视化</span>
          <span class="nav-card-desc">全方位图表分析</span>
        </router-link>
        <router-link to="/ai-chat" class="nav-card">
          <span class="nav-card-icon">🤖</span>
          <span class="nav-card-title">AI 助手</span>
          <span class="nav-card-desc">智能求职建议</span>
        </router-link>
        <router-link to="/ml" class="nav-card">
          <span class="nav-card-icon">🧠</span>
          <span class="nav-card-title">机器学习</span>
          <span class="nav-card-desc">聚类与分类预测</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDashboard } from '../api'

const dashboard = ref({})

function fmtSalary(val) {
  if (!val) return '-'
  return '¥' + (val / 1000).toFixed(1) + 'k'
}

onMounted(async () => {
  try {
    const res = await getDashboard()
    dashboard.value = res.data.data
  } catch (e) {
    console.error('Failed to load dashboard:', e)
  }
})
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-size: 24px;
  color: var(--gold-primary);
  margin-bottom: 4px;
}

.page-desc {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 28px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 36px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  transition: border-color 0.2s;
}

.stat-card:hover {
  border-color: var(--border-gold);
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 8px;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-value.gold {
  color: var(--gold-primary);
}

.stat-value.small {
  font-size: 16px;
}

.section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.nav-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.nav-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
}

.nav-card:hover {
  border-color: var(--border-gold);
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.nav-card-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.nav-card-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.nav-card-desc {
  font-size: 12px;
  color: var(--text-muted);
}
</style>
