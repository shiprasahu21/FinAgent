# FinAgent - Documentation Guide

> **AI-Powered Financial Advisor for Indian Users**
> Multi-agent system built with Agno framework for personal finance and investment guidance

---

## About This Project

FinAgent is a sophisticated financial advisory system that uses specialized AI agents to provide comprehensive financial guidance tailored to the Indian market. It covers everything from tax planning and budgeting to stock analysis and portfolio management.

**Key Highlights:**
- 9 specialized financial agents across 2 teams
- 19 custom financial calculation tools
- Real-time market data integration (NSE/BSE/US markets)
- India-specific tax optimization (80C, 80D, 80CCD)
- RAG-powered knowledge base for tax documents

---

## Documentation Structure

This project contains three main documentation files:

### 1. [README.md](README.md)
**Purpose:** Project introduction
**Content:** Brief one-liner description of the project
**When to use:** Quick reference to understand what FinAgent is

---

### 2. [AGENTS.md](AGENTS.md)
**Purpose:** Agent-focused overview with practical examples
**Content:**
- Overview of all 9 agents organized by team
- Agent roles and capabilities
- Tool descriptions for each agent
- Example queries for each agent
- Financial rules and formulas used
- High-level architecture diagram

**When to use:**
- Understanding what each agent does
- Finding which agent handles specific queries
- Learning about available tools
- Getting example queries to test
- Quick reference for agent capabilities

**Structure:**
```
├── Personal Finance Team (4 agents)
│   ├── General Finance Advisor
│   ├── Spending Analyst
│   ├── Tax Planning Assistant
│   └── Home Planning Advisor
└── Investment Helper Team (5 agents)
    ├── Stock Analyst
    ├── Indian Market Analyst
    ├── Global Market Analyst
    ├── Investment Helper
    └── Portfolio Manager
```

---

### 3. [DOCUMENTATION.md](DOCUMENTATION.md)
**Purpose:** Comprehensive technical documentation
**Content:**
- Complete project overview and architecture
- Detailed agent specifications
- Tool reference with parameters and return values
- Knowledge base and data sources setup
- LLM configuration and authentication
- Financial rules and frameworks
- Technology stack details
- Project structure breakdown
- Getting started guide with installation steps
- API usage examples

**When to use:**
- Setting up the project for the first time
- Understanding the technical architecture
- Configuring LLMs and authentication
- Setting up the knowledge base
- Detailed tool parameter reference
- Troubleshooting and development

**Sections:**
1. Project Overview
2. Architecture Overview
3. Teams and Agents (detailed specs)
4. Tools Reference (complete API)
5. Knowledge Base & Data Sources
6. LLM Configuration & Models
7. Financial Rules & Frameworks
8. Technology Stack
9. Project Structure
10. Getting Started

---

## Quick Navigation

### I want to...

**Understand what FinAgent does**
→ Read [README.md](README.md) and [AGENTS.md](AGENTS.md) overview sections

**Know which agent handles my query**
→ Check [AGENTS.md](AGENTS.md) agent descriptions and example queries

**Set up the project**
→ Follow [DOCUMENTATION.md](DOCUMENTATION.md) Section 10: Getting Started

**Understand the architecture**
→ Read [DOCUMENTATION.md](DOCUMENTATION.md) Section 2: Architecture Overview

**Find tool parameters**
→ Check [DOCUMENTATION.md](DOCUMENTATION.md) Section 4: Tools Reference

**Learn about financial rules used**
→ See [AGENTS.md](AGENTS.md) Key Financial Rules or [DOCUMENTATION.md](DOCUMENTATION.md) Section 7

**Configure authentication**
→ Follow [DOCUMENTATION.md](DOCUMENTATION.md) Section 6.4: Authentication

**Set up knowledge base**
→ Read [DOCUMENTATION.md](DOCUMENTATION.md) Section 5 & 10.5

---

## Technology Overview

| Component | Technology |
|-----------|-----------|
| **Framework** | Agno v2.3.21+ (Multi-agent orchestration) |
| **Orchestrator Model** | Claude Sonnet 4 |
| **Agent Model** | Amazon Nova Lite |
| **Vector Database** | ChromaDB with SentenceTransformer embeddings |
| **Market Data** | YFinance API |
| **Web Search** | Serper API |
| **Server** | FastAPI (AgentOS) on port 5111 |
| **Python Version** | 3.12+ |

---

## Quick Start

```bash
# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run the server
poetry run python main.py
```

Server starts at: `http://localhost:5111`

---

## Agent Capabilities Summary

### Personal Finance Team
- **Life Insurance** calculation (10-20x income rule)
- **Emergency Fund** planning (3-6-12 month rule)
- **Spending Analysis** (50-30-20 rule)
- **Tax Optimization** (Sections 80C, 80D, 80CCD)
- **Tax Regime Comparison** (Old vs New)
- **Buy vs Rent** analysis
- **Home Loan Affordability** (FOIR rule)

### Investment Helper Team
- **Stock Analysis** (P/E, EPS, Beta, fundamentals)
- **Market Tracking** (Nifty, Sensex, S&P 500, Nasdaq)
- **Sector Analysis** (IT, Banking, Pharma, FMCG, Auto)
- **Portfolio Review** (allocation by market cap & sector)
- **Rebalancing** recommendations (100-Age rule)
- **Investment Education** (mutual funds, ELSS, NPS, SIP)

---

## Financial Rules Reference

| Rule | Formula | Usage |
|------|---------|-------|
| **10-20x Income** | Life Insurance = 10-20 × Annual Income | Insurance coverage |
| **3-6-12 Month** | Emergency Fund = Expenses × (3/6/12 months) | Emergency savings |
| **50-30-20** | 50% Needs + 30% Wants + 20% Savings | Budgeting |
| **100 Minus Age** | Equity % = 100 - Age | Asset allocation |
| **FOIR** | Total EMIs ≤ 40-50% of Income | Loan affordability |

---

## Project Structure

```
FinAgent/
├── CLAUDE.md                    # This file - documentation guide
├── README.md                    # Project introduction
├── AGENTS.md                    # Agent overview & examples
├── DOCUMENTATION.md             # Comprehensive technical docs
│
├── main.py                      # Application entry point
├── settings.py                  # Configuration
├── pyproject.toml              # Dependencies
│
├── agents/                      # Agent definitions
│   ├── personal_finance_team.py
│   └── investment_team.py
│
├── core/                        # Core utilities
│   ├── llm.py                  # LLM configuration
│   ├── loader.py               # Agent loader
│   └── ingestion.ipynb         # Knowledge base setup
│
├── data/                        # Data files
├── tmp/chroma/                 # Vector database
└── tests/                       # Test files
```

---

## Environment Variables Required

```env
# Authentication (Intuit IAM)
CLIENT_APP_ID=your_app_id
CLIENT_APP_SECRET=your_app_secret
PROFILE_ID=your_profile_id
EXPERIENCE_ID=your_experience_id

# External Services
SERPER_API_KEY=your_serper_api_key
```

---

## API Usage Example

```bash
# Query Personal Finance Team
curl -X POST http://localhost:5111/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How much emergency fund do I need?",
    "team": "Personal Finance Team"
  }'

# Query Investment Team
curl -X POST http://localhost:5111/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze TCS stock",
    "team": "Investment Helper Team"
  }'
```

---

## Support & Contribution

For questions, issues, or contributions, please refer to:
- Technical details: [DOCUMENTATION.md](DOCUMENTATION.md)
- Agent capabilities: [AGENTS.md](AGENTS.md)
- Project repository: [GitHub link if available]

---

*Last Updated: January 2026*
*FinAgent v0.1.0*
