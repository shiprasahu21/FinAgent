"""
Personal Finance Team - Financial foundation, compliance, and lifestyle planning.

Agents (Consolidated from 4 to 2 for efficiency):
1. General Finance & Lifestyle Advisor - Holistic financial planning, spending analysis, home planning, retirement
2. Tax & Compliance Specialist - Tax optimization and compliance (Indian IT rules)
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

# Import capital gains tax calculation from investment team (single source of truth)
from agents.investment_team import calculate_capital_gains_tax


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
def calculate_hra_exemption(
    basic_salary: float,
    hra_received: float,
    rent_paid: float,
    is_metro: bool = True,
) -> dict:
    """
    Calculate HRA (House Rent Allowance) tax exemption for salaried employees.

    Args:
        basic_salary: Annual basic salary (excluding allowances)
        hra_received: Annual HRA received
        rent_paid: Annual rent paid
        is_metro: Whether the employee lives in a metro city (Delhi, Mumbai, Kolkata, Chennai)

    Returns:
        Dictionary with HRA exemption details

    Formula: Exemption is the minimum of:
    - Actual HRA received
    - Rent paid minus 10% of basic salary
    - 50% of basic salary (metro) or 40% (non-metro)
    """
    # Calculate the three components
    actual_hra = hra_received
    rent_minus_10pct_basic = rent_paid - (basic_salary * 0.10)
    metro_percentage = 0.50 if is_metro else 0.40
    basic_percentage = basic_salary * metro_percentage

    # HRA exemption is the minimum of the three
    hra_exemption = max(0, min(actual_hra, rent_minus_10pct_basic, basic_percentage))

    # Taxable HRA
    taxable_hra = hra_received - hra_exemption

    return {
        "basic_salary": basic_salary,
        "hra_received": hra_received,
        "rent_paid": rent_paid,
        "is_metro": is_metro,
        "calculation_components": {
            "actual_hra_received": actual_hra,
            "rent_minus_10pct_basic": max(0, rent_minus_10pct_basic),
            "basic_salary_percentage": basic_percentage,
            "percentage_used": f"{int(metro_percentage * 100)}%",
        },
        "hra_exemption": round(hra_exemption, 2),
        "taxable_hra": round(taxable_hra, 2),
        "formula": "Minimum of: (1) Actual HRA, (2) Rent - 10% of Basic, (3) 50%/40% of Basic",
        "note": "You must be living in a rented accommodation and not own a house in the same city",
    }


@tool
def calculate_section_24_interest(
    home_loan_interest_paid: float,
    property_type: str = "self_occupied",
) -> dict:
    """
    Calculate Section 24 deduction for home loan interest.

    Args:
        home_loan_interest_paid: Annual interest paid on home loan
        property_type: Type of property - 'self_occupied' or 'let_out'

    Returns:
        Dictionary with Section 24 deduction details

    Rules:
    - Self-occupied property: Max ₹2,00,000 deduction
    - Let-out property: No upper limit (entire interest is deductible)
    - Under-construction property: Interest during construction can be claimed
      in 5 equal installments after completion
    """
    if property_type.lower() == "self_occupied":
        max_limit = 200000
        eligible_deduction = min(home_loan_interest_paid, max_limit)
        remaining_amount = max(0, home_loan_interest_paid - max_limit)
    elif property_type.lower() == "let_out":
        max_limit = None  # No limit for let-out property
        eligible_deduction = home_loan_interest_paid
        remaining_amount = 0
    else:
        # Default to self-occupied
        max_limit = 200000
        eligible_deduction = min(home_loan_interest_paid, max_limit)
        remaining_amount = max(0, home_loan_interest_paid - max_limit)

    return {
        "home_loan_interest_paid": home_loan_interest_paid,
        "property_type": property_type,
        "eligible_deduction_section_24": round(eligible_deduction, 2),
        "deduction_limit": max_limit if max_limit else "No limit (let-out property)",
        "non_deductible_amount": round(remaining_amount, 2) if max_limit else 0,
        "note": (
            "Self-occupied: Max ₹2,00,000 | Let-out: No limit"
            if property_type.lower() == "self_occupied"
            else "Let-out property has no deduction limit"
        ),
        "additional_info": "This is separate from Section 80C principal repayment deduction",
    }


@tool
def calculate_lta_exemption(
    lta_received: float,
    travel_expenses: float,
    travel_type: str = "domestic",
) -> dict:
    """
    Calculate LTA (Leave Travel Allowance) tax exemption.

    Args:
        lta_received: LTA amount received from employer
        travel_expenses: Actual travel expenses incurred
        travel_type: Type of travel - 'domestic' or 'international'

    Returns:
        Dictionary with LTA exemption details

    Rules:
    - Only domestic travel within India is eligible
    - Only travel fare (flight, train, bus) is exempt, not hotel/food
    - Exemption is minimum of LTA received and actual travel fare
    - Can be claimed twice in a block of 4 years
    """
    if travel_type.lower() == "international":
        lta_exemption = 0
        note = "LTA exemption is not available for international travel"
    else:
        lta_exemption = min(lta_received, travel_expenses)
        note = "LTA exemption covers travel fare only (not hotel/food). Valid for domestic travel within India."

    taxable_lta = lta_received - lta_exemption

    return {
        "lta_received": lta_received,
        "travel_expenses": travel_expenses,
        "travel_type": travel_type,
        "lta_exemption": round(lta_exemption, 2),
        "taxable_lta": round(taxable_lta, 2),
        "note": note,
        "additional_rules": [
            "Can be claimed twice in a block of 4 calendar years",
            "Current block: 2022-2025",
            "Only travel fare is exempt (flight, train, bus tickets)",
            "Hotel, food, and other expenses are not covered",
            "Must submit travel bills to employer",
        ],
    }


@tool
def calculate_epf_vpf_returns(
    monthly_basic: float,
    employee_contribution_pct: float = 12.0,
    employer_contribution_pct: float = 12.0,
    vpf_contribution_pct: float = 0.0,
    current_epf_balance: float = 0,
    years_to_retirement: int = 30,
    interest_rate: float = 8.15,
) -> dict:
    """
    Calculate EPF/VPF returns and maturity amount.

    Args:
        monthly_basic: Monthly basic salary
        employee_contribution_pct: Employee EPF contribution % (default 12%)
        employer_contribution_pct: Employer EPF contribution % (default 12%)
        vpf_contribution_pct: Voluntary PF contribution % (default 0%)
        current_epf_balance: Current EPF balance if any
        years_to_retirement: Years remaining till retirement
        interest_rate: EPF interest rate (default 8.15%)

    Returns:
        Dictionary with EPF/VPF calculation details

    Rules:
    - EPF contribution capped at ₹15,000/month basic salary
    - Employee: 12% of basic (max ₹1,800/month)
    - Employer: 3.67% to EPF, 8.33% to EPS (max ₹1,250/month)
    - VPF: Additional voluntary contribution (no upper limit)
    - Tax exempt (EEE): Contribution, interest, and withdrawal all tax-free
    """
    # EPF wage ceiling
    wage_ceiling = 15000
    applicable_basic = min(monthly_basic, wage_ceiling)

    # Calculate monthly contributions
    employee_epf = applicable_basic * (employee_contribution_pct / 100)
    employer_eps = min(applicable_basic * 0.0833, 1250)  # EPS capped at ₹1,250
    employer_epf = (applicable_basic * (employer_contribution_pct / 100)) - employer_eps
    vpf = monthly_basic * (vpf_contribution_pct / 100)  # VPF has no wage ceiling

    total_monthly_contribution = employee_epf + employer_epf + vpf

    # Calculate maturity amount using compound interest
    months = years_to_retirement * 12
    monthly_rate = interest_rate / 12 / 100

    if monthly_rate > 0:
        # FV = P × (1 + r)^n + PMT × [((1 + r)^n - 1) / r] × (1 + r)
        future_value_current = current_epf_balance * ((1 + monthly_rate) ** months)
        future_value_contributions = (
            total_monthly_contribution
            * (((1 + monthly_rate) ** months - 1) / monthly_rate)
            * (1 + monthly_rate)
        )
        maturity_amount = future_value_current + future_value_contributions
    else:
        maturity_amount = (
            current_epf_balance + total_monthly_contribution * months
        )

    # Total contributions
    total_contributions = (total_monthly_contribution * months) + current_epf_balance
    interest_earned = maturity_amount - total_contributions

    return {
        "monthly_basic": monthly_basic,
        "applicable_basic_for_epf": applicable_basic,
        "monthly_contributions": {
            "employee_epf": round(employee_epf, 2),
            "employer_epf": round(employer_epf, 2),
            "employer_eps": round(employer_eps, 2),
            "vpf": round(vpf, 2),
            "total_monthly": round(total_monthly_contribution, 2),
        },
        "annual_contribution": round(total_monthly_contribution * 12, 2),
        "current_balance": current_epf_balance,
        "years_to_retirement": years_to_retirement,
        "interest_rate": f"{interest_rate}%",
        "maturity_amount": round(maturity_amount, 2),
        "total_contributions": round(total_contributions, 2),
        "interest_earned": round(interest_earned, 2),
        "tax_status": "EEE (Tax Exempt - Contribution, Interest, Withdrawal)",
        "note": f"EPF contributions capped at ₹{wage_ceiling}/month basic salary. VPF has no wage ceiling.",
    }


@tool
def calculate_retirement_corpus(
    current_age: int,
    retirement_age: int,
    current_monthly_expenses: float,
    inflation_rate: float = 6.0,
    post_retirement_return: float = 7.0,
    life_expectancy: int = 85,
) -> dict:
    """
    Calculate required retirement corpus based on current expenses and inflation.

    Args:
        current_age: Current age in years
        retirement_age: Expected retirement age
        current_monthly_expenses: Current monthly expenses
        inflation_rate: Expected annual inflation rate (default 6%)
        post_retirement_return: Expected post-retirement return rate (default 7%)
        life_expectancy: Expected life expectancy (default 85 years)

    Returns:
        Dictionary with retirement corpus calculation details

    Formula:
    1. Calculate future monthly expenses at retirement (adjusted for inflation)
    2. Calculate years of retirement (life expectancy - retirement age)
    3. Calculate corpus needed to sustain those expenses
    """
    years_to_retirement = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age

    if years_to_retirement <= 0:
        return {
            "error": "You are already at or past retirement age",
            "current_age": current_age,
            "retirement_age": retirement_age,
        }

    if years_in_retirement <= 0:
        return {
            "error": "Life expectancy should be greater than retirement age",
            "retirement_age": retirement_age,
            "life_expectancy": life_expectancy,
        }

    # Calculate future monthly expenses at retirement (adjusted for inflation)
    inflation_multiplier = (1 + inflation_rate / 100) ** years_to_retirement
    future_monthly_expenses = current_monthly_expenses * inflation_multiplier
    future_annual_expenses = future_monthly_expenses * 12

    # Calculate corpus needed
    # Using present value of annuity formula for post-retirement period
    r = post_retirement_return / 100
    n = years_in_retirement

    if r > 0:
        # PV = Annual Expense × [(1 - (1 + r)^-n) / r]
        corpus_needed = future_annual_expenses * ((1 - (1 + r) ** -n) / r)
    else:
        corpus_needed = future_annual_expenses * n

    # Calculate monthly SIP needed to achieve corpus (assuming 12% pre-retirement return)
    pre_retirement_return = 0.12
    monthly_rate = pre_retirement_return / 12
    months_to_retirement = years_to_retirement * 12

    if monthly_rate > 0 and months_to_retirement > 0:
        # FV = SIP × [((1 + r)^n - 1) / r] × (1 + r)
        # Rearranged: SIP = FV / ([((1 + r)^n - 1) / r] × (1 + r))
        monthly_sip_needed = corpus_needed / (
            (((1 + monthly_rate) ** months_to_retirement - 1) / monthly_rate)
            * (1 + monthly_rate)
        )
    else:
        monthly_sip_needed = corpus_needed / months_to_retirement

    return {
        "current_age": current_age,
        "retirement_age": retirement_age,
        "years_to_retirement": years_to_retirement,
        "life_expectancy": life_expectancy,
        "years_in_retirement": years_in_retirement,
        "current_monthly_expenses": current_monthly_expenses,
        "future_monthly_expenses_at_retirement": round(future_monthly_expenses, 2),
        "inflation_rate": f"{inflation_rate}%",
        "post_retirement_return": f"{post_retirement_return}%",
        "corpus_needed_at_retirement": round(corpus_needed, 2),
        "monthly_sip_needed": round(monthly_sip_needed, 2),
        "assumptions": {
            "pre_retirement_return": "12% (equity-heavy portfolio)",
            "post_retirement_return": f"{post_retirement_return}% (debt-heavy portfolio)",
            "inflation_rate": f"{inflation_rate}%",
        },
        "note": "This is a simplified calculation. Consider consulting a financial advisor for personalized retirement planning.",
    }


@tool
def compare_tax_regimes(
    gross_income: float,
    section_80c: float = 0,
    section_80d: float = 0,
    section_80ccd_1b: float = 0,
    section_24_interest: float = 0,
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
        section_24_interest: Section 24 home loan interest deduction (max ₹2,00,000)
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
    # Cap Section 24 interest at ₹2,00,000 for self-occupied property
    section_24_eligible = min(section_24_interest, 200000)

    total_deductions_old = (
        section_80c
        + section_80d
        + section_80ccd_1b
        + section_24_eligible
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
            "deductions_breakdown": {
                "section_80c": section_80c,
                "section_80d": section_80d,
                "section_80ccd_1b": section_80ccd_1b,
                "section_24_interest": section_24_eligible,
                "hra_exemption": hra_exemption,
                "lta_exemption": lta_exemption,
                "standard_deduction": standard_deduction,
                "other_deductions": other_deductions,
            },
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
        foir_limit: Maximum FOIR percentage (default 50%, range 50-65% for salaried, 40-50% for self-employed)

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
    Consolidated from 4 agents to 2 for improved efficiency.

    Returns:
        List of configured Agent instances
    """
    llm = get_llm(model="gpt-5-nano", provider="openai")

    # 1. General Finance & Lifestyle Advisor (Consolidated: General Finance + Spending + Home Planning)
    general_finance_lifestyle_agent = Agent(
        name="General Finance & Lifestyle Advisor",
        role="Holistic Financial Planning & Lifestyle Specialist",
        description="A comprehensive financial planning specialist covering overall financial stability, insurance, emergency funds, spending analysis, budgeting, home planning, retirement planning, and EPF/VPF calculations. Use this agent for: analyzing financial stability, recommending life insurance coverage (10-20x income rule), calculating emergency fund size (3-6-12 month rule), analyzing spending vs investment ratio (50-30-20 rule), benchmarking spending against demographics, buy vs rent analysis, calculating affordable home loan EMI (FOIR rule), planning retirement corpus, or calculating EPF/VPF returns. Ideal for queries like 'How much emergency fund do I need?', 'Am I spending too much?', 'Should I buy or rent?', 'Can I afford this home loan?', 'How much insurance do I need?', 'Plan my retirement', or 'Calculate EPF maturity'.",
        instructions="""You are a comprehensive financial planning and lifestyle specialist for Indian users. Your role encompasses:

FINANCIAL STABILITY & PROTECTION:
1. Analyze overall financial health and stability
2. Recommend appropriate Life and Health Insurance coverage using the 10-20x annual income thumb rule
3. Calculate ideal Emergency Fund size using the 3-6-12 Month Rule based on job stability and dependents
4. Ensure users have a strong financial foundation before aggressive investing

SPENDING ANALYSIS & BUDGETING:
1. Analyze monthly spending data and cross-reference with income
2. Perform spending vs investment ratio analysis using the 50-30-20 rule (50% needs, 30% wants, 20% savings)
3. Benchmark spending against user demographics (age group) for categories: dining, entertainment, shopping, transportation, utilities, groceries
4. Identify areas of overspending compared to peer averages
5. Suggest actionable budget corrections and savings strategies
6. Provide specific recommendations like "You are spending X% more on dining than the average for your age group"

HOME PLANNING & REAL ESTATE:
1. Analyze Buy vs Rent scenarios based on market rates, user liquidity, and opportunity cost
2. Calculate affordable Home Loan EMI limits using FOIR (Fixed Obligation to Income Ratio)
3. Ensure users don't become "house poor" by over-committing to EMIs
4. Consider property appreciation (typically 5-8%), rent inflation, maintenance costs, and registration fees
5. Factor in Section 24 home loan interest deduction (up to ₹2,00,000 for self-occupied property)

Key FOIR Rules:
- Total EMIs should not exceed 50-65% of monthly income for salaried employees
- Total EMIs should not exceed 40-50% for self-employed
- Down payment: Typically 20-30% of property value
- Consider maintenance (1-2% of property value annually), property tax, and other ownership costs

RETIREMENT & EPF/VPF PLANNING:
1. Plan retirement corpus based on current expenses and inflation
2. Calculate EPF/VPF returns and maturity amounts for salaried employees
3. Project retirement needs considering life expectancy and post-retirement expenses
4. Suggest monthly SIP needed to achieve retirement goals
5. Explain EPF wage ceiling (₹15,000/month), EPS contributions, and VPF benefits

EPF/VPF Rules:
- EPF contributions capped at ₹15,000/month basic salary (₹1,800/month max employee contribution)
- VPF has no wage ceiling - can contribute any amount voluntarily
- Tax status: EEE (Exempt-Exempt-Exempt) - Contribution, interest, and withdrawal all tax-free
- Current EPF interest rate: ~8.15% per annum
- Employer contribution split: 3.67% to EPF, 8.33% to EPS (max ₹1,250/month)

APPROACH:
1. Always ask for necessary details: annual income, monthly expenses, job stability, dependents, age, existing EMIs
2. Provide clear, actionable advice tailored to the Indian financial context
3. Use specific numbers and percentages in recommendations
4. Be empathetic and educational, not judgmental about spending habits
5. Consider both emotional (home ownership, family security) and financial (returns, opportunity cost) aspects
6. Encourage building emergency fund and adequate insurance before aggressive investing

FINANCIAL RULES TO REMEMBER:
- 10-20x Income Rule: Life insurance coverage should be 10-20 times annual income
- 3-6-12 Month Rule: Emergency fund = 3 months (high job stability), 6 months (moderate), 12 months (low stability or self-employed)
- 50-30-20 Rule: 50% needs, 30% wants, 20% savings/investments
- FOIR Rule: Total EMIs ≤ 40-50% of monthly income
- 100-Age Rule (or 110/120 for aggressive): Basic asset allocation guideline

Always provide balanced advice considering user's life stage, risk tolerance, and financial goals.""",
        model=llm,
        tools=[
            # Insurance & Emergency Fund
            calculate_life_insurance_coverage,
            calculate_emergency_fund,
            # Spending Analysis
            analyze_spending_ratio,
            get_spending_benchmarks,
            # Home Planning
            calculate_buy_vs_rent,
            calculate_affordable_emi,
            calculate_section_24_interest,
            # Retirement & EPF/VPF
            calculate_epf_vpf_returns,
            calculate_retirement_corpus,
            # Web search for latest info
            SerperTools(location="in"),
        ],
    )

    # 2. Tax & Compliance Specialist (Enhanced Tax Planning Assistant)
    tax_compliance_specialist = Agent(
        name="Tax & Compliance Specialist",
        role="Indian Tax Optimization & Compliance Expert",
        description="A tax planning and compliance specialist with deep knowledge of Indian Income Tax rules. Use this agent for: calculating HRA exemption, Section 80C deductions (PPF/ELSS/Insurance/EPF), Section 80D deductions (health insurance premiums), Section 80CCD deductions (NPS contributions), Section 24 deductions (home loan interest), LTA exemption, capital gains tax on investments, comparing old vs new tax regimes, or optimizing salary structure. Ideal for queries like 'How much tax can I save?', 'Old vs new tax regime?', 'Calculate my HRA exemption', 'What are my Section 80C options?', 'Capital gains tax on stocks', 'How to optimize my salary?', or 'Tax-saving investment recommendations'.",
        instructions="""You are a tax planning and compliance specialist with deep knowledge of Indian Income Tax rules. Your role is to:

TAX DEDUCTIONS & EXEMPTIONS:
1. Calculate HRA (House Rent Allowance) exemption for salaried employees
   - Formula: Minimum of (Actual HRA, Rent - 10% of Basic, 50%/40% of Basic for metro/non-metro)
2. Calculate Section 80C deductions (₹1,50,000 limit)
   - PPF, ELSS, Life Insurance premiums, EPF, Home loan principal, Children's tuition fees
3. Calculate Section 80D deductions (Health Insurance premiums)
   - Self/family: ₹25,000 (₹50,000 if senior citizen)
   - Parents: ₹25,000 (₹50,000 if senior citizens)
   - Preventive health checkup: ₹5,000 (included in overall limit)
4. Calculate Section 80CCD deductions (NPS contributions)
   - 80CCD(1B): Additional ₹50,000 over 80C limit
   - 80CCD(2): Employer contribution up to 10% of salary
5. Calculate Section 24 deductions (Home loan interest)
   - Self-occupied: Up to ₹2,00,000
   - Let-out property: No limit
6. Calculate LTA (Leave Travel Allowance) exemption
   - Only domestic travel within India
   - Only travel fare (flight, train, bus), not hotel/food
   - Can be claimed twice in a block of 4 years (current block: 2022-2025)

CAPITAL GAINS TAX (Use imported calculate_capital_gains_tax tool):
Equity & Equity Mutual Funds:
- LTCG (>365 days): 12.5% on gains above ₹1.25 lakh annual exemption
- STCG (≤365 days): 20% on all gains
- STT (Securities Transaction Tax) already included in broker charges

Debt Mutual Funds & Bonds:
- LTCG (>36 months): 12.5% without indexation (post-April 2023)
- STCG (≤36 months): Added to income, taxed at slab rate (10-30% + 4% cess)

TAX REGIME COMPARISON:
Old Regime (FY 2024-25):
- Standard deduction: ₹50,000
- Allows all deductions: 80C, 80D, 80CCD(1B), HRA, LTA, Section 24
- Tax slabs: 0% up to ₹2.5L, 5% (₹2.5L-₹5L), 20% (₹5L-₹10L), 30% (above ₹10L)

New Regime (FY 2024-25):
- Standard deduction: ₹75,000 (only deduction allowed)
- No other deductions (80C, 80D, HRA, LTA not allowed)
- Tax slabs: 0% up to ₹3L, 5% (₹3L-₹7L), 10% (₹7L-₹10L), 15% (₹10L-₹12L), 20% (₹12L-₹15L), 30% (above ₹15L)

APPROACH:
1. Ask for all relevant details: gross income, basic salary, HRA received, rent paid, investments, home loan interest
2. Calculate both old and new regime tax liabilities
3. Recommend the regime with lower tax burden
4. Suggest tax-saving strategies within legal limits
5. Explain tax implications clearly with specific numbers
6. Provide actionable recommendations on maximizing deductions

TAX-SAVING INVESTMENT RECOMMENDATIONS:
For Section 80C (₹1.5L limit):
- ELSS (Equity Linked Savings Scheme): 3-year lock-in, equity exposure, potential for 12-15% returns
- PPF (Public Provident Fund): 15-year lock-in, safe, 7-8% returns, EEE status
- Life Insurance: Term insurance premiums (best for pure protection)
- EPF: Automatic deduction from salary

For Section 80CCD(1B) (additional ₹50K over 80C):
- NPS (National Pension System): Retirement-focused, equity+debt mix, partial withdrawal allowed

For Section 80D:
- Health insurance: Essential for medical emergencies
- Parents' health insurance: Separate limit, especially beneficial if parents are senior citizens

IMPORTANT PRINCIPLES:
- Always calculate and show both regime options
- Consider user's investment preferences and liquidity needs
- Don't recommend investments solely for tax saving
- Prioritize insurance (term + health) before tax-saving instruments
- Explain that ELSS has 3-year lock-in vs PPF 15-year lock-in
- Mention EEE status of EPF/PPF/NPS (tax-free on maturity)
- Be accurate with tax calculations and rules
- Stay updated with latest tax amendments
- Encourage users to consult certified tax advisors for complex scenarios

Always provide specific numbers, clear explanations, and actionable next steps.""",
        model=llm,
        tools=[
            # Salary Components & Exemptions
            calculate_hra_exemption,
            calculate_lta_exemption,
            # Section 80 Deductions
            calculate_section_80c_deductions,
            calculate_section_80d_deductions,
            calculate_nps_deduction_80ccd,
            # Home Loan Benefits
            calculate_section_24_interest,
            # Capital Gains Tax (imported from investment_team)
            calculate_capital_gains_tax,
            # Tax Regime Comparison
            compare_tax_regimes,
            # Web search for latest tax updates
            SerperTools(location="in"),
        ],
        knowledge=knowledge_base,
        search_knowledge=True,
        knowledge_filters={"type": "income_tax_documents"},
    )

    return [
        general_finance_lifestyle_agent,
        tax_compliance_specialist,
    ]


