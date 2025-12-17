import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.registration_locators import RegistrationLocators
from utils.playwright_helpers import scroll_to_make_visible


@allure.epic("Visual Regression")
@allure.feature("Registration Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestRegistrationPageVisualRegression:

    locators = RegistrationLocators()

    @allure.title("Registration form snapshot")
    @pytest.mark.pixel_test
    def test_registration_form(self, page, assert_snapshot_with_threshold):

        page.goto(f"{BASE_URL}/app/register/")
        page.wait_for_load_state("networkidle")

        with allure.step("Capture registration form"):
            form = page.locator(self.locators.page_container).first
            expect(form).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            scroll_to_make_visible(form)
            expect(form).to_be_visible(timeout=300)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(form, threshold=0.2)

    @allure.title("Invalid email error modal snapshot")
    @pytest.mark.pixel_test
    def test_invalid_email_error_modal(self, page, assert_snapshot_lenient):
        with allure.step("Navigate to registration page"):
            page.goto(f"{BASE_URL}/app/register/")
            page.wait_for_load_state("networkidle")

        with allure.step("Fill invalid email"):
            email_input = page.locator(self.locators.email_field).first
            expect(email_input).to_be_visible()
            email_input.fill("invalid-email")
            expect(email_input).to_be_visible(timeout=500)

        with allure.step("Click register button"):
            checkbox = page.get_by_role("checkbox").first
            expect(checkbox).to_be_visible()
            checkbox.check()
            expect(checkbox).to_be_checked(timeout=300)

            register_btn = page.get_by_role("button", name="зарегистрироваться").first
            expect(register_btn).to_be_visible(timeout=5000)
            register_btn.click()

        with allure.step("Capture error modal snapshot"):
            error_modal = page.get_by_role("alert").first
            expect(error_modal).to_be_visible(timeout=Timeouts.Toast.VISIBLE)
            expect(error_modal).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_lenient(error_modal, threshold=0.5, mask_elements=["[role='progressbar']"])
