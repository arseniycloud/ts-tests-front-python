import json
import logging
import re

import allure
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.balance_locators import (
    INTERNATIONAL_CARDS,
    RUSSIAN_CARDS,
    BalanceLocators,
)
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot


class BalancePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.locators = BalanceLocators()

    def _is_external_domain(self, url: str) -> bool:
        """Check if URL is on external payment domain."""
        return any(domain in url for domain in ("yoomoney.ru", "gateline"))

    @allure.step("Navigate to balance page")
    def navigate_to_balance(self):
        balance_url = f"{BASE_URL}/app/payment/"
        current_url = self.page.url

        # If on external payment service, return to app first
        if BASE_URL not in current_url or self._is_external_domain(current_url):
            self.page.goto(f"{BASE_URL}/app", wait_until="domcontentloaded", timeout=100000)
            self.page.wait_for_load_state("networkidle", timeout=50000)
            self.page.wait_for_timeout(2000)

        # Navigate to balance page
        response = self.page.goto(balance_url, wait_until="domcontentloaded", timeout=90000)

        # Verify response status
        if response is None:
            raise ValueError("Navigation response is None - page navigation may have failed")

        if response.status != 200:
            raise ValueError(f"Expected HTTP status 200, got {response.status}")

        self.wait_for_page_load()


    @allure.step("Check balance page elements")
    def check_balance_elements(self):
        expect(self.page.locator(self.locators.page_container)).to_be_visible()
        expect(self.page.locator(self.locators.page_body)).to_be_visible()

        balance_form = self.page.locator(self.locators.balance_form)
        expect(balance_form).to_be_visible()

        balance_title = balance_form.locator("h1.payment-block-title")
        expect(balance_title).to_be_visible()
        expect(balance_title).to_contain_text("Баланс:")

        account_balance = self.page.locator(self.locators.account_balance)
        expect(account_balance).to_be_visible()

        attach_screenshot(self.page, "Balance elements verified")

    @allure.step("Check payment methods panel")
    def check_payment_methods_panel(self):
        payment_panel = self.page.locator(self.locators.payment_methods_panel)
        expect(payment_panel).to_be_visible()

        payment_title = payment_panel.locator("h2.payment-block-title")
        expect(payment_title).to_be_visible()
        expect(payment_title).to_contain_text("Способы оплаты:")

        payment_select = self.page.locator(self.locators.payment_methods_select)
        expect(payment_select).to_be_visible()

        expect(self.page.locator(self.locators.sberpay_logo).first).to_be_visible()
        expect(self.page.locator(self.locators.tpay_logo).first).to_be_visible()
        expect(self.page.locator(self.locators.mirpay_logo).first).to_be_visible()
        expect(self.page.locator(self.locators.yoomoney_logo).first).to_be_visible()

        attach_screenshot(self.page, "Payment methods panel verified")

    @allure.step("Check payment amount form")
    def check_payment_amount_form(self):
        payment_form = self.page.locator("form.payment-block")
        expect(payment_form).to_be_visible()

        amount_title = payment_form.locator("h2.payment-block-title")
        expect(amount_title).to_be_visible()
        expect(amount_title).to_contain_text("Сумма:")

        amount_input = self.page.locator(self.locators.payment_amount_input)
        expect(amount_input).to_be_visible()

        pay_button = self.page.locator(self.locators.payment_pay_button)
        expect(pay_button).to_be_visible()
        expect(pay_button).to_contain_text("Пополнить")

        attach_screenshot(self.page, "Payment amount form verified")

    @allure.step("Get account balance text")
    def get_account_balance(self) -> str:
        balance_element = self.page.locator(self.locators.account_balance)
        expect(balance_element).to_be_visible()
        balance = balance_element.text_content().strip()
        attach_screenshot(self.page, "Account balance retrieved")
        return balance

    def _ensure_header_balance_accessible(self) -> None:
        """Ensure header balance element is accessible in tablet/mobile views."""
        header_balance = self.page.locator(self.locators.header_balance)

        if header_balance.is_visible():
            return

        mobile_menu_btn = self.page.locator(".mobile-menu-btn, .t-vertical-menu-ss").first
        if mobile_menu_btn.count() > 0:
            try:

                if mobile_menu_btn.is_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE):
                    mobile_menu_btn.click()
                    menu_block = self.page.locator(".menu-block")
                    expect(menu_block).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)

            except Exception as e:
                logging.debug(f"Failed to open mobile menu to access header balance (continuing): {e}")

    @allure.step("Get header balance text")
    def get_header_balance(self) -> str:
        self._ensure_header_balance_accessible()
        header_balance = self.page.locator(self.locators.header_balance)
        try:
            expect(header_balance).to_be_visible(timeout=Timeouts.Balance.ELEMENT_VISIBLE)

        except Exception as visibility_error:
            logging.debug(f"Header balance not visible, trying to get text content: {visibility_error}")

            try:
                text_content = header_balance.text_content()
                if text_content:
                    logging.warning("Header balance text retrieved from non-visible element - may be stale")
                    return text_content.strip()

            except Exception as text_error:
                logging.debug(f"Failed to get text content from header balance: {text_error}")

            raise visibility_error

        text_content = header_balance.text_content()
        balance = text_content.strip() if text_content else ""

        attach_screenshot(self.page, "Header balance retrieved")
        return balance

    @allure.step("Check balance amount equals {expected_amount}")
    def check_balance_amount(self, expected_amount: int = 50000):
        balance_text = self.get_account_balance()
        balance_clean = balance_text.replace('\u00A0', ' ').replace(' ', '').replace('руб.', '').replace('₽', '')
        numbers = re.findall(r'\d+', balance_clean)

        if numbers:
            balance_value = int(''.join(numbers))
            assert balance_value == expected_amount, \
                f"Expected balance {expected_amount}, but got {balance_value} from text '{balance_text}'"

        else:
            assert False, f"Could not extract balance number from text: '{balance_text}'"

        attach_screenshot(self.page, "Balance amount verified")

    @allure.step("Check header balance amount equals {expected_amount}")
    def check_header_balance_amount(self, expected_amount: int = 50000):
        header_balance_text = self.get_header_balance()
        numbers = re.findall(r'\d+', header_balance_text)

        if numbers:
            balance_value = int(''.join(numbers))
            assert balance_value == expected_amount, \
                f"Expected header balance {expected_amount}, but got {balance_value} from text '{header_balance_text}'"

        else:
            assert False, f"Could not extract balance number from header text: '{header_balance_text}'"

        attach_screenshot(self.page, "Header balance amount verified")

    @allure.step("Get balance amount as integer")
    def get_balance_amount(self) -> int:
        balance_text = self.get_account_balance()
        balance_clean = balance_text.replace('\u00A0', ' ').replace(' ', '').replace('руб.', '').replace('₽', '')
        numbers = re.findall(r'\d+', balance_clean)

        if numbers:
            amount = int(''.join(numbers))
            attach_screenshot(self.page, "Balance amount retrieved")
            return amount

        raise ValueError(f"Could not extract balance number from text: '{balance_text}'")

    @allure.step("Get header balance amount as integer")
    def get_header_balance_amount(self) -> int:
        header_balance_text = self.get_header_balance()
        numbers = re.findall(r'\d+', header_balance_text)

        if numbers:
            amount = int(''.join(numbers))
            attach_screenshot(self.page, "Header balance amount retrieved")
            return amount

        raise ValueError(f"Could not extract balance number from header text: '{header_balance_text}'")

    @allure.step("Open payment methods dropdown")
    def open_payment_methods_dropdown(self):
        self.page.wait_for_load_state("domcontentloaded", timeout=Timeouts.BASE_PAGE_LOAD)

        # Wait for payment methods panel to be visible first
        payment_panel = self.page.locator(self.locators.payment_methods_panel)
        expect(payment_panel).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        # Wait for payment methods select container to be visible
        payment_select = self.page.locator(self.locators.payment_methods_select)
        expect(payment_select).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        select_button = self.page.locator(self.locators.payment_methods_select_button)
        expect(select_button).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
        select_button.click()

        dropdown = self.page.locator(self.locators.payment_methods_dropdown)
        expect(dropdown).to_be_visible(timeout=Timeouts.Balance.ELEMENT_VISIBLE)

    @allure.step("Select payment method: {method}")
    def select_payment_method(self, method: str):
        self.open_payment_methods_dropdown()

        if method == RUSSIAN_CARDS:
            option = self.page.locator(self.locators.dropdown_russian_cards)

        elif method == INTERNATIONAL_CARDS:
            option = self.page.locator(self.locators.dropdown_international_cards)

        else:
            raise ValueError(f"Unknown payment method: {method}")

        expect(option).to_be_visible()
        option.click()
        expect(option).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)

    @allure.step("Get selected payment method")
    def get_selected_payment_method(self) -> str:
        select_button = self.page.locator(self.locators.payment_methods_select_button)
        expect(select_button).to_be_visible()

        method = select_button.text_content().strip()
        attach_screenshot(self.page, "Selected payment method retrieved")
        return method

    @allure.step("Click bank logo at index {index}")
    def click_bank_logo(self, index: int = 0):
        bank_logos = self.page.locator(self.locators.bank_logo)
        expect(bank_logos.nth(index)).to_be_visible()

        bank_logos.nth(index).click()
        attach_screenshot(self.page, "Bank logo clicked")

    @allure.step("Check payment methods switching")
    def check_payment_methods_switching(self):
        selected = self.get_selected_payment_method()
        assert RUSSIAN_CARDS in selected, \
            f"Expected 'Российские карты' to be selected initially, got '{selected}'"

        self.select_payment_method(INTERNATIONAL_CARDS)
        selected = self.get_selected_payment_method()
        assert INTERNATIONAL_CARDS in selected, \
            f"Expected 'Международные карты' to be selected, got '{selected}'"

        self.select_payment_method(RUSSIAN_CARDS)
        selected = self.get_selected_payment_method()
        assert "Российские карты" in selected, \
            f"Expected 'Российские карты' to be selected, got '{selected}'"

        attach_screenshot(self.page, "Payment methods switching verified")

    @allure.step("Check bank logos are clickable")
    def check_bank_logos_clickable(self):
        bank_logos = self.page.locator(self.locators.bank_logo)
        logo_count = bank_logos.count()

        assert logo_count >= 4, f"Expected at least 4 bank logos, got {logo_count}"

        for i in range(min(4, logo_count)):
            logo = bank_logos.nth(i)
            expect(logo).to_be_visible()

            src = logo.get_attribute("src")
            assert src is not None, f"Bank logo {i} should have src attribute"

        attach_screenshot(self.page, "Bank logos verified")

    @allure.step("Fill payment amount: {amount}")
    def fill_payment_amount(self, amount: str):
        amount_input = self.page.locator(self.locators.payment_amount_input)
        expect(amount_input).to_be_visible()

        amount_input.click()
        amount_input.fill(amount)
        attach_screenshot(self.page, "Payment amount filled")

    @allure.step("Check pay button is disabled")
    def check_pay_button_disabled(self):
        pay_button = self.page.locator(self.locators.payment_pay_button)
        expect(pay_button).to_be_visible()
        expect(pay_button).to_be_disabled()
        attach_screenshot(self.page, "Pay button disabled verified")

    @allure.step("Check pay button is enabled")
    def check_pay_button_enabled(self):
        pay_button = self.page.locator(self.locators.payment_pay_button)
        expect(pay_button).to_be_visible()
        expect(pay_button).to_be_enabled()
        attach_screenshot(self.page, "Pay button enabled verified")

    @allure.step("Click pay button")
    def click_pay_button(self):
        pay_button = self.page.locator(self.locators.payment_pay_button)
        expect(pay_button).to_be_visible()

        pay_button.click()
        attach_screenshot(self.page, "Pay button clicked")

    @allure.step("Verify still on payment page")
    def verify_stay_on_payment_page(self):
        current_url = self.page.url

        assert "/app/payment" in current_url, \
            f"Expected to stay on payment page, but URL is {current_url}"
        attach_screenshot(self.page, "Still on payment page verified")

    def _check_amount_in_json(self, post_data_json: dict, expected_amount: str) -> bool:
        amount_fields = ['amount', 'sum', 'value', 'total', 'payment_amount', 'amountRub']
        for key in amount_fields:
            if key in post_data_json:
                amount_value = post_data_json[key]
                if str(amount_value) == expected_amount or amount_value == int(expected_amount):
                    return True
        return False

    @allure.step("Verify amount {expected_amount} exists in request payload")
    def verify_amount_in_request_payload(self, request, expected_amount: str):
        post_data = request.post_data

        if not post_data:
            return expected_amount in request.url or f"amount={expected_amount}" in request.url

        try:
            post_data_json = json.loads(post_data)
            return self._check_amount_in_json(post_data_json, expected_amount)

        except (json.JSONDecodeError, TypeError):
            return expected_amount in post_data

    def _extract_span_value(self, span) -> int | None:
        try:
            if not span.is_visible():
                return None

            text_content = span.text_content()
            if not text_content or text_content.strip() == "":
                return None

            numbers = re.findall(r'\d+', text_content)
            if numbers:
                return int(numbers[0])

        except (ValueError, TypeError) as e:
            logging.debug(f"Failed to extract span value: {e}")
        return None

    @allure.step("Check amount value exists in span and > {min_value}")
    def check_amount_value_in_span(self, min_value: int = 10) -> bool:
        spans = self.page.locator("span")
        span_count = spans.count()

        for i in range(min(span_count, 50)):
            span = spans.nth(i)
            value = self._extract_span_value(span)

            if value and value > min_value:
                attach_screenshot(self.page, "Amount value found in span")
                return True

        attach_screenshot(self.page, "Amount value check completed")
        return False
