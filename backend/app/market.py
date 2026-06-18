from backend.app.models import StockCandidate


INDIAN_CANDIDATES = [
    StockCandidate(
        ticker="HDFCBANK.NS",
        company_name="HDFC Bank",
        sector="Private banking",
        market_cap_tier="large",
        business_quality=5,
        volatility="medium",
        beginner_complexity="medium",
        why_research="Large private bank with broad retail and corporate banking exposure.",
        risks=["Credit cycle risk", "Net interest margin pressure", "Integration and execution risk"],
    ),
    StockCandidate(
        ticker="TCS.NS",
        company_name="Tata Consultancy Services",
        sector="IT services",
        market_cap_tier="large",
        business_quality=5,
        volatility="low",
        beginner_complexity="low",
        why_research="Mature IT services company with strong cash generation and global enterprise clients.",
        risks=["Global tech spending slowdown", "Currency movement", "Margin pressure from wage inflation"],
    ),
    StockCandidate(
        ticker="RELIANCE.NS",
        company_name="Reliance Industries",
        sector="Energy, retail, telecom",
        market_cap_tier="large",
        business_quality=4,
        volatility="medium",
        beginner_complexity="high",
        why_research="Diversified conglomerate across energy, telecom, retail, and new energy ambitions.",
        risks=["Conglomerate complexity", "Commodity cycle exposure", "Capital allocation risk"],
    ),
    StockCandidate(
        ticker="TITAN.NS",
        company_name="Titan Company",
        sector="Consumer discretionary",
        market_cap_tier="large",
        business_quality=4,
        volatility="medium",
        beginner_complexity="medium",
        why_research="Consumer brand with jewellery, watches, and premium retail exposure.",
        risks=["Valuation risk", "Gold price sensitivity", "Discretionary demand slowdown"],
    ),
    StockCandidate(
        ticker="ASIANPAINT.NS",
        company_name="Asian Paints",
        sector="Paints and home decor",
        market_cap_tier="large",
        business_quality=4,
        volatility="medium",
        beginner_complexity="low",
        why_research="Well-known consumer franchise with long operating history.",
        risks=["Competitive intensity", "Raw material inflation", "Housing cycle sensitivity"],
    ),
    StockCandidate(
        ticker="INFY.NS",
        company_name="Infosys",
        sector="IT services",
        market_cap_tier="large",
        business_quality=4,
        volatility="medium",
        beginner_complexity="low",
        why_research="Large IT services exporter with strong governance and global client base.",
        risks=["Demand slowdown", "Discretionary tech budget cuts", "Currency and margin pressure"],
    ),
]


def discover_candidates(limit: int = 6) -> list[StockCandidate]:
    return INDIAN_CANDIDATES[:limit]
