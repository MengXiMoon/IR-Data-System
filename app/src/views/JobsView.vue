<template>
  <div class="jobs">
    <h2 class="page-title">岗位搜索</h2>
    <p class="page-desc">多维度筛选招聘信息</p>

    <div class="filter-bar">
      <div class="filter-group">
        <input v-model="filters.keyword" placeholder="搜索关键词..." class="filter-input" @keyup.enter="search(1)" />
      </div>
      <div class="filter-group">
        <select v-model="filters.city" class="filter-select">
          <option value="">全部城市</option>
          <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
      <div class="filter-group">
        <select v-model="filters.experience" class="filter-select">
          <option value="">全部经验</option>
          <option value="经验不限">经验不限</option>
          <option value="1年以下">1年以下</option>
          <option value="1-3年">1-3年</option>
          <option value="3-5年">3-5年</option>
          <option value="5-10年">5-10年</option>
          <option value="10年以上">10年以上</option>
        </select>
      </div>
      <div class="filter-group">
        <select v-model="filters.education" class="filter-select">
          <option value="">全部学历</option>
          <option value="大专">大专</option>
          <option value="本科">本科</option>
          <option value="硕士">硕士</option>
          <option value="博士">博士</option>
        </select>
      </div>
      <div class="filter-group range-group">
        <input v-model.number="filters.salaryMin" placeholder="最低薪资" class="filter-input small" type="number" />
        <span class="range-sep">-</span>
        <input v-model.number="filters.salaryMax" placeholder="最高薪资" class="filter-input small" type="number" />
      </div>
      <button class="btn-search" @click="search(1)">搜索</button>
    </div>

    <div class="results-header">
      <span>共 {{ total }} 条结果</span>
    </div>

    <div class="job-list">
      <div v-for="job in records" :key="job.id" class="job-card">
        <div class="job-main">
          <h3 class="job-title">{{ job.jobTitle }}</h3>
          <div class="job-meta">
            <span class="job-salary gold">{{ job.salaryRaw }}</span>
            <span class="job-location">{{ job.workLocation }}</span>
            <span class="job-exp">{{ job.experience }}</span>
            <span class="job-edu">{{ job.education }}</span>
          </div>
          <div v-if="job.skillsRaw" class="job-skills">
            <span v-for="(skill, i) in job.skillsRaw.split(' ').slice(0, 8)" :key="i" class="skill-tag">{{ skill }}</span>
          </div>
        </div>
        <div class="job-company">
          <div class="company-name">{{ job.companyName }}</div>
          <div class="company-info">
            <span>{{ job.companyType || '-' }}</span>
            <span>|</span>
            <span>{{ job.companySize || '-' }}</span>
            <span>|</span>
            <span>{{ job.industry || '-' }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="pages > 1" class="pagination">
      <button :disabled="current === 1" @click="search(current - 1)">上一页</button>
      <span v-for="p in visiblePages" :key="p" :class="['page-num', { active: p === current }]" @click="search(p)">{{ p }}</span>
      <button :disabled="current === pages" @click="search(current + 1)">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { searchJobs, getCities } from '../api'

const filters = reactive({
  keyword: '',
  city: '',
  experience: '',
  education: '',
  salaryMin: null,
  salaryMax: null,
})

const cities = ref([])
const records = ref([])
const total = ref(0)
const current = ref(1)
const size = 20
const pages = ref(1)

const visiblePages = computed(() => {
  const p = []
  const start = Math.max(1, current.value - 2)
  const end = Math.min(pages.value, current.value + 2)
  for (let i = start; i <= end; i++) p.push(i)
  return p
})

async function search(page) {
  try {
    const params = { page, size }
    for (const [k, v] of Object.entries(filters)) {
      if (v !== '' && v !== null) params[k] = v
    }
    const res = await searchJobs(params)
    const d = res.data.data
    records.value = d.records
    total.value = d.total
    current.value = d.current
    pages.value = d.pages
  } catch (e) {
    console.error('Search failed:', e)
  }
}

onMounted(async () => {
  try {
    const res = await getCities()
    cities.value = res.data.data
  } catch (e) {}
  search(1)
})
</script>

<style scoped>
.jobs {
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
  margin-bottom: 24px;
}

.filter-bar {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.range-group {
  flex-direction: row;
  align-items: center;
  gap: 6px;
}

.range-sep {
  color: var(--text-muted);
  font-size: 12px;
}

.filter-input {
  padding: 8px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
  width: 180px;
  transition: border-color 0.2s;
}

.filter-input.small {
  width: 100px;
}

.filter-input:focus {
  border-color: var(--gold-primary);
}

.filter-select {
  padding: 8px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
  cursor: pointer;
  transition: border-color 0.2s;
}

.filter-select:focus {
  border-color: var(--gold-primary);
}

.btn-search {
  padding: 8px 28px;
  background: var(--gold-gradient);
  border: none;
  border-radius: 8px;
  color: #000;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-search:hover {
  opacity: 0.9;
}

.results-header {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.job-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  transition: border-color 0.2s;
}

.job-card:hover {
  border-color: var(--border-gold);
}

.job-main {
  flex: 1;
}

.job-title {
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.job-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 10px;
  font-size: 13px;
  color: var(--text-secondary);
}

.job-salary.gold {
  color: var(--gold-primary);
  font-weight: 600;
}

.job-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-tag {
  background: rgba(201, 168, 76, 0.08);
  color: var(--gold-primary);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  border: 1px solid var(--border-gold);
}

.job-company {
  text-align: right;
  min-width: 180px;
}

.company-name {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.company-info {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  gap: 6px;
  justify-content: flex-end;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 28px;
}

.pagination button {
  padding: 6px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.pagination button:hover:not(:disabled) {
  border-color: var(--gold-primary);
  color: var(--gold-primary);
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-num {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-num.active {
  background: var(--gold-gradient);
  border-color: transparent;
  color: #000;
  font-weight: 700;
}

.page-num:hover:not(.active) {
  border-color: var(--gold-primary);
}
</style>
