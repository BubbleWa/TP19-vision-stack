<template>
  <div class="dashboard-page">
    <div class="wrap">

      <!-- ===== State selector ===== -->
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

      <!-- ===== Breaking news ticker ===== -->
      <section class="breaking-row" v-if="breakingNews.length">
        <span v-for="n in breakingNews" :key="n.contact_method">
          <span class="scroll-text">
            {{ n.contact_method }}: {{ n.pct_change }}% ({{ n.window_years[4] }} → {{ n.window_years[0] }})
          </span>
        </span>
      </section>

      <!-- ===== Filters row ===== -->
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

      <!-- ===== Dashboard cards ===== -->
      <section class="dashboard-cards">
        <!-- Card 1 -->
        <div class="card-block" style="background-image: url('/db1.png');"></div>

        <!-- Card 2 -->
        <div class="card-block" style="background-image: url('/db2.png');"></div>

                <!-- Card 3: KPI card -->
        <div class="card-block left-align" style="background-image: url('/db3.png');">
          <h4>Total Losses</h4>
          <p class="kpi-number">${{ kpiTotalLosses.toLocaleString() }}</p>
          <h4>Reported Scams</h4>
          <p class="kpi-number">{{ kpiReportedScams.toLocaleString() }}</p>
        </div>

        <!-- Card 4 -->
        <div class="card-block center-text" style="background-image: url('/db4.png');">
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

        <!-- Card 5 -->
        <div class="card-block center-text" style="background-image: url('/db5.png');">
          <h3>💸 Real-time Scam Losses</h3>
          <p class="kpi-number">{{ counterDisplay }}</p>
          <p style="opacity:.85; margin-top:8px;">
            Updating at ~${{ ratePerMinute.toLocaleString() }} per minute
          </p>
        </div>

        <!-- Card 6 -->
        <div class="card-block center-text top-scams-card" style="background-image: url('/db6.png');">
          <h3>Top Scams by Loss (2025)</h3>
          <ul>
            <li v-for="item in topScams" :key="item.category + item.contact_method">
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

// Chart.js setup
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import { Doughnut } from "vue-chartjs";
ChartJS.register(Title, Tooltip, Legend, ArcElement);

/* ---------- Filter states ---------- */
const states = ref<string[]>([]);
const scamTypes = ref<string[]>([]);
const years = ref<number[]>([]);

const selectedState = ref<string>("");
const selectedScamType = ref<string | null>(null);
const selectedYear = ref<number | null>(null);

/* ---------- KPI values ---------- */
const kpiTotalLosses = ref(0);
const kpiReportedScams = ref(0);
const donutPercent = ref(0);
const peopleOutOf10 = ref(0);
const topScams = ref<any[]>([]);
const breakingNews = ref<any[]>([]);

/* ---------- Live counter state ---------- */
const counterRunning = ref(0);
const ratePerMinute = ref(0);
const ratePerSecond = computed(() => ratePerMinute.value / 60);
let counterTimer: number | null = null;

/** Start or restart the live counter */
function startCounter() {
  if (counterTimer) {
    clearInterval(counterTimer);
    counterTimer = null;
  }

  // Restore saved value if available
  const saved = localStorage.getItem("scamCounterRunning");
  if (saved) counterRunning.value = parseFloat(saved) || 0;

  // Increment every second
  counterTimer = window.setInterval(() => {
    counterRunning.value += ratePerSecond.value;
    localStorage.setItem("scamCounterRunning", String(counterRunning.value));
  }, 1000);
}

// Display formatted counter value
const counterDisplay = computed(() =>
  `$${counterRunning.value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`
);

/* ---------- API loaders ---------- */
async function loadFilters() {
  const f: FiltersResponse = await getFilters();

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

  ratePerMinute.value = stats?.loss_per_minute_2025_4mo?.rate_per_minute ?? 0;
  startCounter();
}

function selectState(s: string) {
  selectedState.value = s;
  loadStats();
}

/* ---------- Donut chart config ---------- */
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

/* ---------- Lifecycle hooks ---------- */
onMounted(loadFilters);
onUnmounted(() => {
  if (counterTimer) clearInterval(counterTimer);
});
</script>


<style scoped>
/* ================= Dashboard wrapper ================= */
.dashboard-page {
  min-height: 100vh;
  background: #C8E6C9;  
  padding: 24px 14px;
  color: white;
  font-family: "Segoe UI", sans-serif;
  font-size: 1.1rem;
}
.wrap {
  max-width: 1240px;
  margin: 0 auto;
}

/* ================= KPI Card with background image ================= */
.kpi-card.total-losses {
  background: url("/db3.png") no-repeat center center;
  background-size: cover;
  color: white; /* Ensure text is visible */
}

