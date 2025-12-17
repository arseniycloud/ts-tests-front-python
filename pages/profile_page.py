import logging

import allure
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.profile_locators import ProfileLocators
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot


class ProfilePage(BasePage):
    """Profile page of TunService website"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.locators = ProfileLocators()

    @allure.step("Navigate to profile page")
    def navigate_to_profile(self):
        profile_url = f"{BASE_URL}/app/profile"
        current_url = self.page.url

        if "/app/profile" in current_url:
            try:
                self.wait_for_page_load()
                self.page.locator(self.locators.profile_container).wait_for(state="visible", timeout=Timeouts.Profile.ELEMENT_VISIBLE)

            except Exception as e:
                logging.debug(f"Failed to wait for profile container on current page (continuing): {e}")
            return

        try:
            self.page.goto(profile_url, wait_until="domcontentloaded", timeout=Timeouts.BASE_PAGE_LOAD)
            # Wait for network idle to ensure profile data API requests complete

            try:
                self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

            except Exception as e:
                logging.warning(f"Failed to wait for networkidle when navigating to profile, falling back to load state: {e}")
                self.page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)
            self.page.locator(self.locators.profile_container).wait_for(state="visible", timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        except Exception as e:

            if "interrupted" in str(e).lower() or "navigation" in str(e).lower():
                expect(self.page.locator("body")).to_be_visible(timeout=Timeouts.ShortWaits.SHORT_PAUSE)
                self.page.goto(profile_url, wait_until="domcontentloaded", timeout=Timeouts.BASE_PAGE_LOAD)
                self.page.locator(self.locators.profile_container).wait_for(state="visible", timeout=Timeouts.Profile.ELEMENT_VISIBLE)

            else:
                raise

        attach_screenshot(self.page, "Profile page loaded")

    @allure.step("Check profile page elements are visible")
    def check_profile_elements(self):
        expect(self.page.locator(self.locators.page_container)).to_be_visible()
        expect(self.page.locator(self.locators.page_body)).to_be_visible()

        # Wait for profile container with longer timeout as it may load asynchronously
        expect(self.page.locator(self.locators.profile_container)).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)
        attach_screenshot(self.page, "Profile elements verified")

    @allure.step("Check 'Your profile' block visibility")
    def check_profile_block(self):
        # Wait for page to be fully loaded
        self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        # Check that profile container exists in DOM first
        profile_container = self.page.locator(self.locators.profile_container)
        assert profile_container.count() > 0, "Profile container should exist in DOM"

        # Wait for profile container to be visible
        expect(profile_container).to_be_visible(timeout=Timeouts.Profile.PROFILE_BLOCKS_LOAD)

        # Check that profile blocks exist in DOM
        profile_blocks = self.page.locator(self.locators.profile_blocks)
        assert profile_blocks.count() > 0, "Profile blocks should exist in DOM"

        # Wait for first profile block to be visible
        expect(profile_blocks.first).to_be_visible(timeout=Timeouts.Profile.PROFILE_BLOCKS_LOAD)

        # Verify profile title exists and is visible
        profile_title = self.page.locator(self.locators.profile_title).first
        assert profile_title.count() > 0, "Profile title should exist in DOM"
        expect(profile_title).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        # Verify profile subtitle exists and is visible
        profile_subtitle = self.page.locator(self.locators.profile_subtitle).first
        assert profile_subtitle.count() > 0, "Profile subtitle should exist in DOM"
        expect(profile_subtitle).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        attach_screenshot(self.page, "Profile block verified")

    @allure.step("Get email from profile")
    def get_email(self) -> str:
        profile_blocks = self.page.locator(self.locators.profile_blocks)
        profile_block = profile_blocks.first

        profile_data = profile_block.locator(self.locators.profile_data_in_wrapper).first
        expect(profile_data).to_be_visible()

        email_value = profile_data.locator(self.locators.profile_data_value)
        email = email_value.text_content()
        email = email.strip() if email else ""
        attach_screenshot(self.page, "Email retrieved from profile")
        return email

    @allure.step("Check that email is displayed in profile")
    def check_email_displayed(self):
        email_value = self.get_email()
        assert "@test.com" in email_value, f"Expected email with @test.com, got {email_value}"
        attach_screenshot(self.page, "Email display verified")

    @allure.step("Check discount block visibility")
    def check_discount_block(self):
        # Wait for page to be fully loaded
        self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        # Check that profile blocks exist in DOM first
        profile_blocks = self.page.locator(self.locators.profile_blocks)
        assert profile_blocks.count() >= 3, f"At least 3 profile blocks should exist in DOM, got {profile_blocks.count()}"

        # Discount block is the 2nd block (index 1) - after profile block
        discount_block = profile_blocks.nth(1)
        expect(discount_block).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        discount_title = discount_block.locator(self.locators.profile_title)
        expect(discount_title).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        discount_data = discount_block.locator(self.locators.profile_data_in_wrapper).first
        expect(discount_data).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        attach_screenshot(self.page, "Discount block verified")

    @allure.step("Get discount percentage value")
    def get_discount_percentage(self) -> str:
        # Wait for page to be fully loaded
        self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        # Check that profile blocks exist in DOM first
        profile_blocks = self.page.locator(self.locators.profile_blocks)
        assert profile_blocks.count() >= 3, f"At least 3 profile blocks should exist in DOM, got {profile_blocks.count()}"

        # Discount block is the 2nd block (index 1)
        discount_block = profile_blocks.nth(1)
        expect(discount_block).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        discount_data = discount_block.locator(self.locators.profile_data_in_wrapper).first
        expect(discount_data).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        discount_value = discount_data.locator(self.locators.profile_data_value)
        discount = discount_value.text_content().strip()

        attach_screenshot(self.page, "Discount percentage retrieved")
        return discount

    @allure.step("Check that cashback block visibility")
    def check_cashback_block(self):
        # Wait for page to be fully loaded
        self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        # Check that profile blocks exist in DOM first
        profile_blocks = self.page.locator(self.locators.profile_blocks)
        assert profile_blocks.count() >= 3, f"At least 3 profile blocks should exist in DOM, got {profile_blocks.count()}"

        # Cashback block is 3rd block (index 2)
        cashback_block = profile_blocks.nth(2)
        expect(cashback_block).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        cashback_title = cashback_block.locator(self.locators.profile_title)
        expect(cashback_title).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        cashback_data = cashback_block.locator(self.locators.profile_data_in_wrapper).first
        expect(cashback_data).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        attach_screenshot(self.page, "Cashback block verified")

    @allure.step("Get cashback percentage value")
    def get_cashback_percentage(self) -> str:
        # Wait for page to be fully loaded
        self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        # Check that profile blocks exist in DOM first
        profile_blocks = self.page.locator(self.locators.profile_blocks)
        assert profile_blocks.count() >= 3, f"At least 3 profile blocks should exist in DOM, got {profile_blocks.count()}"

        # Cashback block is 3rd block (index 2)
        cashback_block = profile_blocks.nth(2)
        expect(cashback_block).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        cashback_data = cashback_block.locator(self.locators.profile_data_in_wrapper).first
        expect(cashback_data).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        cashback_value = cashback_data.locator(self.locators.profile_data_value)
        cashback_text = cashback_value.text_content()
        cashback = cashback_text.strip() if cashback_text else ""

        attach_screenshot(self.page, "Cashback percentage retrieved")
        return cashback

    @allure.step("Get cashback accumulated value")
    def get_cashback_accumulated(self) -> str:
        # Wait for page to be fully loaded
        self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        # Check that profile blocks exist in DOM first
        profile_blocks = self.page.locator(self.locators.profile_blocks)
        assert profile_blocks.count() >= 3, "At least 3 profile blocks should exist in DOM"

        # Cashback block is 3rd block (index 2)
        cashback_block = profile_blocks.nth(2)
        expect(cashback_block).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        # Use cashback_accumulated_value locator which is more reliable
        cashback_value = cashback_block.locator(self.locators.cashback_accumulated_value)
        expect(cashback_value).to_be_visible(timeout=Timeouts.Profile.ELEMENT_VISIBLE)

        cashback = cashback_value.text_content().strip()
        attach_screenshot(self.page, "Cashback accumulated retrieved")
        return cashback
