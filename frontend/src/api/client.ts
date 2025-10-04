// src/api/client.ts
import http from "./http";

// getFilters API
export async function getFilters() {
  const res = await http.get("/filters");
  return res.data;
}

// getStats API
export async function getStats(params: { state: string; scam_type: string; year?: number }) {
  const res = await http.get("/stats", { params });
  return res.data;
}
