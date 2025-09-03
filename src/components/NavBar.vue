<template>
  <header class="navbar-header">
    <div class="navbar-container">
      
      <div class="navbar-left">
        <img src="/logo.png" alt="CyberMate logo" class="logo" />
        <span class="brand">CyberMate</span>
      </div>

      
      <nav class="navbar-nav" :class="{ open: menuOpen }">
        <router-link to="/">Home</router-link>
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/scambot">ScamBot</router-link>
        <router-link to="/riskscore">Risk Score</router-link>
      </nav>

      
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
  background: #3b1d74; 
  padding: 0;
  position: relative;
  z-index: 1000; 
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


.menu-btn {
  display: none;
  font-size: 2rem;
  background: none;
  border: none;
  color: #ffffff;
  cursor: pointer;
}


@media (max-width: 768px) {
  .navbar-nav {
    display: none; 
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
    display: flex; 
  }
  .menu-btn {
    display: block; 
  }
}
</style>
