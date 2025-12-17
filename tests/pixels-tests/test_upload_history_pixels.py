import re

import allure
import pytest
from playwright.sync_api import Route, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from pages.history_page import HistoryPage
from pages.upload_page import UploadPage
from tests.authenticated.helpers.history_helpers import (
    HISTORY_API_ENDPOINT,
    handle_history_route,
    load_mock_data,
)


@allure.epic("Visual Regression")
@allure.feature("Upload History")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestUploadHistoryVisualRegression:

    @allure.title("Info modal in history snapshot")
    @pytest.mark.pixel_test
    def test_info_modal_in_history(self, authenticated_user_new, assert_snapshot_with_threshold):
        page = authenticated_user_new

        with allure.step("Setup mock API route handler"):
            mock_data = load_mock_data()
            limit = 30

            def route_handler(route: Route):
                handle_history_route(route, mock_data=mock_data, limit=limit)

            page.route(f"**{HISTORY_API_ENDPOINT}**", route_handler)

        try:
            with allure.step("Navigate to history page"):
                history_url = f"{BASE_URL}/app/history"
                page.goto(history_url)
                page.wait_for_load_state("domcontentloaded", timeout=30000)
                page.wait_for_load_state("networkidle", timeout=30000)
                history_page = HistoryPage(page)
                history_table = page.locator(history_page.locators.history_table)
                expect(history_table).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            with allure.step("Wait for history rows to load"):
                history_rows = page.locator("tbody tr[data-test-id='history-row']")
                expect(history_rows.first).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)
                expect(history_rows.first).to_be_visible(timeout=500)

            with allure.step("Open info modal"):
                # Find BMW file link like in functional tests
                bmw_file_link = page.locator("a.table-patch-link").filter(has_text=re.compile(r"BMW.*\.bin$"))
                expect(bmw_file_link.first).to_be_visible(timeout=Timeouts.PageLoad.DOMCONTENTLOADED_LONG)

                bmw_history_row = page.locator("tr[data-test-id='history-row']").filter(has=bmw_file_link).first
                expect(bmw_history_row).to_be_visible(timeout=Timeouts.History.ROW_VISIBLE)

                # Find info button in the row - using get_by_role with exact name match
                info_button = bmw_history_row.get_by_role("button", name="Инфо")
                expect(info_button).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)

                # Verify button has correct classes (optional check)
                expect(info_button).to_have_class(re.compile(r".*btn-primary.*"), timeout=1000)

                info_button.click()
                modal_title = page.get_by_label("title")
                expect(modal_title).to_be_visible(timeout=500)

            with allure.step("Capture info modal"):
                # Wait for modal title to appear
                modal_title = page.get_by_label("title")
                expect(modal_title).to_be_visible(timeout=Timeouts.Modal.TITLE_VISIBLE)
                expect(modal_title).to_be_visible(timeout=300)

                # Find modal dialog container using patch-body class or ancestor
                # Try to find by patch-body class first (more specific)
                modal_body = page.locator(".patch-body").first
                if modal_body.count() > 0 and modal_body.is_visible(timeout=1000):
                    modal_dialog = modal_body
                else:
                    # Fallback to ancestor approach
                    modal_dialog = modal_title.locator("xpath=ancestor::dialog | ancestor::div[contains(@class, 'modal')] | ancestor::div[contains(@role, 'dialog')]").first

                expect(modal_dialog).to_be_visible(timeout=Timeouts.Modal.APPEAR)
                # Verify download button exists but don't click it
                download_button = page.get_by_role("button", name="Скачать")
                expect(download_button).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
                expect(download_button).to_be_visible(timeout=300)
                # Wait for animations and rendering to complete
                page.wait_for_timeout(3000)
                assert_snapshot_with_threshold(modal_dialog, threshold=0.15)
        finally:
            page.unroute(f"**{HISTORY_API_ENDPOINT}**")

    @allure.title("DTC disable page snapshot (/remove-dtc)")
    @pytest.mark.pixel_test
    def test_dtc_disable_page_with_errors(self, authenticated_user_new, assert_snapshot_with_threshold):
        page = authenticated_user_new

        with allure.step("Setup mock API route handler"):
            mock_data = load_mock_data()
            limit = 30

            def route_handler(route: Route):
                handle_history_route(route, mock_data=mock_data, limit=limit)

            page.route(f"**{HISTORY_API_ENDPOINT}**", route_handler)

        try:
            with allure.step("Navigate to history page"):
                history_url = f"{BASE_URL}/app/history"
                page.goto(history_url)
                page.wait_for_load_state("networkidle")
                history_page = HistoryPage(page)
                history_table = page.locator(history_page.locators.history_table)
                expect(history_table).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

            with allure.step("Wait for history rows to load"):
                history_rows = page.locator("tbody tr[data-test-id='history-row']")
                expect(history_rows.first).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)
                expect(history_rows.first).to_be_visible(timeout=500)

            with allure.step("Click disable DTC button"):
                # Find BMW file link like in functional tests
                bmw_file_link = page.locator("a.table-patch-link").filter(has_text=re.compile(r"BMW.*\.bin$"))
                if bmw_file_link.count() > 0:
                    expect(bmw_file_link.first).to_be_visible(timeout=Timeouts.PageLoad.DOMCONTENTLOADED_LONG)
                    bmw_history_row = page.locator("tr[data-test-id='history-row']").filter(has=bmw_file_link).first
                    expect(bmw_history_row).to_be_visible(timeout=Timeouts.History.ROW_VISIBLE)
                    disable_button = bmw_history_row.get_by_role("button", name="Откл DTC")
                else:
                    # Fallback to first row if BMW file not found in mock data
                    first_row = history_rows.first
                    disable_button = first_row.get_by_role("button", name="Откл DTC")

                expect(disable_button).to_be_visible(timeout=Timeouts.History.DTC_BUTTON_VISIBLE)
                disable_button.click()
                page.wait_for_url(re.compile(r".*remove-dtc.*"), timeout=Timeouts.BASE_PAGE_LOAD)
                page.wait_for_load_state("domcontentloaded")

            with allure.step("Enter error code and capture form"):
                # Use full textbox name like in functional tests
                error_code_input = page.get_by_role("textbox", name="Введите коды ошибок (не более 10 штук) (на пример 042Е, 255F)")
                expect(error_code_input).to_be_visible(timeout=Timeouts.Upload.ERROR_CODE_INPUT_VISIBLE)
                error_code_input.click()
                error_code_input.fill("244A")
                expect(error_code_input).to_be_visible(timeout=500)

                check_button = page.get_by_role("button", name="проверить")
                expect(check_button).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
                expect(check_button).to_be_visible(timeout=1000)

                # Find form container using ancestor from input field
                history_form = error_code_input.locator("xpath=ancestor::form | ancestor::div[contains(@class, 'form')] | ancestor::div[contains(@class, 'container')]").first
                expect(history_form).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
                expect(history_form).to_be_visible(timeout=500)
                # Wait for animations and rendering to complete
                page.wait_for_timeout(1000)
                assert_snapshot_with_threshold(history_form, threshold=0.2)
        finally:
            page.unroute(f"**{HISTORY_API_ENDPOINT}**")

    @allure.title("DTC disable page snapshot (/remove-dtc)")
    @pytest.mark.pixel_test
    def test_dtc_disable_page(self, authenticated_user_with_balance, assert_snapshot_lenient):

        page = authenticated_user_with_balance
        upload_page = UploadPage(page)

        with allure.step("Upload file and apply order"):
            upload_page.upload_file("BMW.bin")
            upload_page.select_file_parameters("Car", "BMW, MINI", "Diesel engines", "Bosch EDC15")
            upload_page.search_solutions(wait_time=0)
            solutions_found = upload_page.get_solutions_locator()
            solutions_found.first.wait_for(state="visible", timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            upload_page.select_solution_by_index(1)
            upload_page.focus_order_total_area()
            upload_page.dismiss_currency_modal()
            upload_page.apply_order(wait_time=0)
            # Wait for server to process order - need guaranteed minimum wait time
            page.wait_for_timeout(2000)

        with allure.step("Navigate to history and click disable DTC button"):
            history_url = f"{BASE_URL}/app/history"
            page.goto(history_url)
            page.wait_for_load_state("networkidle")

            bmw_file_link = page.locator("a.table-patch-link").filter(has_text=re.compile(r"BMW.*\.bin$")).first
            expect(bmw_file_link).to_be_visible(timeout=Timeouts.PageLoad.DOMCONTENTLOADED_LONG)
            bmw_history_row = page.locator("tr[data-test-id='history-row']").filter(has=bmw_file_link).first
            expect(bmw_history_row).to_be_visible(timeout=Timeouts.History.ROW_VISIBLE)

            disable_button = bmw_history_row.get_by_role("button", name="Откл DTC")
            expect(disable_button).to_be_visible(timeout=Timeouts.History.DTC_BUTTON_VISIBLE)
            disable_button.click()

            # Wait for navigation to remove-dtc page
            page.wait_for_url(re.compile(r".*remove-dtc.*"), timeout=Timeouts.BASE_PAGE_LOAD)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_load_state("networkidle")

        with allure.step("Capture DTC disable page"):
            # Use full textbox name like in functional tests
            error_code_input = page.get_by_role("textbox", name="Введите коды ошибок (не более 10 штук) (на пример 042Е, 255F)")
            expect(error_code_input).to_be_visible(timeout=Timeouts.Upload.ERROR_CODE_INPUT_VISIBLE)

            # Wait for network idle to ensure page is fully loaded and stable
            upload_page.wait_for_network_idle()
            page.wait_for_timeout(500)

            # Найти форму как ancestor от input поля (как в test_dtc_disable_page_with_errors)
            history_form = error_code_input.locator("xpath=ancestor::form | ancestor::div[contains(@class, 'form')] | ancestor::div[contains(@class, 'container')]").first
            expect(history_form).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            # Define mask selectors for dynamic content
            mask_selectors = [
                "#task_number",  # Номер задания
                "#task_number_copy",  # Кнопка копирования номера задания
                "a[href*='/app/history/'] span.text-gray-400",  # История (номер задания в ссылке)
                "td:has-text('Файл') + td",  # Файл (следующий td после "Файл")
                "time",  # Дата покупки
                "td:has-text('Цена') + td",  # Цена (следующий td после "Цена")
                "td:has-text('Software') + td",  # Software (следующий td после "Software")
                "td:has-text('Upgrade') + td",  # Upgrade (следующий td после "Upgrade")
            ]

            # Использовать сам locator вместо screenshot(), чтобы маски работали
            # pytest-playwright-visual-snapshot применяет маски при создании скриншота
            page.wait_for_timeout(500)
            assert_snapshot_lenient(history_form, threshold=0.8, mask_elements=mask_selectors)
