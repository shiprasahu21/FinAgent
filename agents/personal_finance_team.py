"""
Personal Finance Team - Financial foundation, compliance, and lifestyle planning.

Agents:
1. General Finance Agent - Holistic Financial Advisor
2. Spending Analysis Agent - Expense Tracker & Analyst
3. Tax Planning Assistant Agent - Compliance Specialist (Indian IT rules)
4. Home Planning Agent - Real Estate Planner
"""

from typing import List
from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.team import Team
from agno.tools import tool
from agno.tools.serper import SerperTools
from agno.vectordb.chroma import ChromaDb

from core.llm import get_llm


knowledge_base = Knowledge(
    name="Financial Documents",
    description="This is a knowledge base for financial documents which includes income tax documents, personal financing documents, etc.",
    vector_db=ChromaDb(
        collection="financial_documents",
        path="tmp/chroma",
        persistent_client=True,
        embedder=SentenceTransformerEmbedder(id="all-MiniLM-L6-v2"),
    ),
    max_results=10,
)

# =============================================================================
# CUSTOM TOOLS FOR PERSONAL FINANCE TEAM
# =============================================================================


@tool
def calculate_life_insurance_coverage(
    annual_income: float, multiplier: float = 15.0
) -> dict:
    """
    Calculate recommended life insurance sum assured using thumb rules.

    Args:
        annual_income: User's annual income in INR
        multiplier: Multiplier for sum assured (default 15x, range 10-20x)

    Returns:
        Dictionary with recommended coverage details
    """
    min_coverage = annual_income * 10
    recommended_coverage = annual_income * multiplier
    max_coverage = annual_income * 20

    return {
        "annual_income": annual_income,
        "minimum_coverage_10x": min_coverage,
        "recommended_coverage": recommended_coverage,
        "maximum_coverage_20x": max_coverage,
        "multiplier_used": multiplier,
        "rule": "10-20x annual income thumb rule",
    }


@tool
def calculate_emergency_fund(
    monthly_expenses: float,
    job_stability: str = "moderate",
    dependents: int = 0,
) -> dict:
    """
    Calculate ideal emergency fund size using the 3-6-12 Month Rule.

    Args:
        monthly_expenses: Monthly living expenses in INR
        job_stability: Job stability level - 'high', 'moderate', or 'low'
        dependents: Number of dependents

    Returns:
        Dictionary with emergency fund recommendations
    """
    # Base months based on job stability
    stability_months = {
        "high": 3,
        "moderate": 6,
        "low": 12,
    }

    base_months = stability_months.get(job_stability.lower(), 6)

    # Add 1 month for each dependent
    total_months = base_months + dependents

    # Cap at 12 months
    total_months = min(total_months, 12)

    emergency_fund = monthly_expenses * total_months

    return {
        "monthly_expenses": monthly_expenses,
        "job_stability": job_stability,
        "dependents": dependents,
        "recommended_months": total_months,
        "emergency_fund_amount": emergency_fund,
        "rule": "3-6-12 Month Rule based on job stability and dependents",
    }


@tool
def analyze_spending_ratio(
    monthly_income: float,
    monthly_savings: float,
    monthly_investments: float,
) -> dict:
    """
    Analyze spending vs investment ratio using the 50-30-20 rule.

    Args:
        monthly_income: Monthly income in INR
        monthly_savings: Monthly savings in INR
        monthly_investments: Monthly investments in INR

    Returns:
        Dictionary with spending analysis and recommendations
    """
    total_saved = monthly_savings + monthly_investments
    spending = monthly_income - total_saved

    spending_pct = (spending / monthly_income) * 100
    savings_pct = (monthly_savings / monthly_income) * 100
    investment_pct = (monthly_investments / monthly_income) * 100

    # 50-30-20 rule: 50% needs, 30% wants, 20% savings
    ideal_spending_pct = 80  # Needs + Wants
    ideal_savings_pct = 20  # Savings + Investments

    status = "healthy" if (savings_pct + investment_pct) >= 20 else "needs_improvement"

    return {
        "monthly_income": monthly_income,
        "spending": spending,
        "spending_percentage": round(spending_pct, 2),
        "savings_percentage": round(savings_pct, 2),
        "investment_percentage": round(investment_pct, 2),
        "total_savings_investment_pct": round(savings_pct + investment_pct, 2),
        "ideal_savings_pct": ideal_savings_pct,
        "status": status,
        "rule": "50-30-20 Rule (50% needs, 30% wants, 20% savings)",
    }


