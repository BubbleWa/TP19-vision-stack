<template>
  <header class="navbar-header">
    <div class="navbar-container">
      <!-- 左侧 logo 和品牌名 -->
      <div class="navbar-left">
        <img src="../assets/logo.png" alt="CyberMate logo" class="logo" />
        <span class="brand">CyberMate</span>
      </div>

      <!-- 右侧导航 -->
      <nav class="navbar-nav" :class="{ open: menuOpen }">
        <router-link to="/">Home</router-link>
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/scambot">ScamBot</router-link>
        <router-link to="/riskscore">Risk Score</router-link>
      </nav>

      <!-- 手机端菜单按钮 -->
      <button class="menu-btn" @click="menuOpen = !menuOpen">☰</button>
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue"
const menuOpen = ref(false)
</script>

<style scoped>
.navbar-header {
  background: #3b1d74; /* 深紫色背景 */
  padding: 0;
  position: relative;
  z-index: 1000; /* 永远在最上层 */
}

.navbar-container {
  max-width: 1300px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 16px 32px;
  justify-content: space-between;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.brand {
  font-size: 1.8rem;
  font-weight: 700;
  color: #ffffff;
  margin-right: 24px;
  font-family: 'Segoe UI', sans-serif;
}

/* 默认导航栏 */
.navbar-nav {
  display: flex;
  gap: 32px;
}
.navbar-nav a {
  font-size: 1.4rem;
  color: #ffffff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}
.navbar-nav a:hover {
  color: #60a5fa;
  text-decoration: underline;
}
.navbar-nav a.router-link-active {
  color: #60a5fa;
  font-weight: bold;
}

/* 手机端菜单按钮（默认隐藏） */
.menu-btn {
  display: none;
  font-size: 2rem;
  background: none;
  border: none;
  color: #ffffff;
  cursor: pointer;
}

/* ========= 响应式 ========= */
@media (max-width: 768px) {
  .navbar-nav {
    display: none; /* 默认不显示 */
    flex-direction: column;
    background: #3b1d74;
    position: absolute;
    top: 60px;
    right: 20px;
    padding: 16px;
    border-radius: 8px;
    gap: 16px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
  .navbar-nav.open {
    display: flex; /* 点击后显示 */
  }
  .menu-btn {
    display: block; /* 小屏幕才显示 ☰ */
  }
}
</style>
