<template>
  <div class="risk-page">
    <!-- ===== Background Meteor Effect ===== -->
    <canvas id="meteorCanvas"></canvas>

    <!-- ===== Page Title Section ===== -->
    <section class="risk-header">
      <div class="title-row">
        <!-- Loader Animation (3x3 grid) -->
        <div class="loader">
          <div class="cell d-1"></div>
          <div class="cell d-2"></div>
          <div class="cell d-3"></div>
          <div class="cell d-4"></div>
          <div class="cell d-1"></div>
          <div class="cell d-2"></div>
          <div class="cell d-3"></div>
          <div class="cell d-4"></div>
          <div class="cell d-1"></div>
        </div>
        <!-- Title -->
        <h2>Risk Score</h2>
      </div>


    <!-- ===== Hover Box (PC hover + Mobile click) ===== -->
<div class="hover-box">
  <div class="square" @click.stop="toggleImage">❓</div>
  <div class="hint-box">
    Click on the “?” icon to learn how the Risk Score works.
  </div>
  <!-- PC hover + Mobile click -->
  <!-- PC 端 hover + Mobile 点击 -->
  <div v-if="showImage" class="img-wrapper">
    <img src="/example.png" alt="Preview" class="hover-img" />
    <button class="close-btn" @click="showImage = false">✖</button>
  </div>

  <img 
    src="/example.png" 
    alt="Preview" 
    class="hover-img" 
    :class="{ 'show-mobile': showImage }" 
  />
</div>


      <!-- Subtitle -->
      <p>
        Not sure if your post sounds risky? Paste it here before sharing on Facebook, Instagram, or anywhere online. 
        We’ll flag warning signs and show you how safe it is.
      </p>
    </section>

    <!-- ===== 3D Card with Input + State Selector ===== -->
    <div class="parent">
      <div class="card">
        <div class="glass"></div>

        <!-- Input Area -->
        <div class="content">
          <label for="textInput" class="title">Paste text</label>
          <textarea
            id="textInput"
            v-model="userText"
            placeholder="Paste or type your text here..."
            class="risk-textarea"
          ></textarea>
        </div>

        <!-- Bottom Section: Dropdown + Button -->
        <div class="bottom">
          <div class="state-wrapper">
            <label for="stateSelect" class="input-label small">Select State</label>
            <select id="stateSelect" v-model="state" class="state-select">
              <option value="ALL">All States</option>
              <option value="VIC">VIC</option>
              <option value="NSW">NSW</option>
              <option value="QLD">QLD</option>
              <option value="WA">WA</option>
              <option value="SA">SA</option>
              <option value="TAS">TAS</option>
              <option value="NT">NT</option>
              <option value="ACT">ACT</option>
            </select>
          </div>

          <div class="view-more">
            <button class="check-btn" @click="analyzeRisk">Check</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== Loading State ===== -->
    <div v-if="loading" class="mt-4 text-lg">Analyzing...</div>

    <!-- ===== Error Message ===== -->
    <div v-else-if="result?.errorMessage" class="mt-4 text-red-600">
      {{ result.errorMessage }}
    </div>

    <!-- ===== Risk Result Section ===== -->
    <section v-else-if="result?.analysis?.analysis" class="form-container">
      <!-- Risk Level -->
      <h3 class="heading">
        Risk Level: 
        <span
          v-if="result.analysis.analysis.score"
          class="risk-badge"
          :class="result.analysis.analysis.score.toLowerCase()"
        >
          {{ result.analysis.analysis.score }}
        </span>
      </h3>

      <!-- Labels -->
      <p v-if="result.analysis.analysis.labels?.length" class="c1">
        <strong>Labels:</strong> {{ result.analysis.analysis.labels.join(", ") }}
      </p>

      <!-- Highlighted Phrases -->
      <div v-if="result.analysis.analysis.highlights?.length" class="c2">
        <h4>Highlighted Phrases:</h4>
        <ul>
          <li v-for="(h, i) in result.analysis.analysis.highlights" :key="i">
            "{{ h.phrase }}" → <em>{{ h.category }}</em>
          </li>
        </ul>
      </div>

      <!-- Educational Tips -->
      <div v-if="result.analysis.analysis.tips?.length" class="c2">
        <h4>Educational Tips:</h4>
        <ul>
          <li v-for="(t, i) in result.analysis.analysis.tips" :key="i">
            {{ t.tip }}
          </li>
        </ul>
      </div>

      <!-- Applicable Laws -->
      <div v-if="result.analysis.analysis.laws?.length" class="c2">
        <h4>Applicable Laws:</h4>
        <ul>
          <li v-for="(law, i) in result.analysis.analysis.laws" :key="i">
            <strong>{{ law.law_name }}</strong> ({{ law.state }})  
            <br />{{ law.law_desc }}
            <br /><a :href="law.law_url" target="_blank">Read more</a>
          </li>
        </ul>
      </div>

      <!-- Reporting Information -->
      <div v-if="result.analysis.analysis.reporting?.length" class="c2">
        <h4>Where to Report:</h4>
        <ul>
          <li v-for="(r, i) in result.analysis.analysis.reporting" :key="i">
            <strong>{{ r.authority_name }}</strong>:  
            <a :href="r.report_url" target="_blank">{{ r.short_desc }}</a>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue"
