# FinAgent - Agents Overview

FinAgent is a multi-agent financial advisory system built with specialized teams. The system has been optimized from 9 agents to 5 agents organized in 2 specialized teams, plus a meta-team for unified routing.

---

## 🏦 Financial Advisor Team (Meta-Team)

> *Unified financial guidance with intelligent routing*

This is the top-level team that orchestrates between specialized teams. It automatically routes queries to the appropriate team based on the context.

**Structure:**
- Personal Finance Team (2 agents)
- Investment Helper Team (3 agents)

**What it does:**
- Analyzes incoming queries and routes to the appropriate specialized team
- Coordinates between teams for queries spanning multiple domains
- Provides integrated advice considering both personal finance and investment aspects

**Use this team for:** Any financial query - it will automatically route to the appropriate specialists.

---

## 🏠 Personal Finance Team

> *Financial foundation, compliance, and lifestyle planning*

This team focuses on personal financial stability, tax optimization, and real estate decisions for Indian users. **Consolidated from 4 agents to 2 for improved efficiency.**

### 1. General Finance & Lifestyle Advisor

| **Role** | Holistic Financial Planning & Lifestyle Specialist |
|----------|---------------------------------------------------|
| **Purpose** | Comprehensive financial planning covering overall financial stability, insurance, emergency funds, spending analysis, budgeting, home planning, retirement planning, and EPF/VPF calculations |

**What it does:**
- **Insurance & Protection**: Recommends life insurance coverage using the **10-20x annual income rule**
- **Emergency Fund**: Calculates ideal emergency fund size using the **3-6-12 Month Rule**
- **Spending Analysis**: Performs spending vs investment ratio analysis using the **50-30-20 rule**
- **Budgeting**: Benchmarks spending against demographics (age group) for various categories
- **Home Planning**: Buy vs Rent analysis, affordable EMI limits using **FOIR rule**
- **Retirement**: Plans retirement corpus based on expenses and inflation
- **EPF/VPF**: Calculates EPF/VPF returns and maturity amounts

**Tools:**
| Tool | Description |
|------|-------------|
| `calculate_life_insurance_coverage` | Recommends life insurance sum assured (10-20x annual income) |
| `calculate_emergency_fund` | Calculates emergency fund based on job stability & dependents (3-6-12 months) |
| `analyze_spending_ratio` | Analyzes spending vs savings using 50-30-20 rule |
| `get_spending_benchmarks` | Returns spending benchmarks by age group & category |
| `calculate_buy_vs_rent` | Compares buying vs renting over a time period |
| `calculate_affordable_emi` | Calculates max EMI using FOIR rule (40-50% of income) |
| `calculate_section_24_interest` | Home loan interest deduction (Section 24) |
| `calculate_retirement_corpus` | Required retirement corpus calculation |
| `calculate_epf_vpf_returns` | EPF/VPF maturity and returns projection |
| `SerperTools` | Web search for latest financial information |

**Example Queries:**
- "How much life insurance do I need?"
- "Calculate my emergency fund for 6 months"
- "Am I spending too much on dining out?"
- "Should I buy or rent a house?"
- "Can I afford this home loan?"
- "Plan my retirement corpus"
- "Calculate EPF maturity amount"

---

### 2. Tax & Compliance Specialist

| **Role** | Indian Tax Optimization & Compliance Expert |
|----------|---------------------------------------------|
| **Purpose** | Tax planning and compliance specialist with deep knowledge of Indian Income Tax rules |

**What it does:**
- **HRA Exemption**: Calculates House Rent Allowance tax exemption for salaried employees
- **Section 80C**: Calculates deductions for PPF, ELSS, Insurance, EPF, home loan principal (limit: ₹1,50,000)
- **Section 80D**: Calculates health insurance premium deductions
- **Section 80CCD**: Calculates NPS deductions (80CCD(1B): additional ₹50,000; 80CCD(2): employer contribution)
- **Section 24**: Home loan interest deduction (up to ₹2,00,000 for self-occupied)
- **LTA Exemption**: Leave Travel Allowance exemption calculation
- **Capital Gains Tax**: Tax on investment gains (imported from Investment Team)
- **Tax Regime Comparison**: Compares Old vs New tax regime with recommendations

