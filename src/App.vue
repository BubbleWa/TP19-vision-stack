<script setup>
import NavBar from './components/NavBar.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedLang = ref('en')

// 跳转到 ScamBot 页面
const goToScamBot = () => {
  router.push('/scambot')
}
</script>

<template>
  <div class="app-wrapper">
    <!-- 导航栏 -->
    <NavBar />

    <!-- 页面路由内容 -->
    <router-view />

    <!-- ScamBot 浮窗 -->
    <div class="scambot-floating" @click="goToScamBot">
      <img src="/bot.png" alt="ScamBot" />
      <span>ScamBot</span>
    </div>

    <!-- 左下角语言切换器浮窗 -->
    <div class="language-switcher">
      <select v-model="selectedLang">
        <option value="en">English</option>
        <option value="jp">日本語</option>
        <option value="ar">العربية</option>
        <option value="zh">中文</option>
        <option value="es">Español</option>
        <option value="fr">Français</option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.app-wrapper {
  position: relative;
  min-height: 100vh;
}

/* ScamBot 浮窗 */
.scambot-floating {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #6d28d9;
  color: white;
  padding: 10px 14px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
  z-index: 999;
}
.scambot-floating img {
  width: 30px;
  height: 30px;
}
.scambot-floating:hover {
  background: #4c1d95;
  transform: translateY(-3px);
}

/* 语言切换浮窗 */
.language-switcher {
  position: fixed;
  bottom: 20px;
  left: 20px;
  background: #6d28d9;
  padding: 8px 12px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  z-index: 999;
}
.language-switcher select {
  border: none;
  background: transparent;
  color: white;
  font-size: 1rem;
  font-weight: 500;
  outline: none;
  cursor: pointer;
}
.language-switcher select option {
  color: black;
}
</style>