/* ================= State selector (buttons) ================= */
.state-selector {
  display: flex;
  flex-wrap: wrap;
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
  min-width: 120px;
  text-align: center;
  background: linear-gradient(135deg, #13678A); 
  color: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s, background 0.3s;
}
.state-btn:hover {
  background: linear-gradient(135deg, #2563eb);
  transform: scale(1.05);        
}
.state-btn.active {
  background: linear-gradient(135deg, #45C4B0, #1e40af);
  transform: scale(1.08);
}

/* ================= Breaking news row (ticker) ================= */
.breaking-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin: 10px 0 18px;
}
.breaking-row span {
  display: inline-block;
  position: relative;
  overflow: hidden;
  width: 220px;
  height: 30px;
  line-height: 30px;
  background: #13678A;
  border-radius: 6px;
  padding: 0 10px;
  font-weight: bold;
  font-size: 1.05rem;
  box-shadow: 0 4px 10px rgba(0,0,0,.2);
  color: white;
  white-space: nowrap;
}
.breaking-row span .scroll-text {
  display: inline-block;
  padding-left: 40%;         
  animation: marquee 7s linear infinite;
}
@keyframes marquee {
  0%   { transform: translateX(0%); }
  100% { transform: translateX(-100%); }
}

/* ================= Filter row (dropdowns) ================= */
.filter-select {
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  background: #13678A;
  color: white;
  font-size: 1.05rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0,0,0,.2);

  /* Fix for cutting issue */
  min-width: fit-content;   /* allow auto expand */
  max-width: 100%;          /* prevent overflow */
  white-space: nowrap;      /* keep text in one line */
  overflow: visible;        /* show full text */
}
.filter-row {
  display: flex;
  justify-content: center;
  gap: 30px;   /* horizontal gap */
  margin: 40px 0; /* vertical spacing */
}
.filter-select option {
  color: black;
}

/* ================= Dashboard cards layout ================= */
.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* Card1 & Card2 specific: keep aspect ratio 16:9 */
.card-block {
  background-size: contain;     /* keep scale ratio */
  background-repeat: no-repeat; /* no repeat */
  background-position: center;  /* centered */
  aspect-ratio: 16 / 9;         /* fixed ratio */
}

/* ================= Left aligned content inside card ================= */
.left-align {
  align-items: flex-start;  
  text-align: left;         
  padding-left: 30px;       
}

/* ================= Dashboard cards layout ================= */
.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}


.card-block {
  background-size: cover;
  background-position: center;
  box-shadow: 0 8px 16px rgba(0,0,0,.25);
  color: black;

  
  min-height: 18em;   
  padding: 2em;
  
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;

  font-size: clamp(0.9rem, 1.2vw, 1.2rem);
}


.card-block h3,
.card-block h4,
.card-block p,
.card-block ul,
.card-block li {
  font-size: 1.2em;     
  line-height: 1.4;
  margin: 0.5em 0;
  max-width: 100%;
  word-wrap: break-word;
  overflow-wrap: anywhere;
}


.kpi-number {
  font-size: 3em;  
  font-weight: bold;
  margin-top: 0.5em;
  line-height: 1.3;
}

/* ================= People row (likelihood card) ================= */
.people-row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 4px;
  font-size: clamp(14px, 4vw, 22px);
  margin: 14px 0;
}
.person { opacity: 0.3; }
.person.active { opacity: 1; }


/* ================= Fix for Top Scams Card ================= */
.top-scams-card {
  text-align: left;             /* Left align text for readability */
  padding: 16px;
  max-width: 100%;              /* Prevent overflow */
  word-wrap: break-word;        /* Break long words */
  overflow-wrap: anywhere;      /* Ensure wrapping */
}

.top-scams-card h3 {
  font-size: clamp(0.8rem, 1.5vw, 1.4rem);  /* Responsive heading */
  margin-bottom: 4px;
  text-align: center;            /* Keep title centered */
}

.top-scams-card ul {
  font-size: clamp(0.7rem, 1vw, 1rem);   /* Responsive list text */
  line-height: 1.5;
  padding-left: 18px;            /* Proper bullet spacing */
  margin: 0;
  max-width: 100%;               /* Force text to stay inside */
}

.top-scams-card li {
  margin-bottom: 10px;
  word-break: break-word;        /* Break inside list items */
}
.card-block.left-align {
  align-items: flex-start;   
  text-align: left;          
  padding-left: 20px;        
}

/* ================= Responsive adjustments ================= */
@media (max-width: 1024px) {
  .wrap { padding: 0 16px; }
  .dashboard-cards { grid-template-columns: 1fr 1fr; }
  .image-card p, .stat-card p { font-size: 0.9rem; }
}
@media (max-width: 768px) {
  .filter-row { flex-direction: column; gap: 12px; }
  .filter-select { width: 100%; }
  .image-card p, .stat-card p { font-size: 0.85rem; }
}
@media (max-width: 640px) {
  .dashboard-cards { grid-template-columns: 1fr; }
  .breaking-row { flex-direction: column; align-items: center; }
  .breaking-row span { width: 100%; text-align: center; }
  .kpi-card, .likelihood-card, .top-scams-card {
    width: 100%;
    box-sizing: border-box;
  }
}

/* ================= Global overflow fix ================= */
html, body, .dashboard-page, .wrap {
  max-width: 100%;
  overflow-x: hidden; /* prevent horizontal scroll */
}
.dashboard-cards > * {
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}

/* ================= Breaking news pill width override ================= */
.breaking-row span {
  width: 360px;              
  padding: 0 14px;           
}
.breaking-row span.wide,
.breaking-row span:last-child {
  width: 320px;              
}
@media (max-width: 1024px) {
  .breaking-row span,
  .breaking-row span.wide {
    width: 300px;            
  }
}
@media (max-width: 640px) {
  .breaking-row {
    flex-direction: column;  
    align-items: center;
  }
  .breaking-row span,
  .breaking-row span.wide {
    width: 100%;             
  }
}

</style>
