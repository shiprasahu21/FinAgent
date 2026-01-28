"""
Investment Helper Team - Wealth accumulation, market research, and portfolio growth.

Agents (Consolidated from 5 to 3 for efficiency):
1. Market Intelligence Agent - Comprehensive Market Analyst (Stock/Indian/Global Markets)
2. Investment Advisor - Education, SIP Planning & Tax Guidance
3. Portfolio Manager - Portfolio Analysis, Allocation & Rebalancing
"""

from typing import Any, Dict, List
from agno.agent import Agent
from agno.team import Team
from agno.tools import tool
from agno.tools.serper import SerperTools
from core.llm import get_llm


# =============================================================================
# CONSTANTS
# =============================================================================

# Market cap thresholds in INR (in crores)
LARGE_CAP_THRESHOLD = 20000 * 10**7  # 20,000 Cr+
MID_CAP_THRESHOLD = 5000 * 10**7  # 5,000-20,000 Cr

# Rebalancing threshold percentage
REBALANCING_THRESHOLD = 5

# Age-based allocation limits
MIN_EQUITY_PERCENTAGE = 20
MAX_EQUITY_PERCENTAGE = 80


# =============================================================================
# CUSTOM TOOLS FOR INVESTMENT TEAM
# =============================================================================


@tool
def get_stock_metrics(symbol: str) -> Dict[str, Any]:
    """
    Fetch real-time stock performance metrics using YFinance.

    Args:
        symbol: Stock ticker symbol (e.g., 'RELIANCE.NS' for NSE, 'TCS.NS')

    Returns:
        Dictionary with stock metrics (P/E, EPS, Beta, etc.)
    """
    if not symbol or not symbol.strip():
        return {"error": "Stock symbol cannot be empty", "symbol": symbol}

    try:
        import yfinance as yf

        stock = yf.Ticker(symbol.strip().upper())
        info = stock.info

        # Check if valid data was returned
        if not info or "symbol" not in info and "longName" not in info:
            return {"error": f"No data found for symbol: {symbol}", "symbol": symbol}

        return {
            "symbol": symbol,
            "name": info.get("longName", "N/A"),
            "current_price": info.get(
                "currentPrice", info.get("regularMarketPrice", "N/A")
            ),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "forward_pe": info.get("forwardPE", "N/A"),
            "eps": info.get("trailingEps", "N/A"),
            "beta": info.get("beta", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "50_day_avg": info.get("fiftyDayAverage", "N/A"),
            "200_day_avg": info.get("twoHundredDayAverage", "N/A"),
            "volume": info.get("volume", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
        }
    except ImportError:
        return {
            "error": "yfinance package not installed. Install with: pip install yfinance"
        }
    except Exception as e:
        return {"error": f"Failed to fetch stock data: {str(e)}", "symbol": symbol}


@tool
def get_stock_history(symbol: str, period: str = "1mo") -> Dict[str, Any]:
    """
    Fetch historical stock data.

    Args:
        symbol: Stock ticker symbol
        period: Time period - '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'

    Returns:
        Dictionary with historical price data
    """
    valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"]
    if period not in valid_periods:
        return {
            "error": f"Invalid period '{period}'. Must be one of: {', '.join(valid_periods)}",
            "symbol": symbol,
        }

    if not symbol or not symbol.strip():
        return {"error": "Stock symbol cannot be empty", "symbol": symbol}

    try:
        import yfinance as yf

        stock = yf.Ticker(symbol.strip().upper())
        hist = stock.history(period=period)

        if hist.empty:
            return {"error": f"No historical data found for {symbol}", "symbol": symbol}

        # Calculate returns
        start_price = float(hist["Close"].iloc[0])
        end_price = float(hist["Close"].iloc[-1])
        period_return = ((end_price - start_price) / start_price) * 100

        return {
            "symbol": symbol,
            "period": period,
            "start_date": str(hist.index[0].date()),
            "end_date": str(hist.index[-1].date()),
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "high": round(float(hist["High"].max()), 2),
            "low": round(float(hist["Low"].min()), 2),
            "avg_volume": int(hist["Volume"].mean()),
            "period_return_pct": round(period_return, 2),
        }
    except ImportError:
        return {
            "error": "yfinance package not installed. Install with: pip install yfinance"
        }
    except Exception as e:
        return {"error": f"Failed to fetch historical data: {str(e)}", "symbol": symbol}


@tool
def get_index_data(index_symbol: str) -> Dict[str, Any]:
    """
    Fetch data for major market indices.

    Args:
        index_symbol: Index symbol ('^NSEI' for Nifty 50, '^BSESN' for Sensex,
                      '^GSPC' for S&P 500, '^IXIC' for Nasdaq)

    Returns:
        Dictionary with index data
    """
    if not index_symbol or not index_symbol.strip():
        return {"error": "Index symbol cannot be empty"}

    try:
        import yfinance as yf

        index_names = {
            "^NSEI": "Nifty 50",
            "^BSESN": "BSE Sensex",
            "^GSPC": "S&P 500",
            "^IXIC": "Nasdaq Composite",
            "^DJI": "Dow Jones Industrial Average",
        }

        index = yf.Ticker(index_symbol)
        info = index.info
        hist = index.history(period="5d")

        if not hist.empty:
            current = float(hist["Close"].iloc[-1])
            prev = float(hist["Close"].iloc[-2]) if len(hist) > 1 else current
            change = current - prev
            change_pct = (change / prev) * 100 if prev != 0 else 0
        else:
            current = info.get("regularMarketPrice", "N/A")
            change = info.get("regularMarketChange", 0)
            change_pct = info.get("regularMarketChangePercent", 0)

        return {
            "symbol": index_symbol,
            "name": index_names.get(index_symbol, info.get("shortName", "N/A")),
            "current_value": (
                round(current, 2) if isinstance(current, (int, float)) else current
            ),
            "change": round(change, 2) if isinstance(change, (int, float)) else change,
            "change_percent": (
                round(change_pct, 2)
                if isinstance(change_pct, (int, float))
                else change_pct
            ),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        }
    except ImportError:
        return {
            "error": "yfinance package not installed. Install with: pip install yfinance"
        }
    except Exception as e:
        return {
            "error": f"Failed to fetch index data: {str(e)}",
            "index_symbol": index_symbol,
        }


def _fetch_index_performance(
    symbol: str, name: str, period: str = "5d"
) -> Dict[str, Any]:
    """
    Helper function to fetch index performance data.

    Args:
        symbol: Index symbol
        name: Display name for the index
        period: Historical period to fetch

    Returns:
        Dictionary with index performance data or error
    """
    try:
        import yfinance as yf

        index = yf.Ticker(symbol)
        hist = index.history(period=period)

        if not hist.empty and len(hist) > 0:
            current = float(hist["Close"].iloc[-1])
            prev = float(hist["Close"].iloc[-2]) if len(hist) > 1 else current
            change_pct = ((current - prev) / prev) * 100 if prev != 0 else 0

            return {
                "value": round(current, 2),
                "change_pct": round(change_pct, 2),
            }
        else:
            return {"error": "Data unavailable"}
    except Exception:
        return {"error": "Data unavailable"}


@tool
def get_indian_market_overview() -> Dict[str, Any]:
    """
    Get overview of Indian stock market (Nifty 50, Sensex, and major sectors).

    Returns:
        Dictionary with Indian market overview
    """
    try:
        import yfinance as yf

        indices = {
            "^NSEI": "Nifty 50",
            "^BSESN": "Sensex",
            "^NSEBANK": "Nifty Bank",
            "^CNXIT": "Nifty IT",
            "^CRSLDX": "Nifty 500",
            "^CNXAUTO": "Nifty Auto",
            "^CNXPHARMA": "Nifty Pharma",
            "^CNXFMCG": "Nifty FMCG",
        }

        result = {"indices": {}}

        for symbol, name in indices.items():
            result["indices"][name] = _fetch_index_performance(symbol, name, "7d")

        return result
    except ImportError:
        return {
            "error": "yfinance package not installed. Install with: pip install yfinance"
        }
    except Exception as e:
        return {"error": f"Failed to fetch Indian market overview: {str(e)}"}


@tool
def get_global_market_overview() -> Dict[str, Any]:
    """
    Get overview of global stock markets (US, Europe, Asia).

    Returns:
        Dictionary with global market overview
    """
    try:
        import yfinance as yf

        indices = {
            # US Markets
            "^GSPC": "S&P 500 (US)",
            "^IXIC": "Nasdaq (US)",
            "^DJI": "Dow Jones (US)",
            # India
            "^NSEI": "Nifty 50 (India)",
            "^BSESN": "Sensex (India)",
            # UK
            "^FTSE": "FTSE 100 (UK)",
            # Japan
            "^N225": "Nikkei 225 (Japan)",
            # China
            "000001.SS": "Shanghai Composite (China)",
            "^HSI": "Hang Seng (HK)",
        }

        result = {"indices": {}}

        for symbol, name in indices.items():
            result["indices"][name] = _fetch_index_performance(symbol, name, "5d")

        return result
    except ImportError:
        return {
            "error": "yfinance package not installed. Install with: pip install yfinance"
        }
    except Exception as e:
        return {"error": f"Failed to fetch global market overview: {str(e)}"}


@tool
def analyze_portfolio_allocation(holdings: str) -> Dict[str, Any]:
    """
    Analyze portfolio allocation by market cap and sector.

    Args:
        holdings: JSON string of holdings, e.g., '[{"symbol": "RELIANCE.NS", "quantity": 10}, ...]'

    Returns:
        Dictionary with portfolio analysis
    """
    try:
        import json
        import yfinance as yf

        holdings_list = json.loads(holdings)

        if not isinstance(holdings_list, list):
            return {"error": "Holdings must be a JSON array of objects"}

        if not holdings_list:
            return {"error": "Holdings list cannot be empty"}

        portfolio = {
            "holdings": [],
            "total_value": 0,
            "allocation_by_cap": {"large": 0, "mid": 0, "small": 0},
            "allocation_by_sector": {},
        }

        for holding in holdings_list:
            if not isinstance(holding, dict):
                continue

            symbol = holding.get("symbol")
            quantity = holding.get("quantity", 0)

            if not symbol:
                portfolio["holdings"].append({"error": "Missing symbol in holding"})
                continue

            try:
                stock = yf.Ticker(symbol)
                info = stock.info

                price = info.get("currentPrice", info.get("regularMarketPrice", 0))
                market_cap = info.get("marketCap", 0)
                sector = info.get("sector", "Unknown")

                value = price * quantity
                portfolio["total_value"] += value

                # Classify by market cap using constants
                if market_cap >= LARGE_CAP_THRESHOLD:
                    cap_category = "large"
                elif market_cap >= MID_CAP_THRESHOLD:
                    cap_category = "mid"
                else:
                    cap_category = "small"

                portfolio["holdings"].append(
                    {
                        "symbol": symbol,
                        "name": info.get("longName", symbol),
                        "quantity": quantity,
                        "price": round(price, 2),
                        "value": round(value, 2),
                        "sector": sector,
                        "market_cap_category": cap_category,
                    }
                )

                portfolio["allocation_by_cap"][cap_category] += value
                portfolio["allocation_by_sector"][sector] = (
                    portfolio["allocation_by_sector"].get(sector, 0) + value
                )

            except Exception as e:
                portfolio["holdings"].append(
                    {
                        "symbol": symbol,
                        "error": f"Failed to fetch data: {str(e)}",
                    }
                )

        # Convert to percentages
        if portfolio["total_value"] > 0:
            for cap in portfolio["allocation_by_cap"]:
                pct = (
                    portfolio["allocation_by_cap"][cap] / portfolio["total_value"]
                ) * 100
                portfolio["allocation_by_cap"][cap] = round(pct, 2)

            for sector in portfolio["allocation_by_sector"]:
                pct = (
                    portfolio["allocation_by_sector"][sector] / portfolio["total_value"]
                ) * 100
                portfolio["allocation_by_sector"][sector] = round(pct, 2)

        portfolio["total_value"] = round(portfolio["total_value"], 2)

        return portfolio
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format for holdings: {str(e)}"}
    except ImportError:
        return {
            "error": "yfinance package not installed. Install with: pip install yfinance"
        }
    except Exception as e:
        return {"error": f"Failed to analyze portfolio: {str(e)}"}


@tool
def calculate_age_based_allocation(
    age: int, risk_tolerance: str = "moderate", allocation_rule: str = "auto"
) -> Dict[str, Any]:
    """
    Calculate recommended asset allocation using modern age-based rules.

    Args:
        age: Investor's age
        risk_tolerance: Risk tolerance - 'conservative', 'moderate', 'aggressive'
        allocation_rule: Allocation rule - '100', '110', '120', or 'auto' (default: 'auto')
                        'auto' selects rule based on risk tolerance

    Returns:
        Dictionary with recommended allocation

    Allocation Rules Explained:
    - 100 Minus Age: Traditional conservative approach (e.g., age 30 → 70% equity)
    - 110 Minus Age: Modern moderate approach for longer lifespans (e.g., age 30 → 80% equity)
    - 120 Minus Age: Aggressive approach for young investors (e.g., age 30 → 90% equity)

    Recommendation for Indian Investors:
    - Use 110-age for most investors (accounts for longer life expectancy)
    - Use 120-age for young investors (<35) with high risk tolerance
    - Use 100-age only for very conservative investors or near retirement
    """
    # Validate inputs
    if not isinstance(age, int) or age < 18 or age > 100:
        return {"error": "Age must be an integer between 18 and 100"}

    valid_risk_levels = ["conservative", "moderate", "aggressive"]
    if risk_tolerance.lower() not in valid_risk_levels:
        return {
            "error": f"Invalid risk tolerance. Must be one of: {', '.join(valid_risk_levels)}"
        }

    valid_rules = ["100", "110", "120", "auto"]
    if allocation_rule.lower() not in valid_rules:
        return {
            "error": f"Invalid allocation rule. Must be one of: {', '.join(valid_rules)}"
        }

    # Auto-select rule based on risk tolerance and age
    if allocation_rule.lower() == "auto":
        if risk_tolerance.lower() == "conservative":
            selected_rule = 100
            rule_name = "100 Minus Age (Conservative)"
        elif risk_tolerance.lower() == "moderate":
            selected_rule = 110
            rule_name = "110 Minus Age (Moderate)"
        else:  # aggressive
            # Use 120 for young investors, 110 for older
            selected_rule = 120 if age < 40 else 110
            rule_name = f"{selected_rule} Minus Age (Aggressive)"
    else:
        selected_rule = int(allocation_rule)
        rule_name = f"{selected_rule} Minus Age Rule"

    # Calculate base equity allocation
    base_equity = selected_rule - age

    # Apply bounds
    equity_pct = max(MIN_EQUITY_PERCENTAGE, min(MAX_EQUITY_PERCENTAGE, base_equity))
    debt_pct = 100 - equity_pct

    # Add gold allocation (5-10% for diversification)
    gold_pct = 5 if age < 40 else 7

    # Adjust equity and debt to accommodate gold
    equity_pct_with_gold = round(equity_pct * (1 - gold_pct / 100))
    debt_pct_with_gold = round(debt_pct * (1 - gold_pct / 100))

    # Ensure total is 100%
    total_check = equity_pct_with_gold + debt_pct_with_gold + gold_pct
    if total_check != 100:
        equity_pct_with_gold = 100 - debt_pct_with_gold - gold_pct

    # Equity breakdown based on age
    if age < 35:
        equity_breakdown = {
            "large_cap": 40,
            "mid_cap": 35,
            "small_cap": 15,
            "international": 10,
        }
    elif age < 50:
        equity_breakdown = {
            "large_cap": 50,
            "mid_cap": 30,
            "small_cap": 10,
            "international": 10,
        }
    else:
        equity_breakdown = {
            "large_cap": 60,
            "mid_cap": 25,
            "small_cap": 5,
            "international": 10,
        }

    # Debt breakdown
    debt_breakdown = {
        "ppf_epf": 40,
        "debt_funds": 30,
        "fixed_deposits": 20,
        "bonds": 10,
    }

    # Gold breakdown
    gold_breakdown = {
        "sovereign_gold_bonds": 60,  # Best option: tax-free after 8 years
        "gold_etf": 30,  # Liquid and no storage hassle
        "digital_gold": 10,  # Small allocation for liquidity
    }

    # Calculate comparison with other rules
    comparisons = {}
    for rule in [100, 110, 120]:
        rule_equity = max(MIN_EQUITY_PERCENTAGE, min(MAX_EQUITY_PERCENTAGE, rule - age))
        rule_debt = 100 - rule_equity
        comparisons[f"{rule}_minus_age"] = {
            "equity": rule_equity,
            "debt": rule_debt,
            "description": _get_rule_description(rule, age),
        }

    return {
        "age": age,
        "risk_tolerance": risk_tolerance,
        "rule_used": rule_name,
        "selected_rule_number": selected_rule,
        "recommended_allocation": {
            "equity_percentage": equity_pct_with_gold,
            "debt_percentage": debt_pct_with_gold,
            "gold_percentage": gold_pct,
            "note": "Gold allocation provides diversification and inflation hedge",
        },
        "equity_breakdown": {
            k: round(v * equity_pct_with_gold / 100, 1)
            for k, v in equity_breakdown.items()
        },
        "debt_breakdown": {
            k: round(v * debt_pct_with_gold / 100, 1)
            for k, v in debt_breakdown.items()
        },
        "gold_breakdown": {
            k: round(v * gold_pct / 100, 1) for k, v in gold_breakdown.items()
        },
        "rule_comparison": comparisons,
        "rebalancing_frequency": f"Annually or when allocation deviates by >{REBALANCING_THRESHOLD}%",
        "recommendations": [
            f"At age {age}, {selected_rule}-age rule suggests {equity_pct}% equity",
            f"With gold allocation: {equity_pct_with_gold}% equity, {debt_pct_with_gold}% debt, {gold_pct}% gold",
            "Gold acts as inflation hedge and portfolio stabilizer",
            f"Review allocation as you age - gradually shift to {selected_rule-10} or {selected_rule-20} rule",
            "Rebalance annually or when allocation drifts by >5%",
        ],
        "why_this_rule": _get_rule_rationale(selected_rule, age, risk_tolerance),
    }


def _get_rule_description(rule: int, age: int) -> str:
    """Helper function to describe allocation rules."""
    equity = max(MIN_EQUITY_PERCENTAGE, min(MAX_EQUITY_PERCENTAGE, rule - age))
    if rule == 100:
        return f"Conservative: {equity}% equity - Traditional approach, more cautious"
    elif rule == 110:
        return f"Moderate: {equity}% equity - Modern approach for longer lifespans"
    else:  # 120
        return f"Aggressive: {equity}% equity - Growth-focused for long-term investors"


def _get_rule_rationale(rule: int, age: int, risk_tolerance: str) -> str:
    """Helper function to explain why this rule was selected."""
    years_to_retirement = max(0, 60 - age)

    if rule == 100:
        return (
            f"100-age rule selected for your {risk_tolerance} risk tolerance. "
            f"At age {age}, this conservative approach prioritizes capital preservation. "
            f"With ~{years_to_retirement} years to retirement, this balances safety with moderate growth."
        )
    elif rule == 110:
        return (
            f"110-age rule is ideal for your {risk_tolerance} profile at age {age}. "
            f"This modern approach accounts for longer life expectancy (75+ years) and inflation. "
            f"With ~{years_to_retirement} years to retirement, you have time for wealth growth while maintaining balance."
        )
    else:  # 120
        return (
            f"120-age rule selected for your {risk_tolerance} risk tolerance at age {age}. "
            f"This aggressive approach maximizes growth potential. "
            f"With ~{years_to_retirement} years to retirement, you have time to ride out market volatility and benefit from compounding."
        )


@tool
def calculate_capital_gains_tax(
    buy_price: float,
    sell_price: float,
    holding_period_days: int,
    quantity: int,
    is_equity: bool = True,
) -> Dict[str, Any]:
    """
    Calculate capital gains tax for Indian investors.

    Args:
        buy_price: Purchase price per unit/share
        sell_price: Selling price per unit/share
        holding_period_days: Number of days the asset was held
        quantity: Number of units/shares
        is_equity: True for equity/equity mutual funds, False for debt instruments

    Returns:
        Dictionary with detailed tax calculation breakdown

    Tax Rules (as of 2024-25):
    Equity (Stocks/Equity Mutual Funds):
    - LTCG (>365 days): 12.5% on gains above ₹1.25 lakh (no indexation)
    - STCG (≤365 days): 20% on all gains
    - STT (Securities Transaction Tax) applies

    Debt (Debt Mutual Funds/Bonds):
    - LTCG (>36 months): 12.5% with indexation benefit
    - STCG (≤36 months): Added to income, taxed at slab rate (assumed 30% for calculation)
    """
    # Input validation
    if buy_price <= 0 or sell_price <= 0:
        return {"error": "Buy price and sell price must be greater than 0"}

    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}

    if holding_period_days < 0:
        return {"error": "Holding period cannot be negative"}

    # Calculate gains
    total_buy_value = buy_price * quantity
    total_sell_value = sell_price * quantity
    total_gain = total_sell_value - total_buy_value

    # If loss, no tax
    if total_gain <= 0:
        return {
            "transaction_type": "Equity" if is_equity else "Debt",
            "holding_period_days": holding_period_days,
            "buy_value": round(total_buy_value, 2),
            "sell_value": round(total_sell_value, 2),
            "total_gain_or_loss": round(total_gain, 2),
            "capital_loss": round(abs(total_gain), 2),
            "tax_type": "N/A - Capital Loss",
            "taxable_gain": 0,
            "tax_rate": "N/A",
            "tax_amount": 0,
            "net_proceeds": round(total_sell_value, 2),
            "note": "Capital loss can be carried forward for 8 years to offset future capital gains",
        }

    # Calculate tax based on asset type and holding period
    if is_equity:
        # Equity: LTCG if held > 365 days, else STCG
        equity_ltcg_threshold = 365
        equity_ltcg_exemption = 125000  # ₹1.25 lakh exemption

        if holding_period_days > equity_ltcg_threshold:
            # Long Term Capital Gains - Equity
            tax_type = "LTCG - Equity"
            taxable_gain = max(0, total_gain - equity_ltcg_exemption)
            tax_rate = 12.5
            tax_amount = taxable_gain * (tax_rate / 100)
            exemption_used = min(total_gain, equity_ltcg_exemption)

            return {
                "transaction_type": "Equity (Stocks/Equity Mutual Funds)",
                "holding_period_days": holding_period_days,
                "holding_period": f"{holding_period_days} days ({round(holding_period_days/365, 1)} years)",
                "buy_value": round(total_buy_value, 2),
                "sell_value": round(total_sell_value, 2),
                "total_gain": round(total_gain, 2),
                "tax_type": tax_type,
                "ltcg_exemption_limit": equity_ltcg_exemption,
                "exemption_used": round(exemption_used, 2),
                "taxable_gain": round(taxable_gain, 2),
                "tax_rate": f"{tax_rate}%",
                "tax_amount": round(tax_amount, 2),
                "net_proceeds": round(total_sell_value - tax_amount, 2),
                "effective_tax_rate": f"{round((tax_amount/total_gain)*100, 2)}%",
                "notes": [
                    "STT (Securities Transaction Tax) is already included in broker charges",
                    f"₹{exemption_used:,.2f} gain is exempt under ₹1.25 lakh annual limit",
                    "LTCG exemption is per financial year (Apr-Mar)",
                ],
            }
        else:
            # Short Term Capital Gains - Equity
            tax_type = "STCG - Equity"
            taxable_gain = total_gain
            tax_rate = 20
            tax_amount = taxable_gain * (tax_rate / 100)

            return {
                "transaction_type": "Equity (Stocks/Equity Mutual Funds)",
                "holding_period_days": holding_period_days,
                "holding_period": f"{holding_period_days} days",
                "buy_value": round(total_buy_value, 2),
                "sell_value": round(total_sell_value, 2),
                "total_gain": round(total_gain, 2),
                "tax_type": tax_type,
                "taxable_gain": round(taxable_gain, 2),
                "tax_rate": f"{tax_rate}%",
                "tax_amount": round(tax_amount, 2),
                "net_proceeds": round(total_sell_value - tax_amount, 2),
                "effective_tax_rate": f"{round((tax_amount/total_gain)*100, 2)}%",
                "notes": [
                    "STT (Securities Transaction Tax) is already included in broker charges",
                    "No exemption available for STCG on equity",
                    "Consider holding for >365 days to qualify for LTCG benefits",
                ],
            }
    else:
        # Debt: LTCG if held > 36 months (3 years), else STCG
        debt_ltcg_threshold = 1095  # 36 months = 3 years

        if holding_period_days > debt_ltcg_threshold:
            # Long Term Capital Gains - Debt
            # Note: Indexation benefit was removed from April 2023
            tax_type = "LTCG - Debt"
            taxable_gain = total_gain
            tax_rate = 12.5
            tax_amount = taxable_gain * (tax_rate / 100)

            return {
                "transaction_type": "Debt (Debt Mutual Funds/Bonds)",
                "holding_period_days": holding_period_days,
                "holding_period": f"{holding_period_days} days ({round(holding_period_days/365, 1)} years)",
                "buy_value": round(total_buy_value, 2),
                "sell_value": round(total_sell_value, 2),
                "total_gain": round(total_gain, 2),
                "tax_type": tax_type,
                "taxable_gain": round(taxable_gain, 2),
                "tax_rate": f"{tax_rate}% (without indexation)",
                "tax_amount": round(tax_amount, 2),
                "net_proceeds": round(total_sell_value - tax_amount, 2),
                "effective_tax_rate": f"{round((tax_amount/total_gain)*100, 2)}%",
                "notes": [
                    "Indexation benefit removed from April 2023 onwards",
                    "For debt funds purchased before April 2023, old rules may apply",
                    "Consult a tax advisor for grandfathering provisions",
                ],
            }
        else:
            # Short Term Capital Gains - Debt
            tax_type = "STCG - Debt"
            taxable_gain = total_gain
            # Debt STCG is added to income and taxed at slab rate
            # Assuming highest slab for calculation (30% + 4% cess = 31.2%)
            assumed_slab_rate = 30
            cess = 4  # 4% cess on income tax
            effective_rate = assumed_slab_rate * (1 + cess / 100)
            tax_amount = taxable_gain * (effective_rate / 100)

            return {
                "transaction_type": "Debt (Debt Mutual Funds/Bonds)",
                "holding_period_days": holding_period_days,
                "holding_period": f"{holding_period_days} days",
                "buy_value": round(total_buy_value, 2),
                "sell_value": round(total_sell_value, 2),
                "total_gain": round(total_gain, 2),
                "tax_type": tax_type,
                "taxable_gain": round(taxable_gain, 2),
                "tax_rate": f"As per income tax slab (assumed {assumed_slab_rate}% + 4% cess)",
                "assumed_tax_rate": f"{round(effective_rate, 2)}%",
                "estimated_tax_amount": round(tax_amount, 2),
                "net_proceeds": round(total_sell_value - tax_amount, 2),
                "effective_tax_rate": f"{round((tax_amount/total_gain)*100, 2)}%",
                "notes": [
                    "STCG on debt is added to your total income",
                    f"Tax calculated assuming {assumed_slab_rate}% tax slab + 4% cess",
                    "Actual tax depends on your total income and tax slab",
                    "If in 20% or 10% slab, actual tax will be lower",
                ],
            }


@tool
def calculate_sip_returns(
    monthly_investment: float,
    expected_annual_return: float,
    years: int,
    step_up_percentage: float = 0,
) -> Dict[str, Any]:
    """
    Calculate SIP (Systematic Investment Plan) returns with optional annual step-up.

    Args:
        monthly_investment: Monthly SIP amount in INR
        expected_annual_return: Expected annual return percentage (e.g., 12 for 12%)
        years: Investment duration in years
        step_up_percentage: Annual increase in SIP amount (e.g., 10 for 10% yearly increase)

    Returns:
        Dictionary with detailed SIP projection including:
        - Total invested amount
        - Maturity value
        - Total returns
        - Year-by-year breakdown
        - Comparison with lump sum investment
        - Inflation-adjusted returns

    Example:
        ₹5,000/month SIP at 12% for 10 years with 10% annual step-up
    """
    # Input validation
    if monthly_investment <= 0:
        return {"error": "Monthly investment must be greater than 0"}

    if expected_annual_return <= 0 or expected_annual_return > 50:
        return {
            "error": "Expected annual return must be between 0 and 50% (be realistic!)"
        }

    if years <= 0 or years > 50:
        return {"error": "Investment duration must be between 1 and 50 years"}

    if step_up_percentage < 0 or step_up_percentage > 50:
        return {"error": "Step-up percentage must be between 0 and 50%"}

    # Convert annual return to monthly return
    monthly_rate = expected_annual_return / 12 / 100

    # Calculate SIP with step-up
    total_invested = 0
    maturity_value = 0
    current_monthly_sip = monthly_investment
    year_by_year = []

    for year in range(1, years + 1):
        year_start_value = maturity_value
        year_invested = 0

        # Calculate for each month in the year
        for month in range(12):
            total_invested += current_monthly_sip
            year_invested += current_monthly_sip
            maturity_value = (maturity_value + current_monthly_sip) * (1 + monthly_rate)

        year_returns = maturity_value - year_start_value - year_invested

        year_by_year.append(
            {
                "year": year,
                "monthly_sip": round(current_monthly_sip, 2),
                "invested_this_year": round(year_invested, 2),
                "total_invested": round(total_invested, 2),
                "value_at_year_end": round(maturity_value, 2),
                "returns_this_year": round(year_returns, 2),
                "total_returns": round(maturity_value - total_invested, 2),
            }
        )

        # Apply step-up for next year
        current_monthly_sip = current_monthly_sip * (1 + step_up_percentage / 100)

    total_returns = maturity_value - total_invested

    # Calculate equivalent lump sum investment
    lump_sum_factor = (1 + expected_annual_return / 100) ** years
    equivalent_lump_sum = total_invested / lump_sum_factor

    # Calculate lump sum returns if invested at start
    lump_sum_invested = monthly_investment * 12 * years  # Total if paid upfront
    lump_sum_maturity = lump_sum_invested * lump_sum_factor
    lump_sum_returns = lump_sum_maturity - lump_sum_invested

    # Inflation-adjusted returns (assuming 6% inflation)
    inflation_rate = 6
    real_return_rate = (
        ((1 + expected_annual_return / 100) / (1 + inflation_rate / 100)) - 1
    ) * 100
    inflation_adjusted_value = maturity_value / ((1 + inflation_rate / 100) ** years)

    # Calculate XIRR (approximate using formula)
    # For SIP, XIRR ≈ expected return
    approximate_xirr = expected_annual_return

    result = {
        "sip_details": {
            "monthly_investment": round(monthly_investment, 2),
            "annual_return": f"{expected_annual_return}%",
            "duration_years": years,
            "step_up_percentage": f"{step_up_percentage}%",
        },
        "summary": {
            "total_invested": round(total_invested, 2),
            "maturity_value": round(maturity_value, 2),
            "total_returns": round(total_returns, 2),
            "returns_percentage": f"{round((total_returns/total_invested)*100, 2)}%",
            "wealth_gain": f"{round(maturity_value/total_invested, 2)}x",
        },
        "comparison_with_lump_sum": {
            "sip_maturity": round(maturity_value, 2),
            "lump_sum_needed_at_start": round(equivalent_lump_sum, 2),
            "advantage": f"SIP is better - you invest gradually instead of ₹{round(equivalent_lump_sum, 2):,} upfront",
            "note": "SIP allows rupee cost averaging and reduces timing risk",
        },
        "inflation_adjusted": {
            "assumed_inflation": f"{inflation_rate}%",
            "real_return_rate": f"{round(real_return_rate, 2)}%",
            "purchasing_power_today": round(inflation_adjusted_value, 2),
            "note": f"₹{round(maturity_value, 2):,} in {years} years = ₹{round(inflation_adjusted_value, 2):,} in today's money",
        },
        "year_by_year_projection": year_by_year[
            :5
        ],  # Show first 5 years in summary
        "final_year": year_by_year[-1],  # Show last year
        "notes": [
            f"Starting SIP: ₹{monthly_investment:,.0f}/month",
            f"Final SIP (Year {years}): ₹{round(current_monthly_sip, 2):,.0f}/month"
            if step_up_percentage > 0
            else "No step-up applied",
            f"Total invested over {years} years: ₹{round(total_invested, 2):,}",
            f"Maturity value: ₹{round(maturity_value, 2):,}",
            f"Returns: ₹{round(total_returns, 2):,} ({round((total_returns/total_invested)*100, 2)}%)",
            "Returns assume constant rate and reinvestment of gains",
            "Actual returns may vary based on market performance",
            "Consider step-up SIP to beat inflation and increase wealth faster",
        ],
    }

    return result


@tool
def calculate_sip_for_goal(
    target_amount: float,
    years: int,
    expected_annual_return: float = 12.0,
    inflation_rate: float = 6.0,
) -> Dict[str, Any]:
    """
    Calculate monthly SIP needed to reach a financial goal.

    Args:
        target_amount: Target amount needed (in today's money)
        years: Time horizon in years
        expected_annual_return: Expected annual return percentage (default: 12%)
        inflation_rate: Expected inflation rate (default: 6%)

    Returns:
        Dictionary with required monthly SIP and goal projection

    Example:
        Need ₹50 lakhs for child's education in 15 years
    """
    # Input validation
    if target_amount <= 0:
        return {"error": "Target amount must be greater than 0"}

    if years <= 0 or years > 50:
        return {"error": "Time horizon must be between 1 and 50 years"}

    if expected_annual_return <= 0 or expected_annual_return > 50:
        return {"error": "Expected annual return must be between 0 and 50%"}

    if inflation_rate < 0 or inflation_rate > 20:
        return {"error": "Inflation rate must be between 0 and 20%"}

    # Adjust target for inflation
    future_value_needed = target_amount * ((1 + inflation_rate / 100) ** years)

    # Calculate monthly SIP needed using FV of annuity formula
    # FV = P × [(1 + r)^n - 1] / r
    # Where P = monthly payment, r = monthly rate, n = number of months
    monthly_rate = expected_annual_return / 12 / 100
    num_months = years * 12

    # Rearrange formula to solve for P (monthly SIP)
    if monthly_rate > 0:
        monthly_sip_needed = future_value_needed * monthly_rate / (
            ((1 + monthly_rate) ** num_months) - 1
        )
    else:
        monthly_sip_needed = future_value_needed / num_months

    total_investment = monthly_sip_needed * num_months
    total_returns = future_value_needed - total_investment

    # Calculate with 10% step-up
    step_up_result = calculate_sip_returns(
        monthly_investment=monthly_sip_needed * 0.7,  # Start with lower amount
        expected_annual_return=expected_annual_return,
        years=years,
        step_up_percentage=10,
    )

    return {
        "goal_details": {
            "target_amount_today": round(target_amount, 2),
            "future_value_needed": round(future_value_needed, 2),
            "time_horizon_years": years,
            "expected_return": f"{expected_annual_return}%",
            "assumed_inflation": f"{inflation_rate}%",
        },
        "required_sip": {
            "monthly_sip_needed": round(monthly_sip_needed, 2),
            "total_investment": round(total_investment, 2),
            "expected_returns": round(total_returns, 2),
            "returns_percentage": f"{round((total_returns/total_investment)*100, 2)}%",
        },
        "alternative_with_step_up": {
            "starting_sip": round(monthly_sip_needed * 0.7, 2),
            "step_up": "10% annually",
            "note": f"Start with ₹{round(monthly_sip_needed * 0.7, 2):,}/month and increase by 10% yearly",
            "final_monthly_sip": step_up_result["final_year"]["monthly_sip"]
            if "final_year" in step_up_result
            else "N/A",
        },
        "inflation_impact": {
            "today_value": round(target_amount, 2),
            "future_value": round(future_value_needed, 2),
            "inflation_factor": f"{round(future_value_needed/target_amount, 2)}x",
            "note": f"Due to {inflation_rate}% inflation, ₹{round(target_amount, 2):,} today = ₹{round(future_value_needed, 2):,} in {years} years",
        },
        "recommendations": [
            f"Invest ₹{round(monthly_sip_needed, 2):,} per month for {years} years",
            f"Choose equity mutual funds for {years}+ year goals (expected return: {expected_annual_return}%)",
            "Start a 10% step-up SIP to beat inflation automatically",
            "Review and rebalance portfolio annually",
            "Consider increasing SIP with salary increments",
        ],
        "common_goals": self._get_common_goal_examples(years),
    }


def _get_common_goal_examples(years: int) -> list:
    """Helper function to provide common goal examples based on time horizon."""
    if years <= 5:
        return [
            "Short-term goals (1-5 years):",
            "- Emergency fund buildup",
            "- Car purchase",
            "- Vacation/travel",
            "- Marriage (if planning soon)",
            "Recommended: Hybrid/Debt funds for lower risk",
        ]
    elif years <= 10:
        return [
            "Medium-term goals (5-10 years):",
            "- Home down payment",
            "- Child's school education",
            "- Business startup fund",
            "- Major home renovation",
            "Recommended: Balanced/Hybrid funds (60-70% equity)",
        ]
    else:
        return [
            "Long-term goals (10+ years):",
            "- Child's higher education",
            "- Child's marriage",
            "- Retirement corpus",
            "- Wealth creation",
            "Recommended: Pure equity funds (100% equity) for maximum growth",
        ]


@tool
def calculate_goal_corpus(
    goal_amount: float,
    years_to_goal: int,
    inflation_rate: float = 6.0,
    expected_return: float = 12.0,
    existing_corpus: float = 0,
) -> Dict[str, Any]:
    """
    Calculate investment needed for major life goals with inflation adjustment.

    Args:
        goal_amount: Target amount needed in today's money (INR)
        years_to_goal: Years until the goal
        inflation_rate: Expected inflation rate (default: 6%)
        expected_return: Expected investment return (default: 12%)
        existing_corpus: Any existing savings for this goal (default: 0)

    Returns:
        Dictionary with:
        - Inflation-adjusted goal amount
        - Monthly SIP needed
        - Lump sum investment needed
        - Strategy recommendations
        - Goal-specific advice

    Common Goals:
        - Child's higher education: ₹25-50 lakhs
        - Child's marriage: ₹20-30 lakhs
        - Home down payment (20%): Based on property price
        - Retirement corpus: 25x annual expenses
        - International vacation: ₹5-10 lakhs
    """
    # Input validation
    if goal_amount <= 0:
        return {"error": "Goal amount must be greater than 0"}

    if years_to_goal <= 0 or years_to_goal > 50:
        return {"error": "Years to goal must be between 1 and 50"}

    if inflation_rate < 0 or inflation_rate > 20:
        return {"error": "Inflation rate must be between 0 and 20%"}

    if expected_return <= 0 or expected_return > 50:
        return {"error": "Expected return must be between 0 and 50%"}

    if existing_corpus < 0:
        return {"error": "Existing corpus cannot be negative"}

    # Calculate inflation-adjusted future value
    future_value_needed = goal_amount * ((1 + inflation_rate / 100) ** years_to_goal)

    # Calculate future value of existing corpus
    future_value_of_existing = existing_corpus * (
        (1 + expected_return / 100) ** years_to_goal
    )

    # Remaining amount needed
    remaining_needed = max(0, future_value_needed - future_value_of_existing)

    # Calculate monthly SIP needed (if remaining amount > 0)
    if remaining_needed > 0:
        monthly_rate = expected_return / 12 / 100
        num_months = years_to_goal * 12

        if monthly_rate > 0:
            monthly_sip_needed = remaining_needed * monthly_rate / (
                ((1 + monthly_rate) ** num_months) - 1
            )
        else:
            monthly_sip_needed = remaining_needed / num_months

        total_sip_investment = monthly_sip_needed * num_months
        sip_returns = remaining_needed - total_sip_investment
    else:
        monthly_sip_needed = 0
        total_sip_investment = 0
        sip_returns = 0

    # Calculate lump sum needed today
    lump_sum_needed = remaining_needed / ((1 + expected_return / 100) ** years_to_goal)

    # Determine investment strategy based on time horizon
    if years_to_goal <= 3:
        risk_category = "Low Risk"
        recommended_allocation = {"debt": 70, "equity": 30}
        recommended_instruments = [
            "Liquid funds",
            "Short-term debt funds",
            "FDs for assured returns",
            "Hybrid funds (conservative)",
        ]
        expected_return_range = "7-9%"
    elif years_to_goal <= 7:
        risk_category = "Moderate Risk"
        recommended_allocation = {"debt": 40, "equity": 60}
        recommended_instruments = [
            "Balanced/Hybrid funds",
            "Large-cap equity funds",
            "Debt funds for stability",
            "Index funds (Nifty 50)",
        ]
        expected_return_range = "10-12%"
    else:
        risk_category = "High Risk (Aggressive)"
        recommended_allocation = {"debt": 20, "equity": 80}
        recommended_instruments = [
            "Diversified equity funds",
            "Large + Mid cap funds",
            "Index funds (Nifty 500)",
            "ELSS for tax benefits",
            "Small-cap funds (10-15%)",
        ]
        expected_return_range = "12-15%"

    # Calculate with step-up SIP (10% annual increase)
    if monthly_sip_needed > 0:
        step_up_starting_sip = monthly_sip_needed * 0.7  # Start with 70%
        step_up_projection = calculate_sip_returns(
            monthly_investment=step_up_starting_sip,
            expected_annual_return=expected_return,
            years=years_to_goal,
            step_up_percentage=10,
        )
        step_up_final_value = step_up_projection["summary"]["maturity_value"]
    else:
        step_up_starting_sip = 0
        step_up_final_value = 0

    # Goal-specific templates
    goal_templates = _get_goal_template(goal_amount, years_to_goal)

    result = {
        "goal_summary": {
            "goal_name": goal_templates.get("name", "Custom Goal"),
            "target_amount_today": round(goal_amount, 2),
            "future_value_needed": round(future_value_needed, 2),
            "years_to_goal": years_to_goal,
            "inflation_impact": f"{round((future_value_needed/goal_amount - 1)*100, 1)}% increase due to inflation",
        },
        "existing_investments": {
            "current_corpus": round(existing_corpus, 2),
            "future_value": round(future_value_of_existing, 2),
            "remaining_needed": round(remaining_needed, 2),
        },
        "investment_options": {
            "option_1_sip": {
                "monthly_sip": round(monthly_sip_needed, 2),
                "total_investment": round(total_sip_investment, 2),
                "expected_returns": round(sip_returns, 2),
                "maturity_value": round(remaining_needed, 2),
                "recommendation": "Best for regular income earners",
            },
            "option_2_step_up_sip": {
                "starting_monthly_sip": round(step_up_starting_sip, 2),
                "annual_increase": "10%",
                "final_monthly_sip": step_up_projection["final_year"]["monthly_sip"]
                if step_up_final_value > 0
                else 0,
                "recommendation": "Start lower, increase with salary hikes",
            },
            "option_3_lump_sum": {
                "invest_today": round(lump_sum_needed, 2),
                "one_time_investment": "Pay once and let it grow",
                "recommendation": "If you have surplus funds available now",
            },
        },
        "strategy_recommendation": {
            "risk_category": risk_category,
            "time_horizon": f"{years_to_goal} years",
            "asset_allocation": recommended_allocation,
            "expected_return_range": expected_return_range,
            "recommended_instruments": recommended_instruments,
        },
        "action_plan": [
            f"1. Start monthly SIP of ₹{round(monthly_sip_needed, 2):,} (or ₹{round(step_up_starting_sip, 2):,} with 10% step-up)",
            f"2. Invest in {risk_category.lower()} funds: {', '.join(recommended_instruments[:2])}",
            f"3. Review progress every 6 months",
            f"4. Rebalance allocation as goal approaches (shift to debt)",
            f"5. 2 years before goal, move to liquid/debt funds for safety",
        ],
        "goal_specific_tips": goal_templates.get("tips", []),
        "important_notes": [
            f"Returns assumed: {expected_return}% (may vary with market)",
            f"Inflation assumed: {inflation_rate}% (adjust if needed)",
            "Start early to benefit from compounding",
            "Increase SIP with salary increments (10-15% yearly)",
            "Don't stop SIP during market corrections",
            "Review and adjust goal amount periodically",
        ],
    }

    # Add shortfall warning if existing corpus is insufficient
    if existing_corpus > 0 and future_value_of_existing < future_value_needed:
        result["shortfall_alert"] = {
            "message": "Your existing corpus will not be sufficient",
            "existing_will_grow_to": round(future_value_of_existing, 2),
            "additional_needed": round(remaining_needed, 2),
            "action": f"Start SIP of ₹{round(monthly_sip_needed, 2):,} to bridge the gap",
        }
    elif existing_corpus > 0 and future_value_of_existing >= future_value_needed:
        result["surplus_alert"] = {
            "message": "Great! Your existing corpus is sufficient",
            "existing_will_grow_to": round(future_value_of_existing, 2),
            "surplus": round(future_value_of_existing - future_value_needed, 2),
            "action": "No additional investment needed. Consider investing surplus for other goals.",
        }

    return result


def _get_goal_template(amount: float, years: int) -> Dict[str, Any]:
    """Helper function to provide goal-specific templates and tips."""
    amount_lakhs = amount / 100000

    # Detect goal type based on amount and duration
    if 20 <= amount_lakhs <= 60 and years >= 10:
        return {
            "name": "Child's Higher Education",
            "tips": [
                "Consider ELSS funds for tax benefits (80C)",
                "International education costs 2-3x Indian colleges",
                "Start Sukanya Samriddhi Yojana if daughter (21-year lock-in)",
                "Look into education loans for tax benefits",
                "Consider 50% corpus target, rest via education loan",
            ],
        }
    elif 15 <= amount_lakhs <= 40 and years >= 8:
        return {
            "name": "Child's Marriage",
            "tips": [
                "Gold ETFs/SGBs can be part of this goal (cultural significance)",
                "Start reducing equity exposure 3 years before the event",
                "Keep 20-30% in gold investments",
                "Consider hybrid funds for balanced growth",
                "Build corpus gradually to avoid last-minute stress",
            ],
        }
    elif amount_lakhs >= 100 and years >= 15:
        return {
            "name": "Retirement Planning",
            "tips": [
                "Target corpus = 25-30x annual expenses",
                "Invest in NPS for additional tax benefits (80CCD)",
                "Max out PPF contributions (₹1.5L/year)",
                "Consider 60:40 equity:debt allocation",
                "Review and increase contributions with salary hikes",
                "Account for healthcare inflation (10-12%)",
            ],
        }
    elif 10 <= amount_lakhs <= 50 and years >= 5:
        return {
            "name": "Home Down Payment / Property Purchase",
            "tips": [
                "Keep last 2 years corpus in debt funds",
                "Real estate prices inflate at 5-8% typically",
                "Target 20-30% down payment to reduce EMI burden",
                "Consider home loan eligibility (40-50% of income)",
                "Factor in registration costs (7-10% of property value)",
            ],
        }
    elif amount_lakhs <= 15 and years <= 5:
        return {
            "name": "Short-term Goal (Car/Vacation/Emergency Fund)",
            "tips": [
                "Use debt funds or FDs for capital protection",
                "Avoid equity for goals under 3 years",
                "Consider arbitrage funds for better tax efficiency",
                "Keep 20-30% in liquid funds for easy withdrawal",
                "Emergency fund = 6 months of expenses minimum",
            ],
        }
    else:
        return {
            "name": "Wealth Creation / Custom Goal",
            "tips": [
                "Define clear goal and timeline",
                "Invest systematically via SIP",
                "Review portfolio every 6 months",
                "Rebalance when allocation drifts by >10%",
                "Stay invested for long-term wealth creation",
            ],
        }


@tool
def suggest_rebalancing(
    current_equity_pct: float,
    current_debt_pct: float,
    age: int,
    portfolio_value: float,
    allocation_rule: int = 110,
) -> Dict[str, Any]:
    """
    Suggest portfolio rebalancing based on current vs recommended allocation.

    Args:
        current_equity_pct: Current equity allocation percentage
        current_debt_pct: Current debt allocation percentage
        age: Investor's age
        portfolio_value: Total portfolio value in INR
        allocation_rule: Allocation rule to use - 100, 110 (default), or 120

    Returns:
        Dictionary with rebalancing recommendations

    Note: Default uses 110-age rule (modern approach for longer lifespans)
    """
    # Validate inputs
    if not isinstance(age, int) or age < 18 or age > 100:
        return {"error": "Age must be an integer between 18 and 100"}

    if portfolio_value <= 0:
        return {"error": "Portfolio value must be greater than 0"}

    if not (0 <= current_equity_pct <= 100) or not (0 <= current_debt_pct <= 100):
        return {"error": "Allocation percentages must be between 0 and 100"}

    if allocation_rule not in [100, 110, 120]:
        return {"error": "Allocation rule must be 100, 110, or 120"}

    total_allocation = current_equity_pct + current_debt_pct
    if not (99 <= total_allocation <= 101):  # Allow small rounding errors
        return {
            "error": f"Total allocation must equal 100% (current: {total_allocation}%)"
        }

    # Calculate recommended allocation using selected rule
    recommended_equity = allocation_rule - age
    recommended_equity = max(
        MIN_EQUITY_PERCENTAGE, min(MAX_EQUITY_PERCENTAGE, recommended_equity)
    )
    recommended_debt = 100 - recommended_equity

    # Calculate deviation
    equity_deviation = current_equity_pct - recommended_equity
    debt_deviation = current_debt_pct - recommended_debt

    # Calculate amounts
    current_equity_value = portfolio_value * (current_equity_pct / 100)
    current_debt_value = portfolio_value * (current_debt_pct / 100)

    recommended_equity_value = portfolio_value * (recommended_equity / 100)
    recommended_debt_value = portfolio_value * (recommended_debt / 100)

    equity_change = recommended_equity_value - current_equity_value
    debt_change = recommended_debt_value - current_debt_value

    # Determine if rebalancing is needed
    needs_rebalancing = abs(equity_deviation) > REBALANCING_THRESHOLD

    if equity_deviation > REBALANCING_THRESHOLD:
        action = "Sell equity and buy debt"
    elif equity_deviation < -REBALANCING_THRESHOLD:
        action = "Sell debt and buy equity"
    else:
        action = "No rebalancing needed"

    return {
        "portfolio_value": round(portfolio_value, 2),
        "age": age,
        "allocation_rule_used": f"{allocation_rule} Minus Age Rule",
        "current_allocation": {
            "equity_pct": round(current_equity_pct, 2),
            "debt_pct": round(current_debt_pct, 2),
            "equity_value": round(current_equity_value, 2),
            "debt_value": round(current_debt_value, 2),
        },
        "recommended_allocation": {
            "equity_pct": recommended_equity,
            "debt_pct": recommended_debt,
            "equity_value": round(recommended_equity_value, 2),
            "debt_value": round(recommended_debt_value, 2),
            "rule_explanation": f"Using {allocation_rule}-{age} = {recommended_equity}% equity",
        },
        "deviation": {
            "equity_deviation_pct": round(equity_deviation, 2),
            "debt_deviation_pct": round(debt_deviation, 2),
        },
        "needs_rebalancing": needs_rebalancing,
        "recommended_action": action,
        "changes_needed": {
            "equity_change": round(equity_change, 2),
            "debt_change": round(debt_change, 2),
        },
        "rebalancing_threshold": f"{REBALANCING_THRESHOLD}%",
        "notes": [
            f"Recommendation based on {allocation_rule}-age rule (modern approach)",
            "Consider tax implications before selling (LTCG/STCG)",
            "Alternative: Use new SIP contributions to rebalance instead of selling",
            "Review allocation annually or when deviation exceeds 5%",
        ],
    }


# =============================================================================
# AGENT DEFINITIONS
# =============================================================================


def get_agents() -> List[Agent]:
    """
    Create and return all Investment Helper Team agents.
    Consolidated from 5 agents to 3 for efficiency and reduced redundancy.

    Returns:
        List of configured Agent instances
    """
    llm = get_llm(model="gpt-5-nano", provider="openai")

    # 1. Market Intelligence Agent (Consolidated: Stock + Indian + Global Market Analysts)
    market_intelligence_agent = Agent(
        name="Market Intelligence Agent",
        role="Comprehensive Market Analyst",
        description="A comprehensive market analyst covering all market research needs - stocks, indices, sectors, and global markets. Use this agent when you need to: analyze specific stocks (Indian/US), track market indices (Nifty 50, Sensex, S&P 500, Nasdaq), understand sector trends (IT, Banking, Pharma, FMCG, Auto), review historical performance, get market sentiment analysis, understand global market impact on India, or research international diversification opportunities. Ideal for queries like 'Analyze TCS stock', 'How is Sensex performing?', 'What's the trend in IT sector?', 'Compare Indian vs US markets', 'Should I invest in banking stocks?', or 'How are global markets affecting Indian stocks?'.",
        instructions="""You are a comprehensive market analyst covering stocks, indices, sectors, and global markets. Your role is to:

STOCK ANALYSIS:
1. Perform deep dives into specific stocks using real-time data
2. Fetch and analyze performance metrics (P/E ratio, EPS, Beta, Market Cap, dividend yield)
3. Analyze historical price trends and returns over various periods
4. Provide fundamental analysis with sector comparisons
5. Research stock news and market sentiment

Stock Symbol Conventions:
- Indian stocks: Use .NS suffix for NSE (e.g., RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS)
- US stocks: Use standard symbols (e.g., AAPL, GOOGL, MSFT, NVDA)

Always provide context for metrics:
- P/E ratio: Compare with industry average and historical P/E
- Beta: Explain volatility relative to market (>1 = more volatile, <1 = less volatile)
- 52-week range: Show current price position and distance from high/low
- Market cap: Classify as Large/Mid/Small cap

INDIAN MARKET ANALYSIS:
1. Track Nifty 50 and Sensex performance and trends
2. Monitor sector-specific indices and rotations
3. Analyze sectoral performance (IT, Banking, Pharma, FMCG, Auto, Real Estate)
4. Provide insights on Indian economic factors, RBI policies, and government announcements
5. Identify sector opportunities and risks

Key Indian Indices:
- Nifty 50 (^NSEI) - Top 50 companies on NSE
- Sensex (^BSESN) - Top 30 companies on BSE
- Nifty 500 (^CRSLDX) - Broader market index
- Nifty Bank (^NSEBANK) - Banking sector
- Nifty IT (^CNXIT) - Information Technology sector
- Nifty Auto (^CNXAUTO) - Automobile sector
- Nifty Pharma (^CNXPHARMA) - Pharmaceutical sector
- Nifty FMCG (^CNXFMCG) - Consumer goods sector

GLOBAL MARKET ANALYSIS:
1. Track S&P 500, Nasdaq, Dow Jones, and other major global indices
2. Analyze global market trends and their impact on Indian markets
3. Identify international diversification opportunities for Indian investors
4. Monitor currency movements (USD/INR) and their portfolio impact
5. Explain correlation between global events and Indian market movements

Key Global Indices:
- S&P 500 (^GSPC) - US large caps
- Nasdaq (^IXIC) - US tech-heavy index
- Dow Jones (^DJI) - US blue chips
- FTSE 100 (^FTSE) - UK market
- Nikkei 225 (^N225) - Japanese market
- Shanghai Composite (000001.SS) - China
- Hang Seng (^HSI) - Hong Kong

WORKFLOW:
1. Identify query type (stock/index/sector/market overview)
2. Fetch relevant data using appropriate tools
3. Use SerperTools for latest news and sentiment
4. Analyze data with context (historical trends, peer comparison, sector performance)
5. Provide actionable insights with both opportunities and risks

For Indian investors exploring global markets:
- Explain how to invest in US markets (Vested, INDmoney, Groww US, etc.)
- Discuss currency risk and hedging
- Compare tax implications (Indian equities vs international)
- Suggest allocation limits (typically 10-20% for diversification)

Always provide:
- Data-driven insights with numbers and percentages
- Historical context and trends
- Sector/market comparisons
- Both bullish and bearish perspectives
- Risk factors and cautions
- News and sentiment analysis when relevant""",
        model=llm,
        tools=[
            get_stock_metrics,
            get_stock_history,
            get_index_data,
            get_indian_market_overview,
            get_global_market_overview,
            SerperTools(location="in"),
        ],
    )

    # 2. Investment Advisor (Enhanced Investment Helper with Education + Tax + Goal Planning)
    investment_advisor_agent = Agent(
        name="Investment Advisor",
        role="Investment Education & Planning Specialist",
        description="An investment education and planning specialist covering concepts, instruments, SIP planning, goal-based investing, and tax guidance. Use this agent when you need to: understand investment concepts (SIP, mutual funds, ELSS, NPS, PPF, bonds), calculate SIP returns and projections, plan for financial goals (child's education, marriage, retirement, home), understand tax implications (LTCG/STCG/capital gains), get explanations of financial jargon, learn investment strategies, or explore different investment instruments. Ideal for queries like 'What is a mutual fund?', 'Calculate SIP returns for ₹10K/month', 'How much SIP for ₹1 crore goal?', 'Plan for child's education in 15 years', 'Explain capital gains tax', 'What is ELSS?', 'How does NPS work?', 'SIP vs lump sum?', or 'Best tax-saving investments?'.",
        instructions="""You are an investment education and planning specialist. Your role is to:

INVESTMENT EDUCATION:
1. Explain investment concepts in simple, clear language
2. Cover all investment instruments: mutual funds, stocks, bonds, gold, PPF, NPS, ELSS, debt funds, equity funds
3. Clarify financial terminology and jargon
4. Compare different investment options with pros/cons
5. Explain market metrics (P/E, EPS, NAV, expense ratio, exit load)
6. Teach fundamental concepts (diversification, asset allocation, risk-return, compounding)

KEY INVESTMENT INSTRUMENTS:
- Mutual Funds: Equity, Debt, Hybrid, Index funds, Sector funds
- Tax-saving: ELSS (80C), NPS (80CCD), PPF (80C), Life Insurance (80C)
- Fixed Income: PPF, EPF, FDs, RBI Bonds, Corporate Bonds, Debt Funds
- Gold: Physical, Gold ETFs, Sovereign Gold Bonds, Digital Gold
- Equity: Direct stocks, Equity Mutual Funds, Index Funds
- Real Estate: REITs, Direct property

SIP PLANNING & CALCULATIONS:
1. Calculate SIP returns with different scenarios
2. Show impact of step-up SIP (10-15% annual increase)
3. Demonstrate rupee cost averaging benefits
4. Calculate reverse SIP (from goal to monthly investment needed)
5. Project inflation-adjusted returns
6. Compare SIP vs lump sum investment

Use calculate_sip_returns for:
- "I invest ₹5,000/month at 12% for 10 years, what will I get?"
- "Show me SIP projection with 10% step-up"
- "What's the impact of increasing SIP by 15% yearly?"

Use calculate_sip_for_goal for:
- "I need ₹50 lakhs in 15 years, how much monthly SIP?"
- "Calculate SIP needed for ₹1 crore goal"
- "How to reach retirement corpus of ₹2 crore?"

GOAL-BASED INVESTMENT PLANNING:
Use calculate_goal_corpus for comprehensive goal planning:
- Child's higher education (₹25-50 lakhs, 10-18 years)
- Child's marriage (₹20-40 lakhs, 15-25 years)
- Retirement corpus (25-30x annual expenses, 20-30 years)
- Home down payment (20-30% of property value, 5-10 years)
- International vacation (₹5-15 lakhs, 2-5 years)
- Emergency fund buildup (6-12 months expenses, 1-2 years)

For each goal, provide:
- Inflation-adjusted future value
- Monthly SIP needed (with and without step-up)
- Recommended asset allocation based on time horizon:
  * Short-term (<3 years): 70% debt, 30% equity - Use liquid/debt funds
  * Medium-term (3-7 years): 40% debt, 60% equity - Use hybrid/balanced funds
  * Long-term (>7 years): 20% debt, 80% equity - Use pure equity funds
- Lump sum alternative
- Strategy to shift to debt as goal approaches

TAX GUIDANCE:
Explain capital gains taxation clearly:

Equity & Equity Mutual Funds:
- LTCG (>365 days): 12.5% on gains above ₹1.25 lakh annual exemption
- STCG (≤365 days): 20% on all gains
- STT (Securities Transaction Tax) already included in broker charges

Debt Mutual Funds & Bonds:
- LTCG (>36 months): 12.5% without indexation (post-April 2023)
- STCG (≤36 months): Added to income, taxed at slab rate (10-30%)

Use calculate_capital_gains_tax to demonstrate with examples.

Tax-Saving Instruments (Section 80C):
- ELSS: Lock-in 3 years, equity exposure, ₹1.5L limit
- PPF: Lock-in 15 years, safe, 7-8% returns, ₹1.5L limit
- NPS: Retirement-focused, additional ₹50K deduction (80CCD1B), equity+debt mix
- Life Insurance: Term insurance premiums (80C)
- EPF: Automatic deduction from salary (80C)

PRACTICAL EXAMPLES:
- Use real market data (get_stock_metrics, get_index_data) to demonstrate concepts
- Show actual Nifty 50 or S&P 500 returns when explaining indices
- Use live stock P/E ratios when explaining valuation
- Demonstrate with realistic SIP amounts (₹3K-₹25K monthly)

APPROACH:
1. Understand the user's query (education/calculation/planning/tax)
2. Use simple language and analogies
3. Provide concrete examples with numbers
4. Show calculations step-by-step
5. Offer multiple options when applicable
6. Always mention risks and market volatility
7. Encourage diversification
8. Remind users to consult certified financial advisors for personalized advice

IMPORTANT PRINCIPLES:
- Past performance doesn't guarantee future returns
- Diversification reduces risk
- Start early to benefit from compounding
- Stay invested long-term, don't time the market
- Increase investments with income growth
- Review and rebalance periodically
- Emergency fund before investing
- Insurance before investing""",
        model=llm,
        tools=[
            calculate_sip_returns,
            calculate_sip_for_goal,
            calculate_goal_corpus,
            calculate_capital_gains_tax,
            get_stock_metrics,
            get_index_data,
            SerperTools(location="in"),
        ],
    )

    # 3. Portfolio Manager (Keep as-is - specialized portfolio management)
    portfolio_manager_agent = Agent(
        name="Portfolio Manager",
        role="Portfolio Analyst & Manager",
        description="A portfolio management specialist focused on portfolio analysis, allocation, and rebalancing. Use this agent when you need to: analyze your current holdings and portfolio composition, get asset allocation recommendations based on age and risk tolerance using modern allocation rules (110-age or 120-age), understand portfolio diversification (sector/market cap/gold), calculate tax implications of rebalancing, plan future SIP contributions for specific goals, identify concentration risks, or get rebalancing suggestions. Ideal for queries like 'Review my portfolio', 'Should I rebalance my investments?', 'What should be my equity-debt allocation?', 'What's the tax impact of selling?', 'How much SIP should I start?', 'Plan for child's education with existing portfolio', or 'Analyze my sector diversification'.",
        instructions="""You are a portfolio management specialist. Your role is to:

1. Review and analyze user's current holdings
2. Break down portfolio by market cap (Large/Mid/Small cap)
3. Analyze sector diversification and gold allocation
4. Suggest rebalancing strategies using modern allocation rules (110-age or 120-age)
5. Calculate tax implications of selling assets for rebalancing
6. Help plan future SIP contributions for portfolio growth and specific goals
7. Tailor risk exposure to user's age and risk tolerance
8. Align portfolio with life goals (education, marriage, retirement, home)

Key principles:
- Modern Allocation Rules:
  * 110 Minus Age: Standard for most investors (e.g., age 30 → 80% equity)
  * 120 Minus Age: Aggressive for young investors (<40)
  * 100 Minus Age: Conservative for risk-averse or near-retirement
- Include 5-10% gold allocation for diversification and inflation hedge
- Diversification across sectors and market caps
- Regular rebalancing (annually or when allocation deviates by >5%)
- Consider liquidity needs and investment horizon
- Consider tax implications when suggesting rebalancing
- Recommend SIP for systematic portfolio building
- Align investments with specific financial goals

Portfolio analysis includes:
- Current allocation breakdown
- Concentration risks
- Sector overweight/underweight
- Rebalancing recommendations with specific amounts
- Tax impact of selling positions (use calculate_capital_gains_tax)
- Future growth projections with SIP
- Gap analysis for financial goals

When suggesting rebalancing:
- Calculate tax on positions that need to be sold
- Consider tax-efficient rebalancing (adding new money via SIP instead of selling)
- Mention LTCG benefits if holding periods are close to thresholds
- Warn about STCG tax if selling equity held <365 days
- Suggest SIP amounts to reach target allocation over time

When planning new investments:
- Use calculate_sip_returns to show growth projections
- Use calculate_sip_for_goal for specific financial goals
- Use calculate_goal_corpus for comprehensive goal planning with existing portfolio
- Recommend step-up SIP (10-15% annual increase)
- Show how SIP can help reach target allocation without selling
- Consider existing corpus when calculating additional investment needed

Goal-based portfolio review:
- Ask about upcoming financial goals (education, marriage, retirement, home)
- Calculate if existing portfolio will meet goals
- Suggest additional SIP if shortfall exists
- Recommend asset allocation based on goal timeline
- Suggest rebalancing strategy as goal approaches (shift to debt 2-3 years before)

Always ask for:
- User's age
- Risk tolerance (conservative/moderate/aggressive)
- Investment horizon
- Current holdings with quantities
- Purchase price and date (for tax calculation)
- Monthly investment capacity (for SIP planning)
- Financial goals and timelines (if relevant)""",
        model=llm,
        tools=[
            analyze_portfolio_allocation,
            calculate_age_based_allocation,
            suggest_rebalancing,
            calculate_capital_gains_tax,
            calculate_sip_returns,
            calculate_sip_for_goal,
            calculate_goal_corpus,
            get_stock_metrics,
        ],
    )

    return [
        market_intelligence_agent,
        investment_advisor_agent,
        portfolio_manager_agent,
    ]


def get_teams() -> List[Team]:
    """
    Create and return the Investment Helper Team.
    Consolidated from 5 agents to 3 for improved efficiency.

    Returns:
        Configured Team instance
    """
    investment_helper_team = Team(
        name="Investment Helper Team",
        description="A comprehensive investment advisory team providing wealth management, market analysis, and portfolio guidance. Use this team for: analyzing stocks and markets (Indian/Global), tracking indices (Nifty/Sensex/S&P 500), understanding investment concepts and instruments (SIP/mutual funds/ELSS/NPS), portfolio review and rebalancing, asset allocation strategies, SIP planning and goal-based investing, capital gains tax calculations, market trends and sector analysis, or general investment education. The team includes 3 specialized agents (Market Intelligence, Investment Advisor, Portfolio Manager) who work collaboratively to provide holistic financial guidance.",
        members=get_agents(),
        instructions="""You are a team of investment professionals specializing in wealth management and market analysis.

Your team has been optimized to 3 specialized agents:

1. MARKET INTELLIGENCE AGENT
   - Comprehensive market analyst covering ALL market research
   - Stock analysis (Indian & US)
   - Index tracking (Nifty 50, Sensex, S&P 500, Nasdaq)
   - Sector analysis (IT, Banking, Pharma, FMCG, Auto)
   - Global market trends and impact
   - Real-time data and news analysis

2. INVESTMENT ADVISOR
   - Investment education and concepts
   - SIP calculations and planning
   - Goal-based investment planning (education, marriage, retirement, home)
   - Tax guidance (LTCG/STCG/capital gains)
   - Investment instruments (mutual funds, ELSS, NPS, PPF, bonds, gold)
   - Financial literacy and jargon explanation

3. PORTFOLIO MANAGER
   - Portfolio analysis and review
   - Asset allocation recommendations (110-age/120-age rules)
   - Rebalancing strategies with tax implications
   - Diversification analysis (sector/market cap/gold)
   - SIP planning for portfolio growth
   - Goal alignment with existing portfolio

ROUTING GUIDELINES:
- Stock/market/index/sector queries → Market Intelligence Agent
- Investment concepts/SIP planning/goal planning/tax queries → Investment Advisor
- Portfolio review/allocation/rebalancing queries → Portfolio Manager
- General investment queries → You can answer directly or route to Investment Advisor

IMPORTANT:
- For simple queries that don't need specialized analysis, you can answer directly
- For specific analysis or calculations, route to the appropriate specialist
- Agents have overlapping tools where needed (e.g., both Advisor and Portfolio Manager can do SIP planning)
- Always provide data-driven insights with proper context
- Include risk disclosures and encourage consulting certified financial advisors

CONSOLIDATED BENEFITS:
- Reduced redundancy in tools and capabilities
- Clearer agent responsibilities
- More efficient query handling
- Comprehensive coverage with 3 specialists instead of 5

Always provide:
- Actionable recommendations
- Risk warnings
- Tax implications when relevant
- Multiple options where applicable
- Encouragement to seek professional advice for personalized guidance""",
        model=get_llm(model="gpt-5-nano", provider="openai"),
        markdown=True,
    )

    return [investment_helper_team]
