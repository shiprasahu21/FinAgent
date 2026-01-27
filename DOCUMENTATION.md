# FinAgent - Comprehensive Documentation

> **Financial Advisor Agent OS for Indians**  
> A multi-agent financial advisory system built for personal finance management, tax optimization, and investment guidance tailored to the Indian financial ecosystem.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Overview](#2-architecture-overview)
3. [Teams and Agents](#3-teams-and-agents)
   - [Personal Finance Team](#31-personal-finance-team)
   - [Investment Helper Team](#32-investment-helper-team)
4. [Tools Reference](#4-tools-reference)
5. [Knowledge Base & Data Sources](#5-knowledge-base--data-sources)
6. [LLM Configuration & Models](#6-llm-configuration--models)
7. [Financial Rules & Frameworks](#7-financial-rules--frameworks)
8. [Technology Stack](#8-technology-stack)
9. [Project Structure](#9-project-structure)
10. [Getting Started](#10-getting-started)

---

## 1. Project Overview

### 1.1 Introduction

**FinAgent** is a sophisticated multi-agent financial advisory system designed specifically for Indian users. It leverages modern AI/ML capabilities through the **Agno** framework to provide comprehensive financial guidance across two specialized domains:

- **Personal Finance Management** - Covering budgeting, tax planning, insurance, and real estate decisions
- **Investment Advisory** - Providing market analysis, portfolio management, and investment education

### 1.2 Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Agent Architecture** | Specialized agents working collaboratively within teams |
| **India-Specific** | Tailored for Indian tax laws (80C, 80D, 80CCD), markets (NSE/BSE), and financial instruments |
| **Real-Time Data** | Live stock prices and market data via YFinance integration |
| **Knowledge Base** | RAG-powered knowledge base for tax documents and financial guides |
| **Web Search** | Integrated Serper API for latest news and information |
| **FastAPI Server** | AgentOS provides a REST API for agent interactions |

### 1.3 Use Cases

- Personal financial health assessment
- Tax optimization and regime comparison (Old vs New)
- Emergency fund and insurance coverage calculations
- Home loan affordability and buy vs rent analysis
- Stock and market analysis (Indian & Global)
- Portfolio allocation and rebalancing recommendations
- Investment education and concept explanations

---

## 2. Architecture Overview

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FinAgent OS                               │
│                    (FastAPI Server - Port 5111)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────────────┐    ┌─────────────────────────────┐   │
│   │   Personal Finance      │    │    Investment Helper         │   │
│   │        Team             │    │         Team                 │   │
│   │   (Claude Sonnet 4)     │    │     (Claude Sonnet 4)        │   │
│   ├─────────────────────────┤    ├─────────────────────────────┤   │
│   │                         │    │                              │   │
│   │ ┌─────────────────────┐ │    │ ┌─────────────────────────┐ │   │
│   │ │ General Finance     │ │    │ │ Stock Analyst           │ │   │
│   │ │ Advisor             │ │    │ │ (Nova Lite)             │ │   │
│   │ │ (Nova Lite)         │ │    │ └─────────────────────────┘ │   │
│   │ └─────────────────────┘ │    │ ┌─────────────────────────┐ │   │
│   │ ┌─────────────────────┐ │    │ │ Indian Market Analyst   │ │   │
│   │ │ Spending Analyst    │ │    │ │ (Nova Lite)             │ │   │
│   │ │ (Nova Lite)         │ │    │ └─────────────────────────┘ │   │
│   │ └─────────────────────┘ │    │ ┌─────────────────────────┐ │   │
│   │ ┌─────────────────────┐ │    │ │ Global Market Analyst   │ │   │
│   │ │ Tax Planning        │ │    │ │ (Nova Lite)             │ │   │
│   │ │ Assistant           │ │    │ └─────────────────────────┘ │   │
│   │ │ (Nova Lite + KB)    │ │    │ ┌─────────────────────────┐ │   │
│   │ └─────────────────────┘ │    │ │ Investment Helper       │ │   │
│   │ ┌─────────────────────┐ │    │ │ (Nova Lite)             │ │   │
│   │ │ Home Planning       │ │    │ └─────────────────────────┘ │   │
│   │ │ Advisor             │ │    │ ┌─────────────────────────┐ │   │
│   │ │ (Nova Lite)         │ │    │ │ Portfolio Manager       │ │   │
│   │ └─────────────────────┘ │    │ │ (Nova Lite)             │ │   │
│   │                         │    │ └─────────────────────────┘ │   │
│   └─────────────────────────┘    └─────────────────────────────┘   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                         Shared Resources                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ ChromaDB     │  │ YFinance     │  │ Serper Web Search        │  │
│  │ Vector Store │  │ Market Data  │  │ (News & Information)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Design Principles

1. **Separation of Concerns**: Each agent has a specific domain expertise and set of tools
2. **Team-Based Routing**: Teams use an orchestrator model (Claude Sonnet 4) to route queries to the most appropriate specialist agent
3. **Tool-Augmented LLMs**: Agents are equipped with custom tools for calculations and external API integrations
4. **Knowledge Augmentation**: RAG (Retrieval Augmented Generation) for tax documents and financial guides
5. **Dynamic Loading**: Agents are dynamically loaded from the `agents/` folder at startup

### 2.3 Query Flow

```
User Query
    │
    ▼
┌─────────────────┐
│   AgentOS       │
│   (Router)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Team Selection                   │
│  (Based on query content/description)    │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│    Team Orchestrator (Claude Sonnet 4)   │
│    Routes to appropriate specialist      │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│    Specialist Agent (Nova Lite)          │
│    - Uses tools for calculations         │
│    - Queries knowledge base if needed    │
│    - Searches web for latest info        │
└────────┬────────────────────────────────┘
         │
         ▼
    Response
```

---

## 3. Teams and Agents

### 3.1 Personal Finance Team

> *Financial foundation, compliance, and lifestyle planning for Indian users*

| Property | Value |
|----------|-------|
| **Team Name** | Personal Finance Team |
| **Orchestrator Model** | `anthropic.claude-sonnet-4-20250514-v1-0` |
| **Members** | 4 Agents |
| **Knowledge Base** | Financial Documents (ChromaDB) |
| **Focus Areas** | Budgeting, Tax Planning, Insurance, Real Estate |

#### 3.1.1 General Finance Advisor

| Property | Value |
|----------|-------|
| **Name** | General Finance Advisor |
| **Role** | Holistic Financial Advisor |
| **Model** | `amazon.nova-lite-v1-0` |
| **Knowledge Base** | None |

**Description:**  
Analyzes overall financial stability and provides foundational financial recommendations for Indian users.

**Capabilities:**
- Life and health insurance coverage recommendations using 10-20x annual income rule
- Emergency fund calculations using 3-6-12 Month Rule
- Spending vs investment ratio analysis using 50-30-20 rule

**Tools:**

| Tool | Description |
|------|-------------|
| `calculate_life_insurance_coverage` | Calculates recommended life insurance sum assured (10-20x annual income) |
| `calculate_emergency_fund` | Calculates ideal emergency fund based on job stability & dependents |
| `analyze_spending_ratio` | Analyzes spending vs savings using 50-30-20 rule |
| `SerperTools` | Web search for financial news and information |

**Example Queries:**
- "How much life insurance do I need if I earn ₹15 lakhs per year?"
- "What should be my emergency fund if my monthly expenses are ₹50,000?"
- "Am I saving enough? My income is ₹1 lakh/month and I save ₹15,000"

---

#### 3.1.2 Spending Analyst

| Property | Value |
|----------|-------|
| **Name** | Spending Analyst |
| **Role** | Expense Tracker & Analyst |
| **Model** | `amazon.nova-lite-v1-0` |
| **Knowledge Base** | None |

**Description:**  
Tracks and analyzes monthly expenses, identifies overspending patterns, and suggests budget corrections based on demographic benchmarks.

**Capabilities:**
- Cross-references spending data with income
- Benchmarks spending against user demographics (age group)
- Identifies areas of overspending compared to averages
- Provides actionable budget correction recommendations

**Tools:**

| Tool | Description |
|------|-------------|
| `get_spending_benchmarks` | Returns spending benchmarks by age group & category |
| `analyze_spending_ratio` | Analyzes spending vs savings using 50-30-20 rule |
| `SerperTools` | Web search for budgeting tips and information |

**Spending Categories Tracked:**
- Dining
- Entertainment
- Shopping
- Transportation
- Utilities
- Groceries

**Example Queries:**
- "Am I spending too much on dining out for my age group (30-40)?"
- "How does my spending compare to others in my age bracket?"
- "Where can I cut expenses to save more?"

---

#### 3.1.3 Tax Planning Assistant

| Property | Value |
|----------|-------|
| **Name** | Tax Planning Assistant |
| **Role** | Indian Tax Compliance Specialist |
| **Model** | `amazon.nova-lite-v1-0` |
| **Knowledge Base** | ✅ Financial Documents (income_tax_documents) |

**Description:**  
Specializes in Indian Income Tax optimization, helping users maximize deductions and choose the most beneficial tax regime.

**Capabilities:**
- Section 80C deductions calculation (PPF, ELSS, Insurance, EPF, etc.)
- Section 80D deductions for health insurance premiums
- Section 80CCD(1B) and 80CCD(2) for NPS contributions
- Old vs New Tax Regime comparison with recommendations

**Tools:**

| Tool | Description |
|------|-------------|
| `calculate_section_80c_deductions` | Calculates 80C deductions (limit: ₹1,50,000) |
| `calculate_section_80d_deductions` | Calculates health insurance deductions |
| `calculate_nps_deduction_80ccd` | Calculates NPS deductions under 80CCD(1B) & 80CCD(2) |
| `compare_tax_regimes` | Compares Old vs New tax regime with recommendations |
| `SerperTools` | Web search for latest tax updates |

**Key Tax Rules:**

| Section | Limit | Applicable Instruments |
|---------|-------|------------------------|
| 80C | ₹1,50,000 | PPF, ELSS, EPF, Life Insurance, Home Loan Principal, Tuition Fees |
| 80D | ₹25,000 / ₹50,000 | Health Insurance (self/senior parents) |
| 80CCD(1B) | ₹50,000 | Additional NPS contribution |
| 80CCD(2) | 10% of salary | Employer NPS contribution |

**Example Queries:**
- "How much tax can I save with NPS?"
- "Should I choose old or new tax regime? My salary is ₹18 lakhs"
- "Calculate my total 80C deductions"

---

#### 3.1.4 Home Planning Advisor

| Property | Value |
|----------|-------|
| **Name** | Home Planning Advisor |
| **Role** | Real Estate Planner |
| **Model** | `amazon.nova-lite-v1-0` |
| **Knowledge Base** | None |

**Description:**  
Guides real estate decisions including buy vs rent analysis and home loan affordability calculations to prevent users from becoming "house poor."

**Capabilities:**
- Buy vs Rent scenario analysis with property appreciation and rent inflation
- Home loan EMI affordability using FOIR (Fixed Obligation to Income Ratio)
- Considers opportunity cost, maintenance, and ownership expenses

**Tools:**

| Tool | Description |
|------|-------------|
| `calculate_buy_vs_rent` | Compares buying vs renting over a specified time period |
| `calculate_affordable_emi` | Calculates max EMI using FOIR rule (40-50% of income) |
| `SerperTools` | Web search for real estate trends |

**FOIR Rule Parameters:**
- Maximum EMIs: 40-50% of monthly income
- Default down payment: 20% of property value
- Default loan tenure: 20 years
- Default interest rate: 8.5%

**Example Queries:**
- "Should I buy or rent a ₹80 lakh apartment in Bangalore?"
- "How much home loan can I afford with ₹1.5 lakh monthly income?"
- "I already pay ₹20,000 car EMI. What's my home loan capacity?"

---

### 3.2 Investment Helper Team

> *Wealth accumulation, market research, and portfolio growth*

| Property | Value |
|----------|-------|
| **Team Name** | Investment Helper Team |
| **Orchestrator Model** | `anthropic.claude-sonnet-4-20250514-v1-0` |
| **Members** | 5 Agents |
| **Knowledge Base** | None (uses real-time data) |
| **Focus Areas** | Stock Analysis, Market Research, Portfolio Management, Investment Education |

#### 3.2.1 Stock Analyst

| Property | Value |
|----------|-------|
| **Name** | Stock Analyst |
| **Role** | Equity Researcher |
| **Model** | `amazon.nova-lite-v1-0` |
| **Knowledge Base** | None |

**Description:**  
Performs deep dives into specific stocks using real-time market data, providing fundamental analysis insights for both Indian and US markets.

**Capabilities:**
- Real-time stock metrics (P/E, EPS, Beta, Market Cap)
- Historical price trends and returns analysis
- Fundamental analysis insights
- Latest stock news and sentiment via web search

**Tools:**

| Tool | Description |
|------|-------------|
| `get_stock_metrics` | Fetches real-time stock metrics via YFinance |
| `get_stock_history` | Fetches historical price data (1d to 5y) |
| `SerperTools` | Web search for stock news and analysis |

**Stock Symbol Conventions:**
- **Indian NSE Stocks**: Use `.NS` suffix (e.g., `RELIANCE.NS`, `TCS.NS`, `INFY.NS`)
- **Indian BSE Stocks**: Use `.BO` suffix (e.g., `RELIANCE.BO`)
- **US Stocks**: Standard symbols (e.g., `AAPL`, `GOOGL`, `MSFT`)

**Metrics Returned:**
- Current Price
- P/E Ratio (Trailing & Forward)
- EPS (Earnings Per Share)
- Beta (Volatility measure)
- Market Cap
- Dividend Yield
- 52-Week High/Low
- 50 & 200 Day Moving Averages
- Volume
- Sector & Industry

**Example Queries:**
- "Analyze TCS stock for me"
- "What's the P/E ratio of Reliance?"
- "Show me Apple's performance over the last year"
- "Compare HDFC Bank and ICICI Bank fundamentals"

---

#### 3.2.2 Indian Market Analyst

| Property | Value |
|----------|-------|
| **Name** | Indian Market Analyst |
| **Role** | Domestic Market Strategist |
| **Model** | `amazon.nova-lite-v1-0` |
| **Knowledge Base** | None |

**Description:**  
Specializes in tracking and analyzing Indian stock markets, sector trends, and economic factors affecting domestic investments.

**Capabilities:**
- Nifty 50 and Sensex performance tracking
- Sector-specific index analysis (IT, Banking, Pharma, FMCG, Auto)
- Sector rotation and market sentiment analysis
- RBI policy and government announcement impact analysis

**Tools:**

| Tool | Description |
|------|-------------|
| `get_indian_market_overview` | Overview of all major Indian indices |
| `get_index_data` | Fetches specific index data |
| `get_stock_metrics` | Fetches individual stock metrics |
| `SerperTools` | Web search for Indian market news |

**Tracked Indian Indices:**

| Symbol | Index Name |
|--------|------------|
| `^NSEI` | Nifty 50 |
| `^BSESN` | BSE Sensex |
| `^NSEBANK` | Nifty Bank |
| `^CNXIT` | Nifty IT |
| `^CRSLDX` | Nifty 500 |
| `^CNXAUTO` | Nifty Auto |
| `^CNXPHARMA` | Nifty Pharma |
| `^CNXFMCG` | Nifty FMCG |

**Example Queries:**
- "How is the Indian IT sector performing?"
- "What's the Sensex trend today?"
- "Should I invest in banking stocks now?"
- "How is Nifty 50 doing this week?"

---

#### 3.2.3 Global Market Analyst

| Property | Value |
|----------|-------|
| **Name** | Global Market Analyst |
| **Role** | Global Market Strategist |
| **Model** | `amazon.nova-lite-v1-0` |
| **Knowledge Base** | None |

**Description:**  
Analyzes international markets and their impact on Indian investments, providing insights for global diversification strategies.

**Capabilities:**
- S&P 500, Nasdaq, Dow Jones tracking
- Global market trends and India correlation
- International diversification opportunities
- USD/INR currency impact analysis

**Tools:**

| Tool | Description |
|------|-------------|
| `get_global_market_overview` | Overview of global indices (US, Europe, Asia) |
| `get_index_data` | Fetches specific index data |
| `get_stock_metrics` | Fetches individual stock metrics |

**Tracked Global Indices:**

| Symbol | Index Name | Region |
|--------|------------|--------|
| `^GSPC` | S&P 500 | US |
| `^IXIC` | Nasdaq Composite | US |
| `^DJI` | Dow Jones Industrial Average | US |
| `^FTSE` | FTSE 100 | UK |
| `^N225` | Nikkei 225 | Japan |
| `000001.SS` | Shanghai Composite | China |
| `^HSI` | Hang Seng | Hong Kong |

**Example Queries:**
- "How are US tech stocks performing?"
- "What's the S&P 500 trend?"
- "Should I diversify into global markets?"
- "How does US market affect Indian stocks?"

---

#### 3.2.4 Investment Helper

| Property | Value |
|----------|-------|
| **Name** | Investment Helper |
| **Role** | Investment Education Specialist |
| **Model** | `amazon.nova-lite-v1-0` |
| **Knowledge Base** | None |

**Description:**  
Serves as a financial literacy expert, educating users about investment concepts, instruments, and market terminology.

**Capabilities:**
- Explains investment instruments (SGB, ELSS, NPS, PPF, SIP, Mutual Funds)
- Clarifies investment terminology and jargon
- Helps understand market data and stock metrics
- Demonstrates concepts with live market data

**Tools:**

| Tool | Description |
|------|-------------|
| `get_stock_metrics` | Demonstrates concepts with live stock data |
| `get_index_data` | Shows real index data for examples |
| `get_indian_market_overview` | Indian market context |
| `get_global_market_overview` | Global market context |
| `SerperTools` | Web search for latest information |

**Topics Covered:**
- Mutual funds (types, selection, expense ratios)
- Fixed income instruments (FDs, bonds, debt funds)
- Gold investments (Physical, ETF, SGB)
- Tax-saving instruments (ELSS, NPS, PPF)
- Retirement planning basics
- Insurance types (Term, ULIP, Endowment)
- Stock market basics and financial metrics

**Example Queries:**
- "What is a mutual fund?"
- "Explain P/E ratio to me"
- "What is SIP and how does it work?"
- "What's the difference between FD and debt funds?"
- "How does ELSS work for tax saving?"

---

#### 3.2.5 Portfolio Manager

| Property | Value |
|----------|-------|
| **Name** | Portfolio Manager |
| **Role** | Portfolio Analyst & Manager |
| **Model** | `amazon.nova-lite-v1-0` |
| **Knowledge Base** | None |

**Description:**  
Specializes in portfolio analysis, asset allocation recommendations, and rebalancing strategies based on age and risk tolerance.

**Capabilities:**
- Portfolio breakdown by market cap (Large/Mid/Small cap)
- Sector diversification analysis
- Age-based allocation using "100 Minus Age" Rule
- Rebalancing recommendations with specific amounts
- Concentration risk identification

**Tools:**

| Tool | Description |
|------|-------------|
| `analyze_portfolio_allocation` | Analyzes holdings by market cap & sector |
| `calculate_age_based_allocation` | Recommends allocation using 100-Age rule |
| `suggest_rebalancing` | Suggests rebalancing actions with amounts |
| `get_stock_metrics` | Fetches current stock prices for holdings |

**Market Cap Classification (INR):**
- **Large Cap**: ₹20,000 Cr+
- **Mid Cap**: ₹5,000 - ₹20,000 Cr
- **Small Cap**: < ₹5,000 Cr

**Portfolio Input Format (JSON):**
```json
[
  {"symbol": "RELIANCE.NS", "quantity": 10},
  {"symbol": "TCS.NS", "quantity": 5},
  {"symbol": "INFY.NS", "quantity": 15}
]
```

**Example Queries:**
- "Review my portfolio"
- "Should I rebalance my investments?"
- "What should be my equity-debt allocation at age 35?"
- "Analyze my sector diversification"

---

## 4. Tools Reference

### 4.1 Personal Finance Tools

| Tool Name | Category | Parameters | Returns |
|-----------|----------|------------|---------|
| `calculate_life_insurance_coverage` | Insurance | `annual_income`, `multiplier` (default: 15) | Min/Recommended/Max coverage |
| `calculate_emergency_fund` | Savings | `monthly_expenses`, `job_stability`, `dependents` | Emergency fund amount & months |
| `analyze_spending_ratio` | Budgeting | `monthly_income`, `monthly_savings`, `monthly_investments` | Spending breakdown & status |
| `get_spending_benchmarks` | Budgeting | `age_group`, `category` | Benchmark percentage for category |
| `calculate_section_80c_deductions` | Tax | `ppf_contribution`, `elss_investment`, `life_insurance_premium`, `home_loan_principal`, `children_tuition_fees`, `epf_contribution` | Breakdown & eligible deduction |
| `calculate_section_80d_deductions` | Tax | `self_health_premium`, `parents_health_premium`, `parents_senior_citizen`, `preventive_health_checkup` | 80D deduction details |
| `calculate_nps_deduction_80ccd` | Tax | `nps_contribution`, `gross_salary`, `employer_contribution` | NPS deduction breakdown |
| `compare_tax_regimes` | Tax | `gross_income`, deduction parameters | Old vs New regime comparison |
| `calculate_buy_vs_rent` | Real Estate | Property details, loan parameters, comparison years | Net cost comparison |
| `calculate_affordable_emi` | Real Estate | `monthly_income`, `existing_emis`, `foir_limit` | Affordable EMI & loan eligibility |

### 4.2 Investment Tools

| Tool Name | Category | Parameters | Returns |
|-----------|----------|------------|---------|
| `get_stock_metrics` | Stock Analysis | `symbol` | P/E, EPS, Beta, Market Cap, etc. |
| `get_stock_history` | Stock Analysis | `symbol`, `period` | Historical prices & returns |
| `get_index_data` | Market Analysis | `index_symbol` | Index value, change, 52-week range |
| `get_indian_market_overview` | Market Analysis | None | All Indian indices overview |
| `get_global_market_overview` | Market Analysis | None | Global indices overview |
| `analyze_portfolio_allocation` | Portfolio | `holdings` (JSON string) | Holdings breakdown by cap/sector |
| `calculate_age_based_allocation` | Portfolio | `age`, `risk_tolerance` | Recommended allocation |
| `suggest_rebalancing` | Portfolio | `current_equity_pct`, `current_debt_pct`, `age`, `portfolio_value` | Rebalancing recommendations |

### 4.3 External Tools

| Tool | Provider | Purpose |
|------|----------|---------|
| `SerperTools` | Serper API | Web search for news, articles, and latest information |
| `YFinance` | Yahoo Finance | Real-time stock prices and market data |

---

## 5. Knowledge Base & Data Sources

### 5.1 ChromaDB Vector Store

FinAgent uses **ChromaDB** as a vector database for storing and retrieving financial documents through RAG (Retrieval Augmented Generation).

**Configuration:**
```python
Knowledge(
    name="Financial Documents",
    description="Knowledge base for financial documents including income tax documents, personal financing documents, etc.",
    vector_db=ChromaDb(
        collection="financial_documents",
        path="tmp/chroma",
        persistent_client=True,
        embedder=SentenceTransformerEmbedder(id="all-MiniLM-L6-v2"),
    ),
    max_results=10,
)
```

| Property | Value |
|----------|-------|
| **Database** | ChromaDB |
| **Collection** | `financial_documents` |
| **Storage Path** | `tmp/chroma/` |
| **Persistence** | Enabled |
| **Embedder** | SentenceTransformer `all-MiniLM-L6-v2` |
| **Max Results** | 10 |

### 5.2 Document Types

| Metadata Type | Description | Used By |
|---------------|-------------|---------|
| `income_tax_documents` | Indian Income Tax guides, circulars, and rules | Tax Planning Assistant |
| `personal_financing_documents` | Personal finance guides and best practices | Personal Finance Team |

### 5.3 Document Ingestion

Documents are ingested using the PDF Reader with fixed-size chunking:

```python
reader = PDFReader(
    chunk_size=500,
    chunking_strategy=FixedSizeChunking(chunk_size=500, overlap=100)
)
```

| Parameter | Value |
|-----------|-------|
| **Reader** | PDFReader |
| **Chunk Size** | 500 characters |
| **Overlap** | 100 characters |

### 5.4 Real-Time Data Sources

| Source | Data Type | Integration |
|--------|-----------|-------------|
| **YFinance** | Stock prices, metrics, historical data | Direct Python API |
| **Serper API** | Web search, news articles | SerperTools integration |
| **Intuit IAM** | Authentication tokens | GraphQL API |

---

## 6. LLM Configuration & Models

### 6.1 Model Overview

FinAgent uses a two-tier model architecture:

| Tier | Model | Purpose | Used By |
|------|-------|---------|---------|
| **Orchestrator** | `anthropic.claude-sonnet-4-20250514-v1-0` | Team coordination & routing | Team level |
| **Specialist** | `amazon.nova-lite-v1-0` | Individual agent tasks | All agents |

### 6.2 Available Models

```python
# Default model
get_llm()  # amazon.nova-lite-v1-0

# Available options
get_llm("amazon.nova-lite-v1-0")           # Fast, cost-effective
get_llm("anthropic.claude-sonnet-4-20250514-v1-0")  # High capability
get_llm("gpt-5-nano-2025-08-07-oai")       # GPT variant
```

### 6.3 LLM Provider Configuration

FinAgent uses **OpenAILike** adapter to connect to a custom LLM execution service:

```python
OpenAILike(
    base_url=f"https://llmexecution.api.intuit.com/v3/lt/{model}",
    extra_headers={
        "intuit_experience_id": settings.experience_id,
        "intuit_originating_assetalias": "Intuit.coe.pecomplianceremediation",
        "Authorization": _get_auth_token(),
    },
)
```

### 6.4 Authentication

Authentication is handled via Intuit IAM with token caching:

```python
# Token acquisition via GraphQL
url = "https://identityinternal.api.intuit.com/v1/graphql"
IAM_MUTATION = """mutation identitySignInInternalApplicationWithPrivateAuth..."""
```

**Required Environment Variables:**

| Variable | Description |
|----------|-------------|
| `CLIENT_APP_SECRET` | Client application secret |
| `CLIENT_APP_ID` | Client application ID |
| `EXPERIENCE_ID` | Intuit experience ID |
| `PROFILE_ID` | Profile ID for authentication |
| `SERPER_API_KEY` | API key for Serper web search |

---

## 7. Financial Rules & Frameworks

### 7.1 Personal Finance Rules

| Rule | Formula | Usage |
|------|---------|-------|
| **10-20x Income Rule** | Life Insurance = 10-20 × Annual Income | Insurance coverage |
| **3-6-12 Month Rule** | Emergency Fund = Monthly Expenses × (3/6/12 months based on job stability) | Emergency fund |
| **50-30-20 Rule** | 50% Needs + 30% Wants + 20% Savings | Budgeting |
| **FOIR Rule** | Total EMIs ≤ 40-50% of Monthly Income | Loan affordability |

### 7.2 Investment Rules

| Rule | Formula | Usage |
|------|---------|-------|
| **100 Minus Age Rule** | Equity % = 100 - Age | Asset allocation |
| **5% Rebalancing Threshold** | Rebalance when allocation deviates >5% | Portfolio rebalancing |

### 7.3 Age-Based Allocation Adjustments

**Risk Tolerance Adjustments:**
```
Conservative: Base Equity - 10%
Moderate:     Base Equity + 0%
Aggressive:   Base Equity + 10%
```

**Equity Limits:**
- Minimum: 20%
- Maximum: 80%

### 7.4 Equity Breakdown by Age

| Age Group | Large Cap | Mid Cap | Small Cap | International |
|-----------|-----------|---------|-----------|---------------|
| < 35 | 40% | 35% | 15% | 10% |
| 35-50 | 50% | 30% | 10% | 10% |
| > 50 | 60% | 25% | 5% | 10% |

### 7.5 Debt Breakdown

| Instrument | Allocation |
|------------|------------|
| PPF/EPF | 40% |
| Debt Funds | 30% |
| Fixed Deposits | 20% |
| Bonds | 10% |

---

## 8. Technology Stack

### 8.1 Core Framework

| Component | Package | Version | Purpose |
|-----------|---------|---------|---------|
| **Agent Framework** | `agno` | ≥2.3.21 | Multi-agent orchestration |
| **Python** | Python | ≥3.12 | Runtime |

### 8.2 Agno Extensions

The project uses several Agno extensions:

```
agno[anthropic,chromadb,ddgs,openai,os,pdf,yfinance]
```

| Extension | Purpose |
|-----------|---------|
| `anthropic` | Claude model support |
| `chromadb` | Vector database integration |
| `ddgs` | DuckDuckGo search |
| `openai` | OpenAI-compatible API support |
| `os` | AgentOS server capabilities |
| `pdf` | PDF document processing |
| `yfinance` | Yahoo Finance data integration |

### 8.3 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `agno` | ≥2.3.21, <3.0.0 | Agent framework |
| `ddgs` | ≥9.10.0, <10.0.0 | DuckDuckGo search |
| `python-dotenv` | ≥1.0.0, <2.0.0 | Environment variable management |
| `sentence-transformers` | ≥5.2.0, <6.0.0 | Text embeddings for RAG |
| `pydantic-settings` | (via agno) | Configuration management |
| `yfinance` | (via agno) | Financial data API |
| `chromadb` | (via agno) | Vector database |
| `requests` | (via agno) | HTTP client |

### 8.4 External Services

| Service | Purpose | Authentication |
|---------|---------|----------------|
| Intuit LLM Execution API | LLM inference | IAM Token |
| Intuit IAM | Authentication | App ID + Secret |
| Serper API | Web search | API Key |
| Yahoo Finance | Market data | None (public) |

---

## 9. Project Structure

```
FinAgent/
├── main.py                      # Application entry point
├── settings.py                  # Pydantic settings configuration
├── pyproject.toml               # Project dependencies (Poetry)
├── poetry.lock                  # Locked dependencies
├── AGENTS.md                    # Agent overview documentation
├── DOCUMENTATION.md             # This comprehensive documentation
│
├── agents/                      # Agent definitions
│   ├── __init__.py              # Agent package exports
│   ├── investment_team.py       # Investment Helper Team (5 agents)
│   └── personal_finance_team.py # Personal Finance Team (4 agents)
│
├── core/                        # Core utilities
│   ├── __init__.py              # Core package exports
│   ├── llm.py                   # LLM configuration & auth
│   ├── loader.py                # Dynamic agent loader
│   └── ingestion.ipynb          # Knowledge base ingestion notebook
│
├── tmp/                         # Temporary storage
│   └── chroma/                  # ChromaDB persistent storage
│       └── chroma.sqlite3       # Vector database
│
└── test.ipynb                   # Testing notebook
```

### 9.1 Key Files

| File | Purpose |
|------|---------|
| `main.py` | Creates AgentOS instance and starts FastAPI server |
| `settings.py` | Loads environment variables via Pydantic |
| `agents/investment_team.py` | Defines 5 investment agents + tools + team |
| `agents/personal_finance_team.py` | Defines 4 finance agents + tools + team |
| `core/llm.py` | LLM factory with authentication |
| `core/loader.py` | Dynamic agent discovery and AgentOS creation |

---

## 10. Getting Started

### 10.1 Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)
- Access to Intuit IAM and LLM services
- Serper API key (for web search)

### 10.2 Installation

```bash
# Clone the repository
cd FinAgent

# Install dependencies using Poetry
poetry install

# Or using pip
pip install -e .
```

### 10.3 Environment Setup

Create a `.env` file in the project root:

```env
# Authentication
CLIENT_APP_ID=your_app_id
CLIENT_APP_SECRET=your_app_secret
PROFILE_ID=your_profile_id
EXPERIENCE_ID=your_experience_id

# External Services
SERPER_API_KEY=your_serper_api_key
```

### 10.4 Running the Server

```bash
# Using Poetry
poetry run python main.py

# Or directly
python main.py
```

The server will start on `http://localhost:5111` with hot-reload enabled.

### 10.5 Knowledge Base Setup

To ingest documents into the knowledge base:

1. Open `core/ingestion.ipynb` in Jupyter
2. Place PDF documents in the appropriate directory
3. Run the ingestion cells with appropriate metadata tags

```python
# Example: Ingest tax documents
kn.add_content(
    path="path/to/tax_documents/",
    reader=reader,
    metadata={"type": "income_tax_documents"},
)
```

### 10.6 API Usage

Once the server is running, you can interact with agents via the AgentOS API:

```bash
# Example: Query the Personal Finance Team
curl -X POST http://localhost:5111/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How much emergency fund do I need?", "team": "Personal Finance Team"}'
```

---

## Appendix

### A. Agent Summary Table

| Team | Agent | Role | Model | Tools Count |
|------|-------|------|-------|-------------|
| Personal Finance | General Finance Advisor | Holistic Financial Advisor | Nova Lite | 4 |
| Personal Finance | Spending Analyst | Expense Tracker & Analyst | Nova Lite | 3 |
| Personal Finance | Tax Planning Assistant | Indian Tax Compliance Specialist | Nova Lite | 5 |
| Personal Finance | Home Planning Advisor | Real Estate Planner | Nova Lite | 3 |
| Investment | Stock Analyst | Equity Researcher | Nova Lite | 3 |
| Investment | Indian Market Analyst | Domestic Market Strategist | Nova Lite | 4 |
| Investment | Global Market Analyst | Global Market Strategist | Nova Lite | 3 |
| Investment | Investment Helper | Investment Education Specialist | Nova Lite | 5 |
| Investment | Portfolio Manager | Portfolio Analyst & Manager | Nova Lite | 4 |

### B. Tool Dependencies

```
Personal Finance Tools (10):
├── calculate_life_insurance_coverage
├── calculate_emergency_fund
├── analyze_spending_ratio
├── get_spending_benchmarks
├── calculate_section_80c_deductions
├── calculate_section_80d_deductions
├── calculate_nps_deduction_80ccd
├── compare_tax_regimes
├── calculate_buy_vs_rent
└── calculate_affordable_emi

Investment Tools (8):
├── get_stock_metrics (YFinance)
├── get_stock_history (YFinance)
├── get_index_data (YFinance)
├── get_indian_market_overview (YFinance)
├── get_global_market_overview (YFinance)
├── analyze_portfolio_allocation (YFinance)
├── calculate_age_based_allocation
└── suggest_rebalancing

External Tools:
├── SerperTools (Web Search)
└── YFinance (Market Data)
```

---

*Documentation generated for FinAgent v0.1.0*  
*Last updated: January 2026*

