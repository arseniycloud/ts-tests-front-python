import allure
import pytest
from playwright.sync_api import Route, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.app_locators import AppLocators
from pages.history_page import HistoryPage
from tests.authenticated.helpers.history_helpers import (
    HISTORY_API_ENDPOINT,
    handle_history_route,
    load_mock_data,
)


@allure.epic("Visual Regression")
@allure.feature("History Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestHistoryPageVisualRegression:

    @allure.title("History page snapshot")
    @pytest.mark.pixel_test
    def test_history_page(self, authenticated_user_with_balance, assert_snapshot_lenient):
        page = authenticated_user_with_balance

        with allure.step("Navigate to history page"):
            history_url = f"{BASE_URL}/app/history"
            page.goto(history_url)
            page.wait_for_load_state("networkidle")

        with allure.step("Verify history page elements"):
            history_page = HistoryPage(page)
            # Wait for page to be fully loaded before checking elements
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(1000)
            history_page.check_history_elements()

        with allure.step("Capture history page snapshot"):
            # Guarantee full page load - wait for page to be ready
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(2000)
            # Try to wait for table, but don't fail if it's not present (empty history)
            history_table = page.locator(history_page.locators.history_table)
            if history_table.count() > 0:
                expect(history_table).to_be_visible(timeout=5000)
            # Mask header_container to avoid dynamic content differences
            assert_snapshot_lenient(page, threshold=1.0, mask_elements=[AppLocators.header_container])

    @allure.title("History pagination with mocked API snapshot")
    @pytest.mark.pixel_test
    def test_history_pagination_with_mock_pixel(self, authenticated_user_new, assert_snapshot_lenient):
        """Pixel version of test_history_pagination_with_mock - captures first page after loading with mocks"""
        page = authenticated_user_new

        with allure.step("Setup mock API route handler"):
            mock_data = load_mock_data()
            limit = 30

            def route_handler(route: Route):
                handle_history_route(route, mock_data=mock_data, limit=limit)

            page.route(f"**{HISTORY_API_ENDPOINT}**", route_handler)

        try:
            with allure.step("Navigate to history page directly"):
                history_url = f"{BASE_URL}/app/history"
                page.goto(history_url)
                page.wait_for_load_state("domcontentloaded")
                history_page = HistoryPage(page)
                expect(page.locator(history_page.locators.history_table)).to_be_visible(
                    timeout=Timeouts.History.HISTORY_TABLE_VISIBLE
                )

            with allure.step("Wait for history data to load"):
                history_rows_locator = page.locator("tbody tr[data-test-id='history-row']")
                expect(history_rows_locator.first).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)
                page.wait_for_timeout(500)

            with allure.step("Capture first page of history snapshot"):
                history_page.check_pagination_visible()
                # Guarantee full page load - wait for table to be stable
                expect(page.locator(history_page.locators.history_table)).to_be_visible(timeout=30000)
                page.wait_for_timeout(2000)
                # Mask header_container to avoid dynamic content differences
                assert_snapshot_lenient(page, threshold=0.5, mask_elements=[AppLocators.header_container])
        finally:
            page.unroute(f"**{HISTORY_API_ENDPOINT}**")
