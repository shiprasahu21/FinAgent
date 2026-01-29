# FinAgent - Backend Architecture

> **AI-Powered Financial Advisory System for Indian Users**
> Optimized multi-agent system: 9 → 5 agents | 2 specialized teams | Real-time market data

## Quick Reference

| Team | Agents | Primary Focus | Key Tools |
|------|--------|---------------|-----------|
| **Personal Finance** | 2 | Financial stability, tax optimization, lifestyle planning | 17 tools (insurance, emergency fund, tax calculations, home planning) |
| **Investment Helper** | 3 | Market analysis, portfolio management, investment education | 13 tools (stock metrics, SIP planning, portfolio analysis) |

**Technology Stack:** Agno v2.3.21+ \| Claude Sonnet 4 (orchestrator) \| Amazon Nova Lite (agents) \| ChromaDB \| YFinance \| FastAPI

**Stock Symbols:** Indian stocks use `.NS` suffix (e.g., `TCS.NS`, `RELIANCE.NS`) \| US stocks use standard symbols (e.g., `AAPL`, `MSFT`)

---

## System Architecture

**Meta-Team:** Financial Advisor Team orchestrates between specialized teams with intelligent routing. Use for any financial query - automatically routes to appropriate specialists.

---

## 🏠 Personal Finance Team

*Consolidated from 4 agents to 2 for improved efficiency*

### 1. General Finance & Lifestyle Advisor

**Scope:** Insurance, emergency funds, spending analysis, budgeting, home planning, retirement, EPF/VPF

**Capabilities:**
- Life insurance coverage (10-20x income rule)
- Emergency fund sizing (3-6-12 month rule based on job stability)
- Spending analysis & budgeting (50-30-20 rule + age-based benchmarks)
- Buy vs Rent analysis with FOIR rule (40-50% EMI limit)
- Retirement corpus planning
- EPF/VPF returns projection

