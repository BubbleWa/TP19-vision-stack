<template>
  <div class="scambot-page">
    <!-- Purple header card -->
    <div class="header-card">
      <h2>🤖 ScamDetector</h2>
      <p>
        Hi! I’m ScamMate, your scam-spotting buddy.<br>
        Paste a suspicious message or upload a screenshot—I’ll flag risks for you.
      </p>
    </div>

    <!-- Input section -->
    <div class="risk-grid">
      <section class="card doc-card">
        <!-- Toolbar -->
        <div class="doc-toolbar">
          <button class="btn ghost" @click="pasteFromClipboard">Paste text</button>
        </div>

        <!-- Input textarea -->
        <textarea
          v-model="userInput"
          class="doc-input"
          placeholder="Paste or type the suspicious message here..."
        ></textarea>

        <!-- Actions -->
        <div class="doc-actions">
          <input
            id="fileInput"
            type="file"
            class="hidden"
            accept="image/*,text/plain"
            @change="handleFile"
          >
          <button class="btn primary" @click="analyze" :disabled="loading">
            {{ loading ? "Checking..." : "Detect" }}
          </button>
        </div>

        <!-- Error message -->
        <div v-if="error" class="result text-red-600">
          {{ error }}
        </div>

        <!-- Result panel -->
        <div v-if="result" class="result-panel">
          <!-- Top section: Verdict / Confidence / Guide -->
          <div class="result-grid">
            <!-- Verdict + Category -->
            <div class="card result-card">
              <p><strong>Verdict:</strong>
                <span :class="result.verdict === 'Scam' ? 'tag danger' : 'tag safe'">
                  {{ result.verdict || "Unknown" }}
                </span>
              </p>
              <p><strong>Detected Category:</strong> {{ result.category || "Unclassified" }}</p>
              <p><strong>Authority to Report To:</strong>
                <span class="tag info">
                  {{ result.authority ? result.authority : "ScamWatch" }}
                </span>
              </p>

              <!-- Green button with hyperlink -->
              <a
                href="https://www.scamwatch.gov.au/report-a-scam"
                target="_blank"
                rel="noopener noreferrer"
                class="btn report"
              >
                Report to ScamWatch
              </a>
            </div>

            <!-- Confidence Score with animated circle -->
            <div class="card result-card center">
              <p><strong>Confidence Score</strong></p>
              <svg class="progress-ring" width="140" height="140">
                <circle
                  class="progress-ring__background"
                  stroke="#e5e7eb"
                  stroke-width="12"
                  fill="transparent"
                  r="60"
                  cx="70"
                  cy="70"
                />
                <circle
                  class="progress-ring__circle"
                  stroke="#7c3aed"
                  stroke-width="12"
                  fill="transparent"
                  r="60"
                  cx="70"
                  cy="70"
                  :style="circleStyle"
                />
              </svg>
              <div class="circle-label">
                {{ Math.round(animatedScore) }}%
              </div>
            </div>

            <!-- Step-by-step Guide -->
            <div class="card result-card">
              <p><strong>Step-by-Step Guide</strong></p>
              <ul class="guide">
                <li class="ok">✅ Stop contact. Don’t click links or pay.</li>
                <li class="ok">✅ Take screenshots and save sender details.</li>
                <li class="ok">✅ If you shared bank details: contact your bank immediately.</li>
                <li class="ok">✅ Change passwords and enable MFA.</li>
                <li class="bad">❌ Don’t trust the link inside the message.</li>
                <li class="ok">✅ Submit to ScamWatch to help authorities track trends.</li>
              </ul>
            </div>
          </div>

          <!-- Bottom section: Rules -->
          <div class="card result-card full">
            <p><strong>Triggered Patterns:</strong></p>
            <ul class="list-disc pl-5">
              <li v-for="(r, i) in result.reasons" :key="i">{{ r }}</li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// Vue 3 composition API
import { ref, computed } from "vue"
import { detectScam } from "@/services/scambot"

// States
const userInput = ref("")
const loading = ref(false)
const error = ref("")
const result = ref(null)

// Confidence score animation
const animatedScore = ref(0) // This animates from 0 to real score
let scoreInterval = null

// Analyze function: call backend API
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

// Animate confidence score with smooth increase
function startScoreAnimation(target) {
  clearInterval(scoreInterval)
  animatedScore.value = 0
  scoreInterval = setInterval(() => {
    if (animatedScore.value < target) {
      animatedScore.value += 1
    } else {
      clearInterval(scoreInterval)
    }
  }, 15)
}

// Style for circular progress ring
const circleStyle = computed(() => {
  const radius = 60
  const circumference = 2 * Math.PI * radius
  const percent = animatedScore.value / 100
  const offset = circumference - percent * circumference
  return {
    strokeDasharray: `${circumference} ${circumference}`,
    strokeDashoffset: offset,
    transition: "stroke-dashoffset 0.3s linear"
  }
})

// Clipboard paste
async function pasteFromClipboard() {
  try {
    const txt = await navigator.clipboard.readText()
    if (txt) userInput.value = txt
  } catch (e) {
    console.warn("Clipboard not available", e)
  }
}

