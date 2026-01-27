# FinAgent - Agents Overview

FinAgent is a multi-agent financial advisory system built with two specialized teams: **Personal Finance Team** and **Investment Helper Team**. Each team contains domain-specific agents with access to custom tools for financial calculations and market analysis.

---

## 🏠 Personal Finance Team

> *Financial foundation, compliance, and lifestyle planning*p[-'8ki
'9/i/"m9,;/';.'';=]][][]
]\
[]]

This team focuses on personal financial stability, tax optimization, and real estate decisions for Indian users.

### 1. General Finance Advisor

| **Role** | Holistic Financial Advisor |
|----------|---------------------------|
| **Purpose** | Analyzes overall financial stability and provides foundational financial recommendations |

**What it does:**
- Suggests life and health insurance coverage using the **10-20x annual income rule**
- Calculates ideal emergency fund size using the **3-6-12 Month Rule**
- Performs spending vs investment ratio analysis using the **50-30-20 rule**

**Tools:**
| Tool | Description |
|------|-------------|
| `calculate_life_insurance_coverage` | Recommends life insurance sum assured (10-20x annual income) |
| `calculate_emergency_fund` | Calculates emergency fund based on job stability & dependents |
| `analyze_spending_ratio` | Analyzes spending vs savings using 50-30-20 rule |

