import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: '/roda-web4/', // GitHub repo name or custom path
  plugins: [vue()]
})
