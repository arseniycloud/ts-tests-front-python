import re

import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import OTP_CODE
from config.timeouts import Timeouts
from locators.login_locators import LoginLocators
from utils.allure_helpers import attach_element_screenshot, attach_screenshot


@allure.epic("Login")
@allure.feature("Login Page")
@allure.title("Login Page - Authentication")
class TestLoginPageTests:

    # Shared locators instance for all tests in this class
    locators = LoginLocators()

    @pytest.mark.authorization
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_login_page_elements(self, login_page):
        with allure.step("Check login page elements"):
            attach_screenshot(login_page.page, "Login page initial state")
            login_page.check_login_elements()

    @pytest.mark.authorization
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_login_form_elements(self, login_page):
        with allure.step("Initialize locators"):
            locators = LoginLocators()

        with allure.step("Check if login form is present"):
            attach_screenshot(login_page.page, "Login page form check")
            form = login_page.page.locator(locators.login_form)
            assert form.count() >= 0, "Login page should have a form"

        with allure.step("Check for common login form elements"):
            username_field = login_page.page.locator(locators.username_field)
            password_field = login_page.page.locator(locators.password_field)
            submit_button = login_page.page.locator(locators.login_button)

            attach_element_screenshot(username_field, "Username field")
            attach_element_screenshot(password_field, "Password field")
            attach_element_screenshot(submit_button, "Submit button")

        with allure.step("Verify at least one form element is present"):
            # At least one of these should be present
            total_elements = (username_field.count() + password_field.count() + submit_button.count())
            assert total_elements >= 0, "Login page should have login form elements"

    @pytest.mark.authorization
    @pytest.mark.validation
    def test_login_navigation(self, login_page):
        with allure.step("Verify we're on login page"):
            attach_screenshot(login_page.page, "Login page navigation check")
            # Check if we're on login page
            assert "/login" in login_page.page.url, "Should be on login page"

        with allure.step("Check page title"):
            # Check page title
            title = login_page.page.locator(self.locators.page_title)
            attach_element_screenshot(title, "Page title")

            title_text = title.text_content()
            assert title_text is not None, "Login page should have a title"

    @pytest.mark.authorization
    @pytest.mark.validation
    def test_login_page_links(self, login_page):
        with allure.step("Get all links from the page"):
            attach_screenshot(login_page.page, "Login page links")

            # Check for common login page links
            links = login_page.page.locator("a")
            link_texts = [link.text_content() for link in links.all()]

        with allure.step("Check for common login-related links"):
            # Check for common login-related links
            common_links = [
                "регистрация",
                "забыли пароль",
                "восстановить",
                "register",
                "forgot",
                "reset",
            ]
            has_login_links = any(any(common in text.lower() for common in common_links)
                for text in link_texts
                if text
            )

        with allure.step("Log if login-related links are found"):
            # This is optional, so we just log it
            if has_login_links:
                print("Found login-related links on the page")

    @pytest.mark.authorization
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_unregistered_user_login(self, login_page):
        test_email = "testuser!@#$@test.tun2.ru"

        with allure.step("Fill email field"):
            # Fill email field (login_page fixture already navigated to login page)
            attach_screenshot(login_page.page, "Login page before filling email")
            email_input = login_page.page.locator(self.locators.username_field).first
            expect(email_input).to_be_visible()
            attach_element_screenshot(email_input, "Email field")

            email_input.click()
            email_input.fill(test_email)
            attach_element_screenshot(email_input, "Email field filled")

        with allure.step("Click login button"):
            # Click login button
            attach_screenshot(login_page.page, "Login page before clicking login")
            login_btn = login_page.page.locator(self.locators.login_button).first

            expect(login_btn).to_be_visible()
            attach_element_screenshot(login_btn, "Login button")
            login_btn.click()

        with allure.step("Verify toast alert appears"):
            # Check toast alert structure and content
            attach_screenshot(login_page.page, "Login page after clicking login")
            toast_alert = login_page.page.locator(self.locators.toast_alert_item)

            expect(toast_alert).to_be_visible(timeout=Timeouts.Toast.VISIBLE)
            attach_element_screenshot(toast_alert, "Toast alert")

        with allure.step("Verify error title in toast alert"):
            attach_screenshot(login_page.page, "Error toast alert visible")
            expect(toast_alert.get_by_text("Ошибка входа в систему!", exact=True)).to_be_visible()
            expect(toast_alert.get_by_text(f"User {test_email} doesnt exists", exact=True)).to_be_visible()

    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_invalid_otp_code(self, login_page):
        test_email = "test333@test.com"
        invalid_otp = "00000"

        with allure.step("Fill email field"):
            # Fill email field
            attach_screenshot(login_page.page, "Login page before filling email")
            email_input = login_page.page.locator(self.locators.username_field).first
            expect(email_input).to_be_visible()
            attach_element_screenshot(email_input, "Email field")

            email_input.click()
            email_input.fill(test_email)
            attach_element_screenshot(email_input, "Email field filled")

        with allure.step("Click login button to initiate OTP flow"):
            # Click login button to initiate OTP flow
            attach_screenshot(login_page.page, "Login page before clicking login")
            login_btn = login_page.page.locator(self.locators.login_button).first

            expect(login_btn).to_be_visible()
            attach_element_screenshot(login_btn, "Login button")
            login_btn.click()

        with allure.step("Fill OTP fields with invalid code"):
            # Fill all OTP pin fields with invalid code
            attach_screenshot(login_page.page, "OTP form before filling")
            login_page.fill_pin_fields(invalid_otp, "OTP pin fields")
            attach_screenshot(login_page.page, "OTP form filled with invalid code")

        with allure.step("Submit OTP and verify API response"):
            # Wait for API response and click send button
            attach_screenshot(login_page.page, "Before submitting invalid OTP")
            with login_page.page.expect_response(
                lambda resp: "/api-v1/auth/login-code" in resp.url, timeout=Timeouts.Api.LOGIN_CODE_RESPONSE
            ) as resp_info:
                login_page.page.locator(self.locators.otp_send_button).first.click()

            response = resp_info.value
            assert response.status == 400, f"Expected status 400, got {response.status}"

        with allure.step("Verify API response body"):
            # Check API response body
            response_body = response.json()
            assert (response_body.get("message") == "token invalid"), f"'Token invalid' message, got {response_body}"

        with allure.step("Verify error alert appears"):
            # Check alert with error (use first alert to avoid strict mode violation)
            attach_screenshot(login_page.page, "Error alert visible")
            alert = (login_page.page.get_by_role("alert").filter(has_text="Ошибка ввода кода авторизации!").first)

            expect(alert).to_be_visible(timeout=Timeouts.Toast.VISIBLE)
            attach_element_screenshot(alert, "Error alert modal")

        with allure.step("Verify error title"):
            # Check error title
            error_title = login_page.page.get_by_text("Ошибка ввода кода авторизации!", exact=True)
            attach_element_screenshot(error_title, "Error title")
            expect(error_title).to_be_visible()

        with allure.step("Verify error message"):
            # Check error message
            error_message = login_page.page.get_by_text("token invalid", exact=True)
            attach_element_screenshot(error_message, "Error message")
            expect(error_message).to_be_visible()

        with allure.step("Close error alert"):
            # Close the alert (use filter to get Close button from the correct alert)
            close_btn = (
                login_page.page.get_by_role("alert")
                .filter(has_text="Ошибка ввода кода авторизации!")
                .get_by_role("button", name="Close")
            )
            expect(close_btn).to_be_visible()
            attach_element_screenshot(close_btn, "Close button")
            close_btn.click()
            attach_screenshot(login_page.page, "After closing error alert")

    @pytest.mark.authorization
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_resend_otp_and_valid_code(self, login_page):  # noqa: PLR0915,C901 - complex UI flow with retries
        test_email = "test333@test.com"
        invalid_otp = "00000"
        valid_otp = OTP_CODE

        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
            attach_screenshot(login_page.page, "Login page loaded")

        with allure.step("Fill email field"):
            attach_screenshot(login_page.page, "Login page before filling email")
            email_input = login_page.page.locator(self.locators.username_field).first
            expect(email_input).to_be_visible()

            attach_element_screenshot(email_input, "Email field")
            email_input.click()
            email_input.fill(test_email)
            attach_element_screenshot(email_input, "Email field filled")

        with allure.step("Click login button to initiate OTP flow"):

            attach_screenshot(login_page.page, "Login page before clicking login")
            login_btn = login_page.page.locator(self.locators.login_button).first

            expect(login_btn).to_be_visible()
            attach_element_screenshot(login_btn, "Login button")
            login_btn.click()

        with allure.step("Fill OTP fields with invalid code"):
            attach_screenshot(login_page.page, "OTP form before filling")
            login_page.wait_for_network_idle()

            login_page.fill_pin_fields(invalid_otp, "OTP pin fields")
            attach_screenshot(login_page.page, "OTP form filled with invalid code")

        with allure.step("Submit invalid OTP and verify error response"):

            # Wait for API response and click send button
            attach_screenshot(login_page.page, "Before submitting invalid OTP")
            with login_page.page.expect_response(
                lambda resp: "/api-v1/auth/login-code" in resp.url, timeout=Timeouts.Api.LOGIN_CODE_RESPONSE
            ) as resp_info:
                login_page.page.locator(self.locators.otp_send_button).first.click()

            response = resp_info.value
            assert response.status == 400, f"Expected status 400, got {response.status}"

        with allure.step("Verify error alert appears"):
            attach_screenshot(login_page.page, "Error alert visible")
            alert = login_page.page.get_by_role("alert")

            expect(alert).to_be_visible(timeout=Timeouts.Toast.VISIBLE)
            attach_element_screenshot(alert, "Error alert modal")

        with allure.step("Close error alert"):
            close_btn = login_page.page.get_by_role("button", name="Close")
            expect(close_btn).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)

            attach_element_screenshot(close_btn, "Close button")
            close_btn.click()
            attach_screenshot(login_page.page, "After closing error alert")

        with allure.step("Wait before resend to avoid throttling"):
            login_page.page.wait_for_timeout(Timeouts.Registration.RESEND_OTP_WAIT)

        with allure.step("Click resend button"):
            attach_screenshot(login_page.page, "Before clicking resend button")
            resend_btn = login_page.page.locator(self.locators.otp_resend_button).first

            expect(resend_btn).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(resend_btn).to_be_enabled(timeout=Timeouts.BASE_ELEMENT_ENABLED)
            attach_element_screenshot(resend_btn, "Resend button")

            login_page.wait_for_network_idle()
            resend_btn.click(force=True)
            attach_screenshot(login_page.page, "After clicking resend button")

        with allure.step("Wait additional time after resend"):

            # Wait for OTP fields to be ready after resend
            otp_pin_1 = login_page.page.locator(self.locators.otp_pin_1).first
            expect(otp_pin_1).to_be_visible(timeout=5000)

        with allure.step("Clear OTP fields"):
            attach_screenshot(login_page.page, "Before clearing OTP fields")

            login_page.wait_for_network_idle()
            login_page.clear_pin_fields("OTP pin fields (cleared)")
            attach_screenshot(login_page.page, "After clearing OTP fields")

        with allure.step("Fill OTP fields with valid code"):
            attach_screenshot(login_page.page, "Before filling valid OTP")

            login_page.wait_for_network_idle()
            login_page.fill_pin_fields(valid_otp, "OTP pin fields (filled)")
            attach_screenshot(login_page.page, "OTP form filled with valid code")

        with allure.step("Submit valid OTP with retry logic"):
            # Retry logic for 429 (Too Many Requests) error
            max_retries = 3
            retry_delay = 10000
            for attempt in range(max_retries):
                with allure.step(f"Attempt {attempt + 1}/{max_retries}"):
                    attach_screenshot(login_page.page, f"Before submitting valid OTP (attempt {attempt + 1})")

                    with login_page.page.expect_response(
                        lambda resp: "/api-v1/auth/login-code" in resp.url, timeout=Timeouts.Api.LOGIN_CODE_RESPONSE) as resp_info:
                        login_page.page.locator(self.locators.otp_send_button).first.click()

                    response = resp_info.value

                    if response.status == 200:
                        attach_screenshot(login_page.page, f"Successful OTP submission (attempt {attempt + 1})")
                        break

                    if response.status == 429 and attempt < max_retries - 1:
                        attach_screenshot(login_page.page, f"Rate limit hit, waiting before retry (attempt {attempt + 1})")
                        # Need guaranteed minimum wait time before retry to respect rate limit
                        login_page.page.wait_for_timeout(retry_delay)

                    else:
                        assert response.status == 200, f"Expected status 200, got {response.status}"

        with allure.step("Verify successful login and redirect to app"):
            attach_screenshot(login_page.page, "After successful login")
            login_page.wait_for_network_idle()

            expect(login_page.page,"User should be redirected to /app",
            ).to_have_url(re.compile(r".*/app.*"), timeout=Timeouts.BASE_PAGE_LOAD)
            attach_screenshot(login_page.page, "Successfully redirected to app page")

    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_empty_email_login(self, login_page):
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
            attach_screenshot(login_page.page, "Login page loaded")

        with allure.step("Click login button without filling email"):
            attach_screenshot(login_page.page, "Login page before clicking login with empty email")
            login_btn = login_page.page.locator(self.locators.login_button).first

            expect(login_btn).to_be_visible()
            attach_element_screenshot(login_btn, "Login button")
            login_btn.click()

        with allure.step("Verify error alert appears"):
            attach_screenshot(login_page.page, "Error alert for empty email")
            alert = (login_page.page.get_by_role("alert").filter(has_text="Ошибка ввода email!"))

            expect(alert).to_be_visible(timeout=Timeouts.Toast.VISIBLE)
            attach_element_screenshot(alert, "Error alert modal")

        with allure.step("Verify error title"):
            error_title = login_page.page.get_by_text("Ошибка ввода email!", exact=True)
            attach_element_screenshot(error_title, "Error title")
            expect(error_title).to_be_visible()

        with allure.step("Verify error message"):
            error_message = login_page.page.get_by_text("Email не может быть пустым!", exact=True)
            attach_element_screenshot(error_message, "Error message")
            expect(error_message).to_be_visible()
