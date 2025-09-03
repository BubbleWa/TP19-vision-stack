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

  font-size: 1.1rem; /* NEW: make all text slightly bigger */
}

.wrap {
  max-width: 1240px;
  margin: 0 auto;
}

.state-btn {
  padding: 14px 22px;             /* bigger size */
  border-radius: 24px;            /* more rounded */
  font-size: 1.1rem;              /* bigger text */
  font-weight: bold;
  border: none;
  cursor: pointer;

  /* gradient background */
  background: linear-gradient(135deg, #60a5fa, #3b82f6); 
  color: #fff;

  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s, background 0.3s;
}

/* hover effect */
.state-btn:hover {
  background: linear-gradient(135deg, #93c5fd, #2563eb);
  transform: scale(1.05);        /* small zoom on hover */
}

/* active (selected) */
.state-btn.active {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: scale(1.08);
}


/* Breaking news */
.breaking-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin: 10px 0 18px;
}
.breaking-row span {
  background: #ef4444;
  padding: 8px 14px; /* slightly bigger for readability */
  border-radius: 6px;
  font-weight: bold;
  font-size: 1.05rem; /* NEW */
  box-shadow: 0 4px 10px rgba(0,0,0,.2);
}

/* Filter row */
.filter-row {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin: 20px 0;
}
.filter-select {
  padding: 10px 16px; /* bigger */
  border-radius: 8px;
  border: none;
  background: #3b82f6;
  color: white;
  font-size: 1.05rem; /* NEW */
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0,0,0,.2);
}
.filter-select option {
  color: black;
}

/* Dashboard cards */
.dashboard-cards {
  display: grid;
  grid-template-columns: 1fr 1.3fr 1fr;
  gap: 20px;
}
.kpi-card, .likelihood-card, .top-scams-card {
  background: #60a5fa; /* lighter blue */
  border-radius: 14px;
  padding: 24px; /* slightly bigger padding */
  box-shadow: 0 8px 16px rgba(0,0,0,.25);
  text-align: center;
  font-size: 1.1rem; /* NEW */
}

.kpi-card i {
  font-size: 34px; /* bigger icon */
  margin-bottom: 8px;
}
.kpi-number {
  font-size: 2.2rem; /* bigger number */
  font-weight: bold;
  margin-top: 8px;
}
.people-row {
  display: flex;
  justify-content: center;
  gap: 6px;
  font-size: 22px; /* bigger people icons */
  margin: 14px 0;
}
.person { opacity: 0.3; }
.person.active { opacity: 1; }

/* Top scams */
.top-scams-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
  font-size: 1.05rem; /* NEW: make list text bigger */
}
.top-scams-card li {
  margin: 14px 0;
}
</style>

