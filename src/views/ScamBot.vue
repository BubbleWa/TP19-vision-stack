<template>
  <div class="page-wrapper">
    <!-- ===== Header ===== -->
    <div class="header-card" data-aos="fade-down">
      <div class="header-flex">
        <!-- Left: Matrix animation -->
        <div class="ai-matrix-loader">
          <span class="digit">0</span>
          <span class="digit">1</span>
          <span class="digit">0</span>
          <span class="digit">1</span>
          <span class="digit">0</span>
          <span class="digit">1</span>
          <span class="digit">0</span>
          <span class="digit">1</span>
          <div class="glow"></div>
        </div>

        <!-- Center: Title -->
        <h2 class="scam-title">ScamDetector</h2>

        <!-- Right: Bot animation -->
        <lottie-player
          src="/AI bot.json"
          background="transparent"
          speed="1"
          style="width: 180px; height: 180px;"
          loop
          autoplay
        />
      </div>

      <p style="font-size: 25px;">
        Hi! I’m ScamMate, your scam-spotting buddy.<br />
        Paste a suspicious message —I’ll flag risks for you.
      </p>
    </div>

    <!-- ===== Input section (radar on the left, textarea on the right) ===== -->
    <section class="input-card" data-aos="fade-up">
      <div class="input-row">
        <!-- Radar on the left -->
        <div class="radar-col">
          <div class="loader">
            <span></span>
          </div>
        </div>

        <!-- Textarea on the right -->
        <textarea
          v-model="userInput"
          class="doc-input"
          placeholder="Paste or type the suspicious message here..."
        ></textarea>
      </div>

      <!-- Action button below -->
      <button class="btn primary" @click="analyze" :disabled="loading">
        {{ loading ? "Checking..." : "Detect" }}
      </button>
    </section>

    <!-- ===== Error ===== -->
    <div v-if="error" class="result text-red-600">
      {{ error }}
    </div>

  <!-- ===== Results ===== -->
  <div v-if="result" class="result-panel" data-aos="fade-up">
    <!-- Verdict + Category -->
    <div class="stack">
      <div class="card">
        <p>
          <strong>Verdict:</strong>
          <span :class="result.verdict === 'Scam' ? 'tag danger' : 'tag safe'">
            {{ result.verdict || "Unknown" }}
          </span>
        </p>
        <p v-if="result.category">
          <strong>Category:</strong>
          <span class="tag">{{ result.category }}</span>
        </p>
      </div>
    </div>

    <!-- Confidence Score -->
    <div class="stack">
      <div class="card center">
        <p>
          <strong>Confidence Score:</strong>
          <span class="score-text">{{ Math.round(animatedScore) }}%</span>
        </p>
        <svg class="progress-ring" width="140" height="140">
          <circle
            class="progress-ring__background"
            stroke="#e5e7eb"
            fill="transparent"
            r="60"
            cx="70"
            cy="70"
          />
          <circle
            class="progress-ring__circle"
            stroke="#7c3aed"
            fill="transparent"
            r="60"
            cx="70"
            cy="70"
            :style="circleStyle"
          />
        </svg>
      </div>
    </div>

    <!-- Step Guide (dynamic from API) -->
    <div class="stack" v-if="result.checklist?.items?.length">
      <div class="card">
        <p><strong>Step-by-Step Guide</strong></p>
        <ul class="guide">
          <li v-for="(item, i) in result.checklist.items" :key="i">
            {{ item }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Triggered patterns -->
    <div class="stack">
      <div class="card full">
        <p><strong>Triggered Patterns:</strong></p>
        <ul class="list-disc pl-5">
          <li v-for="(r, i) in result.reasons" :key="i">{{ r }}</li>
        </ul>
        <!-- Report button -->
        <a
          :href="result.reporting_guide?.url || 'https://www.scamwatch.gov.au/report-a-scam'"
          target="_blank"
          rel="noopener noreferrer"
          class="btn report"
        >
          Report to ScamWatch
        </a>
      </div>
    </div>
  </div>
  </div>
  </template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { detectScam } from "@/services/scambot"
import AOS from "aos"

// State
const userInput = ref("")
const loading = ref(false)
const error = ref("")
const result = ref(null)
const animatedScore = ref(0)
let scoreInterval = null

// Analyze
async function analyze() {
  error.value = ""
  result.value = null
  if (!userInput.value.trim()) return
  loading.value = true
  try {
    result.value = await detectScam(userInput.value.trim())
    startScoreAnimation(Math.round((result.value.score_ml ?? 0) * 100))
  } catch (e) {
    error.value = e.message || "Something went wrong."
  } finally {
    loading.value = false
  }
}

// Animate confidence %
function startScoreAnimation(target) {
  clearInterval(scoreInterval)
  animatedScore.value = 0
  scoreInterval = setInterval(() => {
    if (animatedScore.value < target) animatedScore.value += 1
    else clearInterval(scoreInterval)
  }, 15)
}

// Circle stroke style
const circleStyle = computed(() => {
  const r = 60
  const c = 2 * Math.PI * r
  const pct = animatedScore.value / 100
  return {
    strokeDasharray: `${c} ${c}`,
    strokeDashoffset: c - pct * c,
    transition: "stroke-dashoffset 0.3s linear"
  }
})

onMounted(() => AOS.init())
</script>

<style scoped>
/* ===== Score text inside results ===== */
.score-text {
  font-size: 3.5rem;
  font-weight: 700;
  color: #45C4B0;
  margin-left: 8px; /* spacing from label */
}

/* ===== Page wrapper ===== */
.page-wrapper {
  min-height: 100vh;
  background: #C8E6C9; /* light green background */
  padding: 20px;
}

/* ===== Header animation (matrix digits) ===== */
.ai-matrix-loader {
  width: 120px;
  height: 160px;
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 5px;
  z-index: 10;
}
.digit {
  color: #00ff88;
  font-family: monospace;
  font-size: 18px;
  text-align: center;
  text-shadow: 0 0 5px #00ff88;
  animation: matrix-fall 2s infinite, matrix-flicker 0.5s infinite;
  opacity: 0;
}
@keyframes matrix-fall {
  0% { transform: translateY(-50px); opacity: 0; }
  20%, 80% { transform: translateY(0); opacity: 0.8; }
  100% { transform: translateY(50px); opacity: 0; }
}
@keyframes matrix-flicker {
  0%, 19%, 21%, 100% { opacity: 0.8; }
  20% { opacity: 0.2; }
}

/* ===== Header card ===== */
.header-card {
  background: linear-gradient(135deg, #45c4b0, #9aeba3);
  color: white;
  text-align: center;
  padding: 28px 16px;
  border-radius: 16px;
  margin: 20px;
}
/* Gradient scam-title (always active) */
.scam-title {
  font-size: 4rem;
  font-weight: 800;
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

/* Responsive font size */
@media (min-width: 769px) {
  .scam-title {
    font-size: 3.5rem;
  }
}
@media (max-width: 768px) {
  .scam-title {
    font-size: clamp(2rem, 5vw, 3rem);
  }
}

/* Header responsive layout */
@media (max-width: 768px) {
  .header-flex {
    grid-template-columns: 1fr; /* stack vertically */
    text-align: center;
  }
}
.header-flex {
  display: grid;
  grid-template-columns: 120px 1fr 180px; 
  align-items: center;
  gap: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .header-flex {
    grid-template-columns: 1fr; 
    text-align: center;
  }
    .header-flex .ai-matrix-loader {
    margin: 0 auto; 
  }
  .header-flex lottie-player {
    margin: 0 auto; 
  }
}


/* ===== Input card (radar + textarea) ===== */
.input-card {
  position: relative;
  width: 80%;
  max-width: 1300px;
  margin: 60px auto;
  padding: 20px 20px 24px;
  border-radius: 20px;
  background: #07182e; /* dark card background */
  box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}
.input-row {
  display: flex;
  align-items: stretch;
  gap: 20px;
  width: 100%;
}
@media (max-width: 768px) {
  .input-row {
    flex-direction: column; /* stack vertically on mobile */
  }
  .radar-col {
    margin-bottom: 16px;
  }
  .doc-input {
    flex: 1;
    min-width: 250px;   /* prevent too narrow */
    max-width: 500px;   /* prevent too wide */
    min-height: 120px;
    max-height: 220px;
    border-radius: 12px;
    border: none;
    padding: 14px;
    font-size: 1.2rem;
    color: #f3f6fd;
    background: #0a1527;
    resize: vertical;
    outline: none;
  }
}

/* ===== Radar column ===== */
.radar-col {
  flex: 0 0 240px; /* fixed width */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ===== Radar loader ===== */
.loader {
  position: relative;
  width: 220px;
  height: 220px;
  background: transparent;
  border-radius: 50%;
  border: 1px solid #333;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  filter: drop-shadow(0 14px 28px rgba(0,0,0,0.45));
}
.loader::before {
  content: '';
  position: absolute;
  inset: 20px;
  border: 1px dashed #444;
  border-radius: 50%;
}
.loader::after {
  content: '';
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 1px dashed #444;
}
.loader span {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 50%;
  height: 100%;
  transform-origin: top left;
  animation: radar81 2s linear infinite;
  border-top: 1px dashed #fff;
}
.loader span::before {
  content: '';
  position: absolute;
  inset: 0;
  background: seagreen;
  transform-origin: top left;
  transform: rotate(-55deg);
  filter: blur(30px) drop-shadow(20px 20px 20px seagreen);
}
@keyframes radar81 { to { transform: rotate(360deg); } }

/* ===== Textarea ===== */
.doc-input {
  flex: 1 1 auto;
  min-height: 220px;
  border-radius: 12px;
  border: none;
  padding: 16px;
  font-size: 1.5rem;
  color: #f3f6fd;
  background: #183563;
  resize: vertical;
  outline: none;
}

/* ===== Buttons ===== */
.btn.primary {
  margin-top: 16px;
  background: linear-gradient(90deg, #00c3ff, #7b2ff7);
  color: white;
  padding: 10px 20px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 12px rgba(123, 47, 247, 0.6);
}
.btn.report {
  background: linear-gradient(90deg, #10b981, #059669);
  color: white;
  padding: 10px 16px;
  border-radius: 12px;
  display: inline-block;
  margin-top: 12px;
  font-weight: 600;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn.report:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
}

/* ===== Results panel (stacked cards) ===== */
.result-panel {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}
.stack { transition: 0.25s ease; }
.stack:hover { transform: rotate(5deg); }
.stack:hover .card:before { transform: translateY(-2%) rotate(-4deg); }
.stack:hover .card:after  { transform: translateY(2%) rotate(4deg); }
.card {
  border: 4px solid;
  background-color: #fff;
  position: relative;
  transition: 0.15s ease;
  cursor: pointer;
  padding: 20px;
  border-radius: 12px;
  height: 100%;
}
.card:before,
.card:after {
  content: "";
  position: absolute;
  inset: 0;
  border: 4px solid;
  background-color: #fff;
  transform-origin: center;
  z-index: -1;
  transition: 0.15s ease;
}
.card:before { transform: translateY(-2%) rotate(-6deg); }
.card:after  { transform: translateY( 2%) rotate( 6deg); }

/* ===== Confidence score circle ===== */
.progress-ring__circle {
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
  stroke-linecap: round;
  stroke-width: 18;
}
.progress-ring__background { stroke-width: 18; }
.circle-label {
  position: absolute;
  margin-top: -90px;
  font-size: 1.8rem;
  font-weight: 800;
  color: #45C4B0;
}

/* ===== Tags ===== */
.tag.danger { background: #fee2e2; color: #b91c1c; padding: 2px 6px; border-radius: 6px; }
.tag.safe   { background: #dcfce7; color: #166534; padding: 2px 6px; border-radius: 6px; }
</style>
