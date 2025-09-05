<template>
  <div class="risk-page">
    <!-- Page title -->
    <section class="risk-header">
      <h2>Risk Score Measure coming soon.....</h2>
      <p>
        CyberMate’s Risk Score helps you understand your personal exposure.  
        Based on your online activity and scam history, get a score that shows your digital risk level.
      </p>
    </section>

    <!-- Risk meter card -->
    <section class="risk-card">
      <img src="/risk-meter.png" alt="Risk Meter" class="risk-image" />
      <div class="risk-info">
        <h3>Your Risk Score</h3>
        <p>This is a placeholder — will be powered by API later.</p>
        <button class="risk-btn">Measure Now</button>
      </div>
    </section>
  </div>
</template>

<script setup>
// API integration will be added later
</script>

<style scoped>
/* Page background */
.risk-page {
  background: #f3e8ff;   /* Light purple background */
  min-height: 100vh;
  padding: 100px 20px 20px; /* Top 100px to avoid overlapping the navbar */
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* ===== Title section ===== */
.risk-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 0 10px;
}
.risk-header h2 {
  font-size: 2.8rem;
  font-weight: bold;
  color: #4c1d95;
  margin-bottom: 14px;
}
.risk-header p {
  font-size: 1.4rem;
  max-width: 700px;
  margin: 0 auto;
  color: #333;
  line-height: 1.8;
}

/* ===== Risk card ===== */
.risk-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  background: white;
  padding: 40px 30px;
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  box-shadow: 0 6px 16px rgba(0,0,0,0.1);
  text-align: center;
}
.risk-image {
  width: 220px;
  height: auto;
}
.risk-info h3 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 16px;
}
.risk-info p {
  font-size: 1.3rem;
  margin-bottom: 24px;
  color: #555;
}
.risk-btn {
  background: #facc15;
  padding: 14px 28px;
  border-radius: 10px;
  font-size: 1.4rem;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}
.risk-btn:hover {
  background: #eab308;
  transform: translateY(-2px);
}

/* ===== Responsive layout (side-by-side on large screens) ===== */
@media (min-width: 768px) {
  .risk-card {
    flex-direction: row;
    text-align: left;
    justify-content: center;
  }
  .risk-info {
    flex: 1;
  }
}
</style>