**Tools:**
| Tool | Description |
|------|-------------|
| `calculate_hra_exemption` | HRA tax exemption for salaried employees |
| `calculate_lta_exemption` | LTA exemption for domestic travel |
| `calculate_section_80c_deductions` | Section 80C deductions (limit: ₹1.5L) |
| `calculate_section_80d_deductions` | Section 80D health insurance deductions |
| `calculate_nps_deduction_80ccd` | NPS deductions under 80CCD(1B) & 80CCD(2) |
| `calculate_section_24_interest` | Home loan interest deduction (Section 24) |
| `calculate_capital_gains_tax` | Capital gains tax on investments |
| `compare_tax_regimes` | Old vs New regime comparison |
| `SerperTools` | Web search for latest tax updates |
| Knowledge Base | Access to income tax documents |

**Example Queries:**
- "Calculate my HRA exemption"
- "How much can I save under Section 80C?"
- "What are my Section 80D deductions?"
- "Should I choose old or new tax regime?"
- "Calculate capital gains tax on stock sale"
- "How to optimize my salary structure?"
- "NPS tax benefits explanation"

**Tax Regime Comparison:**
- **Old Regime**: Standard deduction ₹50K, allows all deductions (80C, 80D, HRA, LTA, etc.)
- **New Regime**: Standard deduction ₹75K, no other deductions allowed

---

## 📈 Investment Helper Team

> *Wealth accumulation, market research, and portfolio growth*

This team focuses on investment analysis, market research, and portfolio management. **Consolidated from 5 agents to 3 for improved efficiency.**

### 1. Market Intelligence Agent

| **Role** | Comprehensive Market Analyst |
|----------|------------------------------|
| **Purpose** | Performs comprehensive market research covering stocks, indices, sectors, and global markets |

**What it does:**
- **Stock Analysis**: Deep dives into specific stocks (Indian & US) with real-time metrics
- **Indian Markets**: Tracks Nifty 50, Sensex, sector indices (IT, Banking, Pharma, FMCG, Auto)
- **Global Markets**: Analyzes S&P 500, Nasdaq, Dow Jones, and impact on Indian markets
- **Historical Analysis**: Price trends and returns analysis
- **News & Sentiment**: Latest market news and sentiment analysis

**Stock Symbol Conventions:**
- Indian stocks: `.NS` suffix for NSE (e.g., `RELIANCE.NS`, `TCS.NS`, `INFY.NS`)
- US stocks: Standard symbols (e.g., `AAPL`, `GOOGL`, `MSFT`)

**Tools:**
| Tool | Description |
|------|-------------|
| `get_stock_metrics` | Real-time stock metrics (P/E, EPS, Beta, Market Cap) via YFinance |
| `get_stock_history` | Historical price data (1d to 5y) |
| `get_index_data` | Specific index data (Nifty, Sensex, S&P 500, etc.) |
| `get_indian_market_overview` | Overview of all major Indian indices |
| `get_global_market_overview` | Overview of global indices (US, Europe, Asia) |
| `SerperTools` | Web search for stock news and market information |

**Example Queries:**
- "Analyze TCS stock"
- "How is the IT sector performing?"
- "Compare Nifty 50 and Sensex"
- "What's the S&P 500 trend?"
- "Should I invest in banking stocks?"
- "Impact of US markets on India"
- "Get Reliance stock fundamentals"

---

### 2. Investment Advisor

| **Role** | Investment Education & Planning Specialist |
|----------|-------------------------------------------|
| **Purpose** | Educates about investment concepts, instruments, and provides SIP planning and goal-based investing guidance |