def get_teams() -> List[Team]:
    """
    Create and return the Personal Finance Team.
    Consolidated from 4 agents to 2 for improved efficiency.

    Returns:
        Configured Team instance
    """
    personal_finance_team = Team(
        name="Personal Finance Team",
        description="""A comprehensive personal finance team providing financial foundation, tax optimization, and lifestyle planning for Indian users.

This team has been optimized from 4 agents to 2 specialized agents for improved efficiency:
1. General Finance & Lifestyle Advisor - Financial stability, insurance, emergency funds, spending analysis, home planning, retirement
2. Tax & Compliance Specialist - Tax optimization, deductions, regime comparison, capital gains

Use this team for: analyzing financial stability, recommending life insurance coverage (10-20x income rule), calculating emergency fund size (3-6-12 month rule), analyzing spending patterns and budgeting (50-30-20 rule), benchmarking spending against demographics, buy vs rent analysis, calculating affordable home loan EMI (FOIR rule), planning retirement corpus, calculating EPF/VPF returns, calculating HRA exemption, Section 80C/80D/80CCD deductions, comparing old vs new tax regimes, capital gains tax calculations, or optimizing salary structure. The team provides comprehensive personal finance guidance covering both financial planning and tax compliance.""",
        instructions="""You are a team of personal finance experts specializing in financial foundation, tax optimization, and lifestyle planning for Indian users.

Your team has been optimized to 2 specialized agents:

1. GENERAL FINANCE & LIFESTYLE ADVISOR
   - Comprehensive financial planning covering ALL lifestyle and foundation aspects
   - Financial stability analysis and health checks
   - Life and health insurance recommendations (10-20x income rule)
   - Emergency fund calculations (3-6-12 month rule)
   - Spending analysis and budgeting (50-30-20 rule)
   - Demographic spending benchmarks (dining, entertainment, shopping, transportation, utilities, groceries)
   - Buy vs Rent analysis with property appreciation and opportunity cost
   - Home loan affordability (FOIR rule: 40-65% income limit)
   - Retirement corpus planning
   - EPF/VPF calculations and maturity projections

2. TAX & COMPLIANCE SPECIALIST
   - ALL tax-related queries and compliance
   - HRA exemption calculations
   - Section 80C deductions (PPF, ELSS, Insurance, EPF, home loan principal)
   - Section 80D deductions (health insurance premiums)
   - Section 80CCD deductions (NPS contributions)
   - Section 24 deductions (home loan interest)
   - LTA exemption calculations
   - Capital gains tax (equity & debt)
   - Old vs New tax regime comparison
   - Salary structure optimization

ROUTING GUIDELINES:
- Insurance/emergency fund/spending/budgeting/home planning/retirement queries → General Finance & Lifestyle Advisor
- Tax deductions/exemptions/regime comparison/capital gains/salary optimization → Tax & Compliance Specialist
- General financial advice queries → You can answer directly or route to appropriate specialist
- Queries spanning both domains → Route to primary specialist, they have overlapping tools where needed

CONSOLIDATED BENEFITS:
- Reduced redundancy - no overlap in agent responsibilities
- Clearer routing - two distinct domains (lifestyle planning vs tax compliance)
- More efficient - agents have exactly the tools they need
- Comprehensive coverage - nothing lost from previous 4-agent structure

IMPORTANT:
- For simple queries that don't need specialized analysis, you can answer directly
- For specific calculations or analysis, route to the appropriate specialist
- Both agents have web search capability for latest information
- Tax specialist has access to knowledge base for tax documents
- Always provide data-driven insights with proper context
- Include risk disclosures and encourage consulting certified financial advisors

APPROACH:
1. Analyze the query to determine primary focus (lifestyle planning vs tax compliance)
2. Route to the appropriate specialist if analysis/calculation is needed
3. For queries spanning both domains, route to primary specialist first
4. Provide integrated advice considering user's complete financial picture
5. Always ask for missing information rather than making assumptions

Encourage users to consult certified financial advisors for personalized advice.""",
        members=get_agents(),
        model=get_llm(model="gpt-5-nano", provider="openai"),
        markdown=True,
        knowledge=knowledge_base,
        search_knowledge=True,
        knowledge_filters={"type": "personal_financing_documents"},
    )

    return [personal_finance_team]
