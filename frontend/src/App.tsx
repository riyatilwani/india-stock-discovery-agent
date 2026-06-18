"use client";

import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  BookOpenCheck,
  CheckCircle2,
  ClipboardList,
  IndianRupee,
  Loader2,
  RefreshCw,
  Save,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";
import { api, Candidate, InvestorProfile, JournalEntry, Policy } from "./lib/api";

const emptyProfile: InvestorProfile = {
  name: "Riya",
  age_range: "25-34",
  experience: "beginner",
  risk_tolerance: "moderate",
  horizon_years: 5,
  monthly_investment: 25000,
  emergency_fund_months: 6,
  income_stability: "stable",
  max_drawdown_percent: 25,
  goals: ["Long-term wealth creation"],
  existing_investments: "Index funds, cash savings",
};

function labelClass(label: string) {
  if (label === "Suitable to research") return "label labelGreen";
  if (label === "Caution") return "label labelAmber";
  if (label === "Not suitable") return "label labelRed";
  return "label labelNeutral";
}

function parseGoals(value: string) {
  return value
    .split(",")
    .map((goal) => goal.trim())
    .filter(Boolean);
}

export default function Home() {
  const [profile, setProfile] = useState<InvestorProfile>(emptyProfile);
  const [goalText, setGoalText] = useState(emptyProfile.goals.join(", "));
  const [policy, setPolicy] = useState<Policy | null>(null);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [journal, setJournal] = useState<JournalEntry[]>([]);
  const [selected, setSelected] = useState<Candidate | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const profileCompleteness = useMemo(() => {
    let score = 0;
    if (profile.name) score += 15;
    if (profile.goals.length) score += 15;
    if (profile.emergency_fund_months >= 6) score += 20;
    if (profile.horizon_years >= 3) score += 20;
    if (profile.monthly_investment > 0) score += 15;
    if (profile.existing_investments) score += 15;
    return score;
  }, [profile]);

  async function loadAll() {
    setLoading(true);
    setError(null);
    try {
      const profileResponse = await api.getProfile();
      if (profileResponse.profile) {
        setProfile(profileResponse.profile);
        setGoalText(profileResponse.profile.goals.join(", "));
        const policyResponse = await api.getPolicy();
        setPolicy(policyResponse.policy);
      }
      const [discovered, journalEntries] = await Promise.all([api.discover(), api.getJournal()]);
      setCandidates(discovered);
      setJournal(journalEntries);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load dashboard.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAll();
  }, []);

  async function saveProfile() {
    setSaving(true);
    setError(null);
    try {
      const nextProfile = { ...profile, goals: parseGoals(goalText) };
      const response = await api.saveProfile(nextProfile);
      setProfile(response.profile);
      setPolicy(response.policy);
      const discovered = await api.discover();
      setCandidates(discovered);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to save profile.");
    } finally {
      setSaving(false);
    }
  }

  async function addToJournal(candidate: Candidate, decision: JournalEntry["decision"]) {
    setError(null);
    try {
      const entry = await api.addJournal({
        ticker: candidate.ticker,
        company_name: candidate.company_name,
        suitability_label: candidate.suitability.label,
        decision,
        thesis: candidate.why_research,
        risks: candidate.risks,
        notes: "Captured from discovery dashboard.",
        follow_up_date: null,
      });
      setJournal([entry, ...journal]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to save journal entry.");
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">India equity research</p>
          <h1>Trust-first stock discovery</h1>
        </div>
        <button className="iconButton" onClick={loadAll} aria-label="Refresh dashboard">
          {loading ? <Loader2 className="spin" size={18} /> : <RefreshCw size={18} />}
        </button>
      </header>

      {error && (
        <div className="alert">
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      <section className="metrics">
        <div className="metric">
          <ShieldCheck size={20} />
          <div>
            <span>{profileCompleteness}%</span>
            <p>Profile readiness</p>
          </div>
        </div>
        <div className="metric">
          <IndianRupee size={20} />
          <div>
            <span>{profile.monthly_investment.toLocaleString("en-IN")}</span>
            <p>Monthly capacity</p>
          </div>
        </div>
        <div className="metric">
          <TrendingUp size={20} />
          <div>
            <span>{candidates.length}</span>
            <p>Research candidates</p>
          </div>
        </div>
        <div className="metric">
          <ClipboardList size={20} />
          <div>
            <span>{journal.length}</span>
            <p>Journal entries</p>
          </div>
        </div>
      </section>

      <section className="grid">
        <div className="panel profilePanel">
          <div className="panelHeader">
            <div>
              <p className="eyebrow">Step 1</p>
              <h2>Investor profile</h2>
            </div>
            <button className="primaryButton" onClick={saveProfile} disabled={saving}>
              {saving ? <Loader2 className="spin" size={16} /> : <Save size={16} />}
              Save
            </button>
          </div>

          <div className="formGrid">
            <label>
              Name
              <input value={profile.name} onChange={(e) => setProfile({ ...profile, name: e.target.value })} />
            </label>
            <label>
              Age range
              <select value={profile.age_range} onChange={(e) => setProfile({ ...profile, age_range: e.target.value })}>
                <option>18-24</option>
                <option>25-34</option>
                <option>35-44</option>
                <option>45-54</option>
                <option>55+</option>
              </select>
            </label>
            <label>
              Experience
              <select value={profile.experience} onChange={(e) => setProfile({ ...profile, experience: e.target.value as InvestorProfile["experience"] })}>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </label>
            <label>
              Risk tolerance
              <select value={profile.risk_tolerance} onChange={(e) => setProfile({ ...profile, risk_tolerance: e.target.value as InvestorProfile["risk_tolerance"] })}>
                <option value="conservative">Conservative</option>
                <option value="moderate">Moderate</option>
                <option value="aggressive">Aggressive</option>
              </select>
            </label>
            <label>
              Horizon years
              <input type="number" value={profile.horizon_years} onChange={(e) => setProfile({ ...profile, horizon_years: Number(e.target.value) })} />
            </label>
            <label>
              Monthly investment
              <input type="number" value={profile.monthly_investment} onChange={(e) => setProfile({ ...profile, monthly_investment: Number(e.target.value) })} />
            </label>
            <label>
              Emergency fund months
              <input type="number" value={profile.emergency_fund_months} onChange={(e) => setProfile({ ...profile, emergency_fund_months: Number(e.target.value) })} />
            </label>
            <label>
              Max drawdown comfort
              <input type="number" value={profile.max_drawdown_percent} onChange={(e) => setProfile({ ...profile, max_drawdown_percent: Number(e.target.value) })} />
            </label>
            <label>
              Income stability
              <select value={profile.income_stability} onChange={(e) => setProfile({ ...profile, income_stability: e.target.value as InvestorProfile["income_stability"] })}>
                <option value="unstable">Unstable</option>
                <option value="stable">Stable</option>
                <option value="very_stable">Very stable</option>
              </select>
            </label>
            <label>
              Goals
              <input value={goalText} onChange={(e) => setGoalText(e.target.value)} />
            </label>
          </div>
          <label className="wideField">
            Existing investments
            <textarea value={profile.existing_investments} onChange={(e) => setProfile({ ...profile, existing_investments: e.target.value })} />
          </label>
        </div>

        <div className="panel">
          <div className="panelHeader">
            <div>
              <p className="eyebrow">Step 2</p>
              <h2>Policy guardrails</h2>
            </div>
            <BookOpenCheck size={22} />
          </div>
          {policy ? (
            <div className="policy">
              <div className="policyNumbers">
                <div>
                  <span>{policy.max_single_stock_percent}%</span>
                  <p>Max per stock</p>
                </div>
                <div>
                  <span>{policy.max_direct_stock_allocation_percent}%</span>
                  <p>Max direct stocks</p>
                </div>
              </div>
              <h3>Rules</h3>
              <ul>{policy.rules.map((rule) => <li key={rule}>{rule}</li>)}</ul>
              {policy.warnings.length > 0 && (
                <>
                  <h3>Warnings</h3>
                  <ul className="warningList">{policy.warnings.map((warning) => <li key={warning}>{warning}</li>)}</ul>
                </>
              )}
            </div>
          ) : (
            <p className="muted">Save your investor profile to generate a personal investing policy.</p>
          )}
        </div>
      </section>

      <section className="panel">
        <div className="panelHeader">
          <div>
            <p className="eyebrow">Step 3</p>
            <h2>Research candidates</h2>
          </div>
          <span className="subtleText">Discovery is for research, not buy/sell advice.</span>
        </div>
        <div className="candidateGrid">
          {candidates.map((candidate) => (
            <article className="candidate" key={candidate.ticker}>
              <div className="candidateTop">
                <div>
                  <span className="ticker">{candidate.ticker}</span>
                  <h3>{candidate.company_name}</h3>
                  <p>{candidate.sector}</p>
                </div>
                <span className={labelClass(candidate.suitability.label)}>{candidate.suitability.label}</span>
              </div>
              <p>{candidate.why_research}</p>
              <div className="scoreLine">
                <span>Suitability score</span>
                <strong>{candidate.suitability.score}/100</strong>
              </div>
              <div className="buttonRow">
                <button onClick={() => setSelected(candidate)}>Review</button>
                <button onClick={() => addToJournal(candidate, "watchlist")}>
                  <CheckCircle2 size={15} />
                  Watchlist
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>

      {selected && (
        <section className="panel detailPanel">
          <div className="panelHeader">
            <div>
              <p className="eyebrow">{selected.ticker}</p>
              <h2>{selected.company_name}</h2>
            </div>
            <button className="ghostButton" onClick={() => setSelected(null)}>Close</button>
          </div>
          <div className="detailGrid">
            <div>
              <h3>Reasons</h3>
              <ul>{selected.suitability.reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul>
            </div>
            <div>
              <h3>Risks</h3>
              <ul>{selected.risks.map((risk) => <li key={risk}>{risk}</li>)}</ul>
            </div>
            <div>
              <h3>Next steps</h3>
              <ul>{selected.suitability.next_steps.map((step) => <li key={step}>{step}</li>)}</ul>
            </div>
          </div>
        </section>
      )}

      <section className="panel">
        <div className="panelHeader">
          <div>
            <p className="eyebrow">Step 4</p>
            <h2>Decision journal</h2>
          </div>
          <span className="subtleText">Track your reasoning before any money moves.</span>
        </div>
        <div className="journalList">
          {journal.length === 0 && <p className="muted">No journal entries yet.</p>}
          {journal.map((entry) => (
            <article className="journalItem" key={entry.id}>
              <div>
                <span className="ticker">{entry.ticker}</span>
                <h3>{entry.company_name}</h3>
                <p>{entry.thesis}</p>
              </div>
              <div className="journalMeta">
                <span className={labelClass(entry.suitability_label)}>{entry.suitability_label}</span>
                <span>{entry.decision.replace("_", " ")}</span>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
