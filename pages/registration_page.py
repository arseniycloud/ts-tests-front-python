"""
Registration page class for TunService website
"""
import allure
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL
from locators.registration_locators import RegistrationLocators
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot


class RegistrationPage(BasePage):
    """Registration page of TunService website"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.locators = RegistrationLocators()

    @allure.step("Navigate to registration page with authentication")
    def navigate_to_registration(self):
        if not BASE_URL:
            raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")
        self.page.goto(f"{BASE_URL}/app/register", wait_until="domcontentloaded")
        # Wait for network idle to ensure all resources (images, CSS) are loaded - critical for pixel tests
        self.wait_for_network_idle()
        attach_screenshot(self.page, "Registration page loaded")

    @allure.step("Check registration page elements are visible")
    def check_registration_elements(self):
        # Check page title
        expect(self.page.locator(self.locators.page_title)).to_be_visible()

        # Check page container
        expect(self.page.locator(self.locators.page_container)).to_be_visible()

        # Check email field
        email_field = self.page.locator(self.locators.email_field)
        if email_field.count() > 0:
            expect(email_field.first).to_be_visible()

        # Check register button
        register_button = self.page.locator(self.locators.register_button)
        if register_button.count() > 0:
            expect(register_button.first).to_be_visible()

        attach_screenshot(self.page, "Registration elements verified")

    @allure.step("Check OTP form elements for email: {email} after registration")
    def check_otp_form_elements(self, email: str):
        # Check OTP title
        expect(self.page.locator(self.locators.otp_title)).to_be_visible()
        expect(self.page.locator(self.locators.otp_title).get_by_text("Введите код")).to_be_visible()

        # Check OTP inputs container
        expect(self.page.locator(self.locators.otp_inputs_container)).to_be_visible()

        # Check all OTP pin fields
        for pin_field in self.otp_pin_fields:
            pin_input = self.page.locator(pin_field).first
            expect(pin_input).to_be_visible()

        # Check send button
        send_btn = self.page.locator(self.locators.otp_send_button).first
        expect(send_btn).to_be_visible()
        expect(send_btn.get_by_text("ОТПРАВИТЬ")).to_be_visible()

        # Check resend button
        resend_btn = self.page.locator(self.locators.otp_resend_button).first
        expect(resend_btn).to_be_visible()

        # Check info block with email
        # Check that "Проверьте почту" text is visible
        expect(self.page.get_by_text("Проверьте почту", exact=False)).to_be_visible()

        # Check that email is visible in the <b> tag within info block
        email_element = self.page.locator(self.locators.otp_info_email)
        expect(email_element).to_be_visible()

        # Verify email text exactly matches the one we registered with
        email_text = email_element.text_content()
        assert email == email_text.strip(), f"Expected email '{email}' in info block, but got '{email_text}'"

        # Also check using get_by_text for email
        expect(self.page.get_by_text(email, exact=True)).to_be_visible()

        # Check info text
        expect(self.page.get_by_text("Вам выслано письмо с кодом подтверждения.", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Если письмо не приходит, проверьте папку Спам.", exact=True)).to_be_visible()

        attach_screenshot(self.page, "OTP form elements verified")
