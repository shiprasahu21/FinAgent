"""
Investment Helper Team - Wealth accumulation, market research, and portfolio growth.

Agents:
1. Stock Analysis Agent - Equity Researcher (YFinance, Web Search)
2. Indian Market Analysis Agent - Domestic Strategist
3. Foreign Market Analysis Agent - Global Strategist
4. General Investment Helper Agent - Investment Concierge
5. Portfolio Analyser Agent - Portfolio Manager
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
    age: int, risk_tolerance: str = "moderate"
) -> Dict[str, Any]:
    """
    Calculate recommended asset allocation using the '100 Minus Age' rule.

    Args:
        age: Investor's age
        risk_tolerance: Risk tolerance - 'conservative', 'moderate', 'aggressive'

    Returns:
        Dictionary with recommended allocation
    """
    # Validate inputs
    if not isinstance(age, int) or age < 18 or age > 100:
        return {"error": "Age must be an integer between 18 and 100"}

    valid_risk_levels = ["conservative", "moderate", "aggressive"]
    if risk_tolerance.lower() not in valid_risk_levels:
        return {
            "error": f"Invalid risk tolerance. Must be one of: {', '.join(valid_risk_levels)}"
        }

    # Base equity allocation: 100 - age
    base_equity = 100 - age

    # Adjust based on risk tolerance
    adjustments = {
        "conservative": -10,
        "moderate": 0,
        "aggressive": 10,
    }

    adjustment = adjustments[risk_tolerance.lower()]
    equity_pct = max(
        MIN_EQUITY_PERCENTAGE, min(MAX_EQUITY_PERCENTAGE, base_equity + adjustment)
    )
    debt_pct = 100 - equity_pct

    # Further breakdown based on age
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

    debt_breakdown = {
        "ppf_epf": 40,
        "debt_funds": 30,
        "fixed_deposits": 20,
        "bonds": 10,
    }

    return {
        "age": age,
        "risk_tolerance": risk_tolerance,
        "rule_used": "100 Minus Age Rule",
        "recommended_allocation": {
            "equity_percentage": equity_pct,
            "debt_percentage": debt_pct,
        },
        "equity_breakdown": {
            k: round(v * equity_pct / 100, 1) for k, v in equity_breakdown.items()
        },
        "debt_breakdown": {
            k: round(v * debt_pct / 100, 1) for k, v in debt_breakdown.items()
        },
        "rebalancing_frequency": f"Annually or when allocation deviates by >{REBALANCING_THRESHOLD}%",
    }


@tool
def suggest_rebalancing(
    current_equity_pct: float,
    current_debt_pct: float,
    age: int,
    portfolio_value: float,
) -> Dict[str, Any]:
    """
    Suggest portfolio rebalancing based on current vs recommended allocation.

    Args:
        current_equity_pct: Current equity allocation percentage
        current_debt_pct: Current debt allocation percentage
        age: Investor's age
        portfolio_value: Total portfolio value in INR

    Returns:
        Dictionary with rebalancing recommendations
    """
    # Validate inputs
    if not isinstance(age, int) or age < 18 or age > 100:
        return {"error": "Age must be an integer between 18 and 100"}

    if portfolio_value <= 0:
        return {"error": "Portfolio value must be greater than 0"}

    if not (0 <= current_equity_pct <= 100) or not (0 <= current_debt_pct <= 100):
        return {"error": "Allocation percentages must be between 0 and 100"}

    total_allocation = current_equity_pct + current_debt_pct
    if not (99 <= total_allocation <= 101):  # Allow small rounding errors
        return {
            "error": f"Total allocation must equal 100% (current: {total_allocation}%)"
        }

    # Calculate recommended allocation
    recommended_equity = 100 - age
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
    }


# =============================================================================
# AGENT DEFINITIONS
# =============================================================================


def get_agents() -> List[Agent]:
    """
    Create and return all Investment Helper Team agents.

    Returns:
        List of configured Agent instances
    """
    llm = get_llm()

    # 1. Stock Analysis Agent
    stock_analysis_agent = Agent(
        name="Stock Analyst",
        role="Equity Researcher",
        description="A stock analyst specializing in individual equity research and analysis. Use this agent when you need to: analyze specific stocks (Indian or US), fetch real-time stock metrics (P/E, EPS, Beta, Market Cap), review historical price performance and trends, or get fundamental analysis insights. Ideal for queries like 'Analyze TCS stock', 'What is the P/E ratio of Reliance?', or 'Show me Apple's performance over the last year'.",
        instructions="""You are an equity research analyst specializing in stock analysis. Your role is to:
1. Perform deep dives into specific stocks using real-time data
2. Fetch and analyze performance metrics (P/E ratio, EPS, Beta, Market Cap)
3. Analyze historical price trends and returns
4. Provide fundamental analysis insights

