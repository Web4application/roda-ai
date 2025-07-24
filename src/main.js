import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
app.use(Toast)
import { createApp } from 'vue'
import App from './App.vue'

// 🌐 Router
import router from './router'

// 🧠 State Management (Pinia)
import { createPinia } from 'pinia'

// 🔌 Global Ethereum Injection (Ethers.js)
import { ethers } from 'ethers'

// 🌙 Dark Mode Support
import './styles/theme.css'

// 🚀 App Bootstrap
const app = createApp(App)

// ✅ Provide Pinia
const pinia = createPinia()
app.use(pinia)

// ✅ Provide Router
app.use(router)

// ✅ Inject ethers globally
app.config.globalProperties.$ethers = ethers

// ✅ Mount
app.mount('#app')
