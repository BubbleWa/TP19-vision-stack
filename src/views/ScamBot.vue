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
          <input id="fileInput" type="file" class="hidden" accept="image/*,text/plain" @change="handleFile">
          <button class="btn primary" @click="analyze">Detect</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"

const userInput = ref("") // User input text
const score = ref(0)      // Risk score (0–100)

// Simple analyze function
function analyze() {
  const text = userInput.value.toLowerCase()
  let s = 0
  if (/urgent|password|bank|link|click/.test(text)) s += 20
  score.value = Math.min(100, s)
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
</style>
