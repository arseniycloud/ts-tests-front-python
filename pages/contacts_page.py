import allure
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL
from locators.contacts_locators import ContactsLocators
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot


class ContactsPage(BasePage):
    """Contacts page of TunService website"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.locators = ContactsLocators()

    @allure.step("Navigate to contacts page with authentication")
    def navigate_to_contacts(self):
        if not BASE_URL:
            raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")

        self.page.goto(f"{BASE_URL}/contacts", wait_until="domcontentloaded")
        # Wait for network idle to ensure all resources (images, CSS) are loaded - critical for pixel tests
        self.wait_for_network_idle()

        attach_screenshot(self.page, "Contacts page loaded")

    @allure.step("Check if contacts page elements are visible")
    def check_contacts_elements(self):
        expect(self.page.locator(self.locators.page_title)).to_be_visible()

        contact_info = self.page.locator(self.locators.contact_info)
        if contact_info.count() > 0:
            expect(contact_info.first).to_be_visible()

        attach_screenshot(self.page, "Contacts elements verified")

    @allure.step("Get contact email from page")
    def get_contact_email(self) -> str:
        email_links = self.page.locator(self.locators.email_link)
        if email_links.count() > 0:
            email = email_links.first.get_attribute("href").replace("mailto:", "")
            attach_screenshot(self.page, "Contact email retrieved")
            return email
        attach_screenshot(self.page, "Contact email retrieved")
        return ""

    @allure.step("Get contact phone from page")
    def get_contact_phone(self) -> str:
        phone_links = self.page.locator(self.locators.phone_link)
        if phone_links.count() > 0:
            return phone_links.first.get_attribute("href").replace("tel:", "")

        phone_text = self.page.locator(self.locators.phone_text)

        if phone_text.count() > 0:
            phone = phone_text.first.text_content()
            attach_screenshot(self.page, "Contact phone retrieved")
            return phone

        attach_screenshot(self.page, "Contact phone retrieved")
        return ""

    @allure.step("Check social media links are visible and have correct href attributes")
    def check_social_links(self) -> dict:
        social_links = {}

        youtube_link = self.page.locator(self.locators.youtube_link)
        if youtube_link.count() > 0:
            social_links['youtube'] = youtube_link.first.get_attribute("href")

        vk_link = self.page.locator(self.locators.vk_link)
        if vk_link.count() > 0:
            social_links['vk'] = vk_link.first.get_attribute("href")

        attach_screenshot(self.page, "Social links verified")
        return social_links