@tool
def get_spending_benchmarks(age_group: str, category: str) -> dict:
    """
    Get spending benchmarks for different categories by age group.

    Args:
        age_group: Age group - '20-30', '30-40', '40-50', '50+'
        category: Spending category - 'dining', 'entertainment', 'shopping',
                  'transportation', 'utilities', 'groceries'

    Returns:
        Dictionary with benchmark data for the category
    """
    # Benchmark data (percentage of income)
    benchmarks = {
        "20-30": {
            "dining": 10,
            "entertainment": 8,
            "shopping": 12,
            "transportation": 10,
            "utilities": 8,
            "groceries": 15,
        },
        "30-40": {
            "dining": 8,
            "entertainment": 6,
            "shopping": 10,
            "transportation": 12,
            "utilities": 10,
            "groceries": 18,
        },
        "40-50": {
            "dining": 6,
            "entertainment": 5,
            "shopping": 8,
            "transportation": 12,
            "utilities": 12,
            "groceries": 20,
        },
        "50+": {
            "dining": 5,
            "entertainment": 4,
            "shopping": 6,
            "transportation": 10,
            "utilities": 15,
            "groceries": 22,
        },
    }

    age_benchmarks = benchmarks.get(age_group, benchmarks["30-40"])
    category_benchmark = age_benchmarks.get(category.lower(), None)

    if category_benchmark is None:
        return {
            "error": f"Category '{category}' not found",
            "available_categories": list(age_benchmarks.keys()),
        }

    return {
        "age_group": age_group,
        "category": category,
        "benchmark_percentage": category_benchmark,
        "description": f"Average {category} spending for age group {age_group} is {category_benchmark}% of income",
    }


@tool
def calculate_section_80c_deductions(
    ppf_contribution: float = 0,
    elss_investment: float = 0,
    life_insurance_premium: float = 0,
    home_loan_principal: float = 0,
    children_tuition_fees: float = 0,
    epf_contribution: float = 0,
) -> dict:
    """
    Calculate total Section 80C deductions and remaining limit.

    Args:
        ppf_contribution: Annual PPF contribution
        elss_investment: Annual ELSS mutual fund investment
        life_insurance_premium: Annual life insurance premium
        home_loan_principal: Home loan principal repayment
        children_tuition_fees: Children's tuition fees
        epf_contribution: Employee's EPF contribution

    Returns:
        Dictionary with 80C deduction details
    """
    max_limit = 150000  # Section 80C limit

    total = (
        ppf_contribution
        + elss_investment
        + life_insurance_premium
        + home_loan_principal
        + children_tuition_fees
        + epf_contribution
    )

    eligible_deduction = min(total, max_limit)
    remaining_limit = max(0, max_limit - total)

    return {
        "breakdown": {
            "ppf": ppf_contribution,
            "elss": elss_investment,
            "life_insurance": life_insurance_premium,
            "home_loan_principal": home_loan_principal,
            "tuition_fees": children_tuition_fees,
            "epf": epf_contribution,
        },
        "total_investments": total,
        "section_80c_limit": max_limit,
        "eligible_deduction": eligible_deduction,
        "remaining_limit": remaining_limit,
        "fully_utilized": remaining_limit == 0,
    }