For Indian stocks, use .NS suffix for NSE (e.g., RELIANCE.NS, TCS.NS, INFY.NS)
For US stocks, use standard symbols (e.g., AAPL, GOOGL, MSFT)

Always provide context for the metrics:
- P/E ratio: Compare with industry average
- Beta: Explain volatility relative to market
- 52-week range: Show current price position

Steps to follow:
1. Fetch the stock symbol using SerperTools
2. Fetch the stock metrics and history using the stock symbol
2. Fetch the stock news using SerperTools
3. Analyze the stock metrics and news
4. Provide the analysis

Be objective and present both bullish and bearish perspectives.""",
        model=llm,
        tools=[get_stock_metrics, get_stock_history, SerperTools(location="in")],
    )

    # 2. Indian Market Analysis Agent
    indian_market_agent = Agent(
        name="Indian Market Analyst",
        role="Domestic Market Strategist",
        description="A domestic market strategist focused on Indian stock markets and economy. Use this agent when you need to: track Nifty 50/Sensex performance, analyze Indian sector trends (IT, Banking, Pharma, FMCG, Auto), understand Indian market sentiment and rotations, or get insights on RBI policies and government announcements. Ideal for queries like 'How is the Indian IT sector performing?', 'What's the Sensex trend today?', or 'Should I invest in banking stocks now?'.",
        instructions="""You are a domestic market strategist focused on the Indian stock market. Your role is to:
1. Track Nifty 50 and Sensex performance
2. Monitor sector-specific trends (IT, Banking, Pharma, FMCG, Auto)
3. Analyze sector rotations and market sentiment
4. Provide insights on Indian economic factors affecting markets

Key indices to track:
- Nifty 50 (^NSEI) - Top 50 companies on NSE
- Sensex (^BSESN) - Top 30 companies on BSE
- Nifty 500 (^CNX500) - Broader market index
- Nifty Bank (^NSEBANK) - Banking sector
- Nifty IT (^CNXIT) - IT sector
- Nifty Auto (^CNXAUTO) - Automobile sector
- Nifty Pharma (^CNXPHARMA) - Pharmaceutical sector
- Nifty FMCG (^CNXFMCG) - Consumer goods sector

Tools to use:
- Use get_indian_market_overview to get the overview of the Indian market.
- Use get_index_data to get the data for a specific index.
- Use get_stock_metrics to get the metrics for a specific stock.
- Use search_news to get the news OR search_google to get the web search results for a specific stock/index/sector/economy/government.

Provide actionable insights on:
- Market direction and momentum
- Sector opportunities
- Risk factors specific to Indian markets
- Impact of RBI policies, government announcements, and global factors""",
        model=llm,
        tools=[
            get_indian_market_overview,
            get_index_data,
            get_stock_metrics,
            SerperTools(location="in"),
        ],
    )

    # 3. Foreign Market Analysis Agent
    foreign_market_agent = Agent(
        name="Global Market Analyst",
        role="Global Market Strategist",
        description="A global market strategist specializing in international markets, especially US and major world indices. Use this agent when you need to: track S&P 500/Nasdaq/Dow Jones performance, analyze global market trends and their impact on India, explore international diversification opportunities, or understand currency movements (USD/INR). Ideal for queries like 'How are US tech stocks performing?', 'What's the S&P 500 trend?', 'Should I diversify into global markets?', or 'How does US market affect Indian stocks?'.",
        instructions="""You are a global market strategist focused on international markets, especially US markets. Your role is to:

1. Track S&P 500, Nasdaq, and Dow Jones performance
2. Analyze global market trends and their impact on Indian markets
3. Identify international diversification opportunities for Indian investors
4. Monitor currency movements (USD/INR) and their impact

Key indices:
- S&P 500 (^GSPC) - US large caps
- Nasdaq (^IXIC) - US tech-heavy index
- Dow Jones (^DJI) - US blue chips
- Nifty 50 (^NSEI) - India
- Sensex (^BSESN) - India
- FTSE 100 (^FTSE) - UK market
- Nikkei 225 (^N225) - Japanese market
- Shanghai Composite (000001.SS) - China
- Hang Seng (^HSI) - Hong Kong

For Indian investors, explain:
- How to invest in US markets (Vested, INDmoney, etc.)
- Tax implications of international investing
- Currency hedging considerations
- Global trends affecting Indian portfolios""",
        model=llm,
        tools=[
            get_global_market_overview,
            get_index_data,
            get_stock_metrics,
        ],
    )

    # 4. General Investment Helper Agent
    investment_helper_agent = Agent(
        name="Investment Helper",
        role="Investment Education Specialist",
        description="An investment education specialist and financial literacy expert. Use this agent when you need to: understand investment concepts and terminology, learn about investment instruments (SGB, ELSS, NPS, PPF, SIP, mutual funds), get explanations of financial jargon, understand market metrics, or explore investment basics. Ideal for queries like 'What is a mutual fund?', 'Explain P/E ratio', 'What is SIP?', 'How does ELSS work?', or 'What's the difference between FD and debt funds?'.",
        instructions="""You are an investment education specialist.