// File upload handler
function handleFile(e) {
  const file = e.target.files?.[0]
  if (file) {
    userInput.value += (userInput.value ? "\n\n" : "") + `[Uploaded file: ${file.name}]`
  }
}
</script>

<style scoped>
/* Page background */
.scambot-page {
  background: #f3e8ff;
  min-height: 100vh;
  padding: 20px;
  font-size: 1rem;
}

/* Header card */
.header-card {
  background: linear-gradient(135deg, #7c3aed, #9333ea);
  color: white;
  text-align: center;
  padding: 28px 16px;
  border-radius: 16px;
  margin-bottom: 24px;
}
.header-card h2 {
  font-size: 2rem;
  margin-bottom: 10px;
  font-family: "Poppins", "Nunito", "Segoe UI", sans-serif;
  font-weight: 700;
}
.header-card p {
  font-size: 1.1rem;
  line-height: 1.6;
  font-family: "Poppins", "Nunito", "Segoe UI", sans-serif;
}
@media (min-width: 768px) {
  .header-card h2 { font-size: 2.4rem; }
  .header-card p { font-size: 1.3rem; }
}

/* Wider grid */
.risk-grid {
  max-width: 1200px; /* was 800px */
  margin: 0 auto;
  display: grid;
  padding: 0 20px;
}

/* Card base */
.card {
  background: #ffffff;
  border-radius: 18px; /* rounder */
  padding: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
}
.doc-card { overflow: hidden; }

/* Toolbar */
.doc-toolbar {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 10px;
}

/* Textarea */
.doc-input {
  width: 100%;
  min-height: 200px;
  border: 0;
  outline: 0;
  resize: vertical;
  border-radius: 12px;
  background: #ffeef0;
  padding: 16px;
  font-size: 1rem;
  line-height: 1.6;
  color: #1f2937;
  font-family: "Poppins", "Nunito", "Segoe UI", sans-serif;
  box-sizing: border-box;
}

/* Actions */
.doc-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 12px;
}
.hidden { display: none; }

/* Buttons */
.btn {
  border: 0;
  border-radius: 12px;
  padding: 10px 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: "Poppins", "Nunito", "Segoe UI", sans-serif;
}
.btn.primary {
  background: linear-gradient(90deg, #7c3aed, #9333ea);
  color: #fff;
  box-shadow: 0 8px 18px rgba(124, 58, 237, .35);
}
.btn.primary:hover { filter: brightness(1.1); }
.btn.ghost {
  background: #e9d5ff;
  color: #5b21b6;
}
.btn.report {
  margin-top: 12px;
  background: linear-gradient(90deg, #10b981, #059669);
  color: white;
  padding: 10px 16px;
  border-radius: 12px;
}
.btn.report:hover { filter: brightness(1.1); }

/* Result panel */
.result-panel {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Result grid layout */
.result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 24px; /* more breathing space */
}
@media (max-width: 1000px) {
  .result-grid {
    grid-template-columns: 1fr;
  }
}
.result-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}
.result-card.center {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.result-card.full {
  grid-column: span 3;
}

/* Progress circle */
.progress-ring__circle {
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
  stroke-linecap: round; /* round edges */
}
.circle-label {
  position: absolute;
  margin-top: -90px;
  font-size: 1.6rem;
  font-weight: 700;
  color: #4c1d95;
  font-family: "Poppins", "Nunito", "Segoe UI", sans-serif;
}
/* Make result cards have light blue background */
.result-card {
  background: #f0f9ff; /* very light blue */
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

/* Progress circle thicker stroke */
.progress-ring__circle {
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
  stroke-linecap: round;
  stroke-width: 18; /* was 12 */
}
.progress-ring__background {
  stroke-width: 18; /* match thickness */
}
/* Make result card text bigger */
.result-card p,
.result-card li {
  font-size: 1.05rem; /* slightly larger */
  color: #111827;     /* ensure text stays dark blackish */
}

/* Make strong titles (like Verdict:, Detected Category:) stand out */
.result-card strong {
  font-size: 1.15rem;
  font-weight: 700;
  color: #111827;
}

/* Step-by-step guide */
.guide {
  font-size: 1.05rem;
  line-height: 1.7;
}

/* Confidence Score title bigger */
.result-card.center p {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 10px;
}
.circle-label {
  font-size: 1.8rem; /* bigger percentage */
  font-weight: 800;
}

/* Tags */
.tag {
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  font-family: "Poppins", "Nunito", "Segoe UI", sans-serif;
}
.tag.danger { background: #fee2e2; color: #b91c1c; }
.tag.safe { background: #dcfce7; color: #166534; }
.tag.info { background: #dbeafe; color: #1e40af; }

/* Guide */
.guide {
  margin-top: 10px;
  font-size: 0.95rem;
  line-height: 1.6;
  font-family: "Poppins", "Nunito", "Segoe UI", sans-serif;
}
.guide .ok { color: #065f46; }
.guide .bad { color: #991b1b; }

</style>
