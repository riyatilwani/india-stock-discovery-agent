from backend.app.models import InvestorProfile, StockCandidate, SuitabilityResult


def profile_warnings(profile: InvestorProfile) -> list[str]:
    warnings: list[str] = []
    if profile.emergency_fund_months < 6:
        warnings.append("Build a 6-month emergency fund before increasing individual-stock exposure.")
    if profile.horizon_years < 3:
        warnings.append("A short horizon is usually a poor fit for volatile individual equities.")
    if profile.max_drawdown_percent < 15:
        warnings.append("Your drawdown comfort is low, so single-stock risk should stay limited.")
    return warnings


def investment_policy(profile: InvestorProfile) -> dict:
    if profile.risk_tolerance == "conservative":
        max_single_stock = 3
        satellite = 10
    elif profile.risk_tolerance == "moderate":
        max_single_stock = 5
        satellite = 20
    else:
        max_single_stock = 8
        satellite = 30

    if profile.experience == "beginner":
        max_single_stock = min(max_single_stock, 5)

    return {
        "max_single_stock_percent": max_single_stock,
        "max_direct_stock_allocation_percent": satellite,
        "minimum_horizon_years_for_stocks": 5,
        "rules": [
            "Treat app output as a research queue, not buy/sell advice.",
            "Do not buy a company you cannot explain in plain language.",
            "Wait at least 24 hours before acting on a new idea.",
            "Write a thesis and risks in the journal before investing.",
            "Re-check concentration before adding to any position.",
        ],
        "warnings": profile_warnings(profile),
    }


def assess_suitability(profile: InvestorProfile | None, stock: StockCandidate) -> SuitabilityResult:
    if profile is None:
        return SuitabilityResult(
            label="Insufficient data",
            score=0,
            reasons=["Create an investor profile before evaluating stock ideas."],
            guardrails=["No personalized suitability assessment without a saved profile."],
            next_steps=["Complete the profile form with goals, horizon, risk tolerance, and drawdown comfort."],
        )

    score = 70
    reasons = [f"{stock.company_name} is a {stock.market_cap_tier}-cap company in {stock.sector}."]
    guardrails = [
        "This is not a buy recommendation.",
        "Use this as a starting point for research and journaling.",
    ]
    next_steps = [
        "Read the latest annual report or investor presentation.",
        "Compare valuation and growth with at least two peers.",
        "Write down what would make you avoid or exit the idea.",
    ]

    if profile.emergency_fund_months < 6:
        score -= 25
        reasons.append("Emergency fund is below 6 months, so new equity risk should be limited.")
        guardrails.append("Prioritize emergency fund before increasing direct stock exposure.")

    if profile.horizon_years < 3:
        score -= 25
        reasons.append("Your time horizon is short for individual equities.")
        guardrails.append("Avoid relying on stock ideas for near-term goals.")
    elif profile.horizon_years >= 5:
        score += 5
        reasons.append("Your time horizon is long enough to research equities patiently.")

    if profile.risk_tolerance == "conservative" and stock.volatility == "high":
        score -= 35
        reasons.append("High-volatility stocks do not fit a conservative risk profile.")
    elif profile.risk_tolerance == "moderate" and stock.volatility == "high":
        score -= 15
        reasons.append("High volatility deserves caution for a moderate profile.")
    elif profile.risk_tolerance == "aggressive" and stock.volatility != "high":
        score += 5

    if profile.experience == "beginner" and stock.beginner_complexity == "high":
        score -= 25
        reasons.append("The business or risk profile may be too complex for a beginner.")
        next_steps.append("Explain the revenue model, debt risk, and cycle risk before considering it further.")
    elif profile.experience == "beginner" and stock.beginner_complexity == "low":
        score += 5
        reasons.append("The business is relatively easier for a beginner to study.")

    if profile.max_drawdown_percent < 20 and stock.volatility in {"medium", "high"}:
        score -= 10
        reasons.append("Your drawdown comfort is below the volatility this stock may require.")

    score = max(0, min(100, score))
    if score >= 70:
        label = "Suitable to research"
    elif score >= 45:
        label = "Caution"
    else:
        label = "Not suitable"

    return SuitabilityResult(
        label=label,
        score=score,
        reasons=reasons,
        guardrails=guardrails,
        next_steps=next_steps,
    )
