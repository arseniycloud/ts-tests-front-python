import logging
import re

import allure
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.history_locators import HistoryLocators
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot


class HistoryPage(BasePage):
    """History page of TunService website"""

    BUTTON_FIRST_PAGE = "First Page"
    BUTTON_PREVIOUS_PAGE = "Previous Page"
    BUTTON_NEXT_PAGE = "Next Page"
    BUTTON_LAST_PAGE = "Last Page"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.locators = HistoryLocators()

    @allure.step("Navigate to history page (/app/history)")
    def navigate_to_history(self):
        history_url = f"{BASE_URL}/app/history"

        try:
            self.page.goto(history_url, wait_until="domcontentloaded", timeout=Timeouts.PageLoad.DOMCONTENTLOADED_LONG)

        except Exception as e:
            # Handle navigation interruption (e.g., redirect to payment)
            logging.warning(f"Navigation to history page interrupted, waiting for domcontentloaded: {e}")
            self.page.wait_for_load_state("domcontentloaded", timeout=Timeouts.PageLoad.DOMCONTENTLOADED_LONG)

        self.wait_for_page_load()

        attach_screenshot(self.page, "History page loaded")

    @allure.step("Check history page elements are visible")
    def check_history_elements(self):
        expect(self.page.locator(self.locators.page_container)).to_be_visible()
        expect(self.page.locator(self.locators.page_body)).to_be_visible()

        attach_screenshot(self.page, "History elements verified")

    @allure.step("Check history page header elements are visible")
    def check_history_header_elements(self):
        header_container = self.page.locator(self.locators.header_container)
        expect(header_container).to_be_visible()

        menu_block = self.page.locator(self.locators.menu_block)
        # On tablet/mobile menu may be hidden, try to open it first
        if not menu_block.is_visible():
            mobile_menu_btn = self.page.locator(".mobile-menu-btn, .t-vertical-menu-ss").first

            if mobile_menu_btn.count() > 0:

                try:
                    if mobile_menu_btn.is_visible(timeout=2000):
                        mobile_menu_btn.click()
                        self.wait_short()

                except Exception as e:
                    logging.debug(f"Failed to open mobile menu (continuing): {e}")

            # If still not visible, check if menu exists in DOM (acceptable for tablet)
            if not menu_block.is_visible(timeout=2000):
                # Menu exists in DOM but is hidden - this is acceptable for tablet/mobile
                # Just verify it exists
                assert menu_block.count() > 0, "Menu block should exist in DOM"
                return

        expect(menu_block).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        history_link = self.page.locator(self.locators.history_link)
        if history_link.count() > 0:
            expect(history_link.first).to_be_visible(timeout=Timeouts.History.HISTORY_LINK_VISIBLE)

        attach_screenshot(self.page, "History header elements verified")

    @allure.step("Check history table is visible")
    def check_history_table(self):
        history_table = self.page.locator(self.locators.history_table)

        if history_table.count() > 0:
            expect(history_table.first).to_be_visible(timeout=Timeouts.History.HISTORY_TABLE_VISIBLE)

        attach_screenshot(self.page, "History table verified")

    @allure.step("Check history items count")
    def get_history_items_count(self) -> int:
        history_items = self.page.locator(self.locators.history_item)
        history_rows = self.page.locator(self.locators.history_table_row)
        items_count = history_items.count()
        rows_count = history_rows.count()

        count = max(items_count, rows_count)
        attach_screenshot(self.page, "History items counted")
        return count

    @allure.step("Check if empty state is visible when no history items")
    def check_empty_state(self):
        empty_state = self.page.locator(self.locators.empty_state)

        if empty_state.count() > 0:
            expect(empty_state.first).to_be_visible(timeout=Timeouts.History.EMPTY_STATE_VISIBLE)

        attach_screenshot(self.page, "Empty state verified")

    @allure.step("Check pagination is visible")
    def check_pagination_visible(self):
        pagination = self.page.locator(self.locators.pagination)

        if pagination.count() > 0:
            expect(pagination.first).to_be_visible(timeout=Timeouts.History.PAGINATION_VISIBLE)

        attach_screenshot(self.page, "Pagination verified")

    @allure.step("Get count of pagination buttons count")
    def get_pagination_buttons_count(self) -> int:
        pagination = self.page.locator(self.locators.pagination)

        if pagination.count() == 0:
            return 0

        buttons = pagination.locator("button")
        count = buttons.count()

        attach_screenshot(self.page, "Pagination buttons counted")
        return count

    @allure.step("Check if pagination navigation buttons are present")
    def check_pagination_buttons(self):
        pagination = self.page.locator(self.locators.pagination)

        if pagination.count() == 0:
            return

        first_btn = self.page.get_by_role("button", name=self.BUTTON_FIRST_PAGE).first
        prev_btn = self.page.get_by_role("button", name=self.BUTTON_PREVIOUS_PAGE).first
        next_btn = self.page.get_by_role("button", name=self.BUTTON_NEXT_PAGE).first
        last_btn = self.page.get_by_role("button", name=self.BUTTON_LAST_PAGE).first

        buttons_found = []

        if first_btn.count() > 0:
            buttons_found.append("first")

        if prev_btn.count() > 0:
            buttons_found.append("prev")

        if next_btn.count() > 0:
            buttons_found.append("next")

        if last_btn.count() > 0:
            buttons_found.append("last")

        assert len(buttons_found) > 0, "At least one pagination button should be present"

        attach_screenshot(self.page, "Pagination buttons verified")

    def _parse_page_number(self, text: str | None) -> int | None:
        """Parse page number from text"""

        if not text:
            return None

        try:
            return int(text.strip())

        except ValueError:
            return None

    def _get_current_page_from_buttons(self) -> int | None:
        """Get current page number from pagination buttons"""
        page_buttons = self.page.get_by_role("button").filter(has=self.page.locator("[aria-current='page']"))

        if page_buttons.count() > 0:
            aria_label = page_buttons.first.get_attribute("aria-label")

            if aria_label and aria_label.startswith("Page "):
                return self._parse_page_number(aria_label.replace("Page ", ""))

        page_numbers = self.page.locator(self.locators.pagination_page_number)
        count = page_numbers.count()
        for i in range(count):
            page_btn = page_numbers.nth(i)

            if page_btn.get_attribute("aria-current") == "page":
                page_text = page_btn.text_content()
                return self._parse_page_number(page_text)

        return None

    @allure.step("Get current page number from pagination")
    def get_current_page_number(self) -> int:
        page_num = self._get_current_page_from_buttons()
        if page_num is not None:
            return page_num

        current_page = self.page.locator(self.locators.pagination_current_page)

        if current_page.count() > 0:
            page_text = current_page.first.text_content()
            page_num = self._parse_page_number(page_text)

            if page_num is not None:
                return page_num

        page_num = 1
        attach_screenshot(self.page, "Current page number retrieved")
        return page_num

    def _get_max_page_from_buttons(self) -> int:
        """Get maximum page number from pagination buttons"""
        page_numbers = self.page.locator(self.locators.pagination_page_number)
        max_page = 1

        count = page_numbers.count()
        for i in range(count):
            page_btn = page_numbers.nth(i)
            page_text = page_btn.text_content()
            page_num = self._parse_page_number(page_text)

            if page_num is not None:
                max_page = max(max_page, page_num)

        return max_page

    def _get_total_from_pagination_info(self) -> int | None:
        """Get total pages count from pagination info text"""
        pagination_info = self.page.locator(self.locators.pagination_info)

        if pagination_info.count() == 0:
            return None

        info_text = pagination_info.first.text_content()

        if not info_text:
            return None

        numbers = re.findall(r'\d+', info_text)

        if len(numbers) < 2:
            return None

        try:
            total = int(numbers[-1])
            return total if total > 0 else None

        except ValueError:
            return None

    @allure.step("Get total number of pages from pagination")
    def get_total_pages_count(self) -> int:
        total_from_info = self._get_total_from_pagination_info()

        if total_from_info is not None:
            attach_screenshot(self.page, "Total pages count retrieved")
            return total_from_info

        total = self._get_max_page_from_buttons()
        attach_screenshot(self.page, "Total pages count retrieved")

        return total

    def _click_pagination_button(self, button_name: str):
        """Click pagination button if it's visible and enabled"""
        button = self.page.get_by_role("button", name=button_name).first

        if button.count() > 0:
            expect(button).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

            if not button.is_disabled():
                button.click()
                self.page.wait_for_load_state("networkidle")
                attach_screenshot(self.page, f"Clicked {button_name}")

    @allure.step("Click next page button")
    def click_next_page(self):
        self._click_pagination_button(self.BUTTON_NEXT_PAGE)

    @allure.step("Click previous page button")
    def click_previous_page(self):
        self._click_pagination_button(self.BUTTON_PREVIOUS_PAGE)

    @allure.step("Click first page button")
    def click_first_page(self):
        self._click_pagination_button(self.BUTTON_FIRST_PAGE)

    @allure.step("Click last page button")
    def click_last_page(self):
        self._click_pagination_button(self.BUTTON_LAST_PAGE)

    @allure.step("Click page number {page_number}")
    def click_page_number(self, page_number: int):
        current_page = self.get_current_page_number()
        self._click_pagination_button(f"Page {page_number}")
        self.wait_medium()

        new_page = self.get_current_page_number()
        assert new_page == page_number, f"Should be on page {page_number} after clicking, got {new_page} (was on {current_page})"
        attach_screenshot(self.page, f"Navigated to page {page_number}")

    @allure.step("Check pagination navigation by clicking through pages")
    def check_pagination_navigation(self):
        pagination = self.page.locator(self.locators.pagination)

        if pagination.count() == 0:
            return

        current_page = self.get_current_page_number()
        total_pages = self.get_total_pages_count()

        if total_pages <= 1:
            return

        if current_page < total_pages:
            self.click_next_page()
            new_page = self.get_current_page_number()
            assert new_page > current_page, f"Page should increase after clicking next, got {new_page}"

            if new_page > 1:
                self.click_previous_page()
                prev_page = self.get_current_page_number()
                assert prev_page < new_page, f"Page should decrease after clicking previous, got {prev_page}"

        if total_pages > 1:
            self.click_last_page()
            last_page = self.get_current_page_number()
            assert last_page == total_pages, f"Should be on last page {total_pages}, got {last_page}"

            if last_page > 1:
                self.click_first_page()
                first_page = self.get_current_page_number()
                assert first_page == 1, f"Should be on first page 1, got {first_page}"

        attach_screenshot(self.page, "Pagination navigation verified")

    def _check_row_buttons(self, row):
        """Check buttons in history row"""
        download_link = row.locator(self.locators.history_download_link)

        if download_link.count() > 0:
            expect(download_link.first).to_be_visible(timeout=Timeouts.History.DOWNLOAD_LINK_VISIBLE)

        info_button = row.locator(self.locators.history_item_info_button)

        if info_button.count() > 0:
            expect(info_button.first).to_be_visible(timeout=Timeouts.History.DOWNLOAD_LINK_VISIBLE)

        disable_button = row.locator(self.locators.history_item_disable_button)

        if disable_button.count() > 0:
            expect(disable_button.first).to_be_visible(timeout=Timeouts.History.DTC_BUTTON_VISIBLE)

    def _check_row_time(self, row, row_index: int):
        """Check time in history row"""
        time_element = row.locator(self.locators.history_item_time)

        if time_element.count() > 0:
            time_text = time_element.first.text_content()

            if time_text and time_text.strip() != "":
                return

        time_cells = row.locator("td")
        if time_cells.count() > 0:

            for i in range(time_cells.count()):
                cell_text = time_cells.nth(i).text_content()

                if cell_text and re.search(r'\d{2}:\d{2}', cell_text):
                    return

        assert False, f"Time should not be empty in row {row_index}"

    def _check_row_text_content(self, row, locator, field_name: str, row_index: int):
        """Check text content in history row element"""
        element = row.locator(locator)

        if element.count() > 0:
            text = element.first.text_content()
            assert text and text.strip() != "", f"{field_name} should not be empty in row {row_index}"

    @allure.step("Check if history row contains required elements")
    def check_history_row_elements(self, row_index: int = 0):
        history_rows = self.page.locator(self.locators.history_table_row)
        count = history_rows.count()

        if count == 0 or row_index >= count:
            return

        row = history_rows.nth(row_index)
        expect(row).to_be_visible(timeout=Timeouts.History.FILE_ROW_VISIBLE)

        self._check_row_buttons(row)
        self._check_row_time(row, row_index)
        self._check_row_text_content(row, self.locators.history_item_price, "Price", row_index)
        self._check_row_text_content(row, self.locators.history_item_task, "Task", row_index)

        task_name = row.locator("td").first

        if task_name.count() > 0:
            task_name_text = task_name.text_content()
            assert task_name_text and task_name_text.strip() != "", f"Task name should not be empty in row {row_index}"

        attach_screenshot(self.page, f"History row {row_index} verified")

    @allure.step("Check all history rows on current page")
    def check_all_history_rows_on_page(self):

        with allure.step("Get history rows count"):
            history_rows = self.page.locator(self.locators.history_table_row)
            rows_count = history_rows.count()

        if rows_count == 0:
            return

        for i in range(rows_count):
            with allure.step(f"Check history row {i + 1}"):
                self.check_history_row_elements(row_index=i)

        attach_screenshot(self.page, "All history rows verified")

    @allure.step("Check pagination exists and get total pages count")
    def _check_pagination_and_get_total(self) -> int | None:

        with allure.step("Check if pagination exists"):
            pagination = self.page.locator(self.locators.pagination)
            if pagination.count() == 0:
                return None

        with allure.step("Get total pages count"):
            total_pages = self.get_total_pages_count()
            if total_pages <= 1:
                return None

        return total_pages

    @allure.step("Navigate through all pagination pages and check history rows on each page")
    def navigate_and_check_all_pages(self):
        total_pages = self._check_pagination_and_get_total()

        if total_pages is None:
            with allure.step("No pagination or single page - check rows"):
                self.check_all_history_rows_on_page()
            return

        for page_num in range(1, total_pages + 1):
            with allure.step(f"Navigate to page {page_num} and check rows"):
                if page_num > 1:
                    self.click_page_number(page_num)
                    self.page.wait_for_load_state("networkidle")

                self.check_all_history_rows_on_page()

        attach_screenshot(self.page, "All pages navigated and verified")

    @allure.step("Click button if enabled: {button_name}")
    def _click_button_if_enabled(self, button_name: str):

        with allure.step(f"Find button: {button_name}"):
            button = self.page.get_by_role("button", name=button_name).first

            if button.count() > 0:
                with allure.step("Button found - check visibility and state"):
                    expect(button).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

                    if not button.is_disabled():
                        with allure.step(f"Click button: {button_name}"):
                            button.click()
                            self.page.wait_for_load_state("networkidle")
                            return True
        return False

    @allure.step("Navigate through pagination pages with specific flow")
    def navigate_and_check_pages_flow(self):
        """Navigate through pagination pages with specific flow:
        1. Click Page 1
        2. Click Page 2 (if exists)
        3. Click Previous Page
        4. Click Next Page
        5. Click Page 2 (if exists)
        6. Click First Page
        7. Click Last Page
        Check elements after each navigation step
        """
        total_pages = self._check_pagination_and_get_total()
        if total_pages is None:
            with allure.step("No pagination or single page - check rows"):
                self.check_all_history_rows_on_page()
            return

        with allure.step("Step 1: Click Page 1"):
            self.page.get_by_role("button", name="Page 1").first.click()
            self.wait_medium()
            self.check_all_history_rows_on_page()

        if total_pages >= 2:
            with allure.step("Step 2: Click Page 2"):
                current_before = self.get_current_page_number()
                self.page.get_by_role("button", name="Page 2").first.click()
                self.wait_medium()

                new_page = self.get_current_page_number()
                assert new_page == 2, f"Should be on page 2 after clicking, got {new_page} (was on {current_before})"

                self.check_all_history_rows_on_page()

        with allure.step("Step 3: Click Previous Page"):
            self.page.get_by_role("button", name="Previous Page").first.click()
            self.wait_medium()
            self.check_all_history_rows_on_page()

        with allure.step("Step 4: Click Next Page"):
            current_before = self.get_current_page_number()
            self.page.get_by_role("button", name="Next Page").first.click()
            self.wait_medium()

            new_page = self.get_current_page_number()

            assert new_page > current_before, f"Page should increase after clicking next, got {new_page} (was on {current_before})"
            self.check_all_history_rows_on_page()

        if total_pages >= 2:
            with allure.step("Step 5: Click Page 2 again"):
                current_before = self.get_current_page_number()
                self.page.get_by_role("button", name="Page 2").first.click()
                self.wait_medium()

                new_page = self.get_current_page_number()
                assert new_page == 2, f"Should be on page 2 after clicking, got {new_page} (was on {current_before})"

                self.check_all_history_rows_on_page()

        with allure.step("Step 6: Click First Page"):
            current_before = self.get_current_page_number()
            self.page.get_by_role("button", name="First Page").first.click()
            self.wait_medium()

            new_page = self.get_current_page_number()
            assert new_page == 1, f"Should be on page 1 after clicking first, got {new_page} (was on {current_before})"

            self.check_all_history_rows_on_page()

        with allure.step("Step 7: Click Last Page"):
            current_before = self.get_current_page_number()
            self.page.get_by_role("button", name="Last Page").first.click()
            self.wait_medium()

            new_page = self.get_current_page_number()
            assert new_page == total_pages, f"Should be on last page {total_pages} after clicking, got {new_page} (was on {current_before})"

            self.check_all_history_rows_on_page()

        attach_screenshot(self.page, "Pages flow navigation completed")
