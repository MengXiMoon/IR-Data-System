import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8080',
  timeout: 30000,
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401 || err.response?.status === 403) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export function login(data) { return api.post('/api/auth/login', data) }
export function register(data) { return api.post('/api/auth/register', data) }
export function searchJobs(params) { return api.post('/api/jobs/search', params) }
export function getCities() { return api.get('/api/jobs/cities') }
export function getDashboard() { return api.get('/api/charts/dashboard') }
export function getSalaryStats() { return api.get('/api/charts/salary') }
export function getCityStats() { return api.get('/api/charts/cities') }
export function getEducationStats() { return api.get('/api/charts/education') }
export function getExperienceStats() { return api.get('/api/charts/experience') }
export function getIndustryStats() { return api.get('/api/charts/industry') }
export function getCompanyTypeStats() { return api.get('/api/charts/company-type') }
export function sendMessage(data) { return api.post('/api/ai/chat', data) }
export function getChatHistory(sessionId) { return api.get(`/api/ai/history/${sessionId}`) }
export function clusterPredict(data) { return api.post('/api/ml/cluster', data) }
export function classifyPredict(data) { return api.post('/api/ml/classify', data) }

export default api
