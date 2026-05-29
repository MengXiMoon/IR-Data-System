<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <div class="login-icon">IR</div>
        <h1>招聘数据智能系统</h1>
        <p>Recruitment Data Intelligence</p>
      </div>

      <div class="login-tabs">
        <button :class="['tab', { active: isLogin }]" @click="isLogin = true">登 录</button>
        <button :class="['tab', { active: !isLogin }]" @click="isLogin = false">注 册</button>
      </div>

      <form class="login-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="form.username" type="text" placeholder="请输入用户名" required />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="form.password" type="password" placeholder="请输入密码" required />
        </div>
        <div v-if="!isLogin" class="form-group">
          <label>邮箱</label>
          <input v-model="form.email" type="email" placeholder="请输入邮箱" />
        </div>

        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

        <button type="submit" class="btn-submit">
          {{ isLogin ? '登 录' : '注 册' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const isLogin = ref(true)
const errorMsg = ref('')

const form = reactive({
  username: '',
  password: '',
  email: '',
})

async function handleSubmit() {
  errorMsg.value = ''
  try {
    if (isLogin.value) {
      await auth.login(form.username, form.password)
      router.push('/dashboard')
    } else {
      await auth.register(form.username, form.password, form.email)
      errorMsg.value = '注册成功，请登录'
      isLogin.value = true
      form.password = ''
    }
  } catch (err) {
    errorMsg.value = err.response?.data?.message || '操作失败，请重试'
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  background-image:
    radial-gradient(ellipse at 20% 50%, rgba(201, 168, 76, 0.03) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(201, 168, 76, 0.03) 0%, transparent 50%);
}

.login-card {
  width: 420px;
  padding: 48px 40px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: var(--shadow-gold);
}

.login-header {
  text-align: center;
  margin-bottom: 36px;
}

.login-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: var(--gold-gradient);
  color: #000;
  font-weight: 900;
  font-size: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.login-header h1 {
  font-size: 22px;
  color: var(--gold-primary);
  margin-bottom: 6px;
}

.login-header p {
  font-size: 12px;
  color: var(--text-muted);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.login-tabs {
  display: flex;
  gap: 4px;
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 4px;
  margin-bottom: 28px;
}

.tab {
  flex: 1;
  padding: 8px 0;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--text-muted);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.tab.active {
  background: var(--gold-gradient);
  color: #000;
  font-weight: 600;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 12px;
  color: var(--text-secondary);
  letter-spacing: 0.5px;
}

.form-group input {
  padding: 10px 14px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: var(--gold-primary);
}

.form-group input::placeholder {
  color: var(--text-muted);
}

.error-msg {
  color: #e15759;
  font-size: 13px;
  text-align: center;
}

.btn-submit {
  padding: 12px 0;
  background: var(--gold-gradient);
  border: none;
  border-radius: 8px;
  color: #000;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 4px;
}

.btn-submit:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(201, 168, 76, 0.3);
}
</style>
