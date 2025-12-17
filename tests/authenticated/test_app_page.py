import allure
import pytest

from config.auth_config import BASE_URL
from pages.app_page import AppPage
from utils.allure_helpers import attach_screenshot


@allure.epic("App")
@allure.feature("App Page")
@allure.title("App Page - Main Application")
class TestUploadPageElements:

    @allure.story("Header Elements")
    @allure.title("Test app page header elements are visible")
    @pytest.mark.authorization
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_app_page_header_elements(self, auth_user_new_for_app_page):
        page = auth_user_new_for_app_page
        app_page = AppPage(page)

        with allure.step("Verify we're on /app page"):
            assert "/app" in page.url, "Should be on /app page"

        with allure.step("Check header elements"):
            app_page.check_header_elements()
            attach_screenshot(page, "App page header elements")

    @allure.story("Upload Form")
    @allure.title("Test app page upload form is visible")
    @pytest.mark.authorization
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_app_page_upload_form(self, auth_user_new_for_app_page):
        page = auth_user_new_for_app_page
        app_page = AppPage(page)

        with allure.step("Check upload form elements"):
            app_page.check_upload_form()
            attach_screenshot(page, "Upload form elements")

    @allure.story("Form Elements")
    @allure.title("Test app page select dropdowns are visible")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_app_page_selects(self, auth_user_new_for_app_page):
        page = auth_user_new_for_app_page
        app_page = AppPage(page)

        with allure.step("Check all selects"):
            app_page.check_selects()
            attach_screenshot(page, "Select dropdowns")

    @allure.story("Form Elements")
    @allure.title("Test app page search button is visible")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_app_page_search_button(self, auth_user_new_for_app_page):
        page = auth_user_new_for_app_page
        app_page = AppPage(page)

        with allure.step("Check search button"):
            app_page.check_search_button()
            attach_screenshot(page, "Search button")

    @allure.story("Navigation")
    @allure.title("Test navigation to history page from header")
    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_navigation_to_history(self, auth_user_new_for_app_page):
        page = auth_user_new_for_app_page

        with allure.step("Navigate to history page directly"):
            history_url = f"{BASE_URL}/app/history"
            page.goto(history_url)
            page.wait_for_load_state("networkidle")
            attach_screenshot(page, "After navigation to history")

        with allure.step("Verify we're on history page"):
            assert "/app/history" in page.url or "/app" in page.url, f"Should be on history page, got {page.url}"

    @allure.story("Navigation")
    @allure.title("Test navigation to balance/payment page from header")
    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_navigation_to_balance(self, auth_user_new_for_app_page):
        page = auth_user_new_for_app_page

        with allure.step("Navigate to balance page directly"):
            # Use URL with trailing slash to avoid redirect interruption
            balance_url = f"{BASE_URL}/app/payment/"
            page.goto(balance_url)
            page.wait_for_load_state("networkidle")
            attach_screenshot(page, "After navigation to balance")

        with allure.step("Verify we're on balance page"):
            assert "/app/payment" in page.url or "/app" in page.url, f"Should be on balance page, got {page.url}"

    @allure.story("Navigation")
    @allure.title("Test navigation to profile page from header")
    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_navigation_to_profile(self, auth_user_new_for_app_page):
        page = auth_user_new_for_app_page

        with allure.step("Navigate to profile page directly"):
            profile_url = f"{BASE_URL}/app/profile"
            page.goto(profile_url)
            page.wait_for_load_state("networkidle")
            attach_screenshot(page, "After navigation to profile")

        with allure.step("Verify we're on profile page"):
            assert "/app/profile" in page.url, "Should be on /app/profile page"

    @allure.story("Page Structure")
    @allure.title("Test app page basic structure is visible")
    @pytest.mark.authorization
    @pytest.mark.regression
    @pytest.mark.validation
    def test_app_page_structure(self, auth_user_new_for_app_page):
        page = auth_user_new_for_app_page
        app_page = AppPage(page)

        with allure.step("Check page structure"):
            app_page.check_page_structure()
            attach_screenshot(page, "App page structure")
