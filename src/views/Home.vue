<template>
  <div class="page-wrapper">

    <!-- ===== Hero Section ===== -->
    <section class="hero-banner">
      <div class="hero-overlay">
        <div class="hero-content">
          <div class="hero-content">
            <h2 class="hero-title">
              Stay Safe Online with <span class="highlight">CyberMate</span>
            </h2>
            <p class="hero-subtitle">
              Your trusted mate for spotting scams, boosting digital skills, and staying secure.
            </p>

            <!-- Hero action buttons -->
            <div class="hero-buttons">
              <button class="hero-btn" @click="$router.push('/scambot')">ScamBot</button>
              <button class="hero-btn" @click="$router.push('/riskscore')">Risk Score</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== About Section ===== -->
    <section class="about-section">
      <div class="about-container">

        <!-- Left text -->
        <div class="about-text">
          <h3>About CyberMate</h3>
          <p>
            CyberMate empowers aged 55 and above Australians to recognise, avoid, and report scams.
            Through interactive dashboards, a scam detector bot, and a risk score tracker,
            we make online safety engaging and easy.
          </p>
          <button class="explore-btn" @click="goToDashboard">
            Explore Dashboard
          </button>
        </div>

        <!-- Right stats cards -->
        <div class="about-stats">
          <div
            v-for="(stat, index) in stats"
            :key="index"
            class="stat-card"
            @click="toggleFlip(index)"  
          >
            <div class="stat-inner" :class="{ flipped: stat.isFlipped }">

              <!-- Front side -->
              <div
                class="stat-front"
                :style="{
                  backgroundImage: `url(${stat.image})`,
                  backgroundSize: 'cover',
                  backgroundPosition: 'center'
                }"
              >
                <h4>{{ stat.value }}</h4>
              </div>

              <!-- Back side -->
              <div class="stat-back">
                <p>{{ stat.label }}</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ===== ScamBot Section ===== -->
    <section class="bot-section">
      <div class="bot-container">

        <!-- Left: Chat bubbles -->
        <div class="chat-box">
          <div class="bubble user">
            Got this message:<br />
            “Your parcel is held. Pay $3.50 to release: bit.ly/…”
          </div>
          <div class="bubble bot">
            ⚠️ Risky: urgent payment + shortened link. Do not pay or click.
          </div>
          <div class="bubble user">
            What should I do?
          </div>
          <div class="bubble bot">
            Delete the message and report to Scamwatch.
          </div>
        </div>

        <!-- Right: Info + button -->
        <div class="bot-info">
          <h3>Meet our <span class="highlight">Scam Detector Bot</span></h3>
          <p>
            Just paste a suspicious message,<br />
            and our AI will instantly tell you if it looks like a scam.
          </p>
          <button class="bot-button" @click="goToScamBot">Explore ScamBot</button>
        </div>

      </div>
    </section>

    <!-- ===== Risk Score Section ===== -->
    <section class="risk-section">
      <div class="risk-container">

        <!-- Left: Text -->
        <div class="risk-text">
          <h3>Risk Score Measure</h3>
          <p>
            CyberMate’s Risk Score helps you understand your personal exposure.
            Based on your online activity and scam history, get a score that
            shows your digital risk level.
          </p>
          <button class="risk-button" @click="goToRiskScore">
            Measure your Risk Score
          </button>
        </div>

        <!-- Right: Animation -->
        <div class="risk-animation">
          <Vue3Lottie
            animationLink="/riskimage.json"
            :loop="true"
            :autoplay="true"
          />
        </div>

      </div>
    </section>

    <!-- ===== Floating ScamBot button ===== -->
    <div class="scambot-floating" @click="goToScamBot">
      <img src="/bot.png" alt="ScamBot" />
      <span>ScamBot</span>
    </div>

  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { Vue3Lottie } from "vue3-lottie"

// Stats cards data
const stats = ref([
  { 
    value: "Did you know?", 
    label: "Australians lose billions every year to scams, making online awareness more important than ever.", 
    color: "#bae6fd",
    image: "/img1.png",
    isFlipped: false
  },
  { 
    value: "Who’s at risk?", 
    label: "In 2025, over 7,000 Australians aged 55+ fell victim to scams nationwide.", 
    color: "#fecdd3",
    image: "/img2.png",
    isFlipped: false
  },
  { 
    value: "Reported losses", 
    label: "Scammers stole more than $8.6 million from older Australians in 2025 alone.", 
    color: "#fecaca",
    image: "/img3.png",
    isFlipped: false
  },
  { 
    value: "Top scams to watch", 
    label: "Investment · Phishing · Romance", 
    color: "#fde68a",
    image: "/img4.png",
    isFlipped: false
  }
])

// Router navigation
const router = useRouter()
const goToDashboard = () => router.push("/dashboard")
const goToScamBot = () => router.push("/scambot")
const goToRiskScore = () => router.push("/riskscore")

// Toggle flip for mobile (click)
const toggleFlip = (index) => {
  stats.value[index].isFlipped = !stats.value[index].isFlipped
}
</script>

<style scoped>

/* ===== Page Wrapper ===== */
.page-wrapper {
  background-color: #C8E6C9;
  min-height: 100vh;
  padding: 0;
}