Your role is to:
1. Answer ad-hoc queries about financial concepts
2. Explain investment instruments (SGB, ELSS, NPS, PPF, SIP, etc.)
3. Clarify investment terminology and jargon
4. Help users understand market data and stock metrics

Topics you cover:
- Mutual funds (types, selection, expense ratios)
- Fixed income instruments (FDs, bonds, debt funds)
- Gold investments (Physical, ETF, SGB)
- Tax-saving instruments
- Retirement planning basics
- Insurance (Term, ULIP, Endowment)
- Stock market basics and how to read financial metrics

Always explain concepts in simple terms with examples.
Use analogies when helpful.
You can fetch real stock data to demonstrate concepts with live examples.
Encourage users to do their own research and consult financial advisors for personalized advice.""",
        model=llm,
        tools=[
            get_stock_metrics,
            get_index_data,
            get_indian_market_overview,
            get_global_market_overview,
            SerperTools(location="in"),
        ],
    )

    # 5. Portfolio Analyser Agent
    portfolio_analyser_agent = Agent(
        name="Portfolio Manager",
        role="Portfolio Analyst & Manager",
        description="A portfolio management specialist focused on portfolio analysis, allocation, and rebalancing. Use this agent when you need to: analyze your current holdings and portfolio composition, get asset allocation recommendations based on age and risk tolerance, understand portfolio diversification (sector/market cap), identify concentration risks, or get rebalancing suggestions using the '100 Minus Age' rule. Ideal for queries like 'Review my portfolio', 'Should I rebalance my investments?', 'What should be my equity-debt allocation?', or 'Analyze my sector diversification'.",
        instructions="""You are a portfolio management specialist. Your role is to:

1. Review and analyze user's current holdings
2. Break down portfolio by market cap (Large/Mid/Small cap)
3. Analyze sector diversification
4. Suggest rebalancing strategies based on the "100 Minus Age" rule
5. Tailor risk exposure to user's age and risk tolerance

Key principles:
- 100 Minus Age Rule: Equity % = 100 - Age (adjust for risk tolerance)
- Diversification across sectors and market caps
- Regular rebalancing (annually or when allocation deviates by >5%)
- Consider liquidity needs and investment horizon

Portfolio analysis includes:
- Current allocation breakdown
- Concentration risks
- Sector overweight/underweight
- Rebalancing recommendations with specific amounts

Always ask for:
- User's age
- Risk tolerance (conservative/moderate/aggressive)
- Investment horizon
- Current holdings with quantities""",
        model=llm,
        tools=[
            analyze_portfolio_allocation,
            calculate_age_based_allocation,
            suggest_rebalancing,
            get_stock_metrics,
        ],
    )

    return [
        stock_analysis_agent,
        indian_market_agent,
        foreign_market_agent,
        investment_helper_agent,
        portfolio_analyser_agent,
    ]


def get_teams() -> List[Team]:
    """
    Create and return the Investment Helper Team.

    Returns:
        Configured Team instance
    """
    investment_helper_team = Team(
        name="Investment Helper Team",
        description="A comprehensive investment advisory team providing wealth management, market analysis, and portfolio guidance. Use this team for: analyzing stocks and markets (Indian/Global), understanding investment concepts and instruments, portfolio review and rebalancing, asset allocation strategies, market trends and sector analysis, or general investment education. The team includes specialized agents for stock analysis, Indian markets, global markets, investment education, and portfolio management who work collaboratively to provide holistic financial guidance.",
        members=get_agents(),
        instructions="""You are a team of investment professionals specializing in wealth management and market analysis.

Your collective expertise includes:
- Stock and equity analysis with real-time data
- Indian and global market insights
- Portfolio management and rebalancing strategies
- Investment education and financial literacy
- Age-based asset allocation recommendations

Work collaboratively to provide comprehensive investment guidance. Route queries to the most relevant specialist:
- Stock-specific queries → Stock Analyst
- Indian market questions → Indian Market Analyst
- Global/US market questions → Global Market Analyst
- General investment concepts → Investment Helper
- Portfolio review/rebalancing → Portfolio Manager

IMPORTANT:
- For general queries where you don't require any specific agent, you can directly reply back to user.
- For specific queries, you can route them to the most relevant specialist agent memeber.
- Use only relevant knowledge base documents to answer the user's query.

Always provide data-driven insights with proper context and risk disclosures.
Encourage users to consult certified financial advisors for personalized advice.""",
        model=get_llm("amazon.nova-pro-v1-0"),
        markdown=True,
    )

    return [investment_helper_team]
