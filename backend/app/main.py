from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.db import decode_json, encode_json, get_connection, init_db
from backend.app.market import discover_candidates
from backend.app.models import (
    CandidateWithSuitability,
    InvestorProfile,
    JournalEntry,
    JournalEntryCreate,
    StockCandidate,
    SuitabilityResult,
)
from backend.app.policy import assess_suitability, investment_policy


app = FastAPI(title="India Stock Discovery API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


def row_to_profile(row) -> InvestorProfile | None:
    if row is None:
        return None
    return InvestorProfile(
        name=row["name"],
        age_range=row["age_range"],
        experience=row["experience"],
        risk_tolerance=row["risk_tolerance"],
        horizon_years=row["horizon_years"],
        monthly_investment=row["monthly_investment"],
        emergency_fund_months=row["emergency_fund_months"],
        income_stability=row["income_stability"],
        max_drawdown_percent=row["max_drawdown_percent"],
        goals=decode_json(row["goals_json"]),
        existing_investments=row["existing_investments"],
    )


def get_profile_or_none() -> InvestorProfile | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM investor_profiles WHERE id = 'default'").fetchone()
    return row_to_profile(row)


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/profile")
def get_profile() -> dict:
    profile = get_profile_or_none()
    return {"profile": profile}


@app.put("/profile")
def save_profile(profile: InvestorProfile) -> dict:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO investor_profiles (
                id, name, age_range, experience, risk_tolerance, horizon_years,
                monthly_investment, emergency_fund_months, income_stability,
                max_drawdown_percent, goals_json, existing_investments, updated_at
            )
            VALUES (
                'default', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
            )
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                age_range = excluded.age_range,
                experience = excluded.experience,
                risk_tolerance = excluded.risk_tolerance,
                horizon_years = excluded.horizon_years,
                monthly_investment = excluded.monthly_investment,
                emergency_fund_months = excluded.emergency_fund_months,
                income_stability = excluded.income_stability,
                max_drawdown_percent = excluded.max_drawdown_percent,
                goals_json = excluded.goals_json,
                existing_investments = excluded.existing_investments,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                profile.name,
                profile.age_range,
                profile.experience,
                profile.risk_tolerance,
                profile.horizon_years,
                profile.monthly_investment,
                profile.emergency_fund_months,
                profile.income_stability,
                profile.max_drawdown_percent,
                encode_json(profile.goals),
                profile.existing_investments,
            ),
        )
    return {"profile": profile, "policy": investment_policy(profile)}


@app.get("/policy")
def get_policy() -> dict:
    profile = get_profile_or_none()
    if profile is None:
        raise HTTPException(status_code=404, detail="Create an investor profile first.")
    return {"policy": investment_policy(profile)}


@app.get("/discover", response_model=list[CandidateWithSuitability])
def discover() -> list[CandidateWithSuitability]:
    profile = get_profile_or_none()
    results: list[CandidateWithSuitability] = []
    for candidate in discover_candidates():
        results.append(
            CandidateWithSuitability(
                **candidate.model_dump(),
                suitability=assess_suitability(profile, candidate),
            )
        )
    return results


@app.post("/suitability", response_model=SuitabilityResult)
def suitability(stock: StockCandidate) -> SuitabilityResult:
    return assess_suitability(get_profile_or_none(), stock)


def row_to_journal(row) -> JournalEntry:
    return JournalEntry(
        id=row["id"],
        ticker=row["ticker"],
        company_name=row["company_name"],
        suitability_label=row["suitability_label"],
        decision=row["decision"],
        thesis=row["thesis"],
        risks=decode_json(row["risks_json"]),
        notes=row["notes"],
        follow_up_date=row["follow_up_date"],
        created_at=row["created_at"],
    )


@app.get("/journal", response_model=list[JournalEntry])
def get_journal() -> list[JournalEntry]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM journal_entries ORDER BY created_at DESC").fetchall()
    return [row_to_journal(row) for row in rows]


@app.post("/journal", response_model=JournalEntry)
def add_journal_entry(entry: JournalEntryCreate) -> JournalEntry:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO journal_entries (
                ticker, company_name, suitability_label, decision, thesis,
                risks_json, notes, follow_up_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.ticker.upper(),
                entry.company_name,
                entry.suitability_label,
                entry.decision,
                entry.thesis,
                encode_json(entry.risks),
                entry.notes,
                entry.follow_up_date,
            ),
        )
        row = conn.execute("SELECT * FROM journal_entries WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return row_to_journal(row)
