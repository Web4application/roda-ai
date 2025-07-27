import { createRouter, createWebHistory } from 'vue-router'
import Wallet from '../components/Wallet.vue'
import Swap from '../components/Swap.vue'
import AIChat from '../components/AIChat.vue'

const routes = [
  { path: '/', component: Wallet },
  { path: '/wallet', component: Wallet },
  { path: '/swap', component: Swap },
  { path: '/chat', component: AIChat }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
