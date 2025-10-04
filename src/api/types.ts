// src/api/types.ts

// Response of /filters
export interface FiltersResponse {
  states: string[];
  scam_types: string[];
  years: number[];
}

// Response of /stats
export interface StatsResponse {
  kpis: {
    total_losses: number;
    reports: number;
    avg_loss: number;
  };
  series: any[]; // TODO: can refine once backend defines structure
  breakdown: any[];
  likelihood: {
    state_population_used: number | null;
    likelihood_scammed_pct: number | null;
    likelihood_loss_per_10: number | null;
  };
  top3_by_loss: Array<{
    type: string;
    loss: number;
  }>;
  breaking_news: Array<{
    title: string;
    url?: string;
    date?: string;
  }>;
}
