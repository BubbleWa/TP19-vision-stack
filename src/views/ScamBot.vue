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

    <!-- Layout: now only the left document card -->
    <div class="risk-grid">
      <section class="card doc-card">
        <!-- Toolbar with title + paste -->
        <div class="doc-toolbar">
          <h3>Untitled document</h3>
          <button class="btn ghost" @click="pasteFromClipboard">Paste text</button>
        </div>

        <!-- Input textarea -->
        <textarea
          v-model="userInput"
          class="doc-input"
          placeholder="Paste or type the message here..."
        ></textarea>

        <!-- Actions -->
        <div class="doc-actions">
          <label class="btn light" for="fileInput">Upload screenshot</label>
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

        <!-- Result -->
        <div v-if="error" class="result text-red-600">
          {{ error }}
        </div>

        <div v-if="result" class="result">
          <p><strong>Verdict:</strong> {{ result.verdict }}</p>
          <p><strong>ML Score:</strong> {{ (result.score_ml ?? 0).toFixed(3) }}</p>
          <p><strong>Rules Score:</strong> {{ result.score_rules ?? 0 }}</p>
          <p><strong>Confidence:</strong> {{ Math.round((result.score_ml ?? 0) * 100) }}%</p>

          <div v-if="result.reasons?.length">
            <p><strong>Reasons:</strong></p>
            <ul class="list-disc pl-5">
              <li v-for="(r, i) in result.reasons" :key="i">{{ r }}</li>
            </ul>
          </div>

          <div v-if="result.highlights?.length">
            <p><strong>Flags:</strong></p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(h, i) in result.highlights"
                :key="i"
                class="px-2 py-1 rounded text-xs bg-indigo-100 text-indigo-700"
              >
                {{ h.type }}
              </span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { detectScam } from "@/services/scambot" // ✅ 新增：调用封装的 API

const userInput = ref("")     // User input text
const loading = ref(false)    // Loading state
const error = ref("")         // Error message
const result = ref(null)      // Backend result

/**
 * Analyze function:
 * - Call backend API via detectScam
 * - Show error if fails
 */
async function analyze() {
  error.value = ""
  result.value = null

  if (!userInput.value.trim()) return

  loading.value = true
  try {
    result.value = await detectScam(userInput.value.trim())
  } catch (e) {
    error.value = e.message || "Something went wrong."
  } finally {
    loading.value = false
  }
}

// Paste text from clipboard
async function pasteFromClipboard() {
  try {
    const txt = await navigator.clipboard.readText()
    if (txt) userInput.value = txt
  } catch (e) {
    console.warn("Clipboard not available", e)
  }
}

// Handle file upload
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

/* Purple header */
.header-card {
  background: #7c3aed;
  color: white;
  text-align: center;
  padding: 24px 16px;
  border-radius: 12px;
  margin-bottom: 20px;
}
.header-card h2 { font-size: 1.8rem; margin-bottom: 10px; }
.header-card p  { font-size: 1rem; line-height: 1.6; }
@media (min-width: 768px) {
  .header-card h2 { font-size: 2.4rem; }
  .header-card p  { font-size: 1.3rem; }
}

/* Grid: now only 1 column */
.risk-grid {
  max-width: 800px;
  margin: 0 auto;
  display: grid;
}

/* Card */
.card {
  background: #ffffff;
  border-radius: 14px;
  padding: 18px;
  box-shadow: 0 12px 28px rgba(17, 24, 39, .12);
}
.doc-card { overflow: hidden; }

/* Toolbar */
.doc-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.doc-toolbar h3 { margin: 0; font-size: 1.1rem; color: #111827; }

/* Textarea */
.doc-input {
  width: 100%;
  min-height: 260px;
  border: 0;
  outline: 0;
  resize: vertical;
  border-radius: 10px;
  background: #ffeef0;
  padding: 16px;
  font-size: 1rem;
  line-height: 1.6;
  color: #1f2937;
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
  border-radius: 10px;
  padding: 10px 14px;
  font-weight: 700;
  cursor: pointer;
}
.btn.primary {
  background: #7c3aed;
  color: #fff;
  box-shadow: 0 8px 18px rgba(124, 58, 237, .35);
}
.btn.primary:hover { filter: brightness(1.05); }
.btn.light { background: #f3f4f6; color: #374151; }
.btn.ghost { background: #e9d5ff; color: #5b21b6; }

/* Result */
.result {
  margin-top: 16px;
  padding: 12px;
  border-radius: 10px;
  background: #f9fafb;
  color: #111827;
  font-weight: 600;
}
</style>
