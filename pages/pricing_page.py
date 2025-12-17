import allure
from playwright.sync_api import Page

from config.auth_config import BASE_URL
from locators.pricing_locators import PricingLocators
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot


class PricingPage(BasePage):
    """Pricing page of TunService website"""

    def __init__(self, page: Page):
        super().__init__(page, PricingLocators())
        self.page = page

    @allure.step("Navigate to pricing page with authentication")
    def navigate_to_pricing(self):
        if not BASE_URL:
            raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")

        self.navigate_to(f"{BASE_URL}/price")
        attach_screenshot(self.page, "Pricing page loaded")

    @allure.step("Check that pricing page elements are visible")
    def check_pricing_elements(self):
        selectors = [self.locators.page_title]
        pricing_cards = self.page.locator(self.locators.pricing_cards)

        if pricing_cards.count() > 0:
            selectors.append(self.locators.pricing_cards)

        self.check_page_elements(selectors)
        attach_screenshot(self.page, "Pricing elements verified")

    @allure.step("Get list of available pricing plans")
    def get_pricing_plans(self) -> list:
        plans = []
        pricing_cards = self.page.locator(self.locators.pricing_cards)

        for i in range(pricing_cards.count()):
            card = pricing_cards.nth(i)
            plan_name = card.locator(self.locators.plan_name).text_content()
            plan_price = card.locator(self.locators.plan_price).text_content()
            plans.append({
                "name": plan_name,
                "price": plan_price
            })

        attach_screenshot(self.page, "Pricing plans retrieved")
        return plans

    @allure.step("Select pricing plan: {plan_name}")
    def select_pricing_plan(self, plan_name: str):
        plan_button = self.page.locator(f"button:has-text('{plan_name}'), .plan-card:has-text('{plan_name}') button")

        if plan_button.count() > 0:
            plan_button.first.click()
            self.wait_for_page_load()
            attach_screenshot(self.page, "Pricing plan selected")

    @allure.step("Get count of pricing plans on pricing page")
    def get_pricing_plans_count(self) -> int:
        plans = self.page.locator(self.locators.pricing_cards)
        count = plans.count()
        attach_screenshot(self.page, "Pricing plans counted")
        return count
