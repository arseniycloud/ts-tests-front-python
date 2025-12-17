import logging
from pathlib import Path

import allure
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.app_locators import AppLocators
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot


class AppPage(BasePage):
    """App page (Editor) of TunService website"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.locators = AppLocators()

    @allure.step("Navigate to app page (/app) with authentication")
    def navigate_to_app(self):
        app_url = f"{BASE_URL}/app"
        self.page.goto(app_url, wait_until="domcontentloaded")
        # Wait for network idle to ensure all resources (images, CSS) are loaded - critical for pixel tests
        self.wait_for_network_idle()
        attach_screenshot(self.page, "App page loaded")

    @allure.step("Check if header elements are visible and logo is clickable")
    def check_header_elements(self):
        expect(self.page.locator(self.locators.header_container)).to_be_visible()

        header_logo_img = self.page.locator(self.locators.header_logo_img).first
        expect(header_logo_img).to_be_visible()

        header_logo = self.page.locator(self.locators.header_logo).first

        if header_logo.count() > 0:
            expect(header_logo).to_be_visible(timeout=Timeouts.App.HEADER_LOGO_VISIBLE)
            href = header_logo.get_attribute("href")
            assert href is not None, f"Logo should have href attribute, got {href}"

        menu_block = self.page.locator(self.locators.menu_block)
        assert menu_block.count() > 0, "Menu block should exist in DOM"

        # Open mobile menu if menu items are not visible (tablet/mobile viewports)
        # Use filter to find visible elements (handles both desktop and mobile menu versions)
        tun_link_locator = self.page.locator(self.locators.tun_link)
        visible_tun_link = None

        # Find first visible tun_link element
        for i in range(tun_link_locator.count()):
            if tun_link_locator.nth(i).is_visible(timeout=500):
                visible_tun_link = tun_link_locator.nth(i)
                break

        # If no visible tun_link found, try to open mobile menu
        if not visible_tun_link:
            try:
                logging.debug("Menu items not visible, trying to open mobile menu")
                mobile_menu_btn = self.page.locator(self.locators.mobile_menu_button).first

                if mobile_menu_btn.count() > 0:
                    expect(mobile_menu_btn).to_be_visible(timeout=2000)
                    logging.debug("Mobile menu button found and visible, clicking")

                    mobile_menu_btn.click(force=True)

                    # Wait for menu to open with animation
                    self.page.wait_for_timeout(1500)
                    logging.debug("Waited for menu animation")

            except Exception as e:
                logging.warning(f"Failed to open mobile menu: {e}")

        # Helper function to get visible element from locator
        def get_visible_element(locator_str):
            locator = self.page.locator(locator_str)
            count = locator.count()
            logging.debug(f"Finding visible element for '{locator_str[:50]}...', found {count} elements")

            # Check elements starting from index 1, reserving index 0 as fallback
            # This ensures the first element hasn't been "burned" with a timeout check
            for i in range(1, count):
                elem = locator.nth(i)
                try:
                    if elem.is_visible(timeout=1000):
                        logging.debug(f"Found visible element at index {i}")
                        return elem
                except Exception as e:
                    # Element not visible, try next one
                    logging.debug(f"Element {i} not visible: {type(e).__name__}")
                    continue

            # Return first element (never checked above) so expect().to_be_visible() gets fresh timeout
            logging.debug(f"No visible elements found from index 1-{count-1}, returning first element for fresh visibility check")
            return locator.first

        # Verify menu items are visible (find visible instances for tablet/mobile)
        expect(get_visible_element(self.locators.tun_link)).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
        expect(get_visible_element(self.locators.history_link)).to_be_visible()
        expect(get_visible_element(self.locators.balance_link)).to_be_visible()
        expect(get_visible_element(self.locators.profile_link)).to_be_visible()

        # Logout button - try main locator first, fallback to text search
        logout_elem = get_visible_element(self.locators.logout_button)
        try:
            expect(logout_elem).to_be_visible(timeout=2000)
        except AssertionError:
            # Fallback: search by text "Выйти" for mobile menu, find visible one
            logging.debug("Logout button not found with main locator, trying text search")
            logout_locator = self.page.get_by_text("Выйти")
            logout_found = False

            for i in range(logout_locator.count()):
                try:
                    elem = logout_locator.nth(i)
                    if elem.is_visible(timeout=1000):
                        expect(elem).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
                        logout_found = True
                        break
                except Exception:
                    continue

            if not logout_found:
                # Last resort: just check that at least one exists
                expect(logout_locator.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

        attach_screenshot(self.page, "Header elements verified")

    @allure.step("Check upload form elements are visible and structure is correct")
    def check_upload_form(self):
        upload_form = self.page.locator(self.locators.upload_form)
        expect(upload_form).to_be_visible()

        expect(self.page.locator(self.locators.upload_area)).to_be_visible()

        upload_btn = self.page.locator(self.locators.upload_button)
        expect(upload_btn).to_be_visible()

        upload_label = self.page.locator(self.locators.upload_label)
        expect(upload_label).to_be_visible()
        expect(upload_label).to_contain_text("Загрузить файл ECU")

        file_input = self.page.locator(self.locators.file_input)
        assert file_input.count() > 0, "File input should be present"
        input_type = file_input.get_attribute("type")
        assert input_type == "file", f"Expected file input type='file', got {input_type}"

        expect(self.page.get_by_text("rar, zip, 7zip и другие архивы не поддерживаются")).to_be_visible()
        expect(self.page.get_by_text("Только распакованные файлы")).to_be_visible()

        attach_screenshot(self.page, "Upload form verified")


    @allure.step("Check if all select dropdowns are visible and have correct initial state")
    def check_selects(self):
        type_select = self.page.locator(self.locators.type_select)
        expect(type_select).to_be_visible()

        type_select_input = self.page.locator(self.locators.type_select_input)
        expect(type_select_input).not_to_be_disabled()

        brand_select = self.page.locator(self.locators.brand_select)
        expect(brand_select).to_be_visible()

        brand_select_input = self.page.locator(self.locators.brand_select_input)
        expect(brand_select_input).to_be_disabled()

        engine_select = self.page.locator(self.locators.engine_select)
        expect(engine_select).to_be_visible()

        engine_select_input = self.page.locator(self.locators.engine_select_input)
        expect(engine_select_input).to_be_disabled()

        ecu_select = self.page.locator(self.locators.ecu_select)
        expect(ecu_select).to_be_visible()

        ecu_select_input = self.page.locator(self.locators.ecu_select_input)
        expect(ecu_select_input).to_be_disabled()

        attach_screenshot(self.page, "Select dropdowns verified")

    @allure.step("Check if search button is visible and has correct initial state")
    def check_search_button(self):
        search_button = self.page.locator(self.locators.search_button)
        expect(search_button).to_be_visible()
        expect(self.page.get_by_text("Найти")).to_be_visible()
        expect(search_button).to_be_disabled()

        attach_screenshot(self.page, "Search button verified")

    @allure.step("Upload file: {file_name}")
    def upload_file(self, file_name: str):

        file_path = Path(__file__).parent.parent / "files" / file_name
        assert file_path.exists(), f"File {file_path} does not exist"

        upload_area = self.page.locator(".flex.overflow-hidden.text-ellipsis.w-full.justify-center.items-center")

        if upload_area.count() > 0:
            try:
                upload_area.wait_for(state="visible", timeout=Timeouts.App.UPLOAD_AREA_VISIBLE)
                upload_area.first.click(timeout=Timeouts.App.UPLOAD_AREA_VISIBLE)
                self.wait_short()

            except Exception as e:
                logging.debug(f"Failed to click upload area (continuing): {e}")


        file_input = self.page.locator("input[type='file']").first


        try:
            file_input.set_input_files(str(file_path))

        except Exception as e:
            logging.warning(f"Failed to set input files via locator, falling back to page-level API: {e}")
            self.page.set_input_files("input[type='file']", str(file_path))

        self.wait_standard()

    @allure.step("Select type: {type_name}")
    def select_type(self, type_name: str):
        type_select = self.page.locator(self.locators.type_select)
        expect(type_select).to_be_visible()

        type_select.click()
        self.wait_short()

        self.page.get_by_text(type_name, exact=True).first.click()
        self.wait_short()

        attach_screenshot(self.page, "Type selected")

    @allure.step("Select brand: {brand_name}")
    def select_brand(self, brand_name: str):
        brand_select = self.page.locator(self.locators.brand_select)
        expect(brand_select).to_be_visible()

        is_disabled = brand_select.locator(self.locators.select_disabled).count() > 0

        if is_disabled:
            raise RuntimeError("Brand select is disabled. Select type first.")

        brand_select.click()
        self.wait_short()

        self.page.get_by_text(brand_name, exact=True).first.click()
        self.wait_short()

        attach_screenshot(self.page, "Brand selected")

    @allure.step("Select engine: {engine_name}")
    def select_engine(self, engine_name: str):
        engine_select = self.page.locator(self.locators.engine_select)
        expect(engine_select).to_be_visible()

        is_disabled = engine_select.locator(self.locators.select_disabled).count() > 0
        if is_disabled:
            raise RuntimeError("Engine select is disabled. Select brand first.")

        engine_select.click()
        self.wait_short()

        self.page.get_by_text(engine_name, exact=True).first.click()
        self.wait_short()

        attach_screenshot(self.page, "Engine selected")

    @allure.step("Select ECU: {ecu_name} from dropdown")
    def select_ecu(self, ecu_name: str):
        ecu_select = self.page.locator(self.locators.ecu_select)
        expect(ecu_select).to_be_visible()

        is_disabled = ecu_select.locator(self.locators.select_disabled).count() > 0

        if is_disabled:
            raise RuntimeError("ECU select is disabled. Select engine first.")

        ecu_select.click()
        self.wait_short()

        self.page.get_by_text(ecu_name, exact=True).first.click()
        self.wait_short()

        attach_screenshot(self.page, "ECU selected")

    @allure.step("Click the search button to search for solutions")
    def click_search(self):
        search_button = self.page.locator(self.locators.search_button)
        expect(search_button).to_be_visible()
        expect(search_button).not_to_be_disabled(timeout=Timeouts.Upload.SEARCH_BUTTON_ENABLED)

        search_button.click()
        self.wait_short()

        attach_screenshot(self.page, "Search clicked")

    @allure.step("Navigate to history page")
    def navigate_to_history(self):
        history_link = self.page.locator(self.locators.history_link)
        expect(history_link).to_be_visible()

        history_link.click()
        self.wait_for_page_load()

        attach_screenshot(self.page, "Navigated to history")

    @allure.step("Navigate to balance page from app")
    def navigate_to_balance(self):
        # Open mobile menu if needed (balance link might be hidden in menu on mobile)
        menu_block = self.page.locator(self.locators.menu_block)

        if menu_block.count() > 0:
            try:
                if not menu_block.first.is_visible(timeout=1000):
                    mobile_menu_btn = self.page.locator(self.locators.mobile_menu_button).first

                    if mobile_menu_btn.count() > 0 and mobile_menu_btn.is_visible(timeout=2000):
                        mobile_menu_btn.click()
                        expect(menu_block).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

                        # Additional wait to ensure menu is fully opened
                        self.page.wait_for_timeout(500)

            except Exception as e:
                logging.debug(f"Failed to open mobile menu (continuing): {e}")

        # Find visible balance link (works for both desktop and mobile)
        balance_links = self.page.locator(self.locators.balance_link)
        balance_link = None

        for i in range(balance_links.count()):
            link = balance_links.nth(i)

            if link.is_visible(timeout=1000):
                balance_link = link
                break

        # Fallback: use first link if none found visible
        if balance_link is None:
            balance_link = balance_links.first

        expect(balance_link).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
        balance_link.click()
        self.wait_for_page_load()
        self.wait_standard()

        attach_screenshot(self.page, "Navigated to balance")

    @allure.step("Navigate to profile page from app")
    def navigate_to_profile(self):
        profile_link = self.page.locator(self.locators.profile_link)

        try:
            expect(profile_link).to_be_visible(timeout=Timeouts.App.PROFILE_LINK_VISIBLE)
            profile_link.first.click(timeout=Timeouts.App.PROFILE_LINK_CLICK)
            self.wait_for_page_load()

        except Exception as e:
            logging.warning(f"Failed to click profile link, falling back to direct navigation: {e}")
            self.page.goto(f"{BASE_URL}/app/profile")
            self.wait_for_page_load()

        self.wait_medium()

        attach_screenshot(self.page, "Navigated to profile")

    @allure.step("Logout from application")
    def logout(self):
        logout_button = self.page.locator(self.locators.logout_button)
        expect(logout_button).to_be_visible()

        logout_button.click()
        self.wait_for_page_load()

        attach_screenshot(self.page, "Logged out")

    @allure.step("Check app page basic structure")
    def check_page_structure(self):
        expect(self.page.locator(self.locators.page_container)).to_be_visible()
        expect(self.page.locator(self.locators.page_body)).to_be_visible()

        attach_screenshot(self.page, "Page structure verified")