@tool
def calculate_section_80d_deductions(
    self_health_premium: float = 0,
    parents_health_premium: float = 0,
    parents_senior_citizen: bool = False,
    preventive_health_checkup: float = 0,
) -> dict:
    """
    Calculate Section 80D deductions for health insurance premiums.

    Args:
        self_health_premium: Health insurance premium for self and family
        parents_health_premium: Health insurance premium for parents
        parents_senior_citizen: Whether parents are senior citizens (60+)
        preventive_health_checkup: Preventive health checkup expenses

    Returns:
        Dictionary with 80D deduction details
    """
    # Limits
    self_limit = 25000  # 50000 if self is senior citizen
    parents_limit = 25000 if not parents_senior_citizen else 50000
    checkup_limit = 5000  # Part of overall limit

    # Calculate eligible amounts
    self_eligible = min(self_health_premium, self_limit)
    parents_eligible = min(parents_health_premium, parents_limit)
    checkup_eligible = min(preventive_health_checkup, checkup_limit)

    # Checkup is part of overall limit
    self_with_checkup = min(self_eligible + checkup_eligible, self_limit)

    total_eligible = self_with_checkup + parents_eligible
    max_total = self_limit + parents_limit

    return {
        "self_family_premium": self_health_premium,
        "self_family_eligible": self_eligible,
        "parents_premium": parents_health_premium,
        "parents_eligible": parents_eligible,
        "parents_senior_citizen": parents_senior_citizen,
        "checkup_expenses": preventive_health_checkup,
        "checkup_eligible": checkup_eligible,
        "total_eligible_deduction": total_eligible,
        "maximum_possible": max_total,
    }


@tool
def calculate_nps_deduction_80ccd(
    nps_contribution: float,
    gross_salary: float,
    employer_contribution: float = 0,
) -> dict:
    """
    Calculate Section 80CCD(1B) and 80CCD(2) deductions for NPS.

    Args:
        nps_contribution: Annual NPS contribution by employee
        gross_salary: Annual gross salary
        employer_contribution: Employer's NPS contribution

    Returns:
        Dictionary with NPS deduction details
    """
    # 80CCD(1B) - Additional ₹50,000 deduction over 80C
    ccd_1b_limit = 50000
    ccd_1b_eligible = min(nps_contribution, ccd_1b_limit)

    # 80CCD(2) - Employer contribution up to 10% of salary (14% for govt)
    employer_limit = gross_salary * 0.10
    ccd_2_eligible = min(employer_contribution, employer_limit)

    return {
        "employee_contribution": nps_contribution,
        "employer_contribution": employer_contribution,
        "section_80ccd_1b_eligible": ccd_1b_eligible,
        "section_80ccd_1b_limit": ccd_1b_limit,
        "section_80ccd_2_eligible": ccd_2_eligible,
        "employer_contribution_limit_10pct": employer_limit,
        "total_nps_deduction": ccd_1b_eligible + ccd_2_eligible,
        "note": "80CCD(1B) is additional ₹50,000 over Section 80C limit",
    }


@tool
def compare_tax_regimes(
    gross_income: float,
    section_80c: float = 0,
    section_80d: float = 0,
    section_80ccd_1b: float = 0,
    hra_exemption: float = 0,
    lta_exemption: float = 0,
    standard_deduction: float = 50000,
    other_deductions: float = 0,
) -> dict:
    """
    Compare Old vs New Tax Regime for Indian Income Tax.

    Args:
        gross_income: Gross annual income
        section_80c: Section 80C deductions
        section_80d: Section 80D deductions
        section_80ccd_1b: Section 80CCD(1B) NPS deduction
        hra_exemption: HRA exemption amount
        lta_exemption: LTA exemption amount
        standard_deduction: Standard deduction (default ₹50,000)
        other_deductions: Any other deductions

    Returns:
        Dictionary comparing both tax regimes
    """

    # Old regime tax slabs (FY 2024-25)
    def calculate_old_regime_tax(taxable_income: float) -> float:
        if taxable_income <= 250000:
            return 0
        elif taxable_income <= 500000:
            return (taxable_income - 250000) * 0.05
        elif taxable_income <= 1000000:
            return 12500 + (taxable_income - 500000) * 0.20
        else:
            return 112500 + (taxable_income - 1000000) * 0.30

    # New regime tax slabs (FY 2024-25)
    def calculate_new_regime_tax(taxable_income: float) -> float:
        if taxable_income <= 300000:
            return 0
        elif taxable_income <= 700000:
            return (taxable_income - 300000) * 0.05
        elif taxable_income <= 1000000:
            return 20000 + (taxable_income - 700000) * 0.10
        elif taxable_income <= 1200000:
            return 50000 + (taxable_income - 1000000) * 0.15
        elif taxable_income <= 1500000:
            return 80000 + (taxable_income - 1200000) * 0.20
        else:
            return 140000 + (taxable_income - 1500000) * 0.30

    # Old regime calculations
    total_deductions_old = (
        section_80c
        + section_80d
        + section_80ccd_1b
        + hra_exemption
        + lta_exemption
        + standard_deduction
        + other_deductions
    )
    taxable_income_old = max(0, gross_income - total_deductions_old)
    tax_old = calculate_old_regime_tax(taxable_income_old)

    # New regime - only standard deduction of ₹75,000 allowed
    standard_deduction_new = 75000
    taxable_income_new = max(0, gross_income - standard_deduction_new)
    tax_new = calculate_new_regime_tax(taxable_income_new)

    # Add cess (4%)
    tax_old_with_cess = tax_old * 1.04
    tax_new_with_cess = tax_new * 1.04

    savings = tax_old_with_cess - tax_new_with_cess
    recommended = "new_regime" if savings < 0 else "old_regime"

    return {
        "gross_income": gross_income,
        "old_regime": {
            "total_deductions": total_deductions_old,
            "taxable_income": taxable_income_old,
            "tax_before_cess": tax_old,
            "tax_with_cess": round(tax_old_with_cess, 2),
        },
        "new_regime": {
            "standard_deduction": standard_deduction_new,
            "taxable_income": taxable_income_new,
            "tax_before_cess": tax_new,
            "tax_with_cess": round(tax_new_with_cess, 2),
        },
        "savings_with_new_regime": round(-savings, 2),
        "recommended_regime": recommended,
        "recommendation_reason": f"You save ₹{abs(round(savings, 2))} with {recommended.replace('_', ' ')}",
    }


