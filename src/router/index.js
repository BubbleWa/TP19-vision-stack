import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import ScamBot from '../views/ScamBot.vue'
import RiskScore from '../views/RiskScore.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/scambot', name: 'ScamBot', component: ScamBot },
  { path: '/riskscore', name: 'RiskScore', component: RiskScore },
  
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})


export default router
