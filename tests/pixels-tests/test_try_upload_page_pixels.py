import allure
import pytest
from playwright.sync_api import expect

from config.timeouts import Timeouts
from pages.try_upload_page import TryUploadPage


@allure.epic("Visual Regression")
@allure.feature("Try Upload Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestTryUploadPageVisualRegression:

    @allure.title("Try upload - Solutions found for Mazda snapshot")
    @pytest.mark.pixel_test
    def test_solutions_found_mazda(self, page, assert_snapshot_with_threshold):
        """Test solutions table when solutions are found for Mazda file"""
        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()

        with allure.step("Upload Mazda file"):
            try_upload_page.upload_file("Mazda.bin")

        with allure.step("Select file parameters"):
            try_upload_page.select_file_parameters("Car", "Mazda", "Petrol engines", "Denso SH72xxx")

        with allure.step("Search for solutions"):
            try_upload_page.search_solutions(wait_time=2)
            solutions_found = try_upload_page.get_solutions_locator()
            solutions_found.first.wait_for(state="visible", timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)
            try_upload_page.verify_solutions_found(min_count=1)

        with allure.step("Capture order form area with solutions"):
            order_form_area = page.locator(try_upload_page.locators.order_form_area)
            expect(order_form_area).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(order_form_area.screenshot(), threshold=0.15)

    @allure.title("Try upload - No solutions found snapshot")
    @pytest.mark.pixel_test
    def test_no_solutions_found(self, page, assert_snapshot_with_threshold):
        """Test message when no solutions are found"""
        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()

        with allure.step("Upload file"):
            try_upload_page.upload_file("BMW.bin")

        with allure.step("Select file parameters that won't find solutions"):
            try_upload_page.select_file_parameters("Car", "BMW, MINI", "Petrol engines", "Bosch MEV17.2.1/MEV17.4")

        with allure.step("Search for solutions"):
            try_upload_page.search_solutions(wait_time=Timeouts.Animation.STANDARD // 1000, skip_button_check=True)
            no_solutions_message = page.get_by_text("Если нужного вам решения не нашлось", exact=False)
            expect(no_solutions_message).to_be_visible(timeout=2000)

        with allure.step("Capture no solutions message"):
            order_form = page.locator(try_upload_page.locators.order_form_area)
            order_form.click()
            no_solutions_message = page.get_by_text("Если нужного вам решения не нашлось", exact=False)
            expect(no_solutions_message).to_be_visible(timeout=500)
            no_solutions_message.wait_for(state="visible", timeout=5000)
            expect(no_solutions_message).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(no_solutions_message, threshold=0.2)

    @allure.title("Try upload - DTC modal snapshot")
    @pytest.mark.pixel_test
    def test_dtc_modal(self, page, assert_snapshot_with_threshold):
        """Test DTC codes modal dialog"""
        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()

        with allure.step("Upload Mazda file"):
            try_upload_page.upload_file("Mazda.bin")

        with allure.step("Select file parameters"):
            try_upload_page.select_file_parameters("Car", "Mazda", "Petrol engines", "Denso SH72xxx")

        with allure.step("Search for solutions"):
            try_upload_page.search_solutions(wait_time=2)
            solutions_found = try_upload_page.get_solutions_locator()
            expect(solutions_found.first).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)

        with allure.step("Click on DTC OFF button to open modal"):
            dtc_button = page.get_by_role("button", name="ОТКЛЮЧИТЬ DTC")
            dtc_button.first.click()
            dtc_modal = page.locator(".dtc-modal")
            expect(dtc_modal).to_be_visible(timeout=500)

        with allure.step("Capture DTC modal"):
            dtc_modal.wait_for(state="visible", timeout=Timeouts.Modal.APPEAR)
            expect(dtc_modal).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(dtc_modal, threshold=0.15)
