/// <reference types="vite/client" />

// 让 TS 认识 .vue 文件
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// 让 TS 认识 router
declare module './router' {
  const router: any
  export default router
}