-[=[?o>:


=# 2. Spending Analyst

| **Role** | Expense Tracker & Analyst |
|----------|---------------------------|
| **Purpose** | Tracks and analyzes monthly expenses, identifies overspending, and suggests budget corrections |

**What it does:**
- Cross-references spending data with income
- Benchmarks spending against user demographics (age group)
- Identifies areas of overspending compared to averages
- Provides actionable budget correction recommendations

**Tools:**
| Tool | Description |
|------|-------------|
| `get_spending_benchmarks` | Returns spending benchmarks by age group & category |
| `analyze_spending_ratio` | Analyzes spending vs savings using 50-30-20 rule |

---

### 3. Tax Planning Assistant

| **Role** | Indian Tax Compliance Specialist |
|----------|----------------------------------|
| **Purpose** | Optimizes tax planning under Indian Income Tax rules |

**What it does:**
- Calculates Section 80C deductions (PPF, ELSS, Insurance, EPF, etc.)
- Calculates Section 80D deductions (Health Insurance premiums)
- Calculates Section 80CCD deductions (NPS contributions)
- Compares **Old vs New Tax Regimes** to recommend the most beneficial option

**Tools:**
| Tool | Description |
|------|-------------|
| `calculate_section_80c_deductions` | Calculates 80C deductions (limit: ₹1,50,000) |
| `calculate_section_80d_deductions` | Calculates 80D health insurance deductions |
| `calculate_nps_deduction_80ccd` | Calculates NPS deductions under 80CCD(1B) & 80CCD(2) |
| `compare_tax_regimes` | Compares Old vs New tax regime with recommendations |

---

### 4. Home Planning Advisor

| **Role** | Real Estate Planner |
|----------|---------------------|
| **Purpose** | Guides real estate decisions including buy vs rent analysis and home loan affordability |

**What it does:**
- Analyzes **Buy vs Rent** scenarios based on market rates and user liquidity
- Calculates affordable Home Loan EMI limits using **FOIR (Fixed Obligation to Income Ratio)**
- Prevents users from becoming "house poor" by over-committing to EMIs
- Considers property appreciation, rent inflation, and opportunity cost

**Tools:**
| Tool | Description |
|------|-------------|
| `calculate_buy_vs_rent` | Compares buying vs renting over a time period |
| `calculate_affordable_emi` | Calculates max EMI using FOIR rule (40-50% of income) |

---

## 📈 Investment Helper Team

> *Wealth accumulation, market research, and portfolio growth*

This team focuses on investment analysis, market research, and portfolio management.

### 1. Stock Analyst

| **Role** | Equity Researcher |
|----------|-------------------|
| **Purpose** | Performs deep dives into specific stocks using real-time market data |

**What it does:**
- Fetches and analyzes stock metrics (P/E, EPS, Beta, Market Cap)
- Analyzes historical price trends and returns
- Provides fundamental analysis insights
- Searches for latest stock news and sentiment

**Tools:**
| Tool | Description |
|------|-------------|
| `get_stock_metrics` | Fetches real-time stock metrics via YFinance |
| `get_stock_history` | Fetches historical price data (1d to 5y) |
| `SerperTools` | Web search for news and stock information |

---

### 2. Indian Market Analyst

| **Role** | Domestic Market Strategist |
|----------|---------------------------|
| **Purpose** | Tracks and analyzes Indian stock markets and economic factors |

**What it does:**
- Monitors **Nifty 50, Sensex** and sector-specific indices
- Analyzes sector rotations (IT, Banking, Pharma, FMCG, Auto)
- Provides insights on Indian economic factors affecting markets
- Tracks impact of RBI policies and government announcements

**Tools:**
| Tool | Description |
|------|-------------|
| `get_indian_market_overview` | Overview of all major Indian indices |
| `get_index_data` | Fetches specific index data |
| `get_stock_metrics` | Fetches individual stock metrics |
| `SerperTools` | Web search for market news |

---

### 3. Global Market Analyst

| **Role** | Global Market Strategist |
|----------|--------------------------|
| **Purpose** | Analyzes international markets and their impact on Indian investments |

**What it does:**
- Tracks **S&P 500, Nasdaq, Dow Jones** and other global indices
- Analyzes global market trends and their impact on Indian markets
- Identifies international diversification opportunities
- Monitors **USD/INR** currency movements

**Tools:**
| Tool | Description |
|------|-------------|
| `get_global_market_overview` | Overview of global indices (US, Europe, Asia) |
| `get_index_data` | Fetches specific index data |
| `get_stock_metrics` | Fetches individual stock metrics |

---

### 4. Investment Helper

| **Role** | Investment Education Specialist |
|----------|--------------------------------|
| **Purpose** | Educates users about investment concepts, instruments, and financial literacy |

**What it does:**
- Explains investment instruments (SGB, ELSS, NPS, PPF, SIP, Mutual Funds)
- Clarifies investment terminology and jargon
- Helps users understand market data and stock metrics
- Covers topics: mutual funds, fixed income, gold investments, tax-saving instruments

**Tools:**
| Tool | Description |
|------|-------------|
| `get_stock_metrics` | Demonstrates concepts with live stock data |
| `get_index_data` | Shows real index data for examples |
| `get_indian_market_overview` | Indian market context |
| `get_global_market_overview` | Global market context |
| `SerperTools` | Web search for latest information |

---

### 5. Portfolio Manager

| **Role** | Portfolio Analyst & Manager |
|----------|----------------------------|
| **Purpose** | Analyzes portfolios and provides allocation/rebalancing recommendations |

**What it does:**
- Reviews and analyzes current holdings
- Breaks down portfolio by market cap (Large/Mid/Small cap)
- Analyzes sector diversification
- Suggests rebalancing using the **"100 Minus Age" Rule**
- Tailors risk exposure to user's age and risk tolerance

**Tools:**
| Tool | Description |
|------|-------------|
| `analyze_portfolio_allocation` | Analyzes holdings by market cap & sector |
| `calculate_age_based_allocation` | Recommends allocation using 100-Age rule |
| `suggest_rebalancing` | Suggests rebalancing actions with amounts |
| `get_stock_metrics` | Fetches current stock prices for holdings |

---

## 🔧 Tools Summary

### Personal Finance Tools (10 tools)

| Tool | Category | Purpose |
|------|----------|---------|
| `calculate_life_insurance_coverage` | Insurance | 10-20x income rule for sum assured |
| `calculate_emergency_fund` | Savings | 3-6-12 month rule based on stability |
| `analyze_spending_ratio` | Budgeting | 50-30-20 rule analysis |
| `get_spending_benchmarks` | Budgeting | Age-based spending benchmarks |
| `calculate_section_80c_deductions` | Tax | Section 80C limit ₹1.5L |
| `calculate_section_80d_deductions` | Tax | Health insurance deductions |
| `calculate_nps_deduction_80ccd` | Tax | NPS additional ₹50K deduction |
| `compare_tax_regimes` | Tax | Old vs New regime comparison |
| `calculate_buy_vs_rent` | Real Estate | Buy vs rent scenario analysis |
| `calculate_affordable_emi` | Real Estate | FOIR-based EMI calculation |

### Investment Tools (9 tools)

| Tool | Category | Purpose |
|------|----------|---------|
| `get_stock_metrics` | Stock Analysis | Real-time P/E, EPS, Beta, etc. |
| `get_stock_history` | Stock Analysis | Historical price data |
| `get_index_data` | Market Analysis | Index performance data |
| `get_indian_market_overview` | Market Analysis | Indian indices overview |
| `get_global_market_overview` | Market Analysis | Global indices overview |
| `analyze_portfolio_allocation` | Portfolio | Holdings breakdown by cap/sector |
| `calculate_age_based_allocation` | Portfolio | 100-Age allocation rule |
| `suggest_rebalancing` | Portfolio | Rebalancing recommendations |
| `SerperTools` | Research | Web search for news & info |

---

## 📊 Architecture

```
FinAgent
├── Personal Finance Team
│   ├── General Finance Advisor (insurance, emergency fund, spending)
│   ├── Spending Analyst (budget tracking, benchmarks)
│   ├── Tax Planning Assistant (80C, 80D, 80CCD, regime comparison)
│   └── Home Planning Advisor (buy vs rent, EMI affordability)
│
└── Investment Helper Team
    ├── Stock Analyst (equity research, fundamentals)
    ├── Indian Market Analyst (Nifty, Sensex, sectors)
    ├── Global Market Analyst (S&P 500, Nasdaq, global)
    ├── Investment Helper (education, concepts)
    └── Portfolio Manager (allocation, rebalancing)
```

---

## 🎯 Key Financial Rules Used

| Rule | Description | Agent |
|------|-------------|-------|
| **10-20x Income Rule** | Life insurance = 10-20x annual income | General Finance Advisor |
| **3-6-12 Month Rule** | Emergency fund based on job stability | General Finance Advisor |
| **50-30-20 Rule** | 50% needs, 30% wants, 20% savings | General Finance Advisor, Spending Analyst |
| **100 Minus Age Rule** | Equity % = 100 - Age | Portfolio Manager |
| **FOIR Rule** | EMIs ≤ 40-50% of income | Home Planning Advisor |
| **5% Rebalancing Threshold** | Rebalance when allocation deviates >5% | Portfolio Manager |

