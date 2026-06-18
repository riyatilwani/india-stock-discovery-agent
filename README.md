# India Stock Discovery Agent

A trust-first Indian equity research app for building an investor profile, applying suitability guardrails, discovering stocks to research, and journaling decisions before money moves.

This project is adapted from the `xai_finance_agent` starter template in [Shubham Saboo's awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) repository.

## What It Does

- Captures an investor profile: goals, horizon, risk tolerance, emergency fund, income stability, and drawdown comfort
- Generates native Python investment guardrails instead of relying on LLM prompts for risk control
- Shows Indian stock research candidates with suitability labels
- Saves a local decision journal for watchlist/skipped/bought ideas
- Uses a custom FastAPI backend and Vite React frontend

The app is a research and learning assistant. It does not provide buy/sell recommendations.

## Run Locally

Install dependencies:

```bash
make setup
```

Start the backend:

```bash
make api
```

In another terminal, start the web app:

```bash
make web
```

Open:

```text
http://localhost:3000
```

The API runs at:

```text
http://localhost:8000
```

Local app data is stored in `data/app.db`. This file is ignored by Git.

## Legacy Agno Agent

The original Agno-based agent is still available while the custom app evolves:

```bash
make legacy-agent
```

For the legacy agent, add your xAI key to `.env`:

```bash
echo "XAI_API_KEY=your-api-key-here" > .env
```

## Attribution and License

This repository is a modified derivative of the `xai_finance_agent` starter app from [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps).

Original project: Copyright and license notices remain under the Apache License 2.0. See [LICENSE](LICENSE).
