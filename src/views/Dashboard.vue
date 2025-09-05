<template>
  <div class="dashboard-page">
    <div class="wrap">
      <!-- State selector -->
      <section class="state-selector">
        <button
          v-for="s in states"
          :key="s"
          class="state-btn"
          :class="{ active: s === selectedState }"
          @click="selectState(s)"
        >
          {{ s }}
        </button>
      </section>

      <!-- Breaking news -->
      <section class="breaking-row" v-if="breakingNews.length">
        <span v-for="n in breakingNews" :key="n.contact_method">
          {{ n.contact_method }}: {{ n.pct_change }}% ({{ n.window_years[4] }} → {{ n.window_years[0] }})
        </span>
      </section>

      <!-- Filter row -->
      <section class="filter-row">
        <select v-model="selectedScamType" @change="loadStats" class="filter-select">
          <option :value="null">All Scam Types</option>
          <option v-for="t in scamTypes" :key="t" :value="t">{{ t }}</option>
        </select>

        <select v-model="selectedYear" @change="loadStats" class="filter-select">
          <option :value="null">Last 5 years</option>
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>
      </section>

      <!-- Dashboard cards -->
      <section class="dashboard-cards">
        <!-- KPIs -->
        <div class="kpi-card">
          <i class="fas fa-money-bill-wave"></i>
          <h4>Total Losses</h4>
          <p class="kpi-number">${{ kpiTotalLosses.toLocaleString() }}</p>
        </div>
        <div class="kpi-card">
          <i class="fas fa-exclamation-triangle"></i>
          <h4>Reported Scams</h4>
          <p class="kpi-number">{{ kpiReportedScams.toLocaleString() }}</p>
        </div>

      <!-- Likelihood -->
      <div class="likelihood-card">
        <!-- Removed Doughnut chart -->
        
        <div class="people-row">
          <span
            v-for="n in 10"
            :key="n"
            class="person"
            :class="{ active: n <= peopleOutOf10 }"
          >👤</span>
        </div>
        <p>{{ peopleOutOf10 }} out of 10 faced financial loss</p>
      </div>

      <!-- Likelihood -->
      <div class="likelihood-card">
        <h3>💸 Real-time Scam Losses</h3>
        <p class="kpi-number">{{ counterDisplay }}</p>
        <p style="opacity:.85; margin-top:8px;">
          Updating at ~${{ ratePerMinute.toLocaleString() }} per minute
        </p>
      </div>

        <!-- Top scams -->
        <div class="top-scams-card">
          <h3>Top Scams by Loss (2025)</h3>
          <ul>
            <li v-for="item in topScams" :key="item.category + item.contact_method">
              <i class="fas fa-shield-alt"></i>
              {{ item.category }} — {{ item.scam_type }} ({{ item.contact_method }})
              <br />
              Losses: ${{ item.losses.toLocaleString() }}
            </li>
          </ul>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue";
import { getFilters, getStats } from "@/api/client";
import type { FiltersResponse } from "@/api/types";

// Chart.js
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import { Doughnut } from "vue-chartjs";
ChartJS.register(Title, Tooltip, Legend, ArcElement);

// Filters
const states = ref<string[]>([]);
const scamTypes = ref<string[]>([]);
const years = ref<number[]>([]);

const selectedState = ref<string>("");
const selectedScamType = ref<string | null>(null);
const selectedYear = ref<number | null>(null);

const kpiTotalLosses = ref(0);
const kpiReportedScams = ref(0);
const donutPercent = ref(0);
const peopleOutOf10 = ref(0);
const topScams = ref<any[]>([]);
const breakingNews = ref<any[]>([]);

/* ---------- NEW: Live counter state & helpers (English comments) ---------- */
// Current accumulated amount shown in the counter
const counterRunning = ref(0);

// Rate retrieved from API in AUD per minute
const ratePerMinute = ref(0);

// Convert per-minute rate into per-second
const ratePerSecond = computed(() => ratePerMinute.value / 60);

// Interval id so we can clear it when reloading or unmounting
let counterTimer: number | null = null;

/**
 * Start (or restart) the live counter.
 * Increments the displayed amount every second according to ratePerSecond.
 * Persists the current value in localStorage so it can resume on reload.
 */