import axios from "axios"

/* ===== States ===== */
const userText = ref("")
const state = ref("ALL")
const result = ref(null)
const loading = ref(false)

/* ===== Analyze Function ===== */
const analyzeRisk = async () => {
  if (!userText.value.trim()) {
    alert("Please enter some text to analyze.")
    return
  }

  loading.value = true
  result.value = null
  try {
    const response = await axios.post(
      "https://cybermate-production.up.railway.app/risk/risk_detect",
      { text: userText.value, state: state.value },
      { headers: { "Content-Type": "application/json" } }
    )
    result.value = response.data
  } catch (err) {
    console.error("Error calling Risk Detector:", err)
    result.value = { errorMessage: "Backend error, please try again." }
  } finally {
    loading.value = false
  }
}


const showImage = ref(false)

const toggleImage = () => {
  if (window.innerWidth <= 768) {
    showImage.value = !showImage.value
  }
}

const handleClickOutside = (event) => {
  const hoverBox = document.querySelector(".hover-box")
  if (window.innerWidth <= 768 && hoverBox && !hoverBox.contains(event.target)) {
    showImage.value = false
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside)
})

/* ===== Meteor Background Effect ===== */
onMounted(() => {
  const canvas = document.getElementById("meteorCanvas")
  const ctx = canvas.getContext("2d")
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight

  const meteors = []

  function createMeteor() {
    meteors.push({
      x: Math.random() * canvas.width,
      y: 0,
      length: Math.random() * 80 + 20,
      speed: Math.random() * 4 + 2,
      opacity: Math.random() * 0.8 + 0.2,
    })
  }

  function drawMeteor(m) {
    const gradient = ctx.createLinearGradient(m.x, m.y, m.x - m.length, m.y + m.length)
    gradient.addColorStop(0, `rgba(255,0,255,${m.opacity})`)
    gradient.addColorStop(0.5, `rgba(0,255,255,${m.opacity})`)
    gradient.addColorStop(1, "rgba(0,255,150,0)")
    ctx.strokeStyle = gradient
    ctx.beginPath()
    ctx.moveTo(m.x, m.y)
    ctx.lineTo(m.x - m.length, m.y + m.length)
    ctx.stroke()
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    meteors.forEach((m, i) => {
      m.x -= m.speed
      m.y += m.speed
      drawMeteor(m)
      if (m.y > canvas.height || m.x < 0) meteors.splice(i, 1)
    })
    if (Math.random() < 0.05) createMeteor()
    requestAnimationFrame(animate)
  }

  animate()

  window.addEventListener("resize", () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  })
})
</script>



