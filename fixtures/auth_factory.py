import os
import time

from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL, OTP_CODE
from config.timeouts import Timeouts
from locators.registration_locators import RegistrationLocators
from pages.base_page import BasePage
from utils.user_generator import (
    generate_premium_user,
    generate_user_with_balance,
    generate_user_with_balance_and_discount,
    generate_user_with_zero_balance,
    generate_user_without_balance_but_cashback,
    generate_user_without_balance_but_cashback_and_discount,
    generate_user_without_balance_but_discount,
)

# Global lock for registration delays to prevent HTTP 429
_last_registration_time = 0
_registration_lock = False


class UserRegistrationFactory:
    """Factory for registering users with different parameters"""

    USER_GENERATORS = {
        "premium": generate_premium_user,
        "zero_balance": generate_user_with_zero_balance,
        "with_balance": lambda: generate_user_with_balance(balance=10000),
        "with_balance_and_discount": lambda: generate_user_with_balance_and_discount(balance=10000, discount=20),
        "without_balance_but_cashback": generate_user_without_balance_but_cashback,
        "without_balance_but_discount": generate_user_without_balance_but_discount,
        "without_balance_but_cashback_and_discount": generate_user_without_balance_but_cashback_and_discount,
    }

    @staticmethod
    def ensure_logged_out(page: Page, base_url: str) -> None:
        """Проверяет и выходит из системы если пользователь залогинен"""
        base_page = BasePage(page)

        # Увеличить timeout для WebKit mobile (медленнее загружает страницы)
        browser_type = os.getenv("BROWSER", "chromium").lower()
        timeout = Timeouts.BASE_PAGE_LOAD * 2 if browser_type == "webkit" else Timeouts.BASE_PAGE_LOAD

        try:
            page.goto(
                f"{base_url.rstrip('/')}/app",
                wait_until="domcontentloaded",  # Использовать domcontentloaded для более быстрой загрузки
                timeout=timeout
            )
        except Exception:
            # Fallback: попробовать еще раз с увеличенным timeout
            page.goto(
                f"{base_url.rstrip('/')}/app",
                wait_until="domcontentloaded",
                timeout=timeout * 2
            )

        base_page.check_and_logout("Выйти")


    @staticmethod
    def register_user(
        page: Page,
        user_type: str = "premium",
        logout_after: bool = True,
        use_after_register_click: bool = False
    ) -> str:
        """
        Registers a new user

        Args:
            page: Playwright page object
            user_type: Тип пользователя (premium, zero_balance, with_balance)
            logout_after: Выйти после регистрации (для cleanup)
            use_after_register_click: Использовать таймаут AFTER_REGISTER_CLICK (для with_balance)

        Returns:
            Email зарегистрированного пользователя
        """
        # Ensure logged out
        if logout_after:
            UserRegistrationFactory.ensure_logged_out(page, BASE_URL)

        # Add delay between registrations to prevent HTTP 429
        global _last_registration_time
        current_time = time.time()
        time_since_last = current_time - _last_registration_time
        min_delay = 1.0  # Minimum 1 second between registrations
        if time_since_last < min_delay:
            time.sleep(min_delay - time_since_last)
        _last_registration_time = time.time()

        # Generate user email with worker_id for uniqueness in parallel execution
        try:
            worker_id = os.environ.get('PYTEST_XDIST_WORKER', 'gw0')
            worker_num = int(worker_id.replace('gw', '')) if worker_id.startswith('gw') else 0

        except (ValueError, AttributeError):
            worker_num = 0

        generator = UserRegistrationFactory.USER_GENERATORS.get(user_type, generate_premium_user)

        # Add worker number to email for uniqueness
        email = generator()

        if worker_num > 0:
            email = email.replace('@test.com', f'+w{worker_num}@test.com')

        # Navigate to registration
        register_url = f"{BASE_URL}/app/register"
        page.goto(register_url)

        base_page = BasePage(page)
        base_page.wait_for_page_load()

        # Wait for registration page to be loaded - need guaranteed minimum wait time
        page.wait_for_timeout(Timeouts.Fixture.PAGE_LOAD_AFTER_GOTO)

        # Fill registration form
        reg_locators = RegistrationLocators()
        email_input = page.locator(reg_locators.email_field).first
        expect(email_input).to_be_visible(timeout=Timeouts.Registration.EMAIL_INPUT_VISIBLE)
        expect(email_input).to_be_enabled(timeout=Timeouts.Registration.EMAIL_INPUT_ENABLED)

        email_input.fill(email)

        # Wait for email validation to complete - need guaranteed minimum wait time
        page.wait_for_timeout(1000)

        # Check terms checkbox
        terms_checkbox = page.locator(reg_locators.terms_checkbox).first
        expect(terms_checkbox).to_be_visible()
        expect(terms_checkbox).not_to_be_disabled()

        # Wait for checkbox to be ready - need guaranteed minimum wait time
        page.wait_for_timeout(300)
        terms_checkbox.check()
        expect(terms_checkbox).to_be_checked(timeout=Timeouts.Registration.CHECKBOX_CHECKED)

        # Click register button
        register_btn = page.locator(reg_locators.register_button).first
        expect(register_btn).to_be_visible()
        expect(register_btn).to_be_enabled(timeout=Timeouts.Registration.REGISTER_BUTTON_ENABLED)

        if use_after_register_click:
            register_btn.click()

            # Wait for server to process registration - need guaranteed minimum wait time
            page.wait_for_timeout(1000)

        else:
            # Wait for email validation to complete before clicking register
            page.wait_for_timeout(500)
            register_btn.click()

        # Wait for page to process registration and show OTP form
        base_page.wait_for_network_idle(timeout=Timeouts.BASE_NETWORK_IDLE)

        # Wait for OTP title to appear first (more reliable indicator than container)
        otp_title = page.locator(reg_locators.otp_title).first
        expect(otp_title).to_be_visible(timeout=Timeouts.Registration.OTP_FIELDS_VISIBLE)

        # Then wait for OTP container
        otp_container = page.locator(reg_locators.otp_inputs_container)
        expect(otp_container).to_be_visible(timeout=Timeouts.Registration.OTP_FIELDS_VISIBLE)

        # Then wait for OTP pin fields
        otp_pin_1 = page.locator(reg_locators.otp_pin_1).first
        expect(otp_pin_1).to_be_visible(timeout=Timeouts.Registration.OTP_FIELDS_VISIBLE)

        pin_fields = [
            reg_locators.otp_pin_1,
            reg_locators.otp_pin_2,
            reg_locators.otp_pin_3,
            reg_locators.otp_pin_4,
            reg_locators.otp_pin_5,
        ]

        base_page.fill_otp_fields(OTP_CODE, pin_fields)

        # Submit OTP
        otp_send_button = page.locator(reg_locators.otp_send_button).first
        otp_send_button.click()

        # Wait for login to complete - need guaranteed minimum wait time
        page.wait_for_timeout(Timeouts.Registration.AFTER_OTP_FILL)

        # Verify login
        base_page.navigate_to_app_and_verify(BASE_URL, "Выйти")

        return email