/* ===== HERO ===== */
.hero-banner {
  background-image: url("/cyber-bg.png");
  background-size: cover;
  background-position: center;
  height: 400px;               /* Fixed height */
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.hero-overlay {
  position: absolute;          
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;                
  background-color: rgba(0, 0, 0, 0.4);  /* Transparent overlay */
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  position: relative;          
  text-align: center;
  padding: 0 16px;
}

/* Title with rainbow gradient */
.hero-title {
  font-size: 4rem;             
  font-weight: 800;
  margin-bottom: 20px;
  line-height: 1.3;
  background: linear-gradient(
    90deg,
    #3b82f6,   
    #22c55e,   
    #facc15,   
    #ec4899,   
    #3b82f6    
  );
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientMove 5s infinite linear;
}

/* Subtitle white */
.hero-subtitle {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 20px;
}

/* Responsive Adjustments */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 3rem;
  }
  .hero-subtitle {
    font-size: 1.2rem;
  }
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 2rem;
  }
  .hero-subtitle {
    font-size: 1rem;
  }
}

/* Gradient animation */
@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  100% { background-position: 100% 50%; }
}

/* ===== Hero Buttons ===== */
.hero-buttons {
  display: flex;
  gap: 40px;
  margin-top: 20px;
  justify-content: center;   
}

.hero-btn {
  background: linear-gradient(90deg, #00c3ff, #9AEBA3);
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 140px;          
  text-align: center;
}

.hero-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 12px rgba(123, 47, 247, 0.6);
}

/* Responsive: stack vertically on small screens */
@media (max-width: 640px) {
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  .hero-btn {
    width: 80%;              
  }
}

/* ===== About Section ===== */
.about-section {
  background: linear-gradient(to right, #45C4B0, #9AEBA3);
  padding: 40px 0;
  width: 100%;
  margin: 20px 0 0;
}
.about-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
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
  font-size: 2.6rem;
  font-weight: bold;
  margin-bottom: 16px;
}
.about-text p {
  font-size: 1.3rem;
  line-height: 1.8;
}

/* About stats */
.about-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.stat-card {
  perspective: 1000px;
  position: relative;
  height: 200px;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  font-weight: bold;
  box-shadow: 0 3px 6px rgba(0,0,0,0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}
.stat-card h4 {
  font-size: 1.6rem;
  margin-bottom: 8px;
}

/* Stat card flipping */
.stat-inner {
  transition: transform 0.6s;
  transform-style: preserve-3d;
  width: 100%;
  height: 100%;
  position: relative;
}
/* Hover flip (desktop) */
.stat-card:hover .stat-inner {
  transform: rotateY(180deg);
}
/* Click flip (mobile) */
.stat-inner.flipped {
  transform: rotateY(180deg);
}

.stat-front, .stat-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 3px 6px rgba(0,0,0,0.08);
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.stat-front {
  font-weight: bold;
  font-size: 1.5rem;
}
.stat-back {
  transform: rotateY(180deg);
  background: #fff;
  font-size: 1rem;
  line-height: 1.4;
}
/* White text with shadow */
.stat-front h4,
.stat-front p {
  color: white !important;
  font-weight: bold;
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.8);
  transition: all 0.3s ease;
}

/* ===== Bot Section ===== */
.bot-section {
  background: linear-gradient(to right, #45C4B0, #9AEBA3);
  padding: 40px 0;
  width: 100%;
  margin: 20px 0 0;
  color: black;
}
.bot-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
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
.chat-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 20px 0;
  max-width: 420px;
}
.bubble {
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 1rem;
  line-height: 1.5;
  max-width: 100%;
  word-wrap: break-word;
}
/* User bubble */
.bubble.user {
  align-self: flex-start;
  background-color: #40acdf;
  color: #fff;
  border-bottom-left-radius: 4px;
}
/* Bot bubble */
.bubble.bot {
  align-self: flex-end;
  background-color: #a7f3d0;
  color: #000;
  border-bottom-right-radius: 4px;
}
.bot-info h3 {
  font-size: 2.6rem;
  font-weight: bold;
  margin-bottom: 16px;
}
.bot-info p {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 20px;
}

/* ===== Risk Score Section ===== */
.risk-section {
  background: linear-gradient(to right, #45C4B0, #9AEBA3);
  padding: 40px 0;
  width: 100%;
  margin: 20px 0 0;
}
.risk-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
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
.risk-text h3 {
  font-size: 2.6rem;
  font-weight: bold;
  margin-bottom: 16px;
}
.risk-text p {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 20px;
}
.risk-animation {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}
.risk-animation canvas,
.risk-animation svg {
  width: 100% !important;
  height: auto !important;
}
.risk-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* ===== Buttons ===== */
button,
.explore-btn,
.bot-button,
.risk-button {
  display: inline-block;
  padding: 10px 24px;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.explore-btn {
  background: #13678A;
  color: white;
}
.explore-btn:hover {
  background: #4f46e5;
  transform: translateY(-3px);
}
.bot-button {
  background: #13678A;
  color: white;
}
.bot-button:hover {
  background: #4f46e5;
  transform: translateY(-3px);
}
.risk-button {
  background: #13678A;
  color: white;
}
.risk-button:hover {
  background: #eab308;
  transform: translateY(-3px);
}

/* ===== Floating ScamBot Button ===== */
.scambot-floating {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #45C4B0;
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

/* ===== Extra Components ===== */
.explore-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
/* Animated gradient background card */
.card {
  position: relative;
  width: 100%;
  min-height: 450px;
  border-radius: 30px;
  background: linear-gradient(45deg, #45c4b0, #5eead4, #4ade80);
  background-size: 400% 400%;
  animation: gradientMove 8s ease infinite;
  transition: all 0.5s ease-in-out;
  transform-style: preserve-3d;
  box-shadow: rgba(5, 71, 17, 0) 40px 50px 25px -40px,
              rgba(5, 71, 17, 0.2) 0px 25px 25px -5px;
  padding: 40px;
  box-sizing: border-box;
}

</style>