<style scoped>
/* ===== Background Meteor Effect ===== */
#meteorCanvas {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 0;          /* behind everything */
  width: 100%;
  height: 100%;
  background: #0b132b; /* dark night sky */
}

/* ===== Foreground Container ===== */
.risk-page {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  padding: 100px 20px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 1.2rem;
}

/* ===== Hover Box with Tooltip Image ===== */
.hover-box {
  display: flex;
  flex-direction: column;   
  align-items: center;      
  text-align: center;       
  gap: 8px;                 
}

.square {
  width: 40px;
  height: 40px;
  background: teal;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.25);
}

.hover-img {
  position: absolute;
  top: -20px;
  left: 60px;
  width: 480px;
  height: auto;
  display: none;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.25);
  z-index: 10;
}

/* PC hover */
.hover-box:hover .hover-img {
  display: block;
}

/* Mobile click */
.show-mobile {
  display: block !important;
  max-width: 90vw;
  max-height: 70vh;
}

.hint-box {
  background: rgba(19,103,138,0.85);  
  color: white;
  font-size: 0.9rem;
  padding: 8px 14px;
  border-radius: 8px;
  max-width: 260px;
  line-height: 1.4;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
/* ===== Header Section ===== */
.risk-header {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
  z-index: 10;
}
.title-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  position: relative;
  z-index: 10;
  flex-wrap: wrap;     /* allow wrap on smaller screens */
  text-align: center;
}
.risk-header h2 {
  font-size: 3rem;
  font-weight: bold;
  color: #45C4B0;
  margin-bottom: 14px;
  text-shadow: 0 0 6px #45C4B0, 0 0 12px #00ffaa;
  position: relative;
  z-index: 10;
}
.risk-header p {
  font-size: 1.4rem;
  color: #ddd;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.8;
}

/* ===== Loader Animation (3x3 grid) ===== */
.loader {
  --cell-size: 28px;
  --cell-spacing: 4px;
  --cells: 3;
  --total-size: calc(var(--cells) * (var(--cell-size) + 2 * var(--cell-spacing)));
  display: flex;
  flex-wrap: wrap;
  width: var(--total-size);
  height: var(--total-size);
  flex-shrink: 0;
}
.cell {
  flex: 0 0 var(--cell-size);
  margin: var(--cell-spacing);
  background-color: transparent;
  box-sizing: border-box;
  border-radius: 4px;
  animation: 1.5s ripple ease infinite;
}
.cell.d-1 { animation-delay: 100ms; }
.cell.d-2 { animation-delay: 200ms; }
.cell.d-3 { animation-delay: 300ms; }
.cell.d-4 { animation-delay: 400ms; }

