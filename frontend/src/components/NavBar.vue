<template>
  <header class="navbar-header">
    <div class="navbar-container">
      <!-- Left side: logo + brand -->
      <div class="navbar-left">
        <img src="/logo.png" alt="CyberMate logo" class="logo" />
        <span class="brand">MyCyberMate</span>
      </div>

      <!-- Pill-style navigation -->
      <nav class="navbar-nav pills-nav" :class="{ open: menuOpen }">
        <router-link to="/" :class="{ active: isActive('/') }">Home</router-link>
        <router-link to="/dashboard" :class="{ active: isActive('/dashboard') }">Dashboard</router-link>
        <router-link to="/scambot" :class="{ active: isActive('/scambot') }">ScamBot</router-link>
        <router-link to="/riskscore" :class="{ active: isActive('/riskscore') }">Risk Score</router-link>
      </nav>

      <!-- Mobile menu button -->
      <button class="menu-btn" @click="menuOpen = !menuOpen">☰</button>
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"

// Toggle menu on mobile
const menuOpen = ref(false)

// Detect active route for pill highlight
const route = useRoute()
function isActive(path) {
  return route.path === path
}
</script>

<style scoped>
/* ---------- Header container ---------- */
.navbar-header {
  background: #45C4B0;
  padding: 0;
  position: relative;
  z-index: 1000;
}

.navbar-container {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 12px 12px;
  justify-content: space-between;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo {
  width: 80px;
  height: 80px;
  margin-right: 10px;
}

.brand {
  font-size: 1.8rem;
  font-weight: 700;
  color: #DAFDBA;
  margin-right: 24px;
  font-family: 'Segoe UI', sans-serif;
}

/* ---------- Pill navigation ---------- */
.navbar-nav {
  display: flex;
  gap: 16px;
}

.navbar-nav a {
  font-size: 1.2rem;
  padding: 10px 20px;
  border-radius: 999px; /* Pill shape */
  background-color: transparent;
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.navbar-nav a:hover {
  background-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.navbar-nav a.active {
  background-color: #ffffff;
  color: #45C4B0; /* Main theme color */
  font-weight: 600;
}

/* ---------- Mobile button ---------- */
.menu-btn {
  display: none;
  font-size: 2rem;
  background: none;
  border: none;
  color: #ffffff;
  cursor: pointer;
}

/* ---------- Responsive ---------- */
@media (max-width: 768px) {
  .navbar-nav {
    display: none;
    flex-direction: column;
    background: #012030;
    position: absolute;
    top: 70px;
    right: 20px;
    padding: 16px;
    border-radius: 12px;
    gap: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .navbar-nav.open {
    display: flex;
  }

  .menu-btn {
    display: block;
  }
}
</style>
