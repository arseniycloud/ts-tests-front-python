from dataclasses import dataclass

# Payment method constants
RUSSIAN_CARDS = "Российские карты"
INTERNATIONAL_CARDS = "Международные карты"


@dataclass
class BalanceLocators:
    """Balance page locators"""
    # Page structure
    page_title = "title"
    page_container = "#__nuxt"
    page_body = ".page-body"

    # Balance form
    balance_form = "[data-test-id='balance-form']"
    balance_form_title = "[data-test-id='balance-form'] .payment-block-title"
    account_balance = "[data-test-id='account-balance']"

    # Payment methods panel
    payment_methods_panel = "[data-test-id='payment-methods-panel']"
    payment_methods_title = "[data-test-id='payment-methods-panel'] .payment-block-title"
    payment_methods_select = "[data-test-id='payment-methods-select']"
    payment_methods_select_button = "[data-test-id='payment-methods-select'] button"
    payment_methods_dropdown = "[data-test-id='payment-methods-select'] ul"

    # Payment methods options
    russian_cards_option = "text='Российские карты'"
    international_cards_option = "text='Международные карты'"

    # Payment method logos
    bank_logo = "img[alt='bank-img']"
    sberpay_logo = "img[alt='bank-img'][src*='sberpay']"
    tpay_logo = "img[alt='bank-img'][src*='t-pay']"
    mirpay_logo = "img[alt='bank-img'][src*='mir-pay']"
    yoomoney_logo = "img[alt='bank-img'][src*='yoomoney']"

    # Payment methods dropdown options
    dropdown_russian_cards = "ul li:has-text('Российские карты')"
    dropdown_international_cards = "ul li:has-text('Международные карты')"

    # Payment amount form
    payment_amount_form = "form.payment-block"
    payment_amount_title = "form.payment-block h2.payment-block-title"
    payment_amount_input = "[data-test-id='payment-amount']"
    payment_pay_button = "[data-test-id='payment-pay-btn']"

    # Info text
    payment_info_text = ".text-secondaryTextClr.text-xs"

    # Header balance display (in navigation)
    header_balance = ".menu-block .ts_hover_bg.item-link:has-text('₽')"
