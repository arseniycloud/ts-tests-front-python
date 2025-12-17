import re

import allure
import pytest
from playwright.sync_api import expect

from pages.try_upload_page import TryUploadPage
from utils.allure_helpers import attach_element_screenshot


@allure.epic("Try Upload")
@allure.feature("Try Upload Page")
@allure.title("Try Upload Page - File Processing")
class TestTryUploadPageElements:

    @allure.story("File Upload")
    @allure.title("Test file upload, search and price calculation for Mazda")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_file_upload_mazda(self, page):
        vehicle_type = "Car"
        brand = "Mazda"
        engine = "Petrol engines"
        ecu = "Denso SH72xxx"

        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()

        try_upload_page.reload_page()
        try_upload_page.wait_for_network_idle()

        with allure.step("Upload file"):
            try_upload_page.upload_file(f"{brand}.bin")

        with allure.step("Select file parameters"):
            try_upload_page.select_file_parameters(vehicle_type, brand, engine, ecu)

        with allure.step("Search for solutions"):
            try_upload_page.search_solutions()
            try_upload_page.verify_solutions_found(min_count=5)

        with allure.step("Select solutions and verify prices"):
            try_upload_page.select_solution_by_index(1)
            total_price = try_upload_page.get_order_total()
            assert total_price > 0, f"Order total should be greater than 0, got {total_price}"

        with allure.step("Verify not authenticated panel is visible"):
            try_upload_page.verify_not_auth_panel()

    @allure.story("File Upload")
    @allure.title("Test file upload, search and price calculation for MBSprinter")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_file_upload_mbsprinter(self, page):
        vehicle_type = "Car"
        file_name = "MBSprinter"
        brand = "Mercedes"
        engine = "Diesel engine"
        ecu = "Bosch EDC16"
        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()
        try_upload_page.wait_for_network_idle()

        with allure.step("Upload file"):
            try_upload_page.upload_file(f"{file_name}.bin")

        with allure.step("Select file parameters"):
            try_upload_page.select_file_parameters(vehicle_type, brand, engine, ecu)

        with allure.step("Search for solutions"):
            try_upload_page.search_solutions(wait_time=5)
            try_upload_page.verify_solutions_found(min_count=2)

        with allure.step("Select solutions and verify prices"):
            try_upload_page.select_solution_by_index(1)
            total_price = try_upload_page.get_order_total()
            assert total_price > 0, f"Order total should be greater than 0, got {total_price}"

    @allure.story("File Upload")
    @allure.title("Test file upload, search and price calculation for BMW")
    @pytest.mark.upload
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_file_upload_bmw(self, page):
        vehicle_type = "Car"
        file_name = "BMW"
        brand = "BMW, MINI"
        engine = "Diesel engines"
        ecu = "Bosch EDC16"

        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()

        try_upload_page.reload_page()
        try_upload_page.wait_for_network_idle()

        with allure.step("Upload file"):
            try_upload_page.upload_file(f"{file_name}.bin")

        with allure.step("Select file parameters"):
            try_upload_page.select_file_parameters(vehicle_type, brand, engine, ecu)

        with allure.step("Search for solutions"):
            try_upload_page.search_solutions(wait_time=5)
            try_upload_page.verify_solutions_found(min_count=2)

        with allure.step("Select solutions and verify prices"):
            try_upload_page.select_solution_by_index(1)
            try_upload_page.verify_order_total(expected_price=1860)

            try_upload_page.select_solution_by_index(3)
            try_upload_page.verify_order_total(expected_price=2400)

            try_upload_page.select_solution_by_index(7)
            try_upload_page.verify_order_total(expected_price=3600)

    @allure.story("Error Handling")
    @allure.title("Test message displayed when no solutions are found by engine")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_solutions_not_found_by_engine(self, page):
        vehicle_type = "Car"
        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()

        try_upload_page.reload_page()
        try_upload_page.wait_for_network_idle()

        with allure.step("Upload file"):
            try_upload_page.upload_file("BMW.bin")

        with allure.step("Select file parameters"):
            try_upload_page.select_file_parameters(vehicle_type, "BMW, MINI", "Petrol engines",
                                                   "Bosch MEV17.2.1/MEV17.4")

        with allure.step("Search for solutions"):
            try_upload_page.search_solutions(wait_time=3, skip_button_check=True)
            task_info = page.get_by_text(re.compile(r"Номер задания:.*Файл.*BMW\.bin.*Размер.*Mb"))
            if task_info.count() > 0:
                expect(task_info.first).to_be_visible()
                attach_element_screenshot(task_info.first, "Task info")
                task_info.first.click()

        with allure.step("Verify no solutions message"):
            try_upload_page.verify_no_solutions_message()

    @allure.story("Error Handling")
    @allure.title("Test message displayed when no solutions are found by brand")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_solutions_not_found_by_brand(self, page):
        vehicle_type = "Car"
        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()


        with allure.step("Upload file"):
            try_upload_page.upload_file("MBSprinter.bin")

        with allure.step("Select file parameters"):
            try_upload_page.select_file_parameters(vehicle_type, "BMW, MINI", "Petrol engines",
                                                   "Bosch MEV17.2.1/MEV17.4")

        with allure.step("Search for solutions"):
            try_upload_page.search_solutions(wait_time=3, skip_button_check=True)
            task_info = page.get_by_text(re.compile(r"Номер задания:.*Файл.*BMW\.bin.*Размер.*Mb"))

            if task_info.count() > 0:
                expect(task_info.first).to_be_visible()
                attach_element_screenshot(task_info.first, "Task info")
                task_info.first.click()

        with allure.step("Verify no solutions message"):
            try_upload_page.verify_no_solutions_message()

    @allure.story("Page Elements")
    @allure.title("Test header elements for unregistered users")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_header_elements(self, page):
        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()
        try_upload_page.reload_page()
        try_upload_page.wait_for_network_idle()

        with allure.step("Check header elements"):
            try_upload_page.check_header_elements()

    @allure.story("Page Elements")
    @allure.title("Test upload form elements")
    @pytest.mark.upload
    @pytest.mark.regression
    @pytest.mark.validation
    def test_upload_form_elements(self, page):
        try_upload_page = TryUploadPage(page)
        try_upload_page.navigate_to_try_upload()
        try_upload_page.wait_for_network_idle()

        with allure.step("Check upload form elements"):
            try_upload_page.check_upload_form_elements()
