<template>
  <div class="ml">
    <h2 class="page-title">机器学习</h2>
    <p class="page-desc">聚类分析与分类预测</p>

    <div class="ml-grid">
      <div class="ml-card">
        <div class="card-header">
          <span class="card-icon">🧠</span>
          <h3>KMeans 聚类</h3>
        </div>
        <p class="card-desc">对岗位特征进行聚类分析，发现相似岗位群组</p>
        <div class="feature-inputs">
          <div v-for="i in 3" :key="i" class="feature-row">
            <label>特征 {{ i }}</label>
            <input v-model.number="clusterFeatures[i - 1]" type="number" step="0.01" placeholder="0.00" />
          </div>
        </div>
        <button class="btn-action" @click="runCluster" :disabled="clusterLoading">
          {{ clusterLoading ? '运算中...' : '执行聚类预测' }}
        </button>
        <div v-if="clusterResult !== null" class="result-box">
          <span>预测类别：</span>
          <span class="result-value">{{ clusterResult }}</span>
        </div>
      </div>

      <div class="ml-card">
        <div class="card-header">
          <span class="card-icon">🔮</span>
          <h3>神经网络分类</h3>
        </div>
        <p class="card-desc">使用神经网络对岗位数据进行多分类预测</p>
        <div class="feature-inputs">
          <div v-for="i in 3" :key="i" class="feature-row">
            <label>特征 {{ i }}</label>
            <input v-model.number="classifyFeatures[i - 1]" type="number" step="0.01" placeholder="0.00" />
          </div>
        </div>
        <button class="btn-action" @click="runClassify" :disabled="classifyLoading">
          {{ classifyLoading ? '运算中...' : '执行分类预测' }}
        </button>
        <div v-if="classifyResult !== null" class="result-box">
          <span>预测类别：</span>
          <span class="result-value">{{ classifyResult.prediction }}</span>
          <div class="probabilities">
            <div v-for="(prob, i) in classifyResult.probabilities" :key="i" class="prob-row">
              <span class="prob-label">类别 {{ i }}</span>
              <div class="prob-track">
                <div class="prob-fill" :style="{ width: (prob * 100) + '%' }"></div>
              </div>
              <span class="prob-value">{{ (prob * 100).toFixed(1) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { clusterPredict, classifyPredict } from '../api'

const clusterFeatures = reactive([0.12, 0.45, 0.78])
const classifyFeatures = reactive([0.12, 0.45, 0.78])
const clusterLoading = ref(false)
const classifyLoading = ref(false)
const clusterResult = ref(null)
const classifyResult = ref(null)

async function runCluster() {
  clusterLoading.value = true
  try {
    const res = await clusterPredict({ features: [clusterFeatures.map(Number)] })
    clusterResult.value = res.data.data[0]
  } catch (e) {
    console.error(e)
  } finally {
    clusterLoading.value = false
  }
}

async function runClassify() {
  classifyLoading.value = true
  try {
    const res = await classifyPredict({ features: [classifyFeatures.map(Number)] })
    const d = res.data.data
    classifyResult.value = {
      prediction: d.predictions[0],
      probabilities: d.probabilities[0],
    }
  } catch (e) {
    console.error(e)
  } finally {
    classifyLoading.value = false
  }
}
</script>

<style scoped>
.ml {
  max-width: 1200px;
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

.ml-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.ml-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 28px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.card-icon {
  font-size: 28px;
}

.card-header h3 {
  font-size: 18px;
  color: var(--text-primary);
}

.card-desc {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.feature-inputs {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.feature-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.feature-row label {
  width: 50px;
  font-size: 13px;
  color: var(--text-secondary);
}

.feature-row input {
  flex: 1;
  padding: 8px 14px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.feature-row input:focus {
  border-color: var(--gold-primary);
}

.btn-action {
  width: 100%;
  padding: 10px 0;
  background: var(--gold-gradient);
  border: none;
  border-radius: 8px;
  color: #000;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-action:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.result-box {
  margin-top: 20px;
  padding: 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-gold);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.result-value {
  color: var(--gold-primary);
  font-size: 24px;
  font-weight: 700;
  margin-left: 8px;
}

.probabilities {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.prob-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.prob-label {
  width: 50px;
  font-size: 11px;
  color: var(--text-muted);
}

.prob-track {
  flex: 1;
  height: 6px;
  background: var(--bg-card);
  border-radius: 3px;
  overflow: hidden;
}

.prob-fill {
  height: 100%;
  background: var(--gold-gradient);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.prob-value {
  width: 45px;
  font-size: 11px;
  color: var(--gold-primary);
  text-align: right;
}
</style>
