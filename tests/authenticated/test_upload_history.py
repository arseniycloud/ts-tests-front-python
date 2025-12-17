import logging
import re

import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from pages.history_page import HistoryPage
from pages.upload_page import UploadPage
from utils.allure_helpers import attach_element_screenshot, attach_screenshot


@allure.epic("Upload")
@allure.feature("Upload History")
@allure.title("Upload History - DTC Processing")
class TestUploadHistory:

    @allure.story("DTC Processing")
    @allure.title("Test BMW LSU OFF with DTC disable")
    @pytest.mark.upload
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_bmw_with_dtc_history_disable(self, authenticated_user_with_balance):
        page = authenticated_user_with_balance
        upload_page = UploadPage(page)

        with allure.step("BMW upload with LSU OFF"):
            vehicle_type = "Car"
            upload_page.upload_file("BMW.bin")
            upload_page.select_file_parameters(vehicle_type, "BMW, MINI", "Diesel engines", "Bosch EDC15")
            upload_page.search_solutions(wait_time=0)

            solutions_found = upload_page.get_solutions_locator()
            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            attach_element_screenshot(solutions_found.first, "Solution row")

            upload_page.verify_solutions_found(min_count=1)
            upload_page.select_solution_by_index(1)

            upload_page.focus_order_total_area()
            upload_page.dismiss_currency_modal()

            upload_page.apply_order(wait_time=0)
            expect(page.locator(upload_page.locators.download_button)).to_be_visible(
                timeout=Timeouts.Download.BUTTON_VISIBLE)

            upload_page.wait_for_network_idle()
            attach_screenshot(page, "After order applied")

        with allure.step("Navigate to history page directly"):
            history_url = f"{BASE_URL}/app/history"
            page.goto(history_url)
            page.wait_for_load_state("networkidle")

            bmw_file_link = page.locator("a.table-patch-link").filter(has_text=re.compile(r"BMW.*\.bin$"))
            expect(bmw_file_link.first).to_be_visible(timeout=Timeouts.PageLoad.DOMCONTENTLOADED_LONG)
            attach_screenshot(page, "History page loaded")

        with allure.step("Open info modal for BMW purchase"):
            upload_page.wait_for_network_idle()
            bmw_file_link = page.locator("a.table-patch-link").filter(has_text=re.compile(r"BMW.*\.bin$"))

            expect(bmw_file_link.first).to_be_visible(timeout=Timeouts.PageLoad.DOMCONTENTLOADED_LONG)
            bmw_file_name = bmw_file_link.first.text_content()
            assert bmw_file_name, "BMW file name should be found"

            bmw_history_row = page.locator("tr[data-test-id='history-row']").filter(has=bmw_file_link).first
            expect(bmw_history_row).to_be_visible(timeout=Timeouts.History.ROW_VISIBLE)

            info_button = bmw_history_row.get_by_role("button", name="Инфо")
            expect(info_button).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
            attach_element_screenshot(info_button, "Info button")

            info_button.click()
            modal_title = page.get_by_label("title")
            expect(modal_title).to_be_visible(timeout=Timeouts.Modal.TITLE_VISIBLE)

            attach_element_screenshot(modal_title, "Modal title")
            attach_screenshot(page, "Info modal opened")

        with allure.step("Navigate modal, verify solution and download patched file"):
            page.get_by_text("Применили").click()

            download_button = page.get_by_role("button", name="скачать")
            expect(download_button).to_be_visible(timeout=Timeouts.Download.BUTTON_VISIBLE)
            attach_element_screenshot(download_button, "Download button")

            # Wait a bit for button to be fully ready
            page.wait_for_timeout(500)

            with page.expect_download(timeout=Timeouts.Download.FILE_DOWNLOAD) as download6_info:
                download_button.click()

            download6 = download6_info.value
            assert download6 is not None, "Download should be triggered"

            page.get_by_role("button", name="закрыть").click()
            modal_dialog = page.locator("dialog[role='dialog']")
            expect(modal_dialog).not_to_be_visible(timeout=Timeouts.Modal.NOT_VISIBLE)
            upload_page.wait_for_network_idle()

        with allure.step("Click disable DTC button"):
            upload_page.wait_for_network_idle()
            bmw_file_link = page.locator("a.table-patch-link").filter(has_text=re.compile(r"BMW.*\.bin$")).first
            expect(bmw_file_link).to_be_visible(timeout=Timeouts.PageLoad.DOMCONTENTLOADED_LONG)

            bmw_history_row = page.locator("tr[data-test-id='history-row']").filter(has=bmw_file_link).first
            expect(bmw_history_row).to_be_visible(timeout=Timeouts.History.ROW_VISIBLE)

            disable_button = bmw_history_row.get_by_role("button", name="Откл DTC")
            expect(disable_button).to_be_visible(timeout=Timeouts.History.DTC_BUTTON_VISIBLE)
            attach_element_screenshot(disable_button, "Disable DTC button")

            # Close any open poppers/tooltips that might intercept clicks
            popper = page.locator("div[data-reka-popper-content-wrapper]")
            if popper.count() > 0 and popper.first.is_visible():
                page.keyboard.press("Escape")
                page.wait_for_timeout(300)

            # Try normal click first, if it fails use force click
            try:
                disable_button.click(timeout=5000)

            except Exception as e:
                logging.debug(f"Normal click failed, using force click: {e}")
                disable_button.click(force=True)

            # Wait for navigation to remove-dtc page (not a modal, but a separate page)
            page.wait_for_url(re.compile(r".*remove-dtc.*"), timeout=Timeouts.BASE_PAGE_LOAD)
            page.wait_for_load_state("domcontentloaded")

            # Wait for network idle to ensure page is fully loaded (important for CI)
            try:
                page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

            except Exception as e:
                # Fallback if networkidle takes too long
                logging.warning(f"Failed to wait for networkidle, falling back to load state: {e}")
                page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)

            upload_page.wait_for_network_idle()
            page.wait_for_timeout(500)

        with allure.step("Enter error code 244A, verify and apply DTC disable"):
            # Wait for page to load and input field to be visible
            # Try full name first, then fallback to shorter name (as in upload_page.py)
            try:
                error_code_input = page.get_by_role("textbox", name="Введите коды ошибок (не более 10 штук) (на пример 042Е, 255F)")
                expect(error_code_input).to_be_visible(timeout=Timeouts.Upload.ERROR_CODE_INPUT_VISIBLE)

            except Exception as e:
                # Fallback to shorter name (as used in upload_page.py)
                logging.debug(f"Failed to find error code input with full name, trying shorter name: {e}")
                error_code_input = page.get_by_role("textbox", name="Введите коды ошибок (не более 10 штук)")
                expect(error_code_input).to_be_visible(timeout=Timeouts.Upload.ERROR_CODE_INPUT_VISIBLE)

            attach_element_screenshot(error_code_input, "Error code input field")
            error_code_input.click()

            error_code_input.fill("244A")
            attach_screenshot(page, "Error code entered")

            check_button = page.get_by_role("button", name="проверить")
            expect(check_button).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
            attach_element_screenshot(check_button, "Check button")
            check_button.click()

            errors_found_text = page.get_by_text("Найдены активные ошибки: 244A")
            expect(errors_found_text).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)
            attach_screenshot(page, "Errors found confirmation")

            apply_button = page.get_by_role("button", name="применить")
            expect(apply_button).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
            attach_element_screenshot(apply_button, "Apply button")

            apply_button.click()
            upload_page.wait_for_network_idle()
            attach_screenshot(page, "DTC disabled applied")

            download_button = page.get_by_role("button", name="скачать")
            expect(download_button).to_be_visible(timeout=Timeouts.Download.BUTTON_VISIBLE)
            attach_element_screenshot(download_button, "Download button")

            with page.expect_download(timeout=50000) as download7_info:
                download_button.click()

            download7 = download7_info.value
            assert download7 is not None, "Download should be triggered"

        with allure.step("Navigate to history and verify new DTC disabled entry"):
            history_url = f"{BASE_URL}/app/history"
            page.goto(history_url)
            page.wait_for_load_state("networkidle")

            dtc_disabled_file = page.locator("a.table-patch-link").filter(has_text=re.compile(r"BMW.*DTC.*OFF.*244A\.bin$"))
            expect(dtc_disabled_file.first).to_be_visible(timeout=50000)

        with allure.step("Download DTC disabled file"):
            dtc_disabled_row = page.locator("tr[data-test-id='history-row']").filter(has=dtc_disabled_file).first
            expect(dtc_disabled_row).to_be_visible(timeout=Timeouts.History.ROW_VISIBLE)

            history_page = HistoryPage(page)
            download_link = dtc_disabled_row.locator(history_page.locators.history_download_link)

            if download_link.count() == 0:
                download_link = dtc_disabled_row.locator("a[href*='download']")

            if download_link.count() == 0:
                download_link = dtc_disabled_row.locator("a:has-text('Скачать')")

            if download_link.count() > 0:
                expect(download_link.first).to_be_visible(timeout=Timeouts.Download.BUTTON_VISIBLE)

                with page.expect_download(timeout=Timeouts.BASE_PAGE_LOAD) as download8_info:
                    download_link.first.click()
                download8 = download8_info.value
                assert download8 is not None, "Download should be triggered"

            else:
                # If download link is not found, skip download but continue test
                pass

        with allure.step("Verify transaction details and download patched file"):
            upload_page.wait_for_network_idle()

            dtc_disabled_row = page.locator("tr[data-test-id='history-row']").filter(has=dtc_disabled_file).first
            expect(dtc_disabled_row).to_be_visible(timeout=Timeouts.History.ROW_VISIBLE)

            price_cell = dtc_disabled_row.get_by_text("0 ₽")
            expect(price_cell).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)
            attach_element_screenshot(price_cell, "Price cell")

            info_button = dtc_disabled_row.get_by_role("button", name="Инфо")
            expect(info_button).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
            attach_element_screenshot(info_button, "Info button")
            info_button.click()

            modal_title = page.get_by_label("title")
            expect(modal_title).to_be_visible(timeout=Timeouts.Modal.TITLE_VISIBLE)
            attach_element_screenshot(modal_title, "Modal title")

            dtc_disabled_text = page.get_by_text("Отключили DTC")
            expect(dtc_disabled_text).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)
            attach_element_screenshot(dtc_disabled_text, "DTC disabled text")

            error_code_item = page.get_by_role("listitem").filter(has_text="244A")
            expect(error_code_item).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)
            attach_element_screenshot(error_code_item, "Error code item")

            download_button = page.get_by_role("button", name="скачать")
            expect(download_button).to_be_visible(timeout=Timeouts.Download.BUTTON_VISIBLE)
            attach_element_screenshot(download_button, "Download button")

            with page.expect_download(timeout=50000) as download9_info:
                download_button.click()

            download9 = download9_info.value
            assert download9 is not None, "Download should be triggered"

            close_button = page.get_by_role("button", name="закрыть")
            expect(close_button).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
            attach_element_screenshot(close_button, "Close button")
            close_button.click()

            modal_dialog = page.locator("dialog[role='dialog']")
            expect(modal_dialog).not_to_be_visible(timeout=Timeouts.Modal.NOT_VISIBLE)
