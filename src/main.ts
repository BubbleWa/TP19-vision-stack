import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import router from './router'

// --- Password check ---
console.log("Password check running...");

if (sessionStorage.getItem("authenticated") !== "true") {
  const currentPath = window.location.pathname
  console.log("Not authenticated, current path:", currentPath)

  // if not already on login page, redirect
  if (!currentPath.endsWith("login.html")) {
    const basePath = currentPath.substring(0, currentPath.lastIndexOf("/") + 1)
    console.log("Redirecting to:", basePath + "login.html")
    window.location.href = basePath + "login.html"
  }
}

// --- create and mount Vue app (only once) ---
const app = createApp(App)
app.use(router)
app.mount('#app')
