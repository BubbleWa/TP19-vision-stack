<template>
  <div class="page-wrapper">
    <!-- Hero Section -->
    <section class="hero-banner">
      <div class="hero-overlay">
        <div class="hero-content">
          <h2 class="hero-title">
            Stay Safe Online with <span class="highlight">CyberMate</span>
          </h2>
          <p class="hero-subtitle">
            Your trusted mate for spotting scams, boosting digital skills, and staying secure.
          </p>
          
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section class="about-section">
      <div class="about-container">
        <div class="about-text">
          <h3>About CyberMate</h3>
          <p>
            CyberMate empowers young Australians to recognise, avoid, and report scams.
            Through interactive dashboards, a scam detector bot, and a risk score tracker,
            we make online safety engaging and easy.
          </p>
        </div>

        <div class="about-stats">
          <div
            v-for="(stat, index) in stats"
            :key="index"
            class="stat-card"
            :style="{ backgroundColor: stat.color }"
          >
            <h4>{{ stat.value }}</h4>
            <p>{{ stat.label }}</p>
          </div>
        </div>
      </div>

      <div class="explore-container">
        <button class="explore-btn" @click="goToDashboard">Explore Dashboard</button>
      </div>
    </section>

    <!-- ScamBot Section -->
    <section class="bot-section">
      <div class="bot-container">
        <div class="bot-image">
          <img src="/bot.png" alt="Scam Detector Bot" />
        </div>
        <div class="bot-text">
          <h3>
            Meet our <span class="highlight">Scam Detector Bot</span>
          </h3>
          <p>
            Just paste a suspicious message,<br />
            and our AI will instantly tell you if it looks like a scam.
          </p>
          <button class="bot-button" @click="goToScamBot">Explore ScamBot</button>
        </div>
      </div>
    </section>

    <!-- Risk Score Section -->
    <section class="risk-section">
      <div class="risk-container">
        <div class="risk-image">
          <img src="/risk-meter.png" alt="Risk Score Meter" />
        </div>
        <div class="risk-text">
          <h3>Risk Score Measure</h3>
          <p>
            CyberMate’s Risk Score helps you understand your personal exposure.
            Based on your online activity and scam history, get a score that
            shows your digital risk level.
          </p>
          <button class="risk-button" @click="goToRiskScore">Measure your Risk Score</button>
        </div>
      </div>
    </section>

    <!-- ScamBot in the right corner -->
    <div class="scambot-floating" @click="goToScamBot">
      <img src="/bot.png" alt="ScamBot" />
      <span>ScamBot</span>
    </div>
  </div>
</template>


<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

// Update stats content according to new requirements
const stats = ref([
  { 
    value: "💡 Did you know?", 
    label: "Australians lose billions every year to scams, making online awareness more important than ever.", 
    color: "#bae6fd" 
  },
  { 
    value: "👥 Who’s at risk?", 
    label: "In 2025, over 7,000 Australians aged 55+ fell victim to scams nationwide.", 
    color: "#fecdd3" 
  },
  { 
    value: "💰 Reported losses", 
    label: "Scammers stole more than $8.6 million from older Australians in 2025 alone.", 
    color: "#fecaca" 
  },
  { 
    value: "⚠️ Top scams to watch", 
    label: "Investment · Phishing · Romance", 
    color: "#fde68a" 
  }
])



const router = useRouter()
const goToDashboard = () => router.push("/dashboard")
const goToScamBot = () => router.push("/scambot")
const goToRiskScore = () => router.push("/riskscore")
</script>


<style scoped>
.page-wrapper {
  background-color: #f3e8ff;
  min-height: 100vh;
  padding: 20px 0;
}

