import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts


@allure.epic("Visual Regression")
@allure.feature("Contacts Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestContactsPageVisualRegression:

    @allure.title("Contact info snapshot")
    @pytest.mark.pixel_test
    def test_contact_info(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/contacts")
        page.wait_for_load_state("networkidle")

        with allure.step("Capture contacts page"):
            # Capture main content area
            main_content = page.locator("main, .contact-info, .container").first
            expect(main_content).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(main_content).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(main_content.screenshot(), threshold=0.15)

