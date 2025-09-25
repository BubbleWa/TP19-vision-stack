import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import router from './router'
import '@lottiefiles/lottie-player'
import AOS from 'aos'
import 'aos/dist/aos.css'


// --- Password check ---
console.log("Password check running...")

if (sessionStorage.getItem("authenticated") !== "true") {
  const currentPath = window.location.pathname
  console.log("Not authenticated, current path:", currentPath)

  if (!currentPath.endsWith("login.html")) {
    const basePath = currentPath.substring(0, currentPath.lastIndexOf("/") + 1)
    console.log("Redirecting to:", basePath + "login.html")
    window.location.href = basePath + "login.html"
  }
}

// --- create and mount Vue app ---
const app = createApp(App)

// mark <lottie-player> as custom element
app.config.compilerOptions.isCustomElement = tag => tag === 'lottie-player'

app.use(router)
app.mount('#app')
