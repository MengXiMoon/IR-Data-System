import { defineStore } from 'pinia'
import { login as loginApi, register as registerApi } from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || '',
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      const res = await loginApi({ username, password })
      const { token, username: name } = res.data.data
      this.token = token
      this.username = name
      localStorage.setItem('token', token)
      localStorage.setItem('username', name)
      return res.data
    },
    async register(username, password, email) {
      return await registerApi({ username, password, email })
    },
    logout() {
      this.token = ''
      this.username = ''
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    },
  },
})
