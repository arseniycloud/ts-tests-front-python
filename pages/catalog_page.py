import allure
from playwright.sync_api import Page

from config.auth_config import BASE_URL
from locators.catalog_locators import CatalogLocators
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot


class CatalogPage(BasePage):
    """Catalog page of TunService website"""

    def __init__(self, page: Page):
        super().__init__(page, CatalogLocators())
        self.page = page

    @allure.step("Navigate to catalog page with authentication")
    def navigate_to_catalog(self):
        if not BASE_URL:
            raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")

        self.navigate_to(f"{BASE_URL}/catalog")
        attach_screenshot(self.page, "Catalog page loaded")

    @allure.step("Check if catalog page elements are visible")
    def check_catalog_elements(self):
        self.check_page_elements([self.locators.page_title, self.locators.page_container, self.locators.catalog_panel])
        attach_screenshot(self.page, "Catalog elements verified")

    @allure.step("Search for item: {search_term} in catalog")
    def search_for_item(self, search_term: str):
        search_input = self.page.locator(self.locators.search_input)
        if search_input.count() > 0:
            search_input.first.fill(search_term)
            search_input.first.press("Enter")

            self.wait_for_page_load()
            attach_screenshot(self.page, "Search completed")

    @allure.step("Get catalog items count")
    def get_catalog_items_count(self) -> int:
        items = self.page.locator(self.locators.catalog_items)
        count = items.count()
        attach_screenshot(self.page, "Catalog items counted")
        return count

    @allure.step("Navigate to brand page: {brand_path} in catalog")
    def navigate_to_brand_page(self, brand_path: str = "car/bmw-mini"):
        if not BASE_URL:
            raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")
        self.navigate_to(f"{BASE_URL}/catalog/{brand_path}")
        attach_screenshot(self.page, "Brand page loaded")

    @allure.step("Navigate to engine page for brand path: {brand_path} in catalog")
    def navigate_to_engine_page(self, brand_path: str = "car/bmw-mini"):
        if not BASE_URL:
            raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")

        self.navigate_to(f"{BASE_URL}/catalog/{brand_path}")
        attach_screenshot(self.page, "Engine page loaded")

    @allure.step("Navigate to ECU page: {path}")
    def navigate_to_ecu_page(self, path: str = "car/bmw-mini/diesel"):
        """Navigate to ECU/block selection page"""
        if not BASE_URL:
            raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")

        self.navigate_to(f"{BASE_URL}/catalog/{path}")
        attach_screenshot(self.page, "ECU page loaded")

    @allure.step("Navigate to stock page: {path}")
    def navigate_to_stock_page(self, path: str = "car/bmw-mini/diesel/bosch-edc15"):
        """Navigate to stock list page"""
        if not BASE_URL:
            raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")

        self.navigate_to(f"{BASE_URL}/catalog/{path}")
        attach_screenshot(self.page, "Stock page loaded")

    @allure.step("Get stock items count on stock list page")
    def get_stock_items_count(self) -> int:
        stock_items = self.page.locator(self.locators.stock_items)
        count = stock_items.count()

        attach_screenshot(self.page, "Stock items counted")
        return count

    @allure.step("Get text content of stock item by index: {index}")
    def get_stock_item_text(self, index: int = 0) -> str:
        stock_items = self.page.locator(self.locators.stock_items)
        count = stock_items.count()

        if count <= index:
            attach_screenshot(self.page, f"Stock item missing at index {index}")
            raise IndexError(f"Stock item index {index} is out of bounds. Available count: {count}")

        item = stock_items.nth(index)
        span = item.locator("span").first

        if span.count() == 0:
            attach_screenshot(self.page, f"No span found for stock item at index {index}")
            raise RuntimeError(f"Expected span element not found for stock item at index {index}")

        text = span.text_content()
        if text is None or not text.strip():
            attach_screenshot(self.page, f"Stock item text is empty at index {index}")
            raise ValueError(f"Stock item text content is None or empty at index {index}")

        attach_screenshot(self.page, "Stock item text retrieved")
        return text.strip()

    @allure.step("Click stock item by index: {index}")
    def click_stock_item(self, index: int = 0):
        stock_items = self.page.locator(self.locators.stock_items)
        count = stock_items.count()

        if index >= count:
            attach_screenshot(self.page, "Stock item index out of bounds")
            raise IndexError(f"Stock item index {index} is out of bounds. Available count: {count}")

        item = stock_items.nth(index)
        item.click()

        self.wait_for_page_load()
        attach_screenshot(self.page, "Stock item clicked")
