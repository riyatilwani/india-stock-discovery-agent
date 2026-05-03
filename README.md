# India Stock Discovery Agent

An AI-powered research assistant for discovering Indian stocks worth investigating, using Agno, xAI Grok, Yahoo Finance, and web search.

This project is adapted from the `xai_finance_agent` starter template in [Shubham Saboo's awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) repository.

### Features

- Focused on Indian listed companies, especially NSE tickers such as `RELIANCE.NS` and `TCS.NS`
- Powered by xAI's Grok-4 Fast model through Agno
- Real-time stock data analysis via YFinance
- Web search capabilities through DuckDuckGo
- Beginner-friendly research output with catalysts, risks, and next learning steps
- Interactive AgentOS playground interface

### How to get Started?

1. Clone the GitHub repository
```bash
git clone git@github.com:riyatilwani/india-stock-discovery-agent.git
cd india-stock-discovery-agent
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Get your xAI API key

- Sign up for an [xAI API account](https://console.x.ai/)
- Set your XAI_API_KEY environment variable.
```bash
export XAI_API_KEY='your-api-key-here'
```

4. Run the team of AI Agents
```bash
python xai_finance_agent.py
```

5. Open your web browser and navigate to the URL provided in the console output to interact with the AI financial agent through the playground interface.

Session history is stored locally in `tmp/agentos.db`. This file is ignored by Git so your local conversations are not pushed to GitHub.

6. Connecting Your AgentOS

To manage, monitor, and interact with your financial agent through the AgentOS Control Plane (from your browser), you need to connect your running AgentOS instance:

**Step-by-step guide:**

- Visit the official documentation: [Connecting Your OS](https://docs.agno.com/agent-os/connecting-your-os)
- Follow the steps in the guide to register your local AgentOS and establish the connection.

### Attribution and License

This repository is a modified derivative of the `xai_finance_agent` starter app from [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps).

Original project: Copyright and license notices remain under the Apache License 2.0. See [LICENSE](LICENSE).
