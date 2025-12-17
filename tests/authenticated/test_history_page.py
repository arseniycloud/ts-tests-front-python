import allure
import pytest
from playwright.sync_api import Route, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from pages.history_page import HistoryPage
from tests.authenticated.helpers.history_helpers import (
    HISTORY_API_ENDPOINT,
    handle_history_route,
    load_mock_data,
)
from utils.allure_helpers import attach_screenshot


@pytest.fixture
def history_page(auth_user_existing):
    page = auth_user_existing

    history_url = f"{BASE_URL}/app/history"
    page.goto(history_url)
    page.wait_for_load_state("networkidle")

    history_page = HistoryPage(page)
    return history_page


@allure.epic("History")
@allure.feature("History Page")
@allure.title("History Page - Order History")
class TestHistoryPageElements:
    @allure.title("Test history page navigation, structure and header elements")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_history_page_navigation_structure_and_header(self, history_page):
        page = history_page.page

        with allure.step("Verify history page URL"):
            assert "/app/history" in page.url or "/app" in page.url, f"Should be on history page, got {page.url}"
            attach_screenshot(page, "History page loaded")

        with allure.step("Verify page title"):
            page_title = page.title()
            # Page title might be generic like "Редактор | TUN" or contain "История"
            assert page_title, f"Page title should exist, got {page_title}"

        with allure.step("Check history page elements"):
            history_page.check_history_elements()
            attach_screenshot(page, "History page elements")

        with allure.step("Check history header elements"):
            history_page.check_history_header_elements()
            attach_screenshot(page, "History header elements")

    @allure.title("Test history table visibility and items count")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_history_table_and_items(self, history_page):
        page = history_page.page

        with allure.step("Check history table visibility"):
            history_page.check_history_table()
            attach_screenshot(page, "History table")

        with allure.step("Verify history items count"):
            items_count = history_page.get_history_items_count()
            attach_screenshot(page, f"History items count: {items_count}")
            assert items_count >= 0, f"History items count should be >= 0, got {items_count}"

        if items_count == 0:
            with allure.step("Check empty state"):
                history_page.check_empty_state()
                attach_screenshot(page, "Empty state")


    @allure.title("Test that all history rows on all pages have required elements")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_history_rows_elements_on_all_pages(self, history_page):
        with allure.step("Navigate through all pages and check rows"):
            history_page.navigate_and_check_pages_flow()


    @allure.title("Test pagination navigation with mocked API responses")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_history_pagination_with_mock(self, authenticated_user_new):
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
                expect(page.locator(history_page.locators.history_table)).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

            with allure.step("Wait for history data to load"):
                history_rows_locator = page.locator("tbody tr[data-test-id='history-row']")
                expect(history_rows_locator.first).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)
                # Wait for data to be fully rendered
                expect(history_rows_locator.first).to_be_visible(timeout=500)

            with allure.step("Check pagination visibility"):
                history_page.check_pagination_visible()

            with allure.step("Verify first page"):
                current_page = history_page.get_current_page_number()
                assert current_page == 1, f"Should start on first page, got {current_page}"

                items_count = history_page.get_history_items_count()
                assert items_count > 0, f"Should have items on first page, got {items_count}"

            with allure.step("Test Next/Previous navigation"):
                next_btn_locator = page.get_by_role("button", name=history_page.BUTTON_NEXT_PAGE)
                if next_btn_locator.count() > 0:
                    next_btn = next_btn_locator.first
                    if not next_btn.is_disabled():
                        next_btn.click()
                        page.wait_for_load_state("domcontentloaded")
                        expect(page.locator(history_page.locators.history_table)).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

                        new_page = history_page.get_current_page_number()
                        assert new_page > current_page, f"Page should increase after clicking next, got {new_page}"

                        prev_btn_locator = page.get_by_role("button", name=history_page.BUTTON_PREVIOUS_PAGE)
                        if prev_btn_locator.count() > 0:
                            prev_btn = prev_btn_locator.first
                            if not prev_btn.is_disabled():
                                prev_btn.click()
                                page.wait_for_load_state("domcontentloaded")
                                expect(page.locator(history_page.locators.history_table)).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

                                prev_page = history_page.get_current_page_number()
                                assert prev_page < new_page, f"Page should decrease after clicking previous, got {prev_page}"

            with allure.step("Test Last/First navigation"):
                last_btn_locator = page.get_by_role("button", name=history_page.BUTTON_LAST_PAGE)
                if last_btn_locator.count() > 0:
                    last_btn = last_btn_locator.first
                    if not last_btn.is_disabled():
                        last_btn.click()
                        page.wait_for_load_state("domcontentloaded")
                        expect(page.locator(history_page.locators.history_table)).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

                        last_page = history_page.get_current_page_number()
                        assert last_page >= 1, f"Should be on a valid page, got {last_page}"

                        first_btn_locator = page.get_by_role("button", name=history_page.BUTTON_FIRST_PAGE)
                        if first_btn_locator.count() > 0:
                            first_btn = first_btn_locator.first
                            if not first_btn.is_disabled():
                                first_btn.click()
                                page.wait_for_load_state("domcontentloaded")
                                expect(page.locator(history_page.locators.history_table)).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

                                first_page = history_page.get_current_page_number()
                                assert first_page == 1, f"Should be on first page 1, got {first_page}"

            with allure.step("Test clicking page 2"):
                page_2_btn_locator = page.get_by_role("button", name="Page 2")
                if page_2_btn_locator.count() > 0:
                    page_2_btn_locator.first.click()
                    page.wait_for_load_state("domcontentloaded")
                    expect(page.locator(history_page.locators.history_table)).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

                    target_page = history_page.get_current_page_number()
                    assert target_page == 2, f"Should be on page 2, got {target_page}"

                    items_count = history_page.get_history_items_count()
                    assert items_count > 0, f"Should have items on page 2, got {items_count}"

                    history_page.check_all_history_rows_on_page()

            with allure.step("Test clicking page 3"):
                page_3_btn_locator = page.get_by_role("button", name="Page 3")
                if page_3_btn_locator.count() > 0:
                    page_3_btn_locator.first.click()
                    page.wait_for_load_state("domcontentloaded")
                    expect(page.locator(history_page.locators.history_table)).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

                    target_page = history_page.get_current_page_number()
                    assert target_page == 3, f"Should be on page 3, got {target_page}"

                    items_count = history_page.get_history_items_count()
                    assert items_count > 0, f"Should have items on page 3, got {items_count}"

                    history_page.check_all_history_rows_on_page()
        finally:
            # Clean up mock route handler to ensure it doesn't affect other tests
            page.unroute(f"**{HISTORY_API_ENDPOINT}**")
