"""
Login page class for TunService website
"""
import logging

import allure
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.login_locators import LoginLocators
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot
from utils.playwright_helpers import scroll_to_make_visible


class LoginPage(BasePage):
    """Login page of TunService website"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.locators = LoginLocators()

    @allure.step("Navigate to login page with authentication")
    def navigate_to_login(self):
        self.page.goto(f"{BASE_URL}/app/login", wait_until="domcontentloaded")
        # Wait for network idle to ensure all resources (images, CSS) are loaded - critical for pixel tests
        self.wait_for_network_idle()

        attach_screenshot(self.page, "Login page loaded")

    @allure.step("Check login page elements are visible")
    def check_login_elements(self):
        # Check page title
        expect(self.page.locator(self.locators.page_title)).to_be_visible()

        # Check page container
        expect(self.page.locator(self.locators.page_container)).to_be_visible()

        # Check username/email field
        username_field = self.page.locator(self.locators.username_field).first
        expect(username_field).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        # Check login button
        login_button = self.page.locator(self.locators.login_button).first
        expect(login_button).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        attach_screenshot(self.page, "Login page elements verified")

    @allure.step("Login with credentials: {username} / ******")
    def login_with_credentials(self, username: str, password: str):
        # Fill username field
        username_field = self.page.locator(self.locators.username_field).first
        expect(username_field).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        username_field.fill(username)

        # Fill password field
        password_field = self.page.locator(self.locators.password_field).first
        expect(password_field).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
        password_field.fill(password)

        # Click login button
        btn = self.page.locator(self.locators.login_button).first
        expect(btn).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
        expect(btn).to_be_enabled(timeout=Timeouts.BASE_ELEMENT_ENABLED)

        scroll_to_make_visible(btn)
        expect(btn).to_be_visible(timeout=500)

        attach_screenshot(self.page, "Before login button click")

        # Try normal click first, fallback to force click if needed
        try:
            btn.click(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        except Exception as e:
            # If normal click fails, try clicking the inner span or use force click
            logging.debug(f"Normal click failed, trying alternative click method: {e}")
            inner_span = btn.locator("span").first

            if inner_span.count() > 0:
                inner_span.click(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            else:
                btn.click(force=True, timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        self.wait_for_page_load()

        attach_screenshot(self.page, "After login attempt")

    @allure.step("Check presence of login error message")
    def check_login_error(self) -> bool:
        error_elements = self.page.locator(self.locators.error_message)
        has_error = error_elements.count() > 0 and error_elements.first.is_visible()

        if has_error:
            attach_screenshot(self.page, "Login error message visible")
        return has_error

    @allure.step("Get login error message text")
    def get_login_error_message(self) -> str:
        error_elements = self.page.locator(self.locators.error_message)

        if error_elements.count() > 0:
            message = error_elements.first.text_content()
            attach_screenshot(self.page, f"Error message: {message}")
            return message

        return ""
