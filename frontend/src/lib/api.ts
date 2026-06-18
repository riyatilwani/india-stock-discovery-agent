export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export type InvestorProfile = {
  name: string;
  age_range: string;
  experience: "beginner" | "intermediate" | "advanced";
  risk_tolerance: "conservative" | "moderate" | "aggressive";
  horizon_years: number;
  monthly_investment: number;
  emergency_fund_months: number;
  income_stability: "unstable" | "stable" | "very_stable";
  max_drawdown_percent: number;
  goals: string[];
  existing_investments: string;
};

export type Policy = {
  max_single_stock_percent: number;
  max_direct_stock_allocation_percent: number;
  minimum_horizon_years_for_stocks: number;
  rules: string[];
  warnings: string[];
};

export type Suitability = {
  label: "Suitable to research" | "Caution" | "Not suitable" | "Insufficient data";
  score: number;
  reasons: string[];
  guardrails: string[];
  next_steps: string[];
};

export type Candidate = {
  ticker: string;
  company_name: string;
  sector: string;
  market_cap_tier: "large" | "mid" | "small";
  business_quality: number;
  volatility: "low" | "medium" | "high";
  beginner_complexity: "low" | "medium" | "high";
  why_research: string;
  risks: string[];
  suitability: Suitability;
};

export type JournalEntry = {
  id: number;
  ticker: string;
  company_name: string;
  suitability_label: Suitability["label"];
  decision: "watchlist" | "skip" | "bought" | "review_later";
  thesis: string;
  risks: string[];
  notes: string;
  follow_up_date: string | null;
  created_at: string;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  getProfile: () => request<{ profile: InvestorProfile | null }>("/profile"),
  saveProfile: (profile: InvestorProfile) =>
    request<{ profile: InvestorProfile; policy: Policy }>("/profile", {
      method: "PUT",
      body: JSON.stringify(profile),
    }),
  getPolicy: () => request<{ policy: Policy }>("/policy"),
  discover: () => request<Candidate[]>("/discover"),
  getJournal: () => request<JournalEntry[]>("/journal"),
  addJournal: (entry: Omit<JournalEntry, "id" | "created_at">) =>
    request<JournalEntry>("/journal", {
      method: "POST",
      body: JSON.stringify(entry),
    }),
};
