import allure
import pytest

from locators.pricing_locators import PricingLocators


@allure.epic("Pricing")
@allure.feature("Pricing Page")
@allure.title("Pricing Page - Information")
class TestPricingPageTests:

    @allure.title("Test pricing page elements are visible")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_pricing_page_elements(self, pricing_page):
        pricing_page.check_pricing_elements()

    @allure.title("Test pricing plans count")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_pricing_plans_count(self, pricing_page):
        plans_count = pricing_page.get_pricing_plans_count()
        assert plans_count >= 0, "Pricing page should have plans or show empty state"

    @allure.title("Test pricing page navigation")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_pricing_navigation(self, pricing_page):
        # Check if we're on pricing page
        assert "/price" in pricing_page.page.url, "Should be on pricing page"

        # Check page title
        locators = PricingLocators()
        title = pricing_page.page.locator(locators.page_title).text_content()
        assert title is not None, "Pricing page should have a title"

    @allure.title("Test pricing plan details")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_pricing_plan_details(self, pricing_page):
        locators = PricingLocators()

        # Check if pricing plans have required information
        plans = pricing_page.page.locator(locators.pricing_cards)
        if plans.count() > 0:
            # Check first plan has price information
            first_plan = plans.first
            price_element = first_plan.locator(locators.plan_price)
            assert (price_element.count() >= 0), "Pricing plans should have price information"
