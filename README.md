# FinAgent

**AI-Powered Financial Advisory System for Indian Users**

FinAgent is a multi-agent AI system that provides comprehensive financial guidance tailored for Indian users. Built on the [Agno](https://github.com/agno-agi/agno) framework, it orchestrates 5 specialized agents across 2 teams to cover personal finance, tax optimization, investment planning, and portfolio management -- all accessible through a single unified API.

---

## Key Features

- **Multi-Agent Architecture** -- 5 specialized agents organized into 2 expert teams, orchestrated by a meta-team for intelligent query routing
- **30 Custom Tools** -- Purpose-built financial calculators covering insurance, tax, budgeting, SIP planning, stock analysis, portfolio management, and more
- **India-Focused Tax Engine** -- Full coverage of Indian Income Tax Act (FY 2024-25) including HRA, LTA, Sections 80C/80D/80CCD, capital gains, and Old vs New regime comparison
- **Real-Time Market Data** -- Live stock metrics, Indian & global indices, and historical price analysis via YFinance
- **RAG-Powered Knowledge Base** -- ChromaDB vector store with financial documents for context-aware tax guidance
- **Unified API** -- Single FastAPI endpoint that auto-routes queries to the appropriate specialist team

---

## Architecture Overview

```
                    ┌──────────────────────────┐
                    │   Financial Advisor Team │
                    │       (Meta-Team)        │
                    │   Intelligent Routing    │
                    └─────────┬────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
   ┌──────────▼──────────┐       ┌────────────▼────────────┐
   │ Personal Finance    │       │  Investment Helper      │
   │ Team (2 Agents)     │       │  Team (3 Agents)        │
   │                     │       │                         │
   │ - General Finance & │       │ - Market Intelligence   │
   │   Lifestyle Advisor │       │ - Investment Advisor    │
   │ - Tax & Compliance  │       │ - Portfolio Manager     │
   │   Specialist        │       │                         │
   │                     │       │                         │
   │ 17 Tools            │       │ 13 Tools                │
   └─────────────────────┘       └─────────────────────────┘
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | [Agno](https://github.com/agno-agi/agno) v2.3.21+ |
| Orchestrator LLM | Claude Sonnet 4 |
| Agent LLMs | Amazon Nova Lite |
| Web Framework | FastAPI (via AgentOS) |
| Vector Database | ChromaDB |
| Embeddings | SentenceTransformers (`all-MiniLM-L6-v2`) |
| Market Data | YFinance |
| Web Search | SerperTools |
| Config Management | Pydantic Settings v2 |
| Package Manager | Poetry |
| Language | Python 3.12+ |

---

## Project Structure

```
FinAgent/
├── agents/
│   ├── __init__.py
│   ├── personal_finance_team.py    # General Finance & Tax agents (17 tools)
│   ├── investment_team.py          # Market, Investment & Portfolio agents (13 tools)
│   └── financial_advisor_team.py   # Meta-team orchestrating both teams
├── core/
│   ├── __init__.py
│   ├── llm.py                      # LLM config & authentication
│   ├── loader.py                   # Dynamic agent loader & AgentOS setup
│   └── ingestion.ipynb             # Knowledge base ingestion notebook
├── tests/
│   ├── test.py
│   └── test.ipynb
├── main.py                         # Entry point - FastAPI server on port 5111
├── settings.py                     # Environment variable configuration
├── pyproject.toml                  # Poetry project config & dependencies
├── poetry.lock
├── Backend.md                      # Detailed backend architecture docs
└── README.md
```

---

## Getting Started

### Prerequisites

- Python >= 3.12
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/shiprasahu21/FinAgent.git
cd FinAgent
```

2. **Install dependencies:**

```bash
poetry install
```

3. **Set up environment variables:**

Create a `.env` file in the project root:

```env
# Intuit IAM Authentication (required for Intuit LLM provider)
CLIENT_APP_ID=your_app_id
CLIENT_APP_SECRET=your_app_secret
PROFILE_ID=your_profile_id
EXPERIENCE_ID=your_experience_id

# External Services
SERPER_API_KEY=your_serper_api_key
```

4. **Run the server:**

```bash
poetry run python main.py
```

The server will start at `http://localhost:5111` with hot-reload enabled.

---

## API Usage

FinAgent exposes a REST API via Agno's AgentOS. The meta-team automatically routes your query to the right specialist.

### Chat Endpoint

```bash
curl -X POST http://localhost:5111/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Calculate emergency fund for monthly expenses of ₹50,000",
    "team": "Personal Finance Team"
  }'
```

### Available Teams & Agents

| Team | Agent | Specialization |
|------|-------|----------------|
| **Personal Finance Team** | General Finance & Lifestyle Advisor | Insurance, emergency funds, budgeting, home planning, retirement, EPF/VPF |
| | Tax & Compliance Specialist | HRA, LTA, Section 80C/80D/80CCD, capital gains, regime comparison |
| **Investment Helper Team** | Market Intelligence Agent | Stock metrics, indices, historical data, sector analysis |
| | Investment Advisor | SIP planning, goal-based investing, investment education |
| | Portfolio Manager | Portfolio analysis, asset allocation, rebalancing |
| **Financial Advisor Team** | *(Meta-team)* | Routes queries to the appropriate specialist team |

---

## What You Can Ask

**Personal Finance**
- "How much life insurance coverage do I need on a salary of ₹15 LPA?"
- "Calculate my emergency fund for ₹50K monthly expenses"
- "Should I buy or rent a home in Bangalore for ₹1.2 Cr?"
- "Compare Old vs New tax regime for my ₹18 LPA salary"
- "What are my HRA and LTA exemptions?"
- "Plan my retirement corpus for retiring at 55"

**Investments**
- "Analyze TCS.NS stock -- give me key metrics and recent performance"
- "How is the Indian IT sector performing today?"
- "Plan a SIP to accumulate ₹1 Cr in 10 years"
- "Review my portfolio: 40% RELIANCE.NS, 30% TCS.NS, 30% HDFCBANK.NS"
- "What capital gains tax will I owe on selling equity held for 8 months?"
- "Compare S&P 500 vs Nifty 50 performance"

> **Tip:** Use the Financial Advisor Team (meta-team) for any query -- it automatically routes to the right specialists.

---

## Tools Reference

### Personal Finance Tools (17)

| Tool | Purpose |
|------|---------|
| `calculate_life_insurance_coverage` | 10-20x income rule for sum assured |
| `calculate_emergency_fund` | 3-6-12 month rule based on job stability |
| `analyze_spending_ratio` | 50-30-20 rule analysis |
| `get_spending_benchmarks` | Age-based spending benchmarks |
| `calculate_buy_vs_rent` | Buy vs rent scenario comparison |
| `calculate_affordable_emi` | FOIR-based EMI affordability |
| `calculate_section_24_interest` | Home loan interest deduction (up to ₹2L) |
| `calculate_retirement_corpus` | Required retirement corpus |
| `calculate_epf_vpf_returns` | EPF/VPF maturity projection |
| `calculate_hra_exemption` | HRA tax exemption |
| `calculate_lta_exemption` | LTA exemption for travel |
| `calculate_section_80c_deductions` | Section 80C (limit ₹1.5L) |
| `calculate_section_80d_deductions` | Health insurance deductions |
| `calculate_nps_deduction_80ccd` | NPS additional ₹50K deduction |
| `compare_tax_regimes` | Old vs New regime comparison |
| `calculate_capital_gains_tax` | Capital gains tax computation |
| `SerperTools` | Web search for research |

### Investment Tools (13)

| Tool | Purpose |
|------|---------|
| `get_stock_metrics` | Real-time P/E, EPS, Beta, Market Cap |
| `get_stock_history` | Historical price data (1d to 5y) |
| `get_index_data` | Index performance data |
| `get_indian_market_overview` | Nifty 50, Sensex, sector indices |
| `get_global_market_overview` | S&P 500, Nasdaq, Dow Jones |
| `calculate_sip_returns` | SIP returns with step-up |
| `calculate_sip_for_goal` | Monthly SIP for target goal |
| `calculate_goal_corpus` | Comprehensive goal planning |
| `calculate_capital_gains_tax` | Capital gains tax |
| `analyze_portfolio_allocation` | Holdings by market cap & sector |
| `calculate_age_based_allocation` | Age-based equity allocation |
| `suggest_rebalancing` | Rebalancing recommendations (>5% deviation) |
| `SerperTools` | Web search for news & info |

---

## Financial Rules & Frameworks

| Rule | Formula | Application |
|------|---------|-------------|
| 10-20x Income | Life Insurance = 10-20 x Annual Income | Insurance coverage |
| 3-6-12 Month | Emergency Fund = Expenses x (3/6/12 months) | Emergency savings |
| 50-30-20 | 50% needs + 30% wants + 20% savings | Budgeting |
| 110/120/100 - Age | Equity % = 110/120/100 - Age | Asset allocation |
| FOIR | EMIs <= 40-50% of Income | Loan affordability |
| **LTCG (Equity)** | 12.5% on gains > ₹1.25L (held > 365 days) | Capital gains tax |
| **STCG (Equity)** | 20% (held <= 365 days) | Capital gains tax |
| **Section 80C** | Up to ₹1.5L (PPF, ELSS, EPF, etc.) | Tax deduction |
| **Section 80D** | Health insurance premiums | Tax deduction |
| **Section 80CCD(1B)** | Additional ₹50K for NPS | Tax deduction |
| **Section 24** | Up to ₹2L home loan interest | Tax deduction |

---

## Stock Symbol Format

| Market | Format | Example |
|--------|--------|---------|
| Indian (NSE) | `SYMBOL.NS` | `TCS.NS`, `RELIANCE.NS`, `HDFCBANK.NS` |
| US | `SYMBOL` | `AAPL`, `MSFT`, `GOOGL` |

---

## Important Notes

- Tax calculations follow the **Indian Income Tax Act (FY 2024-25)**
- Market data is fetched **real-time** via the YFinance API
- The Knowledge Base uses **ChromaDB with RAG** for tax document retrieval
- Always consult a **certified financial advisor** for personalized advice
- Past performance does not guarantee future returns

---

## License

This project is part of a dissertation at BITS Pilani.

---

*FinAgent v0.1.0 -- AI-Powered Financial Advisory for India*