@tool
def calculate_buy_vs_rent(
    property_value: float,
    monthly_rent: float,
    down_payment_pct: float = 20,
    loan_tenure_years: int = 20,
    interest_rate: float = 8.5,
    annual_rent_increase: float = 5,
    annual_property_appreciation: float = 6,
    years_to_compare: int = 10,
) -> dict:
    """
    Calculate Buy vs Rent scenario for real estate decision.

    Args:
        property_value: Property value in INR
        monthly_rent: Current monthly rent
        down_payment_pct: Down payment percentage (default 20%)
        loan_tenure_years: Home loan tenure in years
        interest_rate: Annual interest rate on home loan
        annual_rent_increase: Expected annual rent increase percentage
        annual_property_appreciation: Expected annual property appreciation
        years_to_compare: Number of years for comparison

    Returns:
        Dictionary with buy vs rent analysis
    """
    down_payment = property_value * (down_payment_pct / 100)
    loan_amount = property_value - down_payment

    # EMI calculation
    monthly_rate = interest_rate / 12 / 100
    num_payments = loan_tenure_years * 12

    if monthly_rate > 0:
        emi = (
            loan_amount
            * monthly_rate
            * ((1 + monthly_rate) ** num_payments)
            / (((1 + monthly_rate) ** num_payments) - 1)
        )
    else:
        emi = loan_amount / num_payments

    # Total cost of buying over comparison period
    total_emi_paid = emi * 12 * years_to_compare
    property_value_future = property_value * (
        (1 + annual_property_appreciation / 100) ** years_to_compare
    )

    # Total rent paid over comparison period
    total_rent = 0
    current_rent = monthly_rent
    for year in range(years_to_compare):
        total_rent += current_rent * 12
        current_rent *= 1 + annual_rent_increase / 100

    # Net cost comparison
    buy_cost = down_payment + total_emi_paid - (property_value_future - property_value)
    rent_cost = total_rent

    better_option = "buy" if buy_cost < rent_cost else "rent"

    return {
        "property_value": property_value,
        "down_payment": round(down_payment, 2),
        "loan_amount": round(loan_amount, 2),
        "monthly_emi": round(emi, 2),
        "current_monthly_rent": monthly_rent,
        "comparison_period_years": years_to_compare,
        "buying": {
            "total_emi_paid": round(total_emi_paid, 2),
            "property_value_after_period": round(property_value_future, 2),
            "net_cost": round(buy_cost, 2),
        },
        "renting": {
            "total_rent_paid": round(total_rent, 2),
            "final_monthly_rent": round(current_rent, 2),
            "net_cost": round(rent_cost, 2),
        },
        "better_option": better_option,
        "savings": round(abs(buy_cost - rent_cost), 2),
    }


