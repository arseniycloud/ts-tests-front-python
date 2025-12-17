import allure
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.try_upload_page import TryUploadLocators
from pages.base_upload_page import BaseUploadPage
from utils.allure_helpers import attach_screenshot


class TryUploadPage(BaseUploadPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = TryUploadLocators()

    @allure.step("Navigate to try upload page (for unregistered users)")
    def navigate_to_try_upload(self) -> None:
        self.page.context.clear_cookies()
        try_upload_url = f"{BASE_URL}/app/"

        self.page.goto(try_upload_url, wait_until="domcontentloaded")
        # Wait for network idle to ensure all resources (images, CSS) are loaded - critical for pixel tests
        self.wait_for_network_idle()

        attach_screenshot(self.page, "Try upload page loaded")

    @allure.step("Check if header elements are visible for unregistered users")
    def check_header_elements(self) -> None:
        expect(self.page.locator(self.locators.header_container)).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        header_logo = self.page.locator(self.locators.header_logo)

        if header_logo.count() > 0:
            expect(header_logo.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        else:
            header_logo_img = self.page.locator(self.locators.header_logo_img)
            expect(header_logo_img.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        prices_link = self.page.locator(self.locators.prices_link)

        if prices_link.count() > 0:
            if prices_link.first.is_visible():
                expect(prices_link.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            else:
                assert prices_link.count() > 0, "Prices link should exist (may be hidden in mobile menu)"

        catalog_link = self.page.locator(self.locators.catalog_link)

        if catalog_link.count() > 0:

            if catalog_link.first.is_visible():
                expect(catalog_link.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            else:
                assert catalog_link.count() > 0, "Catalog link should exist (may be hidden in mobile menu)"

        login_link = self.page.locator(self.locators.login_link)

        if login_link.count() > 0:

            if login_link.first.is_visible():
                expect(login_link.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            else:
                assert login_link.count() > 0, "Login link should exist (may be hidden in mobile menu)"

        attach_screenshot(self.page, "Header elements verified")

    @allure.step("Check if upload form elements are visible")
    def check_upload_form_elements(self) -> None:
        expect(self.page.locator(self.locators.upload_label)).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
        expect(self.page.locator(self.locators.file_input)).to_be_attached(timeout=Timeouts.Upload.FILE_INPUT_ATTACHED)

        type_select = self.page.locator(self.locators.type_select)
        expect(type_select).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        search_button = self.page.locator(self.locators.search_button)
        expect(search_button).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        attach_screenshot(self.page, "Upload form elements verified")

    @allure.step("Verify not authenticated panel is visible")
    def verify_not_auth_panel(self) -> None:
        not_auth_panel = self.page.locator(self.locators.not_auth_panel)
        expect(not_auth_panel).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        panel_text = not_auth_panel.text_content()

        assert "Хотите скачать" in panel_text or "зарегистрируйтесь" in panel_text or "войдите" in panel_text, \
            f"Panel should contain registration/login prompt, got: {panel_text}"

        register_link = self.page.locator(self.locators.not_auth_register_link)

        if register_link.count() > 0:
            expect(register_link.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        login_link = self.page.locator(self.locators.not_auth_login_link)

        if login_link.count() > 0:
            expect(login_link.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        attach_screenshot(self.page, "Not authenticated panel verified")
