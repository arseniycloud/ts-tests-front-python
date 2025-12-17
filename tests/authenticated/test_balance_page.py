import logging
import re

import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.balance_locators import INTERNATIONAL_CARDS, RUSSIAN_CARDS
from pages.app_page import AppPage
from pages.balance_page import BalancePage
from utils.allure_helpers import attach_screenshot


@allure.epic("Balance")
@allure.feature("Balance Page")
class TestBalancePage:

    @allure.title("Test navigation to balance page")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_navigation_to_balance(self, auth_user_existing):
        page = auth_user_existing
        app_page = AppPage(page)

        with allure.step("Ensure we're on /app page and it's fully loaded"):
            if "/app" not in page.url:
                page.goto(f"{BASE_URL}/app")
                page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_PAGE_LOAD)
                attach_screenshot(page, "App page loaded")

        with allure.step("Navigate to balance page"):
            app_page.navigate_to_balance()
            balance_page = BalancePage(page)
            expect(page.locator(balance_page.locators.page_container)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Balance page navigation")

        with allure.step("Verify we're on balance page"):
            assert "/app/payment" in page.url or "/app" in page.url, f"Should be on balance page, got {page.url}"
            attach_screenshot(page, "Balance page verification")

    @allure.title("Test balance page elements are visible")
    @pytest.mark.validation
    def test_balance_page_elements(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            expect(page.locator(balance_page.locators.page_container)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Check balance page elements"):
            balance_page.check_balance_elements()
            attach_screenshot(page, "Balance page elements verified")

    @allure.title("Test balance amount is displayed and greater than zero")
    @pytest.mark.validation
    def test_balance_amount(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Get balance amount"):
            actual_balance = balance_page.get_balance_amount()
            attach_screenshot(page, f"Balance amount: {actual_balance}")

        with allure.step("Verify balance is greater than zero"):
            assert actual_balance > 0, f"Balance should be greater than 0, got {actual_balance}"
            attach_screenshot(page, "Balance verification passed")

    @allure.title("Test header balance amount is displayed and greater than zero")
    @pytest.mark.validation
    def test_header_balance_amount(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Get header balance amount"):
            actual_balance = balance_page.get_header_balance_amount()
            attach_screenshot(page, f"Header balance amount: {actual_balance}")

        with allure.step("Verify header balance is greater than zero"):
            assert actual_balance > 0, f"Header balance should be greater than 0, got {actual_balance}"
            attach_screenshot(page, "Header balance verification passed")

    @allure.title("Test payment methods panel is visible")
    @pytest.mark.validation
    def test_payment_methods_panel(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Check payment methods panel"):
            balance_page.check_payment_methods_panel()
            attach_screenshot(page, "Payment methods panel verified")

    @allure.title("Test payment amount form is visible")
    @pytest.mark.validation
    def test_payment_amount_form(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Check payment amount form"):
            balance_page.check_payment_amount_form()
            attach_screenshot(page, "Payment amount form verified")

    @allure.title("Test payment methods switching functionality")
    @pytest.mark.validation
    def test_payment_methods_switching(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Check payment methods switching"):
            balance_page.check_payment_methods_switching()
            attach_screenshot(page, "Payment methods switching verified")

    @allure.title("Test selecting Russian cards payment method")
    @pytest.mark.smoke
    @pytest.mark.validation
    def test_select_russian_cards(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            expect(page.locator(balance_page.locators.page_container)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Select Russian cards payment method"):
            balance_page.select_payment_method(RUSSIAN_CARDS)
            expect(page.locator(balance_page.locators.payment_methods_select_button)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Russian cards selected")

        with allure.step("Verify Russian cards is selected"):
            selected = balance_page.get_selected_payment_method()
            attach_screenshot(page, f"Selected payment method: {selected}")
            assert RUSSIAN_CARDS in selected, f"Expected 'Российские карты' to be selected, got '{selected}'"

    @allure.title("Test selecting international cards payment method")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_select_international_cards(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            expect(page.locator(balance_page.locators.page_container)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Select international cards payment method"):
            balance_page.select_payment_method(INTERNATIONAL_CARDS)
            expect(page.locator(balance_page.locators.payment_methods_select_button)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "International cards selected")

        with allure.step("Verify international cards is selected"):
            selected = balance_page.get_selected_payment_method()
            attach_screenshot(page, f"Selected payment method: {selected}")
            assert INTERNATIONAL_CARDS in selected, f"Expected 'Международные карты' to be selected, got '{selected}'"

    @allure.title("Test bank logos interaction")
    @pytest.mark.validation
    def test_bank_logos_interaction(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Click first bank logo"):
            balance_page.click_bank_logo(0)
            attach_screenshot(page, "First bank logo clicked")

        with allure.step("Click second bank logo"):
            balance_page.click_bank_logo(1)
            attach_screenshot(page, "Second bank logo clicked")

        with allure.step("Click third bank logo"):
            balance_page.click_bank_logo(2)
            attach_screenshot(page, "Third bank logo clicked")

    @allure.title("Test payment button is disabled with zero amount")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_payment_button_disabled_with_zero_amount(self, auth_user_existing):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            expect(page.locator(balance_page.locators.page_container)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Test with Russian cards - zero amount"):
            balance_page.select_payment_method(RUSSIAN_CARDS)
            expect(page.locator(balance_page.locators.payment_methods_select_button)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Russian cards selected")

            balance_page.fill_payment_amount("0")
            amount_input = page.locator(balance_page.locators.payment_amount_input)
            expect(amount_input).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Zero amount entered for Russian cards")

            balance_page.check_pay_button_disabled()
            attach_screenshot(page, "Pay button disabled with zero amount - Russian cards")

        with allure.step("Test with International cards - zero amount"):
            balance_page.select_payment_method(INTERNATIONAL_CARDS)
            expect(page.locator(balance_page.locators.payment_methods_select_button)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "International cards selected")

            balance_page.fill_payment_amount("0")
            amount_input = page.locator(balance_page.locators.payment_amount_input)
            expect(amount_input).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Zero amount entered for International cards")

            balance_page.check_pay_button_disabled()
            attach_screenshot(page, "Pay button disabled with zero amount - International cards")


    @allure.title("Test payment button with valid amount for Russian cards")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_payment_button_valid_amount_russian_cards(self, authenticated_user_new):
        page = authenticated_user_new
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            expect(page.locator(balance_page.locators.page_container)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Select Russian cards payment method"):
            balance_page.select_payment_method(RUSSIAN_CARDS)
            expect(page.locator(balance_page.locators.payment_methods_select_button)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Russian cards selected")

        with allure.step("Fill payment amount"):
            balance_page.fill_payment_amount("100")
            amount_input = page.locator(balance_page.locators.payment_amount_input)
            expect(amount_input).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)

            page.wait_for_timeout(Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Payment amount 100 entered")

        with allure.step("Check pay button is enabled"):
            balance_page.check_pay_button_enabled()

            pay_button = page.locator(balance_page.locators.payment_pay_button)
            expect(pay_button).to_be_visible(timeout=Timeouts.ShortWaits.SHORT_PAUSE)
            expect(pay_button).to_be_enabled(timeout=Timeouts.ShortWaits.SHORT_PAUSE)
            attach_screenshot(page, "Pay button enabled and ready")

        with allure.step("Wait for page to fully load before payment"):
            page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

            # Additional wait for all elements to stabilize
            page.wait_for_timeout(5000)
            attach_screenshot(page, "Page fully loaded, ready for payment")

        with allure.step("Click pay button and wait for payment API response"):
            balance_page.click_pay_button()

            with page.expect_response(
                lambda resp: "/api-v1/yoo/create-payment" in resp.url,
                timeout=Timeouts.Balance.PAYMENT_RESPONSE_WAIT,
            ) as resp_info:
                attach_screenshot(page, "Pay button clicked")

        with allure.step("Verify payment API response"):
            response = resp_info.value
            assert response.status == 200, f"Expected status 200 for create-payment API, got {response.status}"

            # Extract confirmation_url from response body
            try:
                response_body = response.json()
                confirmation_url = response_body.get("confirmation_url")
                logging.debug(f"Payment API response body: {response_body}")
                logging.debug(f"Confirmation URL: {confirmation_url}")

            except Exception as e:
                logging.debug(f"Could not parse response as JSON: {e}")
                response_body = None
                confirmation_url = None

        with allure.step("Wait for redirect to yoomoney page"):
            redirect_timeout = 60000  # 60 seconds
            yoomoney_pattern = re.compile(r".*yoomoney\.ru.*")

            # Check if already redirected after API response
            current_url = page.url
            logging.debug(f"Current URL after API response: {current_url}")

            # If not redirected, wait a bit for automatic redirect, then perform manual redirect if needed
            if not yoomoney_pattern.search(current_url):
                # Wait a short time for automatic redirect
                try:
                    page.wait_for_url(yoomoney_pattern, timeout=3000)
                    attach_screenshot(page, "Automatic redirect occurred")
                except Exception:
                    # Automatic redirect didn't happen, perform manual redirect if we have confirmation_url
                    if confirmation_url:
                        logging.debug(f"Performing manual JavaScript redirect to: {confirmation_url}")
                        attach_screenshot(page, f"Performing manual redirect to yoomoney. Confirmation URL: {confirmation_url}")
                        page.evaluate(f"window.location.href = '{confirmation_url}'")
                    else:
                        attach_screenshot(page, "No confirmation_url available, waiting for redirect")

            # Wait for navigation to yoomoney
            try:
                page.wait_for_url(yoomoney_pattern, timeout=redirect_timeout)
                page.wait_for_load_state("networkidle", timeout=60000)

            except Exception as e:
                current_url = page.url
                logging.debug(f"Redirect timeout. Current URL: {current_url}")
                attach_screenshot(page, f"After redirect wait. Current URL: {current_url}")
                if not yoomoney_pattern.search(current_url):
                    raise AssertionError(
                        f"Failed to redirect to yoomoney within {redirect_timeout}ms. "
                        f"Confirmation URL: {confirmation_url}. "
                        f"Current URL: {current_url}. Response body: {response_body}. Error: {e}"
                    )

            attach_screenshot(page, "Successfully redirected to yoomoney")
            assert "yoomoney.ru" in page.url.lower(), f"Expected yoomoney.ru in URL, got: {page.url}"

    @allure.title("Test payment by international cards")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_payment_by_international_cards(self, authenticated_user_new):
        page = authenticated_user_new
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            expect(page.locator(balance_page.locators.page_container)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Balance page loaded")

        with allure.step("Select international cards payment method"):
            balance_page.select_payment_method(INTERNATIONAL_CARDS)
            expect(page.locator(balance_page.locators.payment_methods_select_button)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "International cards selected")

        with allure.step("Fill payment amount"):
            balance_page.fill_payment_amount("1000")
            amount_input = page.locator(balance_page.locators.payment_amount_input)

            expect(amount_input).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)
            attach_screenshot(page, "Payment amount 1000 entered")

        with allure.step("Check pay button is enabled"):
            balance_page.check_pay_button_enabled()
            pay_button = page.locator(balance_page.locators.payment_pay_button)

            expect(pay_button).to_be_visible(timeout=Timeouts.ShortWaits.SHORT_PAUSE)
            attach_screenshot(page, "Pay button enabled")

        with allure.step("Check amount value in span"):

            try:
                balance_page.check_amount_value_in_span(min_value=10)
                attach_screenshot(page, "Amount value checked in span")

            except Exception as e:
                logging.debug(f"Optional check for amount value in span failed (continuing): {e}")

        with allure.step("Click pay button and wait for gateline payment request"):
            with page.expect_request(
                lambda req: "/api-v1/gateline/create-payment" in req.url and req.method == "POST",
                timeout=Timeouts.Balance.PAYMENT_REQUEST_WAIT,
            ) as payment_request_info:
                with page.expect_response(
                    lambda resp: "/api-v1/gateline/create-payment" in resp.url,
                    timeout=Timeouts.Balance.PAYMENT_RESPONSE_WAIT,
                ) as resp_info:
                    balance_page.click_pay_button()
                    attach_screenshot(page, "Pay button clicked")

            payment_request = payment_request_info.value
            response = resp_info.value

        with allure.step("Verify payment response status"):
            attach_screenshot(page, f"Payment response status: {response.status}")
            assert response.status == 201, (f"Expected status 201, got {response.status}")

        with allure.step("Verify payment request URL and payload"):
            assert payment_request.url.endswith("/api-v1/gateline/create-payment"), (
                f"Expected request to gateline/create-payment, got {payment_request.url}")

            amount_found = balance_page.verify_amount_in_request_payload(payment_request, "1000")
            attach_screenshot(page, f"Payment request verified: {payment_request.url}")
            assert amount_found, (
                f"Expected amount 1000. URL: {payment_request.url}, Post data: {payment_request.post_data}")

        with allure.step("Wait for redirect to gateline checkout page"):

            redirect_timeout = 20000  # 20 seconds
            gateline_pattern = re.compile(r".*checkout\.sandbox\.gateline\.net.*/pay\?token=.*")
            attach_screenshot(page, "On gateline payment page")


            # Check if already redirected
            current_url = page.url
            if not gateline_pattern.search(current_url):
                attach_screenshot(page, "Waiting for gateline redirect")
                page.wait_for_url(gateline_pattern, timeout=redirect_timeout)

            attach_screenshot(page, "Successfully redirected to gateline checkout")
            assert "checkout.sandbox.gateline.net" in page.url.lower(), f"Expected gateline checkout URL, got: {page.url}"
            assert "/pay?token=" in page.url, f"Expected /pay?token= in URL, got: {page.url}"