**What it does:**
- **Investment Education**: Explains mutual funds, ELSS, NPS, PPF, bonds, gold, equity, debt funds
- **SIP Planning**: Calculates SIP returns with step-up scenarios
- **Goal-Based Planning**: Plans for child's education, marriage, retirement, home purchase
- **Tax Guidance**: Explains LTCG, STCG, and capital gains tax
- **Financial Literacy**: Clarifies investment terminology and concepts
- **Instrument Comparison**: Compares different investment options with pros/cons

**Key Investment Instruments Covered:**
- **Mutual Funds**: Equity, Debt, Hybrid, Index, ELSS
- **Tax-Saving**: ELSS (80C), NPS (80CCD), PPF (80C)
- **Fixed Income**: PPF, EPF, FDs, Bonds, Debt Funds
- **Gold**: Physical, ETFs, Sovereign Gold Bonds, Digital
- **Equity**: Direct stocks, Equity Funds, Index Funds

**Tools:**
| Tool | Description |
|------|-------------|
| `calculate_sip_returns` | SIP returns with step-up scenarios |
| `calculate_sip_for_goal` | Calculate monthly SIP needed for a goal |
| `calculate_goal_corpus` | Comprehensive goal planning with inflation adjustment |
| `calculate_capital_gains_tax` | Capital gains tax calculation |
| `get_stock_metrics` | Live stock data for examples |
| `get_index_data` | Index data for demonstrations |
| `SerperTools` | Web search for latest investment information |

**Example Queries:**
- "What is a mutual fund?"
- "Calculate SIP returns for ₹10K/month"
- "How much SIP for ₹1 crore in 15 years?"
- "Plan for child's education (₹50 lakhs in 15 years)"
- "Explain ELSS vs PPF"
- "What is capital gains tax?"
- "SIP vs lump sum investment"
- "Best tax-saving investments?"

**Capital Gains Tax Rules:**
- **Equity** (>365 days): LTCG 12.5% on gains above ₹1.25L
- **Equity** (≤365 days): STCG 20%
- **Debt** (>36 months): LTCG 12.5% without indexation
- **Debt** (≤36 months): STCG at income slab rate

---

### 3. Portfolio Manager

| **Role** | Portfolio Analyst & Manager |
|----------|----------------------------|
| **Purpose** | Analyzes portfolios and provides allocation/rebalancing recommendations |

**What it does:**
- **Portfolio Analysis**: Reviews holdings by market cap (Large/Mid/Small) and sector
- **Asset Allocation**: Recommends allocation using **110-Age Rule** (or 120-Age for aggressive)
- **Rebalancing**: Suggests rebalancing when allocation deviates >5%
- **Tax Impact**: Calculates tax implications of rebalancing
- **Goal Alignment**: Aligns portfolio with financial goals
- **SIP Planning**: Suggests SIP contributions for systematic portfolio building

**Modern Allocation Rules:**
- **110 Minus Age**: Standard for most investors (e.g., age 30 → 80% equity)
- **120 Minus Age**: Aggressive for young investors (<40)
- **100 Minus Age**: Conservative for risk-averse or near-retirement
- **Gold**: 5-10% allocation for diversification and inflation hedge

**Tools:**
| Tool | Description |
|------|-------------|
| `analyze_portfolio_allocation` | Analyzes holdings by market cap & sector |
| `calculate_age_based_allocation` | Recommends allocation using 110-Age or 120-Age rule |
| `suggest_rebalancing` | Suggests rebalancing actions with specific amounts |
| `calculate_capital_gains_tax` | Tax impact of selling positions |
| `calculate_sip_returns` | Future portfolio growth with SIP |
| `calculate_sip_for_goal` | SIP needed for specific goals |
| `calculate_goal_corpus` | Goal planning with existing portfolio |
| `get_stock_metrics` | Fetches current stock prices for holdings |

**Example Queries:**
- "Review my portfolio"
- "What should be my equity-debt allocation at age 35?"
- "Should I rebalance my investments?"
- "Calculate tax on selling stocks"
- "How much SIP to add?"
- "Plan for child's education with existing portfolio"
- "Analyze my sector diversification"

---

## 🔧 Tools Summary

### Personal Finance Tools (17 tools)

