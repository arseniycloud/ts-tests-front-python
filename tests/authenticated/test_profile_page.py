"""
Tests for Profile page - authenticated users
"""

import allure
import pytest

from config.auth_config import BASE_URL
from pages.profile_page import ProfilePage
from utils.allure_helpers import attach_screenshot


@allure.epic("Profile")
@allure.feature("Profile Page")
@allure.story("Navigation")
class TestProfileNavigation:

    @allure.title("Test navigation to profile page")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_navigation_to_profile(self, authenticated_user_new):
        page = authenticated_user_new

        with allure.step("Navigate to profile page directly"):
            profile_url = f"{BASE_URL}/app/profile"
            page.goto(profile_url)
            page.wait_for_load_state("networkidle")
        assert "/app/profile" in page.url, "Should be on /app/profile page"


@allure.epic("Profile")
@allure.feature("Profile Page")
@allure.story("Page Elements")
class TestProfileElements:

    @allure.title("Test profile page elements, profile block and email are visible")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_profile_page_elements_and_profile_block(self, authenticated_user_new):
        page = authenticated_user_new
        profile_page = ProfilePage(page)

        with allure.step("Navigate to profile page directly"):
            profile_url = f"{BASE_URL}/app/profile"
            page.goto(profile_url)

            page.wait_for_load_state("networkidle")
            attach_screenshot(page, "Profile page loaded")

        with allure.step("Check profile page elements"):
            profile_page.check_profile_elements()
            attach_screenshot(page, "Profile page elements")

        with allure.step("Check profile block"):
            profile_page.check_profile_block()
            attach_screenshot(page, "Profile block")

        with allure.step("Check email is displayed"):
            profile_page.check_email_displayed()
            attach_screenshot(page, "Email displayed")


@allure.epic("Profile")
@allure.feature("Profile Page")
@allure.story("Discount and Cashback")
class TestProfileDiscountCashback:

    @allure.title("Test discount block is visible and discount percentage is displayed")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_discount_block_and_percentage(self, authenticated_user_new):
        page = authenticated_user_new
        profile_page = ProfilePage(page)

        with allure.step("Navigate to profile page directly"):
            profile_url = f"{BASE_URL}/app/profile"
            page.goto(profile_url)

            page.wait_for_load_state("networkidle")

        with allure.step("Check discount block"):
            profile_page.check_discount_block()
            attach_screenshot(page, "Discount block")

        with allure.step("Check discount percentage"):
            discount = profile_page.get_discount_percentage()
            attach_screenshot(page, f"Discount percentage: {discount}")
            assert "%" in discount, f"Expected discount with %, got {discount}"

        with allure.step("Check cashback block"):
            profile_page.check_cashback_block()
            attach_screenshot(page, "Cashback block")

        with allure.step("Check cashback percentage"):
            cashback = profile_page.get_cashback_percentage()
            attach_screenshot(page, f"Cashback percentage: {cashback}")
            assert "%" in cashback, f"Expected cashback with %, got {cashback}"

        with allure.step("Check cashback accumulated"):
            accumulated = profile_page.get_cashback_accumulated()
            attach_screenshot(page, f"Cashback accumulated: {accumulated}")
            assert "₽" in accumulated, f"Expected cashback accumulated with ₽, got {accumulated}"
