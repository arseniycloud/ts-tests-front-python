import re
from pathlib import Path

import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from pages.history_page import HistoryPage
from pages.profile_page import ProfilePage
from pages.upload_page import UploadPage
from utils.allure_helpers import attach_element_screenshot, attach_screenshot


@allure.epic("Upload")
@allure.feature("Upload Page")
@allure.title("Upload Page - File Processing")
class TestUploadPageElements:


    @allure.story("File Upload")
    @allure.title("Test file upload, search and price calculation for Mazda")
    @pytest.mark.upload
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_file_upload_mazda(self, authenticated_user_new):
        vehicle_type = "Car"
        brand = "Mazda"
        engine = "Petrol engines"
        ecu = "Denso SH72xxx"

        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file(f"{brand}.bin")
            attach_screenshot(page, "After file upload")

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, brand, engine, ecu)
            attach_screenshot(page, "After parameter selection")

        with allure.step("Search for solutions"):
            upload_page.search_solutions()
            upload_page.verify_solutions_found(min_count=2)
            attach_screenshot(page, "Solutions found")

        with allure.step("Select solutions and verify prices"):
            upload_page.select_solution_by_index(1)
            total_price = upload_page.get_order_total()
            assert total_price > 0, f"Order total should be greater than 0, got {total_price}"
            attach_screenshot(page, "Price calculated")

        with allure.step("Apply order and download file"):
            upload_page.apply_order()
            upload_page.verify_order_total(expected_price=1920)

            download_file_path = upload_page.download_patched_file()
            attach_screenshot(page, "File downloaded")
            assert download_file_path.exists()

    @allure.story("File Upload")
    @allure.title("Test file upload, search and price calculation for MBSprinter")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_file_upload_mbsprinter(self, authenticated_user_new):
        vehicle_type = "Car"
        file_name = "MBSprinter"
        brand = "Mercedes"
        engine = "Diesel engine"
        ecu = "Bosch EDC16"

        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file(f"{file_name}.bin")

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, brand, engine, ecu)

        with allure.step("Search for solutions"):
            upload_page.search_solutions()
            upload_page.verify_solutions_found(min_count=2)

        with allure.step("Select solutions and verify prices"):
            upload_page.select_solution_by_index(1)
            total_price = upload_page.get_order_total()
            assert total_price > 0, f"Order total should be greater than 0, got {total_price}"

        with allure.step("Apply order and download file"):
            upload_page.apply_order()
            upload_page.verify_order_total(expected_price=1480)
            download_file_path = upload_page.download_patched_file()
            assert download_file_path.exists()


    @allure.story("DTC OFF Processing")
    @allure.title("Test DTC OFF purchase with error codes input for BMW")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_dtc_off_with_error_codes_bmw(self, authenticated_user_new):
        vehicle_type = "Car"
        file_name = "BMW_255F.bin"
        brand = "BMW, MINI"
        engine = "Diesel engines"
        ecu = "Bosch EDC15"

        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file(file_name)

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, brand, engine, ecu)

        with allure.step("Search for solutions"):
            upload_page.search_solutions(wait_time=2)
            solutions_found = upload_page.get_solutions_locator()
            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            upload_page.verify_solutions_found(min_count=1)

        with allure.step("Select DTC OFF solution and enter error codes"):
            upload_page.select_dtc_off_solution()
            upload_page.enter_error_codes("255D, 245C")
            upload_page.verify_error_codes_dialog()

        with allure.step("Apply order and download file"):
            page.locator(upload_page.locators.order_total).click()
            upload_page.apply_order(wait_time=Timeouts.Animation.STANDARD)
            upload_page.handle_warning_dialog()
            upload_page.apply_order(wait_time=Timeouts.Animation.LONG)
            download_file_path = upload_page.download_patched_file()
            assert download_file_path.exists()

    @allure.story("DTC OFF Processing")
    @allure.title("Test DTC OFF purchase with error codes input for Mercedes")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_dtc_off_with_error_codes_mercedes(self, authenticated_user_new):
        vehicle_type = "Car"
        file_name = "MBSprinter_31029A.bin"
        brand = "Mercedes"
        engine = "Diesel engine"
        ecu = "Bosch EDC16"

        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file(file_name)

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, brand, engine, ecu)

        with allure.step("Search for solutions"):
            upload_page.search_solutions(wait_time=2)
            solutions_found = upload_page.get_solutions_locator()
            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            upload_page.verify_solutions_found(min_count=1)

        with allure.step("Select DTC OFF solution and enter error codes"):
            upload_page.select_dtc_off_solution()
            upload_page.enter_error_codes("255D, 245C")
            upload_page.verify_error_codes_dialog()

        with allure.step("Apply order and download file"):
            page.locator(upload_page.locators.order_total).click()
            upload_page.apply_order(wait_time=Timeouts.Animation.STANDARD)
            upload_page.handle_warning_dialog()
            upload_page.apply_order(wait_time=Timeouts.Animation.LONG)
            download_file_path = upload_page.download_patched_file()
            assert download_file_path.exists()


    @allure.story("Price Calculation")
    @allure.title("Test file upload, search and price calculation")
    @pytest.mark.upload
    @pytest.mark.validation
    def test_file_upload_and_price_calculation(self, authenticated_user_new):
        vehicle_type = "Car"
        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file("BMW.bin")

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, "BMW, MINI", "Diesel engines", "Bosch EDC16")

        with allure.step("Search for solutions"):
            upload_page.search_solutions(wait_time=0)
            solutions_found = upload_page.get_solutions_locator()
            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            attach_element_screenshot(solutions_found.first, "Solution row")
            upload_page.verify_solutions_found(min_count=1)

        with allure.step("Select solutions and verify prices"):
            upload_page.select_solution_by_name("EGR OFF 1480 ₽")
            upload_page.verify_order_total(expected_price=1480)

            upload_page.select_solution_by_name("TUN 1920 ₽")
            upload_page.verify_order_total(expected_price=1920)

            upload_page.select_solution_by_name("DPF OFF 1480 ₽")
            upload_page.verify_order_total(expected_price=1920)

            upload_page.select_solution_by_name("LSU OFF 1480 ₽")
            upload_page.verify_order_total(expected_price=1920)

            upload_page.select_solution_by_name("VSA OFF 1480 ₽ 1860", exact=True)
            upload_page.verify_order_total(expected_price=1920)

            upload_page.select_solution_by_name("Stage2 2880 ₽")
            upload_page.verify_order_total(expected_price=2880)

            upload_page.select_solution_by_name("DPF EGR VSA OFF 1480 ₽")
            upload_page.verify_order_total(expected_price=2880)

        with allure.step("Check DTC modal and cancel"):
            upload_page.select_dtc_off_solution()
            page.get_by_role("button", name="ПОДСКАЗКА").click()
            page.get_by_role("button", name="Закрыть").click()
            page.get_by_role("button", name="ОТМЕНА").click()

        with allure.step("Apply order and download file"):
            upload_page.apply_order()
            order_total = page.locator(upload_page.locators.order_total)
            expect(order_total).to_be_visible(timeout=Timeouts.Upload.ORDER_TOTAL_VISIBLE)
            total_text = order_total.text_content()
            assert "₽" in total_text, f"Order total should contain price, got: {total_text}"
            assert total_text.strip() != "", "Order total should not be empty"

            download_file_path = upload_page.download_patched_file()
            assert download_file_path.exists()

    @allure.story("DTC OFF Processing")
    @allure.title("Test DTC OFF purchase with error codes input and history verification")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_dtc_off_with_error_codes_and_history_check(self, authenticated_user_new):
        vehicle_type = "Car"
        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file("BMW.bin")

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, "BMW, MINI", "Diesel engines", "Bosch EDC16")

        with allure.step("Search for solutions"):
            upload_page.search_solutions(wait_time=0)
            solutions_found = upload_page.get_solutions_locator()
            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)

        with allure.step("Select DTC OFF solution and enter error codes"):
            upload_page.select_dtc_off_solution()
            upload_page.enter_error_codes("255D")
            upload_page.verify_error_codes_dialog()

            dtc_button = page.get_by_role("button", name="ОТКЛЮЧИТЬ DTC (1 CODES)")
            expect(dtc_button).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            attach_element_screenshot(dtc_button, "DTC button")

            dtc_button.click()
            upload_page.enter_error_codes("255D, 242F")

            upload_page.enter_error_codes("255D, 242F, 245C")
            upload_page.verify_error_codes_dialog()

        with allure.step("Apply order and download file"):
            page.locator(upload_page.locators.order_total).click()
            upload_page.apply_order(wait_time=Timeouts.Animation.STANDARD)
            upload_page.handle_warning_dialog()
            upload_page.apply_order(wait_time=Timeouts.Animation.LONG)

            download_file_path = upload_page.download_patched_file()
            assert download_file_path.exists()

        with allure.step("Verify order in history"):
            history_url = f"{BASE_URL}/app/history"
            page.goto(history_url)
            page.wait_for_load_state("networkidle")

            history_page = HistoryPage(page)
            history_page.check_history_elements()

            page_button = page.get_by_role("button", name="Page 1").first

            if page_button.count() > 0:
                page_button.click()
                expect(page.locator(history_page.locators.history_table)).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

            history_table = page.locator(history_page.locators.history_table)
            expect(history_table).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)
            file_name_cell = page.get_by_role("cell", name=re.compile(r"BMW.*DTC.*OFF.*NO_CS\.bin", re.I))

            if file_name_cell.count() == 0:
                file_name_cell = page.get_by_text(re.compile(r"BMW.*DTC.*OFF.*NO_CS\.bin", re.I))

            expect(file_name_cell.first).to_be_visible(timeout=Timeouts.History.FILE_ROW_VISIBLE)
            price_cell = page.get_by_role("cell", name="480 ₽")

            if price_cell.count() == 0:
                price_cell = page.get_by_text("480 ₽")

            expect(price_cell.first).to_be_visible(timeout=Timeouts.History.FILE_ROW_VISIBLE)

        with allure.step("Download file from history"):
            history_rows = page.locator(history_page.locators.history_table_row)

            if history_rows.count() > 0:
                first_row = history_rows.first
                expect(first_row).to_be_visible(timeout=Timeouts.History.FILE_ROW_VISIBLE)

                download_link = first_row.locator(history_page.locators.history_download_link)

                if download_link.count() == 0:
                    download_link = first_row.locator("a[href*='download']")

                if download_link.count() > 0:
                    expect(download_link.first).to_be_visible(timeout=Timeouts.History.DOWNLOAD_LINK_VISIBLE)

                    with page.expect_download() as download_info2:
                        download_link.first.click()

                    download2 = download_info2.value
                    assert download2 is not None, "Download from history should be triggered"

    @pytest.mark.skip(reason="Skipping test due to known issue with payment modal")
    @allure.story("Payment Processing")
    @allure.title("Test that top-up balance option appears when user has zero balance")
    @pytest.mark.upload
    @pytest.mark.validation
    def test_zero_balance_payment_hover_and_top_up_option(self, authenticated_user_zero_balance):
        vehicle_type = "Car"
        page = authenticated_user_zero_balance
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file("BMW.bin")

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, "BMW, MINI", "Diesel engines", "Bosch EDC16")

        with allure.step("Search for solutions and select Stage2"):
            upload_page.search_solutions(wait_time=Timeouts.Animation.STANDARD // 1000)
            upload_page.verify_solutions_found(min_count=3)

            upload_page.select_solution_by_name("Stage2 2880 ₽")

            cashback_toggle = page.locator(upload_page.locators.cashback_toggle)

            if cashback_toggle.count() > 0:
                cashback_toggle.first.click()

            order_cash = page.locator(upload_page.locators.order_cash)
            if order_cash.count() > 0:
                order_cash.click()

        with allure.step("Apply order and verify payment modal"):
            order_apply_btn = page.locator(upload_page.locators.order_apply_button)
            expect(order_apply_btn).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            attach_element_screenshot(order_apply_btn, "Order apply button")

            order_apply_btn.click()
            upload_page.wait_standard()

            need_pay_modal = page.locator(upload_page.locators.need_pay_modal)
            expect(need_pay_modal).to_be_visible(timeout=Timeouts.Modal.APPEAR)
            attach_element_screenshot(need_pay_modal, "Payment modal")

            balance_message = page.get_by_text("Чтобы продолжить, пополните баланс на 3600₽")
            expect(balance_message.first).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)
            attach_element_screenshot(balance_message.first, "Balance message")

        with allure.step("Open payment methods panel"):
            payment_need_modal_pay_btn = page.locator(upload_page.locators.payment_need_modal_pay_btn)
            expect(payment_need_modal_pay_btn).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
            attach_element_screenshot(payment_need_modal_pay_btn, "Payment modal pay button")

            payment_need_modal_pay_btn.click()
            upload_page.wait_standard()

            payment_methods_panel = page.locator(upload_page.locators.payment_methods_panel)
            expect(payment_methods_panel).to_be_visible(timeout=Timeouts.Modal.APPEAR)
            attach_element_screenshot(payment_methods_panel, "Payment methods panel")

            payment_amount_input = page.locator(upload_page.locators.payment_amount)
            expect(payment_amount_input).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)
            attach_element_screenshot(payment_amount_input, "Payment amount input")

            payment_pay_btn = page.locator(upload_page.locators.payment_pay_btn)
            expect(payment_pay_btn).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
            attach_element_screenshot(payment_pay_btn, "Payment pay button")

        with allure.step("Verify balance display and top-up option"):
            balance_display = page.locator(upload_page.locators.balance_display).filter(has_text="Баланс:0")
            if balance_display.count() > 0:
                expect(balance_display.first).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)

            top_up_text = page.get_by_text("Сумма:Пополнить")
            if top_up_text.count() > 0:
                expect(top_up_text.first).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)


    @allure.story("Error Handling")
    @allure.title("Test message displayed when no solutions are found by engine")
    @pytest.mark.upload
    @pytest.mark.validation
    def test_solutions_not_found_by_engine(self, authenticated_user_new):
        vehicle_type = "Car"
        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file("BMW.bin")

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, "BMW, MINI", "Petrol engines", "Bosch MEV17.2.1/MEV17.4")

        with allure.step("Search for solutions"):
            upload_page.search_solutions(wait_time=Timeouts.Animation.STANDARD // 1000, skip_button_check=True)
            task_info = page.get_by_text(re.compile(r"Номер задания:.*Файл.*BMW\.bin.*Размер.*Mb"))

            if task_info.count() > 0:
                expect(task_info.first).to_be_visible()
                attach_element_screenshot(task_info.first, "Task info")
                task_info.first.click()

        with allure.step("Verify no solutions message"):
            upload_page.verify_no_solutions_message()

    @allure.story("Error Handling")
    @allure.title("Test message displayed when no solutions are found by brand")
    @pytest.mark.upload
    @pytest.mark.validation
    def test_solutions_not_found_by_brand(self, authenticated_user_new):
        vehicle_type = "Car"
        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file("MBSprinter.bin")

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, "BMW, MINI", "Petrol engines", "Bosch MEV17.2.1/MEV17.4")

        with allure.step("Search for solutions"):
            upload_page.search_solutions(wait_time=Timeouts.Animation.STANDARD // 1000, skip_button_check=True)
            task_info = page.get_by_text(re.compile(r"Номер задания:.*Файл.*BMW\.bin.*Размер.*Mb"))

            if task_info.count() > 0:
                expect(task_info.first).to_be_visible()
                attach_element_screenshot(task_info.first, "Task info")
                task_info.first.click()

        with allure.step("Verify no solutions message"):
            upload_page.verify_no_solutions_message()



    @allure.story("Cashback Processing")
    @allure.title("Test file upload with cashback usage - two purchases")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_upload_with_cashback_usage(self, authenticated_user_new):
        vehicle_type = "Car"
        file_name = "BMW"
        brand = "BMW, MINI"
        engine = "Diesel engines"
        ecu = "Bosch EDC15"
        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file(f"{file_name}.bin")

        with allure.step("Purchase 1 - Select file parameters"):
            upload_page.select_file_parameters(vehicle_type, brand, engine, ecu)

        with allure.step("First purchase - Search for solutions"):
            upload_page.search_solutions(wait_time=2)
            solutions_found = upload_page.get_solutions_locator()

            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            upload_page.verify_solutions_found(min_count=1)

        with allure.step("First purchase - Select TUN solution and apply"):
            upload_page.select_solution_by_name("TUN 1920 ₽")
            upload_page.apply_order(wait_time=0)
            expect(page.locator(upload_page.locators.download_button)).to_be_visible(
                timeout=Timeouts.Download.BUTTON_VISIBLE)

            upload_page.wait_for_network_idle()
            upload_page.dismiss_currency_modal()

        with allure.step("First purchase - Verify cashback in profile"):
            profile_url = f"{BASE_URL}/app/profile"
            page.goto(profile_url)

            page.wait_for_load_state("networkidle")
            profile_page = ProfilePage(page)

            page.get_by_text("192 ₽").click()

            accumulated = profile_page.get_cashback_accumulated()
            assert "₽" in accumulated, f"Expected cashback accumulated with ₽, got {accumulated}"

            cashback_amount = int("".join(filter(str.isdigit, accumulated)))
            assert cashback_amount == 192, f"Cashback amount should be 192, got {cashback_amount}"

        with allure.step("Second purchase - Navigate to TUN page and reset form"):
            app_url = f"{BASE_URL}/app"
            page.goto(app_url)
            page.wait_for_load_state("networkidle")

        with allure.step("Second purchase - Upload file"):
            upload_page.upload_file("BMW.bin")

        with allure.step("Second purchase - Select file parameters and search solutions"):
            upload_page.select_file_parameters(vehicle_type, brand, engine, ecu)
            upload_page.search_solutions(wait_time=3)

            solutions_found = upload_page.get_solutions_locator()
            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            upload_page.verify_solutions_found(min_count=1)

        with allure.step("Second purchase - Select LSU OFF and apply order with Cashback"):
            upload_page.select_solution_by_name("LSU OFF 1480 ₽")
            upload_page.toggle_cashback_option()

            upload_page.focus_order_total_area()
            upload_page.dismiss_currency_modal()

            upload_page.apply_order(wait_time=0)
            expect(page.locator(upload_page.locators.download_button)).to_be_visible(timeout=Timeouts.Download.BUTTON_VISIBLE)
            upload_page.wait_for_network_idle()

        with allure.step("Second purchase - Verify cashback is used"):
            profile_url = f"{BASE_URL}/app/profile"
            page.goto(profile_url)
            page.wait_for_load_state("networkidle")
            profile_page = ProfilePage(page)

            page.get_by_text("0 ₽").click()

            accumulated = profile_page.get_cashback_accumulated()
            assert "₽" in accumulated, f"Expected cashback accumulated with ₽, got {accumulated}"

            cashback_amount = int("".join(filter(str.isdigit, accumulated)))
            assert cashback_amount == 0, f"Cashback amount should be 0 after second purchase, got {cashback_amount}"

        with allure.step("Verify history transactions"):
            history_url = f"{BASE_URL}/app/history"
            page.goto(history_url)
            page.wait_for_load_state("networkidle")

            # Wait for history table to be visible
            history_table = page.locator("table")
            expect(history_table).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

            cell1 = page.get_by_role("cell", name=re.compile(r"BMW__TUN__NO_CS\.bin")).locator("div")
            expect(cell1).to_be_visible(timeout=Timeouts.History.FILE_LINK_VISIBLE)
            cell1.click()

            cashback_text1 = page.get_by_text(re.compile(r"Зачисление кэшбэка \d+ ₽")).first
            expect(cashback_text1).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            cashback_text1.click()

            # Wait for second file to appear in history (may take longer)
            cell2 = page.get_by_role("cell", name=re.compile(r"BMW__LSU_OFF__NO_CS\.bin")).locator("div")
            expect(cell2).to_be_visible(timeout=Timeouts.History.FILE_LINK_VISIBLE)
            cell2.click()

            cashback_text2 = page.get_by_text(re.compile(r"Списание кэшбэка \d+ ₽")).first
            expect(cashback_text2).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            cashback_text2.click()

        with allure.step("Download file from history"):
            page.get_by_role("button", name="Инфо").first.click()
            page.locator(upload_page.locators.patch_title).click()

            page.get_by_text(re.compile(r"Задание №:.*ФайлBMW__LSU_OFF__NO_CS\.bin")).click()
            page.get_by_text("ПрименилиLSU OFF").click()

            download_path = Path(__file__).parent.parent.parent / "reports" / "patched_files"
            download_path.mkdir(parents=True, exist_ok=True)

            with page.expect_download() as download_info:
                page.get_by_role("button", name="скачать").click()

            download = download_info.value
            assert download is not None, "Download should be triggered"

            download_file_path = download_path / download.suggested_filename
            download.save_as(download_file_path)
            assert download_file_path.exists(), f"Downloaded file should exist at {download_file_path}"

            page.locator(upload_page.locators.close_icon).click()


    @allure.story("Payment Processing")
    @allure.title("Test that payment modal no appears when user has zero balance but cashback")
    @pytest.mark.upload
    @pytest.mark.validation
    def test_zero_balance_with_cashback_payment_modal(self, authenticated_user_without_balance_but_cashback):
        vehicle_type = "Car"
        page = authenticated_user_without_balance_but_cashback
        upload_page = UploadPage(page)

        with allure.step("Upload file and select solution"):
            upload_page.upload_file("BMW.bin")
            upload_page.select_file_parameters(vehicle_type, "BMW, MINI", "Diesel engines", "Bosch EDC16")
            upload_page.search_solutions(wait_time=2)

            solutions_found = upload_page.get_solutions_locator()
            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)

            upload_page.verify_solutions_found(min_count=1)
            upload_page.select_solution_by_index(2)

            cashback_toggle = page.locator(upload_page.locators.cashback_toggle)
            if cashback_toggle.count() > 0:
                cashback_toggle.first.click()

            order_cash = page.locator(upload_page.locators.order_cash)
            if order_cash.count() > 0:
                order_cash.click()

        with allure.step("Apply order and verify payment modal"):
            order_apply_btn = page.locator(upload_page.locators.order_apply_button)
            expect(order_apply_btn).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            order_apply_btn.click()
            upload_page.wait_standard()

            need_pay_modal = page.locator(upload_page.locators.need_pay_modal)
            expect(need_pay_modal).to_be_visible(timeout=Timeouts.Modal.APPEAR)
            attach_screenshot(page, "Payment modal with zero balance but cashback")