function startCounter() {
  // Clear existing interval if already running
  if (counterTimer) {
    clearInterval(counterTimer);
    counterTimer = null;
  }

  // Optional: restore previous value from localStorage
  const saved = localStorage.getItem("scamCounterRunning");
  if (saved) counterRunning.value = parseFloat(saved) || 0;

  // Start incrementing every second
  counterTimer = window.setInterval(() => {
    counterRunning.value += ratePerSecond.value;
    // Optional: persist value
    localStorage.setItem("scamCounterRunning", String(counterRunning.value));
  }, 1000);
}

// Formatted display string with 2 decimals and locale separators
const counterDisplay = computed(() =>
  `$${counterRunning.value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`
);
/* ------------------------------------------------------------------------- */

async function loadFilters() {
  const f: FiltersResponse = await getFilters();

  // 去掉 "Outside of Australia" 和 "Unspecified"
  states.value = f.states.filter(
    s => s !== "Outside of Australia" && s !== "Unspecified"
  );
  scamTypes.value = f.scam_types;
  years.value = f.years.list;

  selectedState.value = states.value[0];
  selectedScamType.value = null;
  selectedYear.value = null;

  await loadStats();
}

async function loadStats() {
  const stats = await getStats({
    state: selectedState.value,
    scam_type: selectedScamType.value || undefined,
    year: selectedYear.value || undefined,
  });

  kpiTotalLosses.value = stats.kpis?.total_losses ?? 0;
  kpiReportedScams.value = stats.kpis?.reports ?? 0;
  donutPercent.value = stats.likelihood?.likelihood_scammed_pct ?? 0;
  peopleOutOf10.value = stats.likelihood?.likelihood_loss_per_10 ?? 0;
  topScams.value = stats.top3_by_loss ?? [];
  breakingNews.value = stats.breaking_news ?? [];

  /* --- NEW: wire the rate for the live counter and start it --- */
  // Expecting stats.loss_per_minute_2025_4mo.rate_per_minute (AUD/min)
  ratePerMinute.value = stats?.loss_per_minute_2025_4mo?.rate_per_minute ?? 0;
  startCounter();
}

function selectState(s: string) {
  selectedState.value = s;
  loadStats();
}

const donutChartData = computed(() => ({
  labels: ["Scammed", "Safe"],
  datasets: [
    {
      data: [donutPercent.value, 100 - donutPercent.value],
      backgroundColor: ["#10b981", "#374151"],
      borderWidth: 0,
    },
  ],
}));
const donutOptions = {
  responsive: true,
  plugins: { legend: { display: false } },
  cutout: "70%",
};

onMounted(loadFilters);

// Ensure we clean the interval on component unmount
onUnmounted(() => {
  if (counterTimer) clearInterval(counterTimer);
});
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: linear-gradient(to bottom right, #f3e8ff, #ede9fe);
  padding: 24px 12px;
  color: white;
  font-family: "Segoe UI", sans-serif;
  font-size: 1.1rem; /* make all text slightly bigger */
}

.wrap {
  max-width: 1240px;
  margin: 0 auto;
}

/* ---------- State buttons ---------- */
.state-selector {
  display: flex;
  flex-wrap: wrap;            /* allow wrapping on small screens */
  justify-content: center;
  gap: 10px;
  margin-bottom: 16px;
}
.state-btn {
  padding: 14px 22px;         
  border-radius: 24px;        
  font-size: 1.1rem;          
  font-weight: bold;
  border: none;
  cursor: pointer;
  min-width: 120px;           /* prevent being too narrow */
  text-align: center;

  background: linear-gradient(135deg, #60a5fa, #3b82f6); 
  color: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s, background 0.3s;
}
.state-btn:hover {
  background: linear-gradient(135deg, #93c5fd, #2563eb);
  transform: scale(1.05);        
}
.state-btn.active {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: scale(1.08);
}

/* ---------- Breaking news ---------- */
.breaking-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin: 10px 0 18px;
}
.breaking-row span {
  background: #ef4444;
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: bold;
  font-size: 1.05rem;
  box-shadow: 0 4px 10px rgba(0,0,0,.2);
}

/* ---------- Filters row ---------- */
.filter-row {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin: 20px 0;
}
.filter-select {
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  background: #3b82f6;
  color: white;
  font-size: 1.05rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0,0,0,.2);
}
.filter-select option {
  color: black;
}