| Tool | Category | Purpose |
|------|----------|---------|
| `calculate_life_insurance_coverage` | Insurance | 10-20x income rule for sum assured |
| `calculate_emergency_fund` | Savings | 3-6-12 month rule based on stability |
| `analyze_spending_ratio` | Budgeting | 50-30-20 rule analysis |
| `get_spending_benchmarks` | Budgeting | Age-based spending benchmarks |
| `calculate_buy_vs_rent` | Real Estate | Buy vs rent scenario analysis |
| `calculate_affordable_emi` | Real Estate | FOIR-based EMI calculation |
| `calculate_section_24_interest` | Tax | Home loan interest deduction |
| `calculate_retirement_corpus` | Retirement | Required retirement corpus |
| `calculate_epf_vpf_returns` | Retirement | EPF/VPF maturity projection |
| `calculate_hra_exemption` | Tax | HRA tax exemption |
| `calculate_lta_exemption` | Tax | LTA exemption for travel |
| `calculate_section_80c_deductions` | Tax | Section 80C limit ₹1.5L |
| `calculate_section_80d_deductions` | Tax | Health insurance deductions |
| `calculate_nps_deduction_80ccd` | Tax | NPS additional ₹50K deduction |
| `compare_tax_regimes` | Tax | Old vs New regime comparison |
| `calculate_capital_gains_tax` | Tax | Capital gains tax calculation |
| `SerperTools` | Research | Web search |

### Investment Tools (13 tools)

| Tool | Category | Purpose |
|------|----------|---------|
| `get_stock_metrics` | Stock Analysis | Real-time P/E, EPS, Beta, etc. |
| `get_stock_history` | Stock Analysis | Historical price data |
| `get_index_data` | Market Analysis | Index performance data |
| `get_indian_market_overview` | Market Analysis | Indian indices overview |
| `get_global_market_overview` | Market Analysis | Global indices overview |
| `calculate_sip_returns` | SIP Planning | SIP returns with step-up |
| `calculate_sip_for_goal` | SIP Planning | Monthly SIP for goal |
| `calculate_goal_corpus` | Goal Planning | Comprehensive goal planning |
| `calculate_capital_gains_tax` | Tax | Capital gains tax |
| `analyze_portfolio_allocation` | Portfolio | Holdings breakdown by cap/sector |
| `calculate_age_based_allocation` | Portfolio | 110-Age or 120-Age rule |
| `suggest_rebalancing` | Portfolio | Rebalancing recommendations |
| `SerperTools` | Research | Web search for news & info |

---

## 📊 Architecture

```
FinAgent
│
├── Financial Advisor Team (Meta-Team)
│   │
│   ├── Personal Finance Team (2 agents)
│   │   ├── General Finance & Lifestyle Advisor
│   │   │   ├── Insurance & Emergency Fund
│   │   │   ├── Spending Analysis & Budgeting
│   │   │   ├── Home Planning (Buy vs Rent, EMI)
│   │   │   └── Retirement & EPF/VPF
│   │   │
│   │   └── Tax & Compliance Specialist
│   │       ├── HRA & LTA Exemptions
│   │       ├── Section 80C, 80D, 80CCD
│   │       ├── Section 24 (Home Loan Interest)
│   │       ├── Capital Gains Tax
│   │       └── Tax Regime Comparison
│   │
│   └── Investment Helper Team (3 agents)
│       ├── Market Intelligence Agent
│       │   ├── Stock Analysis (Indian & US)
│       │   ├── Indian Markets (Nifty, Sensex, Sectors)
│       │   └── Global Markets (S&P 500, Nasdaq)
│       │
│       ├── Investment Advisor
│       │   ├── Investment Education
│       │   ├── SIP Planning & Calculations
│       │   ├── Goal-Based Investing
│       │   └── Capital Gains Tax Guidance
│       │
│       └── Portfolio Manager
│           ├── Portfolio Analysis & Allocation
│           ├── Rebalancing (with Tax Impact)
│           └── Goal Alignment & SIP Planning
```

---

## 🎯 Key Financial Rules Used