/* ===== HERO ===== */
.hero-banner {
  background-image: url("/cyber-bg.png");
  background-size: cover;
  background-position: center;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.hero-overlay {
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-content {
  text-align: center;
  padding: 0 16px;
}
.hero-title {
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin-bottom: 16px;
  line-height: 1.3;
}
@media (min-width: 768px) {
  .hero-title {
    font-size: 3.5rem;
  }
}
.hero-subtitle {
  color: #e5e7eb;
  font-size: 1rem;
  margin-bottom: 20px;
}
@media (min-width: 768px) {
  .hero-subtitle {
    font-size: 1.5rem;
  }
}
.hero-button {
  background: #6366f1;
  color: white;
  padding: 10px 24px;
  font-size: 1rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}
.hero-button:hover {
  background: #4f46e5;
  transform: translateY(-3px);
}

/* ===== ABOUT ===== */
.about-section {
  background: white;
  padding: 40px 20px;
  border-radius: 16px;
  max-width: 1200px;
  margin: 20px auto;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}
.about-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}
@media (min-width: 768px) {
  .about-container {
    grid-template-columns: 1fr 1fr;
    gap: 40px;
  }
}
.about-text h3 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 12px;
}
@media (min-width: 768px) {
  .about-text h3 {
    font-size: 2.8rem;
  }
}
.about-text p {
  font-size: 1rem;
  line-height: 1.6;
}
@media (min-width: 768px) {
  .about-text p {
    font-size: 1.5rem;
  }
}
.about-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.stat-card {
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  font-weight: bold;
  box-shadow: 0 3px 6px rgba(0,0,0,0.08);
}
.stat-card h4 {
  font-size: 1.6rem;
  margin-bottom: 8px;
}
@media (min-width: 768px) {
  .stat-card h4 {
    font-size: 2.6rem;
  }
}
.stat-card p {
  font-size: 1rem;
}
@media (min-width: 768px) {
  .stat-card p {
    font-size: 1.4rem;
  }
}

/* ===== BOT ===== */
.bot-section {
  background: linear-gradient(to right, #6366f1, #3b82f6, #06b6d4);
  padding: 40px 20px;
  border-radius: 16px;
  max-width: 1200px;
  margin: 20px auto;
  color: white;
}
.bot-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  align-items: center;
}
@media (min-width: 768px) {
  .bot-container {
    grid-template-columns: 1fr 1fr;
    gap: 40px;
  }
}
.bot-image img {
  width: 120px;
  height: auto;
  margin: 0 auto;
}
@media (min-width: 768px) {
  .bot-image img {
    width: 180px;
  }
}
.bot-text h3 {
  font-size: 1.8rem;
  margin-bottom: 12px;
}
@media (min-width: 768px) {
  .bot-text h3 {
    font-size: 2.8rem;
  }
}
.bot-text p {
  font-size: 1rem;
  margin-bottom: 16px;
}
@media (min-width: 768px) {
  .bot-text p {
    font-size: 1.5rem;
  }
}
.bot-button {
  background: #4f46e5;
  color: white;
  padding: 10px 24px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
.bot-button:hover {
  background: #4338ca;
}

/* ===== RISK SCORE ===== */
.risk-section {
  background: #f3f4f6;
  padding: 40px 20px;
  border-radius: 16px;
  max-width: 1200px;
  margin: 20px auto;
}
.risk-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  align-items: center;
}
@media (min-width: 768px) {
  .risk-container {
    grid-template-columns: 1fr 1fr;
    gap: 40px;
  }
}
.risk-image img {
  width: 140px;
  margin: 0 auto;
}
@media (min-width: 768px) {
  .risk-image img {
    width: 200px;
  }
}
.risk-text h3 {
  font-size: 1.8rem;
  margin-bottom: 12px;
}
@media (min-width: 768px) {
  .risk-text h3 {
    font-size: 2.4rem;
  }
}
.risk-text p {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 20px;
}
@media (min-width: 768px) {
  .risk-text p {
    font-size: 1.3rem;
  }
}
.risk-button {
  background: #facc15;
  padding: 10px 24px;
  font-size: 1rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}
.risk-button:hover {
  background: #eab308;
}

/* ===== 浮窗 ===== */
.scambot-floating {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #6d28d9;
  color: white;
  padding: 8px 12px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
.scambot-floating img {
  width: 24px;
}

/* ===== UNIFIED BUTTON STYLE ===== */
button,
.explore-btn,
.bot-button,
.risk-button {
  display: inline-block;
  padding: 10px 24px;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;       /* rounded corners */
  cursor: pointer;
  transition: all 0.3s ease; /* smooth hover */
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

/* Explore Dashboard button */
.explore-btn {
  background: #6366f1;
  color: white;
}
.explore-btn:hover {
  background: #4f46e5;
  transform: translateY(-3px);
}

/* ScamBot button */
.bot-button {
  background: #6366f1;   /* same as hero button for consistency */
  color: white;
}
.bot-button:hover {
  background: #4f46e5;
  transform: translateY(-3px);
}

/* Risk Score button */
.risk-button {
  background: #facc15;
  color: #111;
}
.risk-button:hover {
  background: #eab308;
  transform: translateY(-3px);
}

</style>
