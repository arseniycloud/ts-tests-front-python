import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.login_locators import LoginLocators
from utils.playwright_helpers import scroll_to_make_visible


@allure.epic("Visual Regression")
@allure.feature("Login Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestLoginPageVisualRegression:

    # Shared locators instance for all tests in this class
    locators = LoginLocators()

    @allure.title("Login form snapshot")
    @pytest.mark.pixel_test
    def test_login_form(self, page, assert_snapshot_with_threshold):
        with allure.step("Navigate to login page"):
            page.goto(f"{BASE_URL}/app/login")
            page.wait_for_load_state("networkidle")

        with allure.step("Verify login form elements are visible"):
            # Check page container
            page_container = page.locator(self.locators.page_container)
            expect(page_container).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            # Check username/email field
            username_field = page.locator(self.locators.username_field).first
            expect(username_field).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            # Check login button
            login_button = page.locator(self.locators.login_button).first
            expect(login_button).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        with allure.step("Capture login form snapshot"):
            # Use page container as form container, similar to functional tests approach
            # Form elements are already verified above
            form_container = page.locator(self.locators.page_container).first
            expect(form_container).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            scroll_to_make_visible(form_container)
            expect(form_container).to_be_visible(timeout=300)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(form_container, threshold=0.2)

    @allure.title("OTP modal from login snapshot")
    @pytest.mark.pixel_test
    def test_otp_modal_login(self, page, assert_snapshot_with_threshold):
        with allure.step("Navigate to login page"):
            page.goto(f"{BASE_URL}/app/login")
            page.wait_for_load_state("networkidle")

        with allure.step("Fill email and trigger OTP modal"):
            email_input = page.locator(self.locators.username_field).first
            expect(email_input).to_be_visible()
            email_input.fill("test@test.com")
            expect(email_input).to_be_visible(timeout=300)

            login_btn = page.locator(self.locators.login_button).first
            expect(login_btn).to_be_visible()
            login_btn.click()
            page.wait_for_load_state("networkidle")
            otp_pin_1 = page.locator(self.locators.otp_pin_1).first
            expect(otp_pin_1).to_be_visible(timeout=Timeouts.Registration.OTP_FIELDS_VISIBLE)

        with allure.step("Wait for OTP form to appear"):
            expect(otp_pin_1).to_be_visible(timeout=Timeouts.Registration.OTP_FIELDS_VISIBLE)
            expect(otp_pin_1).to_be_visible(timeout=500)

        with allure.step("Capture OTP form snapshot"):
            # Use page container as form container, similar to test_login_form approach
            # OTP pin field is already verified above
            otp_form_container = page.locator(self.locators.page_container).first
            expect(otp_form_container).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            scroll_to_make_visible(otp_form_container)
            expect(otp_form_container).to_be_visible(timeout=300)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(otp_form_container, threshold=0.2, mask_elements=["[role='progressbar']"])

    @allure.title("Invalid OTP code error toast snapshot")
    @pytest.mark.pixel_test
    def test_invalid_otp_toast(self, page, assert_snapshot_lenient):
        with allure.step("Navigate to login page"):
            page.goto(f"{BASE_URL}/app/login")
            page.wait_for_load_state("networkidle")

        with allure.step("Fill email and trigger OTP"):
            email_input = page.locator(self.locators.username_field).first
            expect(email_input).to_be_visible()
            email_input.fill("test@test.com")
            expect(email_input).to_be_visible(timeout=300)

            login_btn = page.locator(self.locators.login_button).first
            expect(login_btn).to_be_visible()
            login_btn.click()
            page.wait_for_load_state("networkidle")

        with allure.step("Enter invalid OTP code"):
            for i in range(1, 6):
                pin = page.locator(f"[data-test-id='pin-{i}']").first
                expect(pin).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
                pin.fill(str(i))
                expect(pin).to_be_visible(timeout=100)

            otp_send = page.locator(self.locators.otp_send_button).first
            expect(otp_send).to_be_visible()
            otp_send.click()
            error_toast = page.get_by_role("alert").filter(has_text="Ошибка ввода кода авторизации!").first
            expect(error_toast).to_be_visible(timeout=Timeouts.Toast.VISIBLE)

        with allure.step("Capture invalid OTP error toast snapshot"):
            expect(error_toast).to_be_visible(timeout=5000)
            expect(error_toast).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_lenient(error_toast, threshold=0.3, mask_elements=["[role='progressbar']"])
