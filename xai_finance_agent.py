# Adapted from the xai_finance_agent starter template in
# https://github.com/Shubhamsaboo/awesome-llm-apps.
# Modified for Indian stock market discovery and beginner investor research.

from os import getenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.xai import xAI
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.os import AgentOS
from dotenv import load_dotenv


load_dotenv()


def validate_environment():
    if getenv("XAI_API_KEY"):
        return

    raise SystemExit(
        "Missing XAI_API_KEY.\n"
        "This app uses xAI Grok through Agno, so model calls require an xAI API key.\n"
        "Set it with: export XAI_API_KEY='your-api-key-here'\n"
        "If your key is set but you see a credits or spending-limit error, fix that in the xAI console."
    )


# Setup local database for AgentOS sessions and agent history.
db = SqliteDb(db_file="tmp/agentos.db")


# create the AI finance agent
agent = Agent(
    name="xAI Finance Agent",
    model=xAI(id="grok-4-1-fast"),
    tools=[
        DuckDuckGoTools(),
        YFinanceTools(
            enable_stock_price=True,
            enable_company_info=True,
            enable_stock_fundamentals=True,
            enable_key_financial_ratios=True,
            enable_analyst_recommendations=True,
            enable_company_news=True,
            enable_historical_prices=True,
        ),
    ],
    instructions=[
        "You are an Indian stock market discovery and research assistant for a beginner investor.",
        "Focus only on Indian listed companies. Prefer NSE tickers ending in .NS, such as RELIANCE.NS or TCS.NS. Use BSE tickers ending in .BO only when NSE data is unavailable.",
        "Help the user discover stocks worth researching, but do not give direct buy, sell, or hold recommendations.",
        "For discovery requests, explain why each stock is interesting now, the recent catalyst or news, basic financial signals, key risks, and what the user should learn next.",
        "Always use tables to display financial or numerical data. For text data, use bullet points and small paragraphs.",
        "Be explicit about uncertainty, stale or missing data, and the difference between facts, estimates, and opinions.",
    ],
    db=db,
    add_history_to_context=True,
    debug_mode=True,
    markdown=True,
    )

# UI for finance agent
agent_os = AgentOS(agents=[agent], db=db)
app = agent_os.get_app()

if __name__ == "__main__":
    validate_environment()
    agent_os.serve(app="xai_finance_agent:app", reload=True)
