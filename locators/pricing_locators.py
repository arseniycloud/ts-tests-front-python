from dataclasses import dataclass


@dataclass
class PricingLocators:
    """Pricing page locators"""
    # Page structure
    page_title = "h1"
    page_container = ".pricing-page, .price-page"

    # Pricing plans
    pricing_cards = ".pricing-card, .price-card, .plan-card"
    plan_name = "h3, h2, .plan-name, .card-title"
    plan_price = ".price, .cost, .amount, .plan-price"
    plan_description = ".plan-description, .card-description, p"
    plan_features = ".plan-features, .features-list, ul"
    plan_button = ".plan-button, .select-plan, button"

    # Plan types
    basic_plan = ".basic-plan, .plan-basic, [data-plan='basic']"
    premium_plan = ".premium-plan, .plan-premium, [data-plan='premium']"
    enterprise_plan = ".enterprise-plan, .plan-enterprise, [data-plan='enterprise']"

    # Pricing sections
    pricing_header = ".pricing-header, .price-header"
    pricing_subtitle = ".pricing-subtitle, .price-subtitle"
    pricing_note = ".pricing-note, .price-note, .disclaimer"

    # Comparison table
    comparison_table = ".comparison-table, .pricing-table"
    comparison_header = ".comparison-header, .table-header"
    comparison_row = ".comparison-row, .table-row"
    comparison_cell = ".comparison-cell, .table-cell"

    # FAQ section
    pricing_faq = ".pricing-faq, .faq-section"
    faq_question = ".faq-question, .question"
    faq_answer = ".faq-answer, .answer"

    # Contact section
    contact_section = ".contact-section, .get-in-touch"
    contact_button = ".contact-button, .get-quote"

    # Currency selector
    currency_selector = ".currency-selector, select[name*='currency']"
    currency_usd = "option[value='USD']"
    currency_eur = "option[value='EUR']"
    currency_rub = "option[value='RUB']"

    # Billing period
    billing_period = ".billing-period, .period-selector"
    monthly_billing = ".monthly, [data-period='monthly']"
    yearly_billing = ".yearly, [data-period='yearly']"

    # Discount badges
    discount_badge = ".discount-badge, .sale-badge"
    popular_badge = ".popular-badge, .recommended"
    new_badge = ".new-badge, .latest"