.cell:nth-child(1) { --cell-color: #00FF87; }
.cell:nth-child(2) { --cell-color: #0CFD95; }
.cell:nth-child(3) { --cell-color: #17FBA2; }
.cell:nth-child(4) { --cell-color: #23F9B2; }
.cell:nth-child(5) { --cell-color: #30F7C3; }
.cell:nth-child(6) { --cell-color: #3DF5D4; }
.cell:nth-child(7) { --cell-color: #45F4DE; }
.cell:nth-child(8) { --cell-color: #53F1F0; }
.cell:nth-child(9) { --cell-color: #60EFFF; }

@keyframes ripple {
  0% { background-color: transparent; }
  30% { background-color: var(--cell-color); }
  60% { background-color: transparent; }
  100% { background-color: transparent; }
}

/* Responsive: stack loader above title */
@media (max-width: 640px) {
  .title-row {
    flex-direction: column;
    gap: 12px;
  }
  .loader {
    --cell-size: 22px;   /* smaller cells on mobile */
    --cell-spacing: 3px;
  }
  .risk-header h2 {
    font-size: 2rem;     /* shrink title */
  }
}
.img-wrapper {
  position: relative;
  display: inline-block;
}


.hover-img {
  position: absolute;
  top: -20px;
  left: 60px;
  width: 480px;
  max-width: 90vw;   
  height: auto;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.25);
  z-index: 10;
}


@media (max-width: 768px) {
  .hover-img {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    max-width: 90vw;
    max-height: 80vh;
  }

  .close-btn {
    position: fixed;
    top: 16px;
    left: 16px;
    background: rgba(0,0,0,0.6);
    color: white;
    border: none;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    font-size: 18px;
    cursor: pointer;
    z-index: 11;
  }
}

/* ===== Static Card Container ===== */
.parent {
  width: 100%;
  max-width: 1100px;
  margin: 40px auto;
  position: relative;
  z-index: 20;
}

.card {
  position: relative;
  width: 100%;
  min-height: 450px;
  border-radius: 30px;
  background: linear-gradient(
    135deg,
    rgba(0, 255, 214, 0.9) 0%,
    rgba(8, 226, 96, 0.9) 100%
  );
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
  padding: 40px;
  box-sizing: border-box;
  z-index: 21;
}

.glass {
  position: absolute;
  inset: 8px;
  border-radius: 30px;
  background: linear-gradient(
    0deg,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0.9) 100%
  );
  border-left: 1px solid white;
  border-bottom: 1px solid white;
}

.content {
  position: relative;
  z-index: 2;
}

.content .title {
  display: block;
  color: #00894d;
  font-weight: 900;
  font-size: 20px;
  margin-bottom: 10px;
}
.risk-textarea {
  width: 100%;
  min-height: 160px;
  border-radius: 12px;
  border: 1px solid #ccc;
  padding: 14px;
  font-size: 1rem;
  line-height: 1.6;
  resize: vertical;
}
.bottom {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-top: 20px;
  transform: translate3d(0, 0, 26px);
}
.state-wrapper {
  flex: 1;
}
.state-select {
  margin-top: 6px;
  padding: 12px 16px;
  border-radius: 10px;
  border: 2px solid #45C4B0;
  font-size: 1rem;
  font-weight: 500;
  background: #f5f3ff;
  color: #45C4B0;
  width: 100%;
}
.check-btn {
  background: #45C4B0;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}
.check-btn:hover {
  transform: translateY(-2px);
}
.parent:hover .card {
  transform: rotate3d(1, 1, 0, 10deg);
  box-shadow: rgba(5,71,17,0.3) 20px 30px 20px -20px,
              rgba(5,71,17,0.1) 0px 15px 20px 0px;
}

/* ===== Risk Result Container ===== */
.form-container {
  max-width: 1100px;
  margin: 30px auto;
  background: rgba(0,25,37,0.95);
  padding: 50px;
  border-left: 5px solid #caf438;
  border-radius: 12px;
  position: relative;
  z-index: 22;
  box-shadow: 0 8px 20px rgba(0,0,0,0.7);
}
.heading {
  display: block;
  color: white;
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 20px;
}
.c1 {
  display: block;
  color: #d3f35f;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 20px;
}
.c2 {
  display: block;
  color: white;
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 20px;
  line-height: 1.6;
}
.form-container ul {
  margin: 10px 0 20px 20px;
}
.form-container a {
  color: #caf438;
  text-decoration: underline;
}
.form-container a:hover {
  color: #ff7a01;
}

/* ===== Risk Badge Colors ===== */
.risk-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: bold;
  text-transform: uppercase;
}
.low {
  background: #004d1a;
  color: #caf438;
  border: 1px solid #caf438;
}
.medium {
  background: #4d3b00;
  color: #ffd84d;
  border: 1px solid #ffd84d;
}
.high {
  background: #4d0000;
  color: #ff6b6b;
  border: 1px solid #ff6b6b;
}
</style>
