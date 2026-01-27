"""
Agents package for FinAgent application.

Contains specialized agent teams:
- Personal Finance Team: Financial foundation, compliance, and lifestyle planning
- Investment Team: Wealth accumulation, market research, and portfolio growth
"""

from .personal_finance_team import get_agents as get_personal_finance_agents
from .investment_team import get_agents as get_investment_agents


def get_all_agents():
    """Get all agents from all teams."""
    return get_personal_finance_agents() + get_investment_agents()


__all__ = [
    "get_personal_finance_agents",
    "get_investment_agents",
    "get_all_agents",
]

