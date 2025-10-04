<script setup>
import NavBar from './components/NavBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Navigate to ScamBot page
const goToScamBot = () => {
  router.push('/scambot')
}
</script>

<template>
  <div class="app-wrapper">
    <!-- Navigation bar -->
    <NavBar />

    <!-- Page route content -->
    <router-view />

    <!-- ScamBot floating button -->
    <div class="scambot-floating" @click="goToScamBot">
      <img src="/bot.png" alt="ScamBot" />
      <span>ScamBot</span>
    </div>
  </div>
</template>

<style scoped>
.app-wrapper {
  position: relative;
  min-height: 100vh;
}

/* ScamBot floating button */
.scambot-floating {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #45C4B0;
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
  background: #45C4B0;
  transform: translateY(-3px);
}
</style>
