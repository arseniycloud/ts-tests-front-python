import logging
from pathlib import Path

import allure
from playwright.sync_api import Page, expect

from config.timeouts import Timeouts
from locators.app_locators import AppLocators
from pages.base_upload_page import BaseUploadPage
from pages.history_page import HistoryPage
from pages.profile_page import ProfilePage
from utils.allure_helpers import attach_screenshot


class UploadPage(BaseUploadPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = AppLocators()

    @allure.step("Download patched file and return path to downloaded file")
    def download_patched_file(self) -> Path:
        self.page.on("dialog", lambda dialog: dialog.accept())

        download_path = Path(__file__).parent.parent / "reports" / "patched_files"
        download_path.mkdir(parents=True, exist_ok=True)

        with self.page.expect_download() as download_info:
            self.page.locator(self.locators.download_button).click()

        download = download_info.value
        assert download is not None, "Download should be triggered"

        download_file_path = download_path / download.suggested_filename
        download.save_as(download_file_path)
        assert download_file_path.exists(), f"Downloaded file should exist at {download_file_path}"

        attach_screenshot(self.page, "Patched file downloaded")
        return download_file_path

    @allure.step("Select DTC OFF solution checkbox")
    def select_dtc_off_solution(self) -> None:
        self.page.get_by_role("row", name="ОТКЛЮЧИТЬ DTC (0 CODES) 480 ₽").get_by_role("checkbox").check()
        attach_screenshot(self.page, "DTC OFF solution selected")

    @allure.step("Enter error codes in DTC OFF input field: {error_codes}")
    def enter_error_codes(self, error_codes: str) -> None:
        error_code_input = self.page.get_by_role("textbox", name="Введите коды ошибок (не более 10 штук)")

        expect(error_code_input).to_be_visible(timeout=Timeouts.Upload.ERROR_CODE_INPUT_VISIBLE)

        error_code_input.click()
        error_code_input.fill(error_codes)
        self.page.get_by_role("button", name="ПРОВЕРИТЬ").click()
        self.wait_standard()

        attach_screenshot(self.page, "Error codes entered")

    @allure.step("Verify error codes dialog")
    def verify_error_codes_dialog(self) -> None:
        detected_errors = self.page.locator("div").filter(has_text="Обнаружены активные ошибки:")

        if detected_errors.count() > 0:
            detected_errors.nth(3).click()
            self.page.get_by_role("button", name="ОК").click()

        attach_screenshot(self.page, "Error codes dialog verified")

    @allure.step("Handle warning dialog if present after applying order")
    def handle_warning_dialog(self) -> None:
        warning_heading = self.page.get_by_role("heading", name="Предупреждение")

        if warning_heading.count() > 0:
            self.page.get_by_role("button", name="продолжить").click()
            attach_screenshot(self.page, "Warning dialog handled")

    @allure.step("Delete uploaded file")
    def delete_uploaded_file(self) -> None:
        delete_icon = self.page.locator(self.locators.upload_area_data_test_id).locator("span").nth(2)

        if delete_icon.count() > 0:
            delete_icon.click()
            self.wait_standard()

        attach_screenshot(self.page, "Uploaded file deleted")

    @allure.step("Apply order and download patched file")
    def apply_order_and_download(self, wait_time: int = 1000) -> Path:
        self.apply_order(wait_time=wait_time)
        downloaded_file = self.download_patched_file()

        attach_screenshot(self.page, "Order applied and file downloaded")
        return downloaded_file

    @allure.step("Navigate to history page and return HistoryPage instance")
    def navigate_to_history(self) -> HistoryPage:
        self.page.locator(self.locators.history_link).click()

        try:
            self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        except Exception as e:
            logging.warning(f"Failed to wait for networkidle when navigating to history, falling back to load state: {e}")
            self.page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)

        attach_screenshot(self.page, "Navigated to history")
        return HistoryPage(self.page)

    @allure.step("Navigate to profile page and return ProfilePage instance")
    def navigate_to_profile(self) -> ProfilePage:
        self.page.locator(self.locators.profile_link).click()

        try:
            self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        except Exception as e:
            logging.warning(f"Failed to wait for networkidle when navigating to profile, falling back to load state: {e}")
            self.page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)

        self.wait_standard()
        attach_screenshot(self.page, "Navigated to profile")
        return ProfilePage(self.page)

    @allure.step("Click on order total area to activate order form")
    def focus_order_total_area(self) -> None:
        order_total = self.page.locator(self.locators.order_total)
        expect(order_total).to_be_visible(timeout=Timeouts.Upload.ORDER_TOTAL_VISIBLE)

        order_total.click()
        attach_screenshot(self.page, "Order total area focused")

    @allure.step("Click rub currency button to dismiss modal if present")
    def dismiss_currency_modal(self) -> None:
        rub_button = self.page.get_by_text("руб")

        if rub_button.count() > 0:
            rub_button.click()
            attach_screenshot(self.page, "Currency modal dismissed")

    @allure.step("Toggle cashback checkbox to enable/disable cashback usage")
    def toggle_cashback_option(self) -> None:
        cashback_toggle = self.page.locator(self.locators.cashback_toggle)

        if cashback_toggle.count() > 0:
            cashback_toggle.first.click()
            attach_screenshot(self.page, "Cashback option toggled")

    @allure.step("Click on order cash button to select cash payment option")
    def select_cash_payment_option(self) -> None:
        order_cash = self.page.locator(self.locators.order_cash)

        if order_cash.count() > 0:
            order_cash.click()
            attach_screenshot(self.page, "Cash payment option selected")

    @allure.step("Verify payment required modal (insufficient balance) is visible")
    def verify_payment_required_modal(self) -> None:
        need_pay_modal = self.page.locator(self.locators.need_pay_modal)
        expect(need_pay_modal).to_be_visible(timeout=Timeouts.Modal.APPEAR)
        attach_screenshot(self.page, "Payment required modal verified")

    @allure.step("Click top-up button in payment required modal to proceed to payment methods")
    def click_top_up_button(self) -> None:
        payment_need_modal_pay_btn = self.page.locator(self.locators.payment_need_modal_pay_btn)
        expect(payment_need_modal_pay_btn).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
        payment_need_modal_pay_btn.click()

        self.wait_standard()
        attach_screenshot(self.page, "Top-up button clicked")

    @allure.step("Verify payment methods selection panel is visible")
    def verify_payment_methods_panel(self) -> None:
        payment_methods_panel = self.page.locator(self.locators.payment_methods_panel)
        expect(payment_methods_panel).to_be_visible(timeout=Timeouts.Modal.APPEAR)
        attach_screenshot(self.page, "Payment methods panel verified")

    @allure.step("Verify payment amount input field is visible")
    def verify_payment_amount_input(self) -> None:
        payment_amount_input = self.page.locator(self.locators.payment_amount)
        expect(payment_amount_input).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)
        attach_screenshot(self.page, "Payment amount input verified")

    @allure.step("Verify payment submit button is visible")
    def verify_payment_submit_button(self) -> None:
        payment_pay_btn = self.page.locator(self.locators.payment_pay_btn)
        expect(payment_pay_btn).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
        attach_screenshot(self.page, "Payment submit button verified")

    @allure.step("Verify balance display contains and shows expected text")
    def verify_balance_display(self, expected_text: str = "Баланс:0") -> None:
        balance_display = self.page.locator(self.locators.balance_display).filter(has_text=expected_text)

        if balance_display.count() > 0:
            expect(balance_display.first).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)
            attach_screenshot(self.page, "Balance display verified")

    @allure.step("Navigate to TUN page from header menu")
    def navigate_to_tun_page(self) -> None:
        self.page.locator(self.locators.tun_link_data_test_id).click()
        self.page.wait_for_load_state("domcontentloaded")

        self.wait_standard()
        attach_screenshot(self.page, "Navigated to TUN page")

    @allure.step("Open patch details by clicking patch title")
    def open_patch_details(self) -> None:
        self.page.locator(self.locators.patch_title).click()
        attach_screenshot(self.page, "Patch details opened")

    @allure.step("Close dialog or modal")
    def close_dialog(self) -> None:
        self.page.locator(self.locators.close_icon).click()
        attach_screenshot(self.page, "Dialog closed")

    @allure.step("Verify and get order total text content")
    def verify_and_get_order_total_text(self) -> str:
        order_total = self.page.locator(self.locators.order_total)
        expect(order_total).to_be_visible(timeout=Timeouts.Upload.ORDER_TOTAL_VISIBLE)

        total_text = order_total.text_content()
        assert "₽" in total_text, f"Order total should contain price, got: {total_text}"
        assert total_text.strip() != "", "Order total should not be empty"

        attach_screenshot(self.page, "Order total text verified")
        return total_text or ""
