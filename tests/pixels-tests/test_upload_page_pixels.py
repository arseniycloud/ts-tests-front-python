import re

import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from pages.upload_page import UploadPage


@allure.epic("Visual Regression")
@allure.feature("Upload Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestUploadPageVisualRegression:

    @allure.title("No solutions found message snapshot")
    @pytest.mark.pixel_test
    def test_no_solutions_found_message(self, authenticated_user_new, assert_snapshot_with_threshold):
        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file("BMW.bin")

        with allure.step("Select file parameters that won't find solutions"):
            upload_page.select_file_parameters("Car", "BMW, MINI", "Petrol engines", "Bosch MEV17.2.1/MEV17.4")

        with allure.step("Search for solutions"):
            upload_page.search_solutions(wait_time=Timeouts.Animation.STANDARD // 1000, skip_button_check=True)
            no_solutions_message = page.get_by_text("Если нужного вам решения не нашлось", exact=False)
            expect(no_solutions_message).to_be_visible(timeout=2000)

        with allure.step("Capture solutions block"):
            # Verify no solutions message is visible
            no_solutions_message = page.get_by_text("Если нужного вам решения не нашлось", exact=False)
            expect(no_solutions_message).to_be_visible(timeout=5000)
            expect(no_solutions_message).to_be_visible(timeout=500)

            # Wait for page to fully load and stabilize
            page.wait_for_load_state("networkidle", timeout=30000)

            # Wait for header to be stable
            header_container = page.locator("[data-test-id='header_container']")
            expect(header_container).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            # Additional wait for animations/rendering to complete
            page.wait_for_timeout(1000)

            # Capture entire solutions block (wrap_main)
            wrap_main = page.locator(upload_page.locators.wrap_main)
            expect(wrap_main).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            # Scroll element into view, aligning to top of viewport
            wrap_main.scroll_into_view_if_needed()

            # Scroll much higher to ensure the block is fully visible with padding from the top
            page.evaluate("window.scrollBy(0, -2000)")

            # Wait for scroll to complete and page to stabilize
            page.wait_for_timeout(500)
            expect(wrap_main).to_be_visible(timeout=1000)

            # Wait for header to be stable after scroll
            expect(header_container).to_be_visible(timeout=1000)
            page.wait_for_timeout(500)

            # Move mouse to task-block to stabilize cursor position and avoid hover effects on other elements
            task_block = page.locator(".task-block").first
            box = task_block.bounding_box()

            if box:
                page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            else:
                # If task-block is not visible, move mouse to a safe position (top-left corner)
                page.mouse.move(0, 0)
            page.wait_for_timeout(200)

            # Elements to mask - use CSS selectors for full page screenshot
            mask_elements = [
                "[data-test-id='profile_link']",
                ".task-number",
                "[data-test-id='header_container']",
                ".t-header"
            ]

            # Capture full page screenshot to allow masking of header outside wrap_main
            assert_snapshot_with_threshold(page, threshold=0.15, mask_elements=mask_elements)

    @allure.title("Upload page with solutions found snapshot")
    @pytest.mark.pixel_test
    def test_upload_page_with_solutions(self, authenticated_user_new, assert_snapshot_with_threshold):
        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file("BMW.bin")

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters("Car", "BMW, MINI", "Diesel engines", "Bosch EDC16")

        with allure.step("Search for solutions"):
            upload_page.search_solutions(wait_time=2)
            solutions_found = upload_page.get_solutions_locator()
            solutions_found.first.wait_for(state="visible", timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            upload_page.verify_solutions_found(min_count=1)

        with allure.step("Capture solutions table"):
            order_table = page.locator(upload_page.locators.order_table)
            expect(order_table).to_be_visible(timeout=500)

            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(order_table.screenshot(), threshold=0.15)

    @allure.title("Upload page after file upload snapshot")
    @pytest.mark.pixel_test
    def test_upload_page_after_file_upload(self, authenticated_user_new, assert_snapshot_with_threshold):
        page = authenticated_user_new
        upload_page = UploadPage(page)

        with allure.step("Upload file"):
            upload_page.upload_file("BMW.bin")
            uploaded_file_name = page.locator(upload_page.locators.uploaded_file_name)
            expect(uploaded_file_name).to_be_visible(timeout=1000)

        with allure.step("Capture upload form with file uploaded"):
            upload_form = page.locator(upload_page.locators.upload_form)
            expect(upload_form).to_be_visible(timeout=500)

            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(upload_form, threshold=0.15)


    @allure.title("Error codes verification dialog snapshot (DTC OFF)")
    @pytest.mark.pixel_test
    def test_error_codes_dialog_dtc(self, authenticated_user_new, assert_snapshot_with_threshold):
        page = authenticated_user_new
        upload_page = UploadPage(page)

        page.goto(f"{BASE_URL}/app")
        page.wait_for_load_state("networkidle")

        with allure.step("Upload BMW file"):
            upload_page.upload_file("BMW.bin")

        with allure.step("Select file parameters"):
            upload_page.select_file_parameters("Car", "BMW, MINI", "Diesel engines", "Bosch EDC16")

        with allure.step("Search for solutions"):
            upload_page.search_solutions(wait_time=2)
            solutions_found = upload_page.get_solutions_locator()
            solutions_found.first.wait_for(state="visible", timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            upload_page.verify_solutions_found(min_count=1)

        with allure.step("Select DTC OFF solution and enter error codes"):
            upload_page.select_dtc_off_solution()
            upload_page.enter_error_codes("255D, 245C")

            page.wait_for_load_state("networkidle")

            # Wait for dialog to appear
            detected_errors = page.locator("div").filter(has_text=re.compile(r"Обнаружены активные ошибки|Найдены активные ошибки"))
            expect(detected_errors.first).to_be_visible(timeout=1000)

        with allure.step("Capture DTC codes HEX tab"):
            expect(detected_errors.first).to_be_visible(timeout=Timeouts.Modal.CONTENT_VISIBLE)
            expect(detected_errors.first).to_be_visible(timeout=500)

            # Click on DTC codes HEX tab to show the codes
            dtc_codes_tab = page.get_by_text("DTC кодыHEX")
            expect(dtc_codes_tab).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
            dtc_codes_tab.click()
            expect(dtc_codes_tab).to_be_visible(timeout=500)

            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)

            # Screenshot the DTC codes HEX element/tab content
            assert_snapshot_with_threshold(dtc_codes_tab, threshold=0.15)



    @allure.title("DTC purchase no errors found snapshot")
    @pytest.mark.pixel_test
    def test_warning_dialog_dtc_purchase(self, authenticated_user_new, assert_snapshot_with_threshold):

        page = authenticated_user_new
        upload_page = UploadPage(page)

        page.goto(f"{BASE_URL}/app")
        page.wait_for_load_state("networkidle")

        with allure.step("Upload file and search solutions"):
            upload_page.upload_file("BMW.bin")
            upload_page.select_file_parameters("Car", "BMW, MINI", "Diesel engines", "Bosch EDC16")
            upload_page.search_solutions(wait_time=2)
            solutions_found = upload_page.get_solutions_locator()
            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            upload_page.verify_solutions_found(min_count=1)

        with allure.step("Select DTC OFF solution and enter error codes"):
            upload_page.select_dtc_off_solution()

            # Use enter_error_codes method which handles button enabling properly
            upload_page.enter_error_codes("0299, 0171")

            # Add wait after enter_error_codes for dialog to appear
            page.wait_for_load_state("networkidle")

            # Wait for dialog to appear
            dtc_codes_tab = page.get_by_text("DTC кодыHEX")
            expect(dtc_codes_tab).to_be_visible(timeout=2000)

        with allure.step("Capture DTC codes HEX tab"):
            # Wait for DTC codes HEX tab to appear after error codes verification
            # Use flexible search - try to find tab directly first
            expect(dtc_codes_tab).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
            dtc_codes_tab.click()
            expect(dtc_codes_tab).to_be_visible(timeout=500)

            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)

            # Screenshot the DTC codes HEX element/tab content
            assert_snapshot_with_threshold(dtc_codes_tab, threshold=0.15)
