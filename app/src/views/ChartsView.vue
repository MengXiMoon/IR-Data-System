<template>
  <div class="charts-page">
    <h2 class="page-title">数据可视化</h2>
    <p class="page-desc">全方位图表分析</p>

    <div class="charts-grid">
      <div class="chart-card">
        <h3 class="chart-title">城市岗位分布 Top10</h3>
        <div class="bar-chart">
          <div v-for="(city, i) in (dashboard.cities || []).slice(0, 10)" :key="i" class="bar-row">
            <span class="bar-label">{{ city.city }}</span>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: barWidth(city.count, maxCityCount) + '%' }"></div>
            </div>
            <span class="bar-count">{{ city.count }}</span>
          </div>
        </div>
      </div>

      <div class="chart-card">
        <h3 class="chart-title">企业类型分布</h3>
        <div class="bar-chart">
          <div v-for="([type, count], i) in topCompanyTypes" :key="i" class="bar-row">
            <span class="bar-label">{{ type }}</span>
            <div class="bar-track">
              <div class="bar-fill gold" :style="{ width: barWidth(count, maxCompanyCount) + '%' }"></div>
            </div>
            <span class="bar-count">{{ count }}</span>
          </div>
        </div>
      </div>

      <div class="chart-card">
        <h3 class="chart-title">学历薪资对比</h3>
        <div class="bar-chart">
          <div v-for="(edu, i) in (dashboard.education || [])" :key="i" class="bar-row">
            <span class="bar-label">{{ edu.education }}</span>
            <div class="bar-track">
              <div class="bar-fill accent" :style="{ width: barWidth(edu.avgSalary, maxEduSalary) + '%' }"></div>
            </div>
            <span class="bar-count">{{ fmtSalary(edu.avgSalary) }}</span>
          </div>
        </div>
      </div>

      <div class="chart-card">
        <h3 class="chart-title">工作经验分布</h3>
        <div class="bar-chart">
          <div v-for="(exp, i) in (dashboard.experience || [])" :key="i" class="bar-row">
            <span class="bar-label">{{ exp.experience }}</span>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: barWidth(exp.count, maxExpCount) + '%' }"></div>
            </div>
            <span class="bar-count">{{ exp.count }}</span>
          </div>
        </div>
      </div>

      <div class="chart-card full-width">
        <h3 class="chart-title">行业分布 Top12</h3>
        <div class="industry-tags">
          <span v-for="([industry, count], i) in topIndustries" :key="i" class="industry-tag">
            {{ industry }}
            <em>{{ count }}</em>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getDashboard } from '../api'

const dashboard = ref({})

const topCompanyTypes = computed(() =>
  Object.entries(dashboard.value.companyType || {}).sort((a, b) => b[1] - a[1]).slice(0, 8)
)
const topIndustries = computed(() =>
  Object.entries(dashboard.value.industry || {}).sort((a, b) => b[1] - a[1]).slice(0, 12)
)
const maxCityCount = computed(() =>
  Math.max(...(dashboard.value.cities || []).map(c => c.count), 1)
)
const maxCompanyCount = computed(() =>
  Math.max(...topCompanyTypes.value.map(([, c]) => c), 1)
)
const maxEduSalary = computed(() =>
  Math.max(...(dashboard.value.education || []).map(e => e.avgSalary), 1)
)
const maxExpCount = computed(() =>
  Math.max(...(dashboard.value.experience || []).map(e => e.count), 1)
)

function barWidth(val, max) {
  return Math.max(8, (val / max) * 100)
}

function fmtSalary(val) {
  if (!val) return '-'
  return '¥' + (val / 1000).toFixed(1) + 'k'
}

onMounted(async () => {
  try {
    const res = await getDashboard()
    dashboard.value = res.data.data
  } catch (e) {
    console.error('Failed to load charts:', e)
  }
})
</script>

<style scoped>
.charts-page {
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

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-title {
  font-size: 15px;
  color: var(--text-primary);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.bar-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bar-label {
  width: 70px;
  font-size: 12px;
  color: var(--text-secondary);
  text-align: right;
  flex-shrink: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bar-track {
  flex: 1;
  height: 8px;
  background: var(--bg-primary);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--gold-gradient);
  border-radius: 4px;
  transition: width 0.6s ease;
}

.bar-fill.gold {
  background: var(--gold-gradient);
}

.bar-fill.accent {
  background: linear-gradient(135deg, #4e79a7, #76b7b2);
}

.bar-count {
  width: 50px;
  font-size: 12px;
  color: var(--text-muted);
  text-align: right;
  flex-shrink: 0;
}

.industry-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.industry-tag {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.industry-tag:hover {
  border-color: var(--gold-primary);
  color: var(--gold-primary);
}

.industry-tag em {
  font-style: normal;
  color: var(--gold-primary);
  font-weight: 600;
}
</style>