**Tools:** 9 tools (see [Tools Summary](#-tools-summary)) + SerperTools for web search

### 2. Tax & Compliance Specialist

**Scope:** Indian Income Tax optimization and compliance (FY 2024-25)

**Capabilities:**
- HRA & LTA exemptions for salaried employees
- Section 80C deductions (PPF, ELSS, insurance, EPF, home loan principal - limit: ₹1.5L)
- Section 80D (health insurance) & 80CCD (NPS - additional ₹50K)
- Section 24 home loan interest deduction (up to ₹2L for self-occupied)
- Capital gains tax calculation (equity & debt)
- Tax regime comparison: Old (₹50K std deduction + all deductions) vs New (₹75K std deduction, no other deductions)

**Tools:** 8 tools (see [Tools Summary](#-tools-summary)) + SerperTools + Knowledge Base (RAG-powered tax documents)

---

## 📈 Investment Helper Team

*Consolidated from 5 agents to 3 for improved efficiency*

### 1. Market Intelligence Agent

**Scope:** Stock analysis, market tracking, sector research (Indian & global)

**Capabilities:**
- Real-time stock metrics (P/E, EPS, Beta, Market Cap) for Indian (NSE/BSE) & US markets
- Indian indices: Nifty 50, Sensex, sector indices (IT, Banking, Pharma, FMCG, Auto)
- Global indices: S&P 500, Nasdaq, Dow Jones
- Historical price analysis (1d to 5y)
- Market news & sentiment via web search

**Tools:** 5 market analysis tools (see [Tools Summary](#-tools-summary)) + SerperTools

### 2. Investment Advisor

**Scope:** Investment education, SIP planning, goal-based investing

**Capabilities:**
- Investment education: Mutual funds (equity, debt, hybrid, index, ELSS), NPS, PPF, bonds, gold, equity
- SIP planning with step-up scenarios and goal-based calculations
- Goal planning: education, marriage, retirement, home purchase
- Tax guidance: LTCG, STCG, capital gains tax
- Instrument comparison with pros/cons

**Tools:** 7 tools including SIP calculators and goal planning (see [Tools Summary](#-tools-summary)) + SerperTools

### 3. Portfolio Manager

**Scope:** Portfolio analysis, asset allocation, rebalancing, goal alignment

**Capabilities:**
- Portfolio analysis by market cap (Large/Mid/Small) and sector
- Age-based allocation: 110-Age (standard), 120-Age (aggressive), 100-Age (conservative)
- Rebalancing recommendations when deviation >5%
- Tax impact calculation for portfolio changes
- Goal-aligned portfolio building with SIP planning
- Gold allocation (5-10% for diversification)

**Tools:** 8 tools including portfolio analysis and rebalancing (see [Tools Summary](#-tools-summary))

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

## Financial Rules & Tax Framework

| Rule/Tax | Formula/Rate | Usage |
|----------|--------------|-------|
| **10-20x Income** | Life Insurance = 10-20 × Annual Income | Insurance coverage |
| **3-6-12 Month** | Emergency Fund = Expenses × (3/6/12 months) | Emergency savings (job stability based) |
| **50-30-20** | 50% needs + 30% wants + 20% savings | Budgeting |
| **110/120/100-Age** | Equity % = 110/120/100 - Age | Asset allocation (standard/aggressive/conservative) |
| **FOIR** | EMIs ≤ 40-50% of Income | Loan affordability |
| **Rebalancing** | When allocation deviates >5% | Portfolio maintenance |
| **LTCG Equity** | 12.5% on gains >₹1.25L (>365 days) | Long-term capital gains |
| **STCG Equity** | 20% (≤365 days) | Short-term capital gains |
| **LTCG Debt** | 12.5% without indexation (>36 months) | Long-term capital gains |
| **STCG Debt** | At income slab rate (≤36 months) | Short-term capital gains |
| **Section 80C** | Limit: ₹1.5L | PPF, ELSS, insurance, EPF, home loan principal |
| **Section 80D** | Health insurance deductions | Age-based limits |
| **Section 80CCD(1B)** | Additional ₹50K for NPS | Extra NPS deduction |
| **Section 24** | Up to ₹2L | Home loan interest (self-occupied) |

---

## Optimization Summary

**9 → 5 agents consolidation benefits:**
- Reduced redundancy & clearer routing
- Improved efficiency & faster responses
- All capabilities preserved with better organization

---

## Example Queries

**Personal Finance:** Emergency fund calculation | Life insurance coverage | Buy vs Rent | Tax regime comparison | Spending analysis | HRA/LTA exemptions | Retirement planning

**Investment:** Stock analysis (TCS.NS, RELIANCE.NS, AAPL) | Market trends (IT, Banking, Pharma) | SIP planning for goals | Portfolio review & rebalancing | Capital gains tax | Sector performance

**Usage:** Use Financial Advisor Team (meta-team) for any query - automatic routing to specialists based on context.

---

## API Usage

**Server:** FastAPI (AgentOS) at `http://localhost:5111`

**Endpoint:** `POST /chat`

```bash
# Query any team
curl -X POST http://localhost:5111/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Calculate emergency fund for ₹50K expenses",
    "team": "Personal Finance Team"
  }'
```

**Environment Variables:**
```env
# Intuit IAM Authentication
CLIENT_APP_ID=your_app_id
CLIENT_APP_SECRET=your_app_secret
PROFILE_ID=your_profile_id
EXPERIENCE_ID=your_experience_id

# External Services
SERPER_API_KEY=your_serper_api_key
```

---

## Important Notes

- Tax calculations: Indian Income Tax Act (FY 2024-25)
- Market data: Real-time via YFinance API
- Knowledge Base: ChromaDB with RAG for tax documents
- Always consult certified financial advisors for personalized advice
- Past performance doesn't guarantee future returns

---

*Last Updated: January 2026 | FinAgent v0.2.0 - Optimized 5-Agent Structure*