@tool
def calculate_affordable_emi(
    monthly_income: float,
    existing_emis: float = 0,
    foir_limit: float = 50,
) -> dict:
    """
    Calculate affordable Home Loan EMI using FOIR (Fixed Obligation to Income Ratio).

    Args:
        monthly_income: Monthly income in INR
        existing_emis: Total of existing EMIs (car loan, personal loan, etc.)
        foir_limit: Maximum FOIR percentage (default 50%, range 40-60%)

    Returns:
        Dictionary with affordable EMI details
    """
    max_foir_amount = monthly_income * (foir_limit / 100)
    available_for_home_emi = max_foir_amount - existing_emis

    if available_for_home_emi < 0:
        available_for_home_emi = 0
        status = "over_leveraged"
    elif available_for_home_emi < monthly_income * 0.30:
        status = "tight"
    else:
        status = "comfortable"

    # Estimate loan amount (assuming 8.5% interest, 20 year tenure)
    interest_rate = 8.5
    tenure_years = 20
    monthly_rate = interest_rate / 12 / 100
    num_payments = tenure_years * 12

    if available_for_home_emi > 0:
        loan_amount = (
            available_for_home_emi
            * (((1 + monthly_rate) ** num_payments) - 1)
            / (monthly_rate * ((1 + monthly_rate) ** num_payments))
        )
    else:
        loan_amount = 0

    return {
        "monthly_income": monthly_income,
        "existing_emis": existing_emis,
        "foir_limit_percentage": foir_limit,
        "max_total_emi_allowed": round(max_foir_amount, 2),
        "available_for_home_emi": round(available_for_home_emi, 2),
        "estimated_loan_eligibility": round(loan_amount, 2),
        "status": status,
        "rule": f"FOIR Rule - Total EMIs should not exceed {foir_limit}% of income",
        "recommendation": (
            "Consider reducing existing EMIs before taking home loan"
            if status == "over_leveraged"
            else "You have room for a home loan EMI"
        ),
    }


# =============================================================================
# AGENT DEFINITIONS
# =============================================================================


def get_agents() -> List[Agent]:
    """
    Create and return all Personal Finance Team agents.

    Returns:
        List of configured Agent instances
    """
    llm = get_llm()

    # 1. General Finance Agent
    general_finance_agent = Agent(
        name="General Finance Advisor",
        role="Holistic Financial Advisor",
        instructions="""You are a holistic financial advisor for Indian users. Your role is to:
1. Analyze the user's overall financial stability
2. Suggest appropriate Life and Health Insurance coverage using the 10-20x annual income thumb rule
3. Calculate ideal Emergency Fund size using the 3-6-12 Month Rule
4. Perform spending vs investment ratio analysis using the 50-30-20 rule

Always ask for necessary details like annual income, monthly expenses, job stability, and number of dependents before providing recommendations.

Provide clear, actionable advice tailored to the Indian financial context. Be empathetic and educational in your responses.""",
        model=llm,
        tools=[
            calculate_life_insurance_coverage,
            calculate_emergency_fund,
            analyze_spending_ratio,
            SerperTools(location="in"),
        ],
    )

    # 2. Spending Analysis Agent
    spending_analysis_agent = Agent(
        name="Spending Analyst",
        role="Expense Tracker & Analyst",
        instructions="""You are an expense tracking and analysis specialist for Indian users. Your role is to:
1. Analyze monthly spending data and cross-reference with income
2. Benchmark spending against user demographics (age group)
3. Identify areas of overspending compared to averages
4. Suggest actionable budget corrections

Categories to analyze: dining, entertainment, shopping, transportation, utilities, groceries.

Provide specific, actionable recommendations like "You are spending X% more on dining than the average for your age group. Consider reducing dining out by Y occasions per month."

Be constructive and supportive, not judgmental about spending habits.""",
        model=llm,
        tools=[
            get_spending_benchmarks,
            analyze_spending_ratio,
            SerperTools(location="in"),
        ],
    )

    # 3. Tax Planning Assistant Agent
    tax_planning_agent = Agent(
        name="Tax Planning Assistant",
        role="Indian Tax Compliance Specialist",
        instructions="""You are a tax planning specialist with deep knowledge of Indian Income Tax rules. Your role is to:

1. Analyze income streams and suggest applicable deductions
2. Calculate Section 80C deductions (PPF, ELSS, Insurance, EPF, etc.)
3. Calculate Section 80D deductions (Health Insurance premiums)
4. Calculate Section 80CCD deductions (NPS contributions)
5. Compare Old vs New Tax Regimes to recommend the most beneficial option

Important rules to remember:
- Section 80C limit: ₹1,50,000
- Section 80D: Up to ₹25,000 for self/family, ₹50,000 for senior citizen parents
- Section 80CCD(1B): Additional ₹50,000 for NPS over 80C limit
- New regime: Standard deduction of ₹75,000, no other deductions

Always calculate and show both regime options to help users make informed decisions.
Be accurate with tax calculations and clearly explain the benefits of each option.""",
        model=llm,
        tools=[
            calculate_section_80c_deductions,
            calculate_section_80d_deductions,
            calculate_nps_deduction_80ccd,
            compare_tax_regimes,
            SerperTools(location="in"),
        ],
        knowledge=knowledge_base,
        search_knowledge=True,
        knowledge_filters={"type": "income_tax_documents"},
    )

    # 4. Home Planning Agent
    home_planning_agent = Agent(
        name="Home Planning Advisor",
        role="Real Estate Planner",
        instructions="""You are a real estate planning specialist for Indian users. Your role is to:

1. Analyze Buy vs Rent scenarios based on market rates and user liquidity
2. Calculate affordable Home Loan EMI limits using FOIR (Fixed Obligation to Income Ratio)
3. Ensure users don't become "house poor" by over-committing to EMIs
4. Consider property appreciation, rent inflation, and opportunity cost

Key rules:
- FOIR: Total EMIs should not exceed 40-50% of monthly income
- Down payment: Typically 20% of property value
- Consider maintenance, property tax, and other ownership costs

Provide balanced advice considering both emotional (owning a home) and financial (investment returns) aspects.
Always factor in the user's current savings, existing EMIs, and future financial goals.""",
        model=llm,
        tools=[
            calculate_buy_vs_rent,
            calculate_affordable_emi,
            SerperTools(location="in"),
        ],
    )

    return [
        general_finance_agent,
        spending_analysis_agent,
        tax_planning_agent,
        home_planning_agent,
    ]


