import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 設定 base path，讓前端資源與 API 呼叫都能透過 Dashboard 反向代理
// （`/app/specialinfo/`）或直接存取（`/`）運作。
export default defineConfig({
  base: '/app/specialinfo/',
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:5055',
    },
  },
})
