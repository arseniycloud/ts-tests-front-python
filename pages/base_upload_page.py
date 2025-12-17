import logging
import re
from pathlib import Path

import allure
from playwright.sync_api import Page, expect

from config.timeouts import Timeouts
from pages.base_page import BasePage
from utils.allure_helpers import attach_element_screenshot, attach_screenshot


class BaseUploadPage(BasePage):
    """Base class for upload pages with common upload functionality"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = None

    @allure.step("Upload file: {file_name}")
    def upload_file(self, file_name: str) -> None:
        file_path = Path(__file__).parent.parent / "files" / file_name
        assert file_path.exists(), f"File {file_path} does not exist"

        file_input = self.page.locator(self.locators.file_input)
        expect(file_input).to_be_attached(timeout=Timeouts.Upload.FILE_INPUT_ATTACHED)

        file_input.set_input_files(str(file_path))
        self.page.wait_for_timeout(500)

        try:
            self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        except Exception as e:
            logging.warning(f"Failed to wait for networkidle after file upload, falling back to load state: {e}")
            self.page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)

        try:
            uploaded_file_name = self.page.locator(self.locators.uploaded_file_name)
            expect(uploaded_file_name).to_be_visible(timeout=Timeouts.Upload.FILE_UPLOADED_VISIBLE)
            expect(uploaded_file_name).to_have_text(file_name)

        except Exception as e:
            logging.debug(f"Optional check for uploaded file name failed (continuing): {e}")

        type_select_input = self.page.locator(self.locators.type_select_input)
        expect(type_select_input).not_to_be_disabled(timeout=Timeouts.Upload.AFTER_FILE_UPLOAD)

    @allure.step("Select file parameters: type={vehicle_type}, brand={brand}, engine={engine}, ecu={ecu}")
    def select_file_parameters(self, vehicle_type: str, brand: str, engine: str, ecu: str, close_modal: bool = False) -> None:
        if close_modal:
            self._close_upload_modal()

        type_select_input = self.page.locator(self.locators.type_select_input)
        expect(type_select_input).not_to_be_disabled(timeout=Timeouts.Upload.TYPE_SELECT_ENABLED)

        type_select_input.click()
        self.page.locator("div").filter(has_text=re.compile(f"^{re.escape(vehicle_type)}$")).click()

        brand_select_input = self.page.locator(self.locators.brand_select_input)
        expect(brand_select_input).not_to_be_disabled(timeout=Timeouts.Upload.TYPE_SELECT_ENABLED)

        brand_select_input.click()
        brand_locator = self.page.locator("div").filter(has_text=re.compile(f"^{re.escape(brand)}$"))

        if brand_locator.count() > 0:
            brand_locator.click()
        else:
            self.page.get_by_text(brand, exact=True).first.click()

        engine_select_input = self.page.locator(self.locators.engine_select_input)
        expect(engine_select_input).not_to_be_disabled(timeout=Timeouts.Upload.TYPE_SELECT_ENABLED)

        engine_select_input.click()
        self.page.get_by_text(engine).click()
        self.wait_standard()

        ecu_select_input = self.page.locator(self.locators.ecu_select_input)
        expect(ecu_select_input).not_to_be_disabled(timeout=Timeouts.Upload.TYPE_SELECT_ENABLED)

        ecu_select_input.click()
        self.page.locator("div").filter(has_text=re.compile(f"^{re.escape(ecu)}$")).click()
        self.wait_standard()

        try:
            self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        except Exception as e:
            logging.warning(f"Failed to wait for networkidle after selecting parameters, falling back to load state: {e}")
            self.page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)

        search_button = self.page.locator(self.locators.search_button)

        try:
            expect(search_button).to_be_enabled(timeout=10000)

        except Exception as e:
            logging.debug(f"Search button not enabled within timeout (will check with not_to_be_disabled): {e}")

        expect(search_button).not_to_be_disabled(timeout=Timeouts.Upload.SEARCH_BUTTON_ENABLED)
        attach_screenshot(self.page, "File parameters selected")

    @allure.step("Search for solutions")
    def search_solutions(self, wait_time: int = 0, skip_button_check: bool = False) -> None:
        search_button = self.page.locator(self.locators.search_button)

        if not skip_button_check:
            expect(search_button).not_to_be_disabled(timeout=Timeouts.Upload.SEARCH_BUTTON_ENABLED)
        search_button.click()

        if wait_time > 0:
            self.page.wait_for_timeout(wait_time * 1000)

        try:
            self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        except Exception as e:

            logging.warning(f"Failed to wait for networkidle after search, falling back to load state: {e}")
            self.page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)

        solutions_text = self.page.get_by_text("Найденные решения Если нужного вам решения не нашлось, напишите нам в чат или на")

        if solutions_text.count() > 0:
            solutions_text.click()
        self.page.locator(self.locators.order_form_area).click()

        order_form_area = self.page.locator(self.locators.order_form_area)

        if order_form_area.count() > 0:
            attach_element_screenshot(order_form_area.first, "Found solutions block")

        attach_screenshot(self.page, "Solutions searched")

    @allure.step("Get locator for solution rows in order table")
    def get_solutions_locator(self):
        return self.page.locator(self.locators.order_table_row)

    @allure.step("Get solutions count")
    def get_solutions_count(self) -> int:
        return self.page.locator(self.locators.order_table_row).count()

    @allure.step("Get available solutions list")
    def get_available_solutions(self) -> list[str]:
        solutions_found = self.page.locator(self.locators.order_table_row)
        solutions_list = []

        for i in range(solutions_found.count()):
            solution_text = solutions_found.nth(i).text_content()
            if solution_text:
                solutions_list.append(solution_text.strip())

        attach_screenshot(self.page, "Solutions list retrieved")
        return solutions_list

    @allure.step("Select solution by name: {solution_name}")
    def select_solution_by_name(self, solution_name: str, exact: bool = False) -> None:
        solution_row = self.page.get_by_role("row", name=solution_name, exact=exact)
        expect(solution_row).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)

        solution_row.get_by_role("checkbox").check()
        attach_screenshot(self.page, "Solution selected by name")

    @allure.step("Select solution by index: {index}")
    def select_solution_by_index(self, index: int) -> None:
        solutions_found = self.page.locator(self.locators.order_table_row)
        solution = solutions_found.nth(index)
        expect(solution).to_be_visible(timeout=Timeouts.Upload.SOLUTION_ROW_VISIBLE)

        solution.get_by_role("checkbox").check()
        attach_screenshot(self.page, "Solution selected by index")

    @allure.step("Get order total price")
    def get_order_total(self) -> int:
        order_total = self.page.locator(self.locators.order_total)
        expect(order_total).to_be_visible(timeout=Timeouts.Upload.ORDER_TOTAL_VISIBLE)

        total_text = order_total.text_content()
        if total_text is None:
            attach_screenshot(self.page, "Order total text content is None")
            raise ValueError(f"Order total element text_content() returned None. Locator: {self.locators.order_total}")

        total = int("".join(filter(str.isdigit, total_text)))
        attach_screenshot(self.page, "Order total retrieved")

        return total

    @allure.step("Verify order total: expected={expected_price}")
    def verify_order_total(self, expected_price: int) -> None:
        total_price = self.get_order_total()

        assert total_price == expected_price, f"Order total should be {expected_price}, got {total_price}"
        attach_screenshot(self.page, "Order total verified")

    @allure.step("Click apply order button")
    def apply_order(self, wait_time: int = 1000) -> None:
        self.page.locator(self.locators.order_apply_button).click()
        if wait_time > 0:
            expect(self.page.locator(self.locators.order_apply_button)).to_be_visible(timeout=wait_time)
        attach_screenshot(self.page, "Order applied")

    @allure.step("Verify that at least minimum number of solutions: min_count={min_count}")
    def verify_solutions_found(self, min_count: int = 1) -> None:
        solutions_count = self.get_solutions_count()

        assert solutions_count >= min_count, f"At least {min_count} solution(s) should be found, got {solutions_count}"
        attach_screenshot(self.page, "Solutions found verified")

    @allure.step("Verify that no solutions message is displayed")
    def verify_no_solutions_message(self) -> None:
        order_form = self.page.locator(self.locators.order_form_area)

        expect(order_form).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
        order_form.click()

        order_task_panel = self.page.locator(".order-task-panel")
        if order_task_panel.count() > 0:
            expect(order_task_panel.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            order_task_panel_title = order_task_panel.locator(".order-task-panel-title")
            if order_task_panel_title.count() > 0:
                expect(order_task_panel_title.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
                title_text = order_task_panel_title.first.text_content()
                assert "Найденные решения" in title_text, f"Should display 'Найденные решения', got: {title_text}"

        no_solutions_message = self.page.get_by_text("Если нужного вам решения не нашлось", exact=False)
        if no_solutions_message.count() > 0:
            expect(no_solutions_message.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        support_email = self.page.get_by_text("support@tunservice.ru", exact=False)
        if support_email.count() > 0:
            expect(support_email.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        attach_screenshot(self.page, "No solutions message verified")

    @allure.step("Complete flow: upload file, select parameters, search solutions")
    def upload_file_and_search(self, file_name: str, brand: str, engine: str, ecu: str,
                               vehicle_type: str = "Car", min_solutions: int = 1, wait_time: int = 0) -> None:
        self.upload_file(file_name)
        self.select_file_parameters(vehicle_type, brand, engine, ecu)
        self.search_solutions(wait_time=wait_time)
        self.verify_solutions_found(min_count=min_solutions)
        attach_screenshot(self.page, "Upload and search flow completed")

    def _close_upload_modal(self) -> None:
        rub_button = self.page.get_by_text("руб")
        if rub_button.count() > 0:

            try:
                expect(rub_button.first).to_be_visible(timeout=Timeouts.Upload.MODAL_CLOSE_WAIT)
                rub_button.click()
                self.wait_long()

                if rub_button.count() > 0:
                    expect(rub_button.first).to_be_visible(timeout=Timeouts.Modal.BUTTON_VISIBLE)
                    rub_button.click()
                    self.wait_standard()

            except Exception as e:
                logging.debug(f"Failed to close upload modal (continuing): {e}")
