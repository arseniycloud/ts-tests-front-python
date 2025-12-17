import re
import time

import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import OTP_CODE
from config.timeouts import Timeouts
from locators.registration_locators import RegistrationLocators
from utils.allure_helpers import attach_element_screenshot
from utils.user_generator import generate_unique_email


@allure.epic("Registration")
@allure.feature("Registration Page")
@allure.title("Registration Page - User Registration")
class TestRegistrationPageTests:

    # Shared locators instance for all tests in this class
    locators = RegistrationLocators()

    @allure.title("Test registration page elements are visible")
    @pytest.mark.authorization
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_registration_page_elements(self, registration_page):
        registration_page.check_registration_elements()


    @allure.title("Test that register button is disabled without email")
    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_empty_email_registration(self, registration_page):
        with allure.step("Verify register button is visible and disabled"):
            register_btn = registration_page.page.locator(self.locators.register_button).first
            expect(register_btn).to_be_visible()
            attach_element_screenshot(register_btn, "Register button (disabled)")

            registration_page.wait_standard()
            expect(register_btn).to_be_disabled()

    @allure.title("Test that invalid email shows error")
    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_invalid_email_registration(self, registration_page):
        with allure.step("Fill email field with invalid email"):
            invalid_email = "invalid-email"
            email_input = registration_page.page.locator(self.locators.email_field).first
            expect(email_input).to_be_visible()

            attach_element_screenshot(email_input, "Email field")
            email_input.fill(invalid_email)

        with allure.step("Check terms checkbox"):
            terms_checkbox = registration_page.page.get_by_role("checkbox")
            expect(terms_checkbox).to_be_visible()

            attach_element_screenshot(terms_checkbox, "Terms checkbox")
            terms_checkbox.check()

        with allure.step("Click register button"):
            register_btn = registration_page.page.get_by_role("button", name="зарегистрироваться")
            expect(register_btn).to_be_visible()

            attach_element_screenshot(register_btn, "Register button")
            register_btn.click()

        with allure.step("Verify error alert is displayed"):
            alert = registration_page.page.get_by_role("alert")
            expect(alert).to_be_visible(timeout=Timeouts.Toast.VISIBLE)
            attach_element_screenshot(alert, "Error alert modal")

            error_title = registration_page.page.get_by_text("Ошибка ввода email!", exact=True)
            expect(error_title).to_be_visible()

            error_message = registration_page.page.get_by_text("Email не корректный!", exact=True)
            expect(error_message).to_be_visible()

        with allure.step("Close the alert"):
            close_btn = registration_page.page.get_by_role("button", name="Close")
            expect(close_btn).to_be_visible()
            attach_element_screenshot(close_btn, "Close button")
            close_btn.click()


    @allure.title("Test registration with existing email")
    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_existing_email_registration(self, registration_page):
        with allure.step("Generate unique email"):
            unique_email = generate_unique_email()

        with allure.step("Fill email field"):
            email_input = registration_page.page.locator(self.locators.email_field).first
            expect(email_input).to_be_visible()

            email_input.fill(unique_email)
            registration_page.wait_standard()

        with allure.step("Check terms checkbox"):
            terms_checkbox = registration_page.page.get_by_role("checkbox")
            expect(terms_checkbox).to_be_visible()

            terms_checkbox.check()
            registration_page.wait_standard()

        with allure.step("Click register button"):
            register_btn = registration_page.page.get_by_role("button", name="зарегистрироваться")
            expect(register_btn).to_be_visible()

            register_btn.click()
            registration_page.wait_standard()

        with allure.step("Verify OTP form appears after registration"):
            registration_page.check_otp_form_elements(unique_email)



    @allure.title("Test that valid email shows OTP form with all elements")
    @pytest.mark.authorization
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_valid_email_registration_otp_form(self, registration_page):
        with allure.step("Generate unique email"):
            unique_email = generate_unique_email()

        with allure.step("Navigate to registration page"):
            registration_page.navigate_to_registration()
            registration_page.wait_standard()

        with allure.step("Fill email field"):
            email_input = registration_page.page.locator(self.locators.email_field).first
            expect(email_input).to_be_visible()
            attach_element_screenshot(email_input, "Email field")

            email_input.fill(unique_email)
            registration_page.wait_standard()

        with allure.step("Check terms checkbox"):
            terms_checkbox = registration_page.page.get_by_role("checkbox")
            expect(terms_checkbox).to_be_visible()
            attach_element_screenshot(terms_checkbox, "Terms checkbox")

            terms_checkbox.check()
            registration_page.wait_standard()

        with allure.step("Click register button"):
            register_btn = registration_page.page.get_by_role("button", name="зарегистрироваться")
            expect(register_btn).to_be_visible()
            attach_element_screenshot(register_btn, "Register button")

            register_btn.click()
            registration_page.wait_standard()

        with allure.step("Verify OTP form elements"):
            registration_page.check_otp_form_elements(unique_email)


    @allure.title("Test that invalid OTP code shows error during registration")
    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_invalid_otp_code_registration(self, registration_page):
        with allure.step("Generate unique email and prepare invalid OTP"):
            unique_email = generate_unique_email()
            invalid_otp = "00000"

        with allure.step("Navigate to registration page"):
            registration_page.navigate_to_registration()

        with allure.step("Fill email field and register"):
            email_input = registration_page.page.locator(self.locators.email_field).first
            expect(email_input).to_be_visible()

            attach_element_screenshot(email_input, "Email field")
            email_input.fill(unique_email)

            terms_checkbox = registration_page.page.get_by_role("checkbox")
            expect(terms_checkbox).to_be_visible()

            attach_element_screenshot(terms_checkbox, "Terms checkbox")
            terms_checkbox.check()

            register_btn = registration_page.page.get_by_role("button", name="зарегистрироваться")
            expect(register_btn).to_be_visible()

            attach_element_screenshot(register_btn, "Register button")
            register_btn.click()

        with allure.step("Fill OTP fields with invalid code"):
            registration_page.fill_pin_fields(invalid_otp, "OTP pin fields")

        with allure.step("Submit invalid OTP code"):
            registration_page.page.locator(self.locators.otp_send_button).first.click()

        with allure.step("Verify error alert is displayed"):
            alert = registration_page.page.get_by_role("alert")
            expect(alert).to_be_visible(timeout=Timeouts.Toast.VISIBLE)
            attach_element_screenshot(alert, "Error alert modal")

            error_title = registration_page.page.get_by_text("Ошибка ввода кода авторизации!", exact=True)
            expect(error_title).to_be_visible()

            error_message = registration_page.page.get_by_text("token invalid", exact=True)
            expect(error_message).to_be_visible()

        with allure.step("Close the alert"):
            close_btn = registration_page.page.get_by_role("button", name="Close")
            expect(close_btn).to_be_visible()
            attach_element_screenshot(close_btn, "Close button")

            close_btn.click()
            expect(close_btn).to_be_visible(timeout=Timeouts.Registration.STANDARD_PAUSE)


    @allure.title("Test resend OTP with invalid code, then resend and enter valid code during registration")
    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_resend_otp_and_valid_code_registration(self, registration_page):
        with allure.step("Generate unique email and prepare OTP codes"):
            unique_email = generate_unique_email()
            invalid_otp = "00000"
            valid_otp = OTP_CODE

        with allure.step("Navigate to registration page"):
            registration_page.navigate_to_registration()
            registration_page.wait_standard()

        with allure.step("Fill email field and register"):
            email_input = registration_page.page.locator(self.locators.email_field).first
            expect(email_input).to_be_visible()
            attach_element_screenshot(email_input, "Email field")
            email_input.fill(unique_email)
            registration_page.wait_standard()

            terms_checkbox = registration_page.page.get_by_role("checkbox")
            expect(terms_checkbox).to_be_visible()
            attach_element_screenshot(terms_checkbox, "Terms checkbox")

            terms_checkbox.check()
            registration_page.wait_standard()

            register_btn = registration_page.page.get_by_role("button", name="зарегистрироваться")
            expect(register_btn).to_be_visible()
            attach_element_screenshot(register_btn, "Register button")

            register_btn.click()
            registration_page.wait_standard()

        with allure.step("Fill OTP fields with invalid code"):
            registration_page.fill_pin_fields(invalid_otp, "OTP pin fields")
            registration_page.wait_standard()

        with allure.step("Submit invalid OTP and close error alert"):
            otp_send_btn = registration_page.page.locator(self.locators.otp_send_button).first
            attach_element_screenshot(otp_send_btn, "OTP send button")
            registration_page.page.locator(self.locators.otp_send_button).first.click()
            alert = registration_page.page.get_by_role("alert")
            expect(alert).to_be_visible(timeout=Timeouts.Registration.STANDARD_PAUSE)
            expect(alert).to_be_visible()
            attach_element_screenshot(alert, "Error alert modal")

            close_btn = registration_page.page.get_by_role("button", name="Close")
            expect(close_btn).to_be_visible()
            attach_element_screenshot(close_btn, "Close button")
            close_btn.click()

        with allure.step("Wait and resend OTP code"):
            wait_time_seconds = Timeouts.Registration.RESEND_OTP_WAIT / 1000
            time.sleep(wait_time_seconds)
            resend_btn = registration_page.page.locator(self.locators.otp_resend_button).first

            expect(resend_btn).to_be_visible()
            attach_element_screenshot(resend_btn, "Resend OTP button")
            resend_btn.click()

        with allure.step("Clear OTP fields and fill with valid code"):
            registration_page.clear_pin_fields("OTP pin fields (cleared)")
            registration_page.fill_pin_fields(valid_otp, "OTP pin fields (filled)")
            registration_page.wait_standard()

        with allure.step("Submit valid OTP code and verify successful registration"):
            registration_page.page.locator(self.locators.otp_send_button).first.click()
            registration_page.wait_standard()

            registration_page.wait_long()
            registration_page.wait_for_network_idle()
            expect(registration_page.page,"User should be redirected to /app",).to_have_url(
                re.compile(r".*/app.*"), timeout=Timeouts.BASE_PAGE_LOAD)