| Rule | Formula | Agent | Usage |
|------|---------|-------|-------|
| **10-20x Income Rule** | Life Insurance = 10-20 × Annual Income | General Finance & Lifestyle Advisor | Insurance coverage |
| **3-6-12 Month Rule** | Emergency Fund = Expenses × (3/6/12 months) | General Finance & Lifestyle Advisor | Emergency savings based on job stability |
| **50-30-20 Rule** | 50% needs, 30% wants, 20% savings | General Finance & Lifestyle Advisor | Budgeting framework |
| **110 Minus Age Rule** | Equity % = 110 - Age | Portfolio Manager | Modern asset allocation |
| **120 Minus Age Rule** | Equity % = 120 - Age | Portfolio Manager | Aggressive allocation for young investors |
| **100 Minus Age Rule** | Equity % = 100 - Age | Portfolio Manager | Conservative allocation |
| **FOIR Rule** | EMIs ≤ 40-50% of Income | General Finance & Lifestyle Advisor | Loan affordability |
| **5% Rebalancing Threshold** | Rebalance when allocation deviates >5% | Portfolio Manager | Portfolio maintenance |

---

## 🔄 Optimization Benefits

The system has been consolidated from **9 agents to 5 agents** for improved efficiency:

### Before (9 agents):
- Personal Finance: 4 agents (General Finance, Spending Analyst, Tax Assistant, Home Advisor)
- Investment: 5 agents (Stock Analyst, Indian Market Analyst, Global Market Analyst, Investment Helper, Portfolio Manager)

### After (5 agents):
- Personal Finance: 2 agents (General Finance & Lifestyle Advisor, Tax & Compliance Specialist)
- Investment: 3 agents (Market Intelligence Agent, Investment Advisor, Portfolio Manager)

### Benefits:
- **Reduced Redundancy**: No overlap in agent responsibilities
- **Clearer Routing**: Distinct domains and specializations
- **Improved Efficiency**: Agents have exactly the tools they need
- **Comprehensive Coverage**: All capabilities preserved despite consolidation
- **Better Performance**: Fewer agent handoffs, faster responses

---

## 📋 Usage Examples

### Personal Finance Queries

```python
# Emergency Fund
"I earn ₹80,000/month and spend ₹50,000. How much emergency fund do I need?"

# Insurance
"Calculate life insurance coverage for ₹12 lakh annual income"

# Home Planning
"Should I buy a ₹80 lakh house or rent for ₹25K/month?"

# Tax Optimization
"Compare old vs new tax regime for ₹15 lakh income with ₹1.5L in 80C"

# Spending Analysis
"Am I overspending? Income ₹1L, savings ₹15K, investments ₹10K"
```

### Investment Queries

```python
# Stock Analysis
"Analyze TCS stock and its fundamentals"

# Market Trends
"How is the banking sector performing?"

# SIP Planning
"Calculate SIP needed for ₹1 crore in 15 years"

# Goal Planning
"Plan investment for child's education (₹50 lakhs in 15 years)"

# Portfolio Review
"Review my portfolio: 10 Reliance, 5 TCS, 20 Infosys (age 35)"

# Tax Impact
"Calculate capital gains tax if I sell 100 shares bought at ₹1000, now ₹1500, held 2 years"
```

---

## 🚀 Getting Started

To use FinAgent:

1. **General Queries**: Use the **Financial Advisor Team** - it will auto-route to specialists
2. **Personal Finance**: Direct queries to **Personal Finance Team**
3. **Investments**: Direct queries to **Investment Helper Team**

The system automatically determines the best agent to handle your query based on the context.

---

## 💡 Important Notes

- All tax calculations follow **Indian Income Tax Act (FY 2024-25)**
- Market data is real-time via **YFinance API**
- Financial rules are India-specific
- Always consult certified financial advisors for personalized advice
- Past performance doesn't guarantee future returns
- Consider risk factors before making investment decisions

---

*Last Updated: January 2026*
*FinAgent v0.2.0 - Optimized Agent Structure*
