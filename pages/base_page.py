import logging

import allure
from playwright.sync_api import Page, expect
import os

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from utils.allure_helpers import attach_element_screenshot, attach_screenshot
from utils.playwright_helpers import scroll_to_make_visible

LOGOUT_BUTTON_TEXT = "Выйти"


class BasePage:

    def __init__(self, page: Page, locators=None):

        self.page = page
        self.locators = locators

    def wait_for_page_load(self, state: str = "domcontentloaded", timeout: int = None):
        timeout = timeout or Timeouts.BASE_PAGE_LOAD
        try:
            self.page.wait_for_load_state(state, timeout=timeout)

        except Exception as e:
            if state == "networkidle":

                try:
                    logging.warning(f"Failed to wait for load state '{state}', falling back to 'load': {e}")
                    self.page.wait_for_load_state("load", timeout=timeout // 2)

                except Exception as e2:
                    logging.warning(f"Failed to wait for load state 'load' as fallback: {e2}")

    @allure.step("Wait for response matching URL pattern: {url_pattern}")
    def wait_for_response(self, url_pattern, timeout: int = None):
        timeout = timeout or Timeouts.BASE_RESPONSE_WAIT

        if isinstance(url_pattern, str):
            # Simple string matching - wait for event and filter by URL

            def check_response(response):
                return url_pattern in response.url

            response = self.page.wait_for_event('response', predicate=check_response, timeout=timeout)
            return response

        else:
            # Callable/lambda function - wait for event with custom filter
            response = self.page.wait_for_event('response', predicate=url_pattern, timeout=timeout)
            return response

    @allure.step("Navigate to URL: {url} | auth={auth}")
    def navigate_to(self, url: str, auth: bool = True):
        self.page.goto(url, wait_until="domcontentloaded")
        # Wait for network idle to ensure all resources (images, CSS) are loaded - critical for pixel tests
        self.wait_for_network_idle()

    @allure.step("Check visibility of elements: {selectors}")
    def check_page_elements(self, selectors: list):

        for selector in selectors:
            expect(self.page.locator(selector)).to_be_visible()
        attach_screenshot(self.page, "Page elements verified")

    @allure.step("Take screenshot: {name} for debugging")
    def take_screenshot(self, name: str = "screenshot"):
        self.page.screenshot(path=f"screenshots/{name}.png")

    @allure.step("Get element color for selector: {selector}")
    def get_element_color(self, selector: str) -> str:
        return self.page.evaluate("""
            (selector) => {
                const element = document.querySelector(selector);
                if (!element) return null;
                return window.getComputedStyle(element).color;
            }
        """, selector)

    @allure.step("Get element background color for selector: {selector}")
    def get_element_background_color(self, selector: str) -> str:
        return self.page.evaluate("""
            (selector) => {
                const element = document.querySelector(selector);
                if (!element) return null;
                return window.getComputedStyle(element).backgroundColor;
            }
        """, selector)

    @allure.step("Get element position for selector: and size {selector}")
    def get_element_position(self, selector: str) -> dict:
        return self.page.evaluate("""
            (selector) => {
                const element = document.querySelector(selector);
                if (!element) return null;
                const rect = element.getBoundingClientRect();
                return {x: rect.x, y: rect.y, width: rect.width, height: rect.height,
                        top: rect.top, left: rect.left, bottom: rect.bottom, right: rect.right};
            }
        """, selector)

    @allure.step("Check if element is visible: {selector}")
    def is_element_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    @allure.step("Scroll to make element visible: {selector}")
    def scroll_to_make_visible(self, selector: str):
        """Scroll page to make element visible in viewport"""
        scroll_to_make_visible(self.page.locator(selector))

    @allure.step("Check if element is in viewport: {selector}")
    def is_element_in_viewport(self, selector: str) -> bool:
        return self.page.evaluate("""
            (selector) => {
                const element = document.querySelector(selector);
                if (!element) return false;
                const rect = element.getBoundingClientRect();
                return rect.top >= 0 && rect.left >= 0 &&
                       rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                       rect.right <= (window.innerWidth || document.documentElement.clientWidth);
            }
        """, selector)

    @allure.step("Validate element color for {selector} equals {expected_color} (±{tolerance})")
    def validate_element_color(self, selector: str, expected_color: str, tolerance: int = 0):
        actual_color = self.get_element_color(selector)

        if actual_color == expected_color:
            return True

        if tolerance > 0:
            return self._compare_colors_with_tolerance(actual_color, expected_color, tolerance)

        return False

    @allure.step("Validate element background color for {selector} equals {expected_color} (±{tolerance})")
    def validate_element_background_color(self, selector: str, expected_color: str, tolerance: int = 0):
        actual_color = self.get_element_background_color(selector)

        if actual_color == expected_color:
            return True

        if tolerance > 0:
            return self._compare_colors_with_tolerance(actual_color, expected_color, tolerance)

        return False

    @allure.step("Validate element position for {selector} matches {expected_position}")
    def validate_element_position(self, selector: str, expected_position: dict):
        actual_position = self._get_element_rect(selector)

        if not actual_position:
            return False

        return self._check_position_values(actual_position, expected_position)

    @allure.step("Get element rect for selector: {selector}")
    def _get_element_rect(self, selector: str) -> dict:
        """Get element bounding rect"""
        return self.page.evaluate("""
            (selector) => {
                const element = document.querySelector(selector);
                if (!element) return null;
                const rect = element.getBoundingClientRect();
                return {x: rect.x, y: rect.y, width: rect.width, height: rect.height,
                        top: rect.top, left: rect.left, bottom: rect.bottom, right: rect.right};
            }
        """, selector)

    def _check_position_values(self, actual_position: dict, expected_position: dict) -> bool:
        """Check position values against expected"""
        for key, expected_value in expected_position.items():
            if key in actual_position:

                if isinstance(expected_value, dict):

                    if not self._check_range(actual_position[key], expected_value):
                        return False

                elif actual_position[key] != expected_value:

                    return False
        return True

    def _check_range(self, actual_value: float, range_dict: dict) -> bool:
        """Check if value is within range"""

        if 'min' in range_dict and actual_value < range_dict['min']:
            return False

        if 'max' in range_dict and actual_value > range_dict['max']:
            return False

        return True

    @allure.step("Validate element is visible: {selector}")
    def validate_element_visibility(self, selector: str):
        return self.page.locator(selector).is_visible()

    def _is_mobile_device(self) -> bool:
        """
        Check if current device is mobile or tablet based on viewport or DEVICE env var.
        Universal method that works with any viewport size.
        Returns True for mobile and tablet devices where elements may be hidden in menu.
        """
        viewport = self.page.viewport_size

        # Check viewport: mobile and tablet typically have width <= 1024px
        # Desktop usually has width > 1024px
        if viewport and viewport["width"] <= 1024:
            return True

        # Check DEVICE env var for mobile/tablet devices
        device = os.getenv("DEVICE", "desktop").lower()
        return device in ["mobile", "tablet", "ipad"]

    def is_visible_or_mobile_hidden(self, locator, timeout=None) -> bool:
        """
        Check if element is visible, or exists in DOM on mobile (hidden but functional).
        Returns True if element passes the check for the current device type.
        """
        timeout = timeout or Timeouts.BASE_ELEMENT_VISIBLE
        try:
            if locator.first.is_visible(timeout=timeout):
                return True

        except Exception:
            pass

        return self._is_mobile_device() and locator.count() > 0

    def assert_visible_or_exists_on_mobile(self, locator, message: str = "Element should be visible"):
        """
        Assert element is visible on desktop, or exists in DOM on mobile/tablet.
        On mobile and tablet devices, elements may be hidden in menu but still exist in DOM.
        """
        if self._is_mobile_device():
            assert locator.count() > 0, message

        else:
            expect(locator.first).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    @allure.step("Validate element is in viewport: {selector}")
    def validate_element_in_viewport(self, selector: str) -> bool:
        return self.is_element_in_viewport(selector)

    @allure.step("Validate responsive layout for {selector} at width {viewport_width}")
    def validate_responsive_layout(self, selector: str, viewport_width: int):
        self.page.set_viewport_size({"width": viewport_width, "height": 800})
        self.page.wait_for_load_state("networkidle")

        is_visible = self.validate_element_visibility(selector)
        is_in_viewport = self.is_element_in_viewport(selector)

        return is_visible and is_in_viewport

    def _compare_colors_with_tolerance(self, color1: str, color2: str, tolerance: int):
        try:
            rgb1 = self._extract_rgb(color1)
            rgb2 = self._extract_rgb(color2)

            if not rgb1 or not rgb2:
                return False

            for i in range(3):
                if abs(rgb1[i] - rgb2[i]) > tolerance:
                    return False

            return True

        except Exception as e:
            logging.debug(f"Failed to compare colors with tolerance: {e}")
            return False

    def _extract_rgb(self, color_str: str):
        try:
            if color_str.startswith('rgb('):
                numbers = color_str[4:-1].split(',')
                return [int(x.strip()) for x in numbers]
            elif color_str.startswith('#'):
                hex_color = color_str[1:]
                return [
                    int(hex_color[0:2], 16),
                    int(hex_color[2:4], 16),
                    int(hex_color[4:6], 16)]

            return None

        except Exception as e:
            logging.debug(f"Failed to extract RGB from color '{color_str}': {e}")
            return None

    @property
    def otp_pin_fields(self) -> list[str]:
        """Return list of OTP pin field locators"""

        if not self.locators:
            raise AttributeError("locators attribute is not set")

        return [
            self.locators.otp_pin_1,
            self.locators.otp_pin_2,
            self.locators.otp_pin_3,
            self.locators.otp_pin_4,
            self.locators.otp_pin_5,
        ]

    @allure.step("Fill OTP pin fields with code")
    def fill_pin_fields(
        self,
        code: str,
        screenshot_label: str | None = None,
        pin_fields: list[str] | None = None,
    ) -> None:
        """Fill OTP pin fields with the provided code"""

        if pin_fields is None:
            pin_fields = self.otp_pin_fields

        for index, (pin_field, digit) in enumerate(zip(pin_fields, code)):
            pin_input = self.page.locator(pin_field).first
            expect(pin_input).to_be_visible()

            if index == 0 and screenshot_label:
                attach_element_screenshot(pin_input, screenshot_label)
            pin_input.fill(digit)

    @allure.step("Clear OTP pin fields")
    def clear_pin_fields(
        self,
        screenshot_label: str | None = None,
        pin_fields: list[str] | None = None,
    ) -> None:

        """Clear all OTP pin fields"""
        if pin_fields is None:
            pin_fields = self.otp_pin_fields

        for index, pin_field in enumerate(pin_fields):
            pin_input = self.page.locator(pin_field).first
            expect(pin_input).to_be_visible()

            if index == 0 and screenshot_label:
                attach_element_screenshot(pin_input, screenshot_label)
            pin_input.clear()

    @allure.step("Fill OTP fields with code: {otp_code}")
    def fill_otp_fields(self, otp_code: str, pin_fields: list) -> None:
        """Legacy method - use fill_pin_fields instead"""
        for pin_field, digit in zip(pin_fields, otp_code):
            pin_input = self.page.locator(pin_field).first
            expect(pin_input).to_be_visible()
            pin_input.fill(digit)

    @allure.step("Check and logout if logged in")
    def check_and_logout(self, logout_button_text: str = LOGOUT_BUTTON_TEXT) -> None:
        self.wait_for_network_idle()

        logout_btn = self.page.get_by_text(logout_button_text)

        if logout_btn.count() > 0:
            logout_btn.first.click(force=True)
            self.wait_for_network_idle()

    @allure.step("Navigate to /app page and verify user is logged in")
    def navigate_to_app_and_verify(self, base_url: str, logout_button_text: str = LOGOUT_BUTTON_TEXT, timeout: int = None) -> None:
        base_url_clean = base_url.rstrip('/')
        app_url = f"{base_url_clean}/app"

        current_url = self.page.url

        if "/app" not in current_url:
            self.page.goto(app_url, wait_until="commit")

    @allure.step("Wait for logout button to be visible")
    def wait_for_logout_button(self, logout_button_text: str = LOGOUT_BUTTON_TEXT, timeout: int = None) -> None:
        timeout = timeout or Timeouts.BASE_ELEMENT_VISIBLE
        logout_btn = self.page.get_by_text(logout_button_text)
        expect(logout_btn).to_be_visible(timeout=timeout)

    def wait_short(self):
        self.page.wait_for_timeout(Timeouts.Animation.SHORT)

    def wait_medium(self):
        self.page.wait_for_timeout(Timeouts.Animation.MEDIUM)

    def wait_standard(self):
        self.page.wait_for_timeout(Timeouts.Animation.STANDARD)

    def wait_long(self):
        self.page.wait_for_timeout(Timeouts.Animation.LONG)

    def wait_for_network_idle(self, timeout: int = None):
        """Wait for network idle state, fallback to load state if networkidle times out"""
        timeout = timeout or Timeouts.BASE_NETWORK_IDLE

        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)

        except Exception as e:
            logging.warning(f"Failed to wait for networkidle, falling back to load state: {e}")
            self.page.wait_for_load_state("load", timeout=Timeouts.BASE_PAGE_LOAD)

    @allure.step("Reload page")
    def reload_page(self, wait_until: str = "domcontentloaded", timeout: int = None) -> None:
        timeout = timeout or Timeouts.BASE_PAGE_LOAD
        self.page.reload(wait_until=wait_until, timeout=timeout)
        self.wait_for_page_load()

    def _set_language_cookie(self):
        """Set Russian language cookie after cookies are cleared"""
        try:

            if not BASE_URL:
                raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")

            # Navigate to site first (required by Playwright for setting cookies)
            current_url = self.page.url
            if not current_url or BASE_URL not in current_url:
                self.page.goto(f"{BASE_URL}/", wait_until="domcontentloaded", timeout=5000)

            # Set language cookie
            self.page.context.add_cookies([{
                "name": "i18n_redirected",
                "value": "ru",
                "domain": BASE_URL.replace("http://", "").replace("https://", "").split("/")[0],
                "path": "/"}])

        except ValueError as e:
            logging.error(f"Configuration error: {e}")
            raise

        except Exception as e:
            logging.warning(f"Failed to set language cookie: {e}")
