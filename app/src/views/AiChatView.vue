<template>
  <div class="ai-chat">
    <h2 class="page-title">AI 智能助手</h2>
    <p class="page-desc">基于大模型的求职顾问</p>

    <div class="chat-container">
      <div class="chat-messages" ref="msgContainer">
        <div v-if="messages.length === 0" class="chat-placeholder">
          <span class="placeholder-icon">🤖</span>
          <p>你好！我是你的专属求职顾问</p>
          <p class="placeholder-hint">可以问我关于薪资、岗位、技能要求等问题</p>
        </div>
        <div v-for="(msg, i) in messages" :key="i" :class="['message', msg.role]">
          <div class="msg-avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
          <div class="msg-content">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="message assistant">
          <div class="msg-avatar">🤖</div>
          <div class="msg-content typing">思考中<span>...</span></div>
        </div>
      </div>

      <div class="chat-input-bar">
        <input
          v-model="input"
          placeholder="输入你的问题..."
          class="chat-input"
          @keyup.enter="send"
          :disabled="loading"
        />
        <button class="btn-send" @click="send" :disabled="loading">发送</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, onMounted } from 'vue'
import { sendMessage as sendMsgApi, getChatHistory } from '../api'

const messages = ref([])
const input = ref('')
const loading = ref(false)
const sessionId = ref('')
const msgContainer = ref(null)

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return
  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true
  await nextTick()
  scrollBottom()

  try {
    const res = await sendMsgApi({ message: text, sessionId: sessionId.value })
    const data = res.data.data
    sessionId.value = data.sessionId
    messages.value.push({ role: 'assistant', content: data.reply })
  } catch (e) {
    messages.value.push({ role: 'assistant', content: '抱歉，服务暂时不可用。' })
  } finally {
    loading.value = false
    await nextTick()
    scrollBottom()
  }
}

function scrollBottom() {
  if (msgContainer.value) {
    msgContainer.value.scrollTop = msgContainer.value.scrollHeight
  }
}

onMounted(async () => {
  if (sessionId.value) {
    try {
      const res = await getChatHistory(sessionId.value)
      messages.value = res.data.data.map(m => ({ role: m.role, content: m.content }))
    } catch (e) {}
  }
})
</script>

<style scoped>
.ai-chat {
  max-width: 900px;
  margin: 0 auto;
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
}

.page-title {
  font-size: 24px;
  color: var(--gold-primary);
  margin-bottom: 4px;
}

.page-desc {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.chat-placeholder p {
  font-size: 15px;
  color: var(--text-secondary);
}

.placeholder-hint {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 8px;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.assistant {
  align-self: flex-start;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.message.user .msg-avatar {
  border-color: var(--border-gold);
}

.msg-content {
  padding: 12px 16px;
  border-radius: 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-secondary);
  white-space: pre-wrap;
  word-break: break-word;
}

.message.user .msg-content {
  background: rgba(201, 168, 76, 0.08);
  border-color: var(--border-gold);
  color: var(--text-primary);
}

.typing {
  color: var(--text-muted);
}

.chat-input-bar {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.chat-input {
  flex: 1;
  padding: 10px 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.chat-input:focus {
  border-color: var(--gold-primary);
}

.chat-input::placeholder {
  color: var(--text-muted);
}

.btn-send {
  padding: 10px 28px;
  background: var(--gold-gradient);
  border: none;
  border-radius: 8px;
  color: #000;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-send:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