def get_teams() -> List[Team]:
    """
    Create and return the Personal Finance Team.

    Returns:
        Configured Team instance
    """
    personal_finance_team = Team(
        name="Personal Finance Team",
        description="A comprehensive personal finance team providing financial foundation, compliance, and lifestyle planning. Use this team for: analyzing financial stability, recommending life insurance coverage, calculating emergency fund size, analyzing spending vs investment ratio, calculating tax deductions, comparing old vs new tax regimes, analyzing buy vs rent scenarios, calculating affordable Home Loan EMI limits, or ensuring users don't become 'house poor' by over-committing to EMIs. The team includes specialized agents for general finance, spending analysis, tax planning, and home planning who work collaboratively to provide holistic financial guidance.",
        instructions="""You are a team of personal finance experts specializing in financial foundation, compliance, and lifestyle planning. Your collective expertise includes:
- Financial stability analysis
- Life insurance coverage recommendations
- Emergency fund size calculations
- Spending vs investment ratio analysis
- Tax deduction calculations
- Buy vs rent scenario analysis
- Affordable Home Loan EMI limits calculations

Work collaboratively to provide comprehensive personal finance guidance. Route queries to the most relevant specialist:
- Financial stability analysis → General Finance Advisor
- Life insurance coverage recommendations → General Finance Advisor
- Emergency fund size calculations → General Finance Advisor
- Spending vs investment ratio analysis → Spending Analyst
- Tax deduction calculations → Tax Planning Assistant
- Buy vs rent scenario analysis → Home Planning Advisor
- Affordable Home Loan EMI limits calculations → Home Planning Advisor

IMPORTANT:
- For general queries where you don't require any specific agent, you can directly reply back to user.
- For specific queries, you can route them to the most relevant specialist agent memeber.
- Use only relevant knowledge base documents to answer the user's query.


Encourage users to consult certified financial advisors for personalized advice.""",
        members=get_agents(),
        model=get_llm("amazon.nova-pro-v1-0"),
        markdown=True,
        knowledge=knowledge_base,
        search_knowledge=True,
        knowledge_filters={"type": "personal_financing_documents"},
    )

    return [personal_finance_team]