/* ---------- Dashboard cards ---------- */
.dashboard-cards {
  display: grid;
  grid-template-columns: 1fr 1.3fr 1fr; /* default 3-column */
  gap: 20px;
}
.kpi-card, .likelihood-card, .top-scams-card {
  background: #60a5fa;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 8px 16px rgba(0,0,0,.25);
  text-align: center;
  font-size: 1.1rem;
}
.kpi-card i {
  font-size: 34px;
  margin-bottom: 8px;
}
.kpi-number {
  font-size: 2.2rem;
  font-weight: bold;
  margin-top: 8px;
}
.people-row {
  display: flex;
  justify-content: center;
  gap: 6px;
  font-size: 22px;
  margin: 14px 0;
}
.person { opacity: 0.3; }
.person.active { opacity: 1; }

/* ---------- Top scams ---------- */
.top-scams-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
  font-size: 1.05rem;
}
.top-scams-card li {
  margin: 14px 0;
}

/* ========== Responsive Layout ========== */

/* Reduce padding for wrap on medium screens */
@media (max-width: 1024px) {
  .wrap {
    padding: 0 16px;
  }
}

/* Filters stack vertically on tablets/phones */
@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  .filter-select {
    width: 100%;
  }
}

/* Dashboard grid: 2 columns on tablets */
@media (max-width: 1024px) {
  .dashboard-cards {
    grid-template-columns: 1fr 1fr;
  }
}

/* Dashboard grid: 1 column on phones */
@media (max-width: 640px) {
  .dashboard-cards {
    grid-template-columns: 1fr;
  }
  .kpi-card, .likelihood-card, .top-scams-card {
    text-align: center;
  }
}

/* Breaking news stack vertically on phones */
@media (max-width: 640px) {
  .breaking-row {
    flex-direction: column;
    align-items: center;
  }
  .breaking-row span {
    width: 100%;
    text-align: center;
  }
}
/* Prevent horizontal overflow on small screens */
@media (max-width: 640px) {
  .dashboard-cards {
    grid-template-columns: 1fr;   /* ensure single column */
  }

  .kpi-card, .likelihood-card, .top-scams-card {
    width: 100%;                  /* force full width */
    box-sizing: border-box;       /* include padding */
    word-wrap: break-word;        /* allow wrapping long text */
    overflow-wrap: break-word;
  }

  /* Adjust KPI numbers to shrink on small screens */
  .kpi-number {
    font-size: 1.6rem;            /* smaller font for long numbers */
    line-height: 1.2;
    word-break: break-word;
  }

  /* Ensure dropdowns also fit screen width */
  .filter-select {
    max-width: 100%;
  }
}
/* ===== Fix card overflow on small screens ===== */

/* 1) Never allow horizontal scrolling on the page */
html, body, .dashboard-page, .wrap {
  max-width: 100%;
  overflow-x: hidden;
}

/* 2) Let grid children shrink inside the grid (very important for mobile) */
.dashboard-cards > * {
  min-width: 0;                /* allow shrinking */
  width: 100%;                 /* take full column width */
  box-sizing: border-box;      /* include padding in width */
  overflow-wrap: anywhere;     /* break long strings/numbers if needed */
  word-break: break-word;
}

/* 3) Scale big numbers responsively so they don't push the card wider */
.kpi-number {
  /* min 1.25rem, prefers 6vw on mobile, caps at your previous 2.2rem */
  font-size: clamp(1.25rem, 6vw, 2.2rem);
  line-height: 1.2;
}

/* 4) Ensure long paragraphs/titles wrap instead of stretching the card */
.likelihood-card p,
.top-scams-card h3,
.top-scams-card li {
  overflow-wrap: anywhere;
  word-break: break-word;
}

/* 5) Controls should never exceed viewport width */
.state-btn,
.filter-select {
  max-width: 100%;
}

/* 6) On phones keep a strict single column and remove any hidden gaps */
@media (max-width: 640px) {
  .dashboard-cards {
    grid-template-columns: 1fr !important;  /* enforce single column */
    margin-right: 0;
  }
}
/* Fix the "people row" on small screens */
.people-row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;      /* allow wrapping on narrow screens */
  gap: 4px;
  font-size: clamp(14px, 4vw, 22px); /* responsive size: min 14px, max 22px */
  margin: 14px 0;
}

.person {
  flex: 0 1 auto;       /* allow shrinking */
  opacity: 0.3;
}
.person.active {
  opacity: 1;
}

</style>


