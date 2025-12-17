import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts


@allure.epic("Visual Regression")
@allure.feature("Pricing Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestPricingPageVisualRegression:

    @allure.title("Pricing plans snapshot")
    @pytest.mark.pixel_test
    def test_pricing_plans(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/price")
        page.wait_for_load_state("networkidle")

        with allure.step("Capture pricing plans"):
            main_content = page.locator("main").first
            expect(main_content).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(main_content).to_be_visible(timeout=1000)
            page.wait_for_load_state("networkidle", timeout=30000)
            expect(main_content).to_be_visible(timeout=1000)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(main_content, threshold=0.15)

