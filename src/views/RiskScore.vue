<template>
  <div class="risk-page">
    <!-- ===== Page title ===== -->
    <section class="risk-header">
      <h2>Risk Score</h2>
      <p>
        Paste or type in your draft text below to check for potentially risky language.  
        We'll highlight any terms to watch for and provide an overall risk assessment.
      </p>
    </section>

    <!-- ===== Input box ===== -->
    <section class="risk-input">
      <label for="textInput" class="input-label">Paste text</label>
      <textarea
        id="textInput"
        v-model="userText"
        placeholder="Paste or type your text here..."
        class="risk-textarea"
      ></textarea>

      <!-- Row with State selector + Button -->
      <div class="action-row">
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

        <button class="check-btn" @click="analyzeRisk">Check</button>
      </div>
    </section>

    <!-- ===== Loading state ===== -->
    <div v-if="loading" class="mt-4 text-lg">Analyzing...</div>

    <!-- ===== Error message ===== -->
    <div v-else-if="result?.errorMessage" class="mt-4 text-red-600">
      {{ result.errorMessage }}
    </div>

    <!-- ===== Risk result ===== -->
    <section v-else-if="result?.analysis?.analysis" class="risk-result">
      <h3>
        Risk Level:
        <span v-if="result.analysis.analysis.score"
              class="risk-badge"
              :class="result.analysis.analysis.score.toLowerCase()">
          {{ result.analysis.analysis.score }}
        </span>
      </h3>

      <!-- Labels -->
      <p v-if="result.analysis.analysis.labels?.length">
        <strong>Labels:</strong> {{ result.analysis.analysis.labels.join(", ") }}
      </p>

      <!-- Highlighted phrases -->
      <div v-if="result.analysis.analysis.highlights?.length">
        <h4>Highlighted Phrases:</h4>
        <ul>
          <li v-for="(h, i) in result.analysis.analysis.highlights" :key="i">
            "{{ h.phrase }}" → <em>{{ h.category }}</em>
          </li>
        </ul>
      </div>

      <!-- Educational tips -->
      <div v-if="result.analysis.analysis.tips?.length">
        <h4>Educational Tips:</h4>
        <ul>
          <li v-for="(t, i) in result.analysis.analysis.tips" :key="i">
            {{ t.tip }}
          </li>
        </ul>
      </div>

      <!-- Applicable laws -->
      <div v-if="result.analysis.analysis.laws?.length">
        <h4>Applicable Laws:</h4>
        <ul>
          <li v-for="(law, i) in result.analysis.analysis.laws" :key="i">
            <strong>{{ law.law_name }}</strong> ({{ law.state }})  
            <br />{{ law.law_desc }}
            <br /><a :href="law.law_url" target="_blank">Read more</a>
          </li>
        </ul>
      </div>

      <!-- Reporting authorities -->
      <div v-if="result.analysis.analysis.reporting?.length">
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
import { ref } from "vue"
import axios from "axios"

// User input text
const userText = ref("")
// Selected state
const state = ref("ALL")
// API response data
const result = ref(null)
// Loading state
const loading = ref(false)

// Function to analyze text using backend API
const analyzeRisk = async () => {
  if (!userText.value.trim()) {
    alert("Please enter some text to analyze.")
    return
  }

  loading.value = true
  result.value = null
  try {
    // Call backend Risk Detector API
    const response = await axios.post(
      "https://cybermate-production.up.railway.app/risk/risk_detect",
      {
        text: userText.value,
        state: state.value,
      },
      {
        headers: { "Content-Type": "application/json" },
      }
    )
    console.log("API response:", response.data) // Debug log
    result.value = response.data
  } catch (err) {
    console.error("Error calling Risk Detector:", err)
    result.value = { errorMessage: "Backend error, please try again." }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ===== Page layout ===== */
.risk-page {
  background: #f3e8ff;
  min-height: 100vh;
  padding: 100px 20px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 1.2rem;
}

/* ===== Header ===== */
.risk-header {
  text-align: center;
  margin-bottom: 40px;
}
.risk-header h2 {
  font-size: 3rem;
  font-weight: bold;
  color: #4c1d95;
  margin-bottom: 14px;
}
.risk-header p {
  font-size: 1.4rem;
  color: #333;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.8;
}

/* ===== Input section ===== */
.risk-input {
  background: #fff;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 1000px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.input-label {
  font-weight: bold;
  font-size: 1.4rem;
  color: #4c1d95;
}
.input-label.small {
  font-size: 1rem;
  margin-bottom: 6px;
}
.risk-textarea {
  width: 100%;
  min-height: 180px;
  border-radius: 10px;
  border: 1px solid #ccc;
  padding: 16px;
  font-size: 1.2rem;
  line-height: 1.8;
  resize: vertical;
}
.action-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 20px;
  margin-top: 10px;
}
.state-wrapper {
  display: flex;
  flex-direction: column;
  flex: 1;
}
.state-select {
  padding: 14px 20px;
  border-radius: 10px;
  border: 2px solid #6d28d9;
  font-size: 1.1rem;
  font-weight: 500;
  background: #f5f3ff; /* light purple */
  color: #4c1d95;
  transition: all 0.3s ease;
  cursor: pointer;
}
.state-select:hover {
  background: #ede9fe;
  border-color: #5b21b6;
}
.state-select:focus {
  outline: none;
  border-color: #4c1d95;
  box-shadow: 0 0 6px rgba(109, 40, 217, 0.5);
}
.check-btn {
  background: #6d28d9;
  color: white;
  padding: 14px 28px;
  border: none;
  border-radius: 10px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}
.check-btn:hover {
  background: #5b21b6;
  transform: translateY(-2px);
}

/* ===== Result box ===== */
.risk-result {
  margin-top: 30px;
  background: #fff;
  padding: 28px;
  border-radius: 14px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 1000px;
  text-align: left;
}
.risk-result h3 {
  font-size: 1.8rem;
  margin-bottom: 16px;
}
.risk-result p {
  font-size: 1.3rem;
  line-height: 1.8;
}
.risk-result span {
  margin-left: 10px;
  font-weight: bold;
}

/* Risk Level Badge */
.risk-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: bold;
  text-transform: uppercase;
}
.low {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #16a34a;
}
.high {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #dc2626;
}
.medium {
  background: #fef9c3;
  color: #854d0e;
  border: 1px solid #facc15;
}
</style>
