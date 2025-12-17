import logging

import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.profile_locators import ProfileLocators
from pages.profile_page import ProfilePage
from utils.playwright_helpers import scroll_to_make_visible


@allure.epic("Visual Regression")
@allure.feature("Profile Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestProfilePageVisualRegression:

    @allure.title("Profile block snapshot")
    @pytest.mark.pixel_test
    def test_profile_block(self, authenticated_user_new, assert_snapshot_lenient):
        page = authenticated_user_new
        profile_page = ProfilePage(page)

        with allure.step("Navigate to profile page"):
            profile_page.navigate_to_profile()
            page.wait_for_timeout(Timeouts.ShortWaits.VERY_SHORT_PAUSE)

        with allure.step("Capture profile block"):
            profile_container = page.locator(ProfileLocators.profile_container).first
            expect(profile_container).to_be_visible(timeout=5000)
            scroll_to_make_visible(profile_container)
            page.wait_for_timeout(1000)
            page.wait_for_load_state("networkidle", timeout=3000)

            profile_blocks = page.locator(ProfileLocators.profile_blocks)
            expect(profile_blocks.first).to_be_visible(timeout=5000)
            first_block = profile_blocks.first
            scroll_to_make_visible(first_block)
            page.wait_for_timeout(1000)
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(1000)
            assert_snapshot_lenient(first_block, threshold=0.8, mask_elements=[ProfileLocators.email_value_container])

    @allure.title("Discount section snapshot")
    @pytest.mark.pixel_test
    def test_discount_section(self, authenticated_user_new, assert_snapshot_with_threshold):
        page = authenticated_user_new

        with allure.step("Navigate to profile page"):
            profile_url = f"{BASE_URL}/app/profile"
            page.goto(profile_url, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)
            except Exception as e:
                logging.warning(f"Failed to wait for networkidle, falling back to load state: {e}")
                page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)

        with allure.step("Find and capture discount section"):
            # Wait for page to be fully loaded
            page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

            # Check that profile blocks exist in DOM first
            profile_blocks = page.locator(ProfileLocators.profile_blocks)
            expect(profile_blocks.nth(1)).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            # Discount block is the 2nd block (index 1) - after profile block
            discount_block = profile_blocks.nth(1)
            expect(discount_block).to_be_visible(timeout=5000)

            # Verify discount title exists
            discount_title = discount_block.locator(ProfileLocators.profile_title)
            expect(discount_title).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            scroll_to_make_visible(discount_block)
            expect(discount_block).to_be_visible(timeout=500)
            page.wait_for_load_state("networkidle", timeout=30000)
            expect(discount_block).to_be_visible(timeout=1000)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(discount_block, threshold=0.2)

    @allure.title("Cashback section snapshot")
    @pytest.mark.pixel_test
    def test_cashback_section(self, authenticated_user_new, assert_snapshot_with_threshold):
        page = authenticated_user_new

        with allure.step("Navigate to profile page"):
            profile_url = f"{BASE_URL}/app/profile"
            page.goto(profile_url, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)
            except Exception as e:
                logging.warning(f"Failed to wait for networkidle, falling back to load state: {e}")
                page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)

        with allure.step("Find and capture cashback section"):
            # Wait for page to be fully loaded
            page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

            # Check that profile blocks exist in DOM first
            profile_blocks = page.locator(ProfileLocators.profile_blocks)
            expect(profile_blocks.nth(2)).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            # Cashback block is 3rd block (index 2)
            cashback_block = profile_blocks.nth(2)
            expect(cashback_block).to_be_visible(timeout=5000)

            # Verify cashback title exists
            cashback_title = cashback_block.locator(ProfileLocators.profile_title)
            expect(cashback_title).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            scroll_to_make_visible(cashback_block)
            expect(cashback_block).to_be_visible(timeout=500)
            page.wait_for_load_state("networkidle", timeout=30000)
            expect(cashback_block).to_be_visible(timeout=1000)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(cashback_block, threshold=0.2)
