from typing import Literal

from pydantic import BaseModel, Field


RiskTolerance = Literal["conservative", "moderate", "aggressive"]
Experience = Literal["beginner", "intermediate", "advanced"]
IncomeStability = Literal["unstable", "stable", "very_stable"]
SuitabilityLabel = Literal["Suitable to research", "Caution", "Not suitable", "Insufficient data"]
Decision = Literal["watchlist", "skip", "bought", "review_later"]


class InvestorProfile(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    age_range: str = Field(min_length=1, max_length=40)
    experience: Experience
    risk_tolerance: RiskTolerance
    horizon_years: int = Field(ge=1, le=40)
    monthly_investment: int = Field(ge=0, le=10_000_000)
    emergency_fund_months: int = Field(ge=0, le=60)
    income_stability: IncomeStability
    max_drawdown_percent: int = Field(ge=0, le=80)
    goals: list[str] = Field(default_factory=list)
    existing_investments: str = Field(default="", max_length=2000)


class StoredInvestorProfile(InvestorProfile):
    id: str
    updated_at: str


class StockCandidate(BaseModel):
    ticker: str
    company_name: str
    sector: str
    market_cap_tier: Literal["large", "mid", "small"]
    business_quality: int = Field(ge=1, le=5)
    volatility: Literal["low", "medium", "high"]
    beginner_complexity: Literal["low", "medium", "high"]
    why_research: str
    risks: list[str]


class SuitabilityResult(BaseModel):
    label: SuitabilityLabel
    score: int = Field(ge=0, le=100)
    reasons: list[str]
    guardrails: list[str]
    next_steps: list[str]


class CandidateWithSuitability(StockCandidate):
    suitability: SuitabilityResult


class JournalEntryCreate(BaseModel):
    ticker: str = Field(min_length=1, max_length=30)
    company_name: str = Field(min_length=1, max_length=120)
    suitability_label: SuitabilityLabel
    decision: Decision
    thesis: str = Field(min_length=1, max_length=3000)
    risks: list[str] = Field(default_factory=list)
    notes: str = Field(default="", max_length=3000)
    follow_up_date: str | None = None


class JournalEntry(JournalEntryCreate):
    id: int
    created_at: str
