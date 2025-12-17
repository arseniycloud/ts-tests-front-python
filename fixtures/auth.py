import logging
import re

import allure
import pytest
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL, OTP_CODE
from config.timeouts import Timeouts
from fixtures.auth_factory import UserRegistrationFactory
from locators.login_locators import LoginLocators
from pages.base_page import BasePage
from pages.upload_page import UploadPage

LOGOUT_BUTTON_TEXT = "Выйти"


def parse_user_info_from_email(email: str) -> dict:
    """Parse user information from email address"""

    user_info = {
        "email": email,
        "balance": None,
        "cashback": None,
        "discount": None,
        "user_type": "basic"
    }

    balance_match = re.search(r'\+(\d+)(?=[+c@]|$)', email)
    if balance_match:
        user_info["balance"] = int(balance_match.group(1))

    cashback_match = re.search(r'\+c(\d+)', email)
    if cashback_match:
        user_info["cashback"] = int(cashback_match.group(1))

    discount_match = re.search(r'\+d(\d+)', email)
    if discount_match:
        user_info["discount"] = int(discount_match.group(1))

    if user_info["balance"] == 0:
        user_info["user_type"] = "zero_balance"
    elif user_info["balance"] and user_info["cashback"] and user_info["discount"]:
        user_info["user_type"] = "premium"
    elif user_info["balance"]:
        user_info["user_type"] = "with_balance"

    return user_info


def format_user_info_for_allure(user_info: dict) -> str:
    lines = [
        "=== User Information ===",
        f"Email: {user_info['email']}",
        f"User Type: {user_info['user_type']}",
    ]

    if user_info["balance"] is not None:
        lines.append(f"Balance: {user_info['balance']} ₽")
    if user_info["cashback"] is not None:
        lines.append(f"Cashback: {user_info['cashback']}%")
    if user_info["discount"] is not None:
        lines.append(f"Discount: {user_info['discount']}%")

    return "\n".join(lines)


def attach_user_info_to_allure(email: str) -> None:
    user_info = parse_user_info_from_email(email)
    user_info_text = format_user_info_for_allure(user_info)
    allure.attach(
        user_info_text,
        name="Test User Information",
        attachment_type=allure.attachment_type.TEXT
    )


def store_user_info_in_playwright(page: Page, email: str) -> dict:
    user_info = parse_user_info_from_email(email)

    page._user_info = user_info
    context = page.context
    context._user_info = user_info

    # Get base headers (including Authorization) from context
    base_headers = getattr(context, "_base_http_headers", {})

    # Merge base headers with user-specific headers
    headers = base_headers.copy()
    headers.update({
        "X-Test-User-Email": user_info["email"],
        "X-Test-User-Type": user_info["user_type"],
        "X-Test-User-Balance": str(user_info["balance"]) if user_info["balance"] is not None else "",
        "X-Test-User-Cashback": str(user_info["cashback"]) if user_info["cashback"] is not None else "",
        "X-Test-User-Discount": str(user_info["discount"]) if user_info["discount"] is not None else "",
    })

    context.set_extra_http_headers(headers)

    return user_info


def get_user_info_from_playwright(page: Page) -> dict | None:
    return getattr(page, "_user_info", None)


def _set_language_cookie(page: Page):
    """Set Russian language cookie after cookies are cleared"""
    try:
        if not BASE_URL:
            raise ValueError("BASE_URL is not set. Please configure BASE_URL in environment variables.")
        # Navigate to site first (required by Playwright for setting cookies)
        current_url = page.url
        if not current_url or BASE_URL not in current_url:
            page.goto(f"{BASE_URL}/", wait_until="domcontentloaded", timeout=5000)
        # Set language cookie
        page.context.add_cookies([{
            "name": "i18n_redirected",
            "value": "ru",
            "domain": BASE_URL.replace("http://", "").replace("https://", "").split("/")[0],
            "path": "/"
        }])
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logging.warning(f"Failed to set language cookie: {e}")


@pytest.fixture(scope="function")
@allure.title("Register new premium user and login, navigate to /app")
def authenticated_user_new(page: Page):
    # Use existing page instead of creating new one to avoid blank tabs
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Clear previous state for test isolation
    page.context.clear_cookies()
    # Re-set language cookie after clearing
    _set_language_cookie(page)

    email = UserRegistrationFactory.register_user(page, user_type="premium", logout_after=True)
    attach_user_info_to_allure(email)
    store_user_info_in_playwright(page, email)
    yield page

    # Teardown
    try:
        page.goto(f"{BASE_URL}/app")
        base_page = BasePage(page)
        base_page.check_and_logout(LOGOUT_BUTTON_TEXT)
    except Exception as e:
        logging.debug(f"Failed to logout during teardown (continuing): {e}")
    finally:
        page.context.clear_cookies()


@pytest.fixture(scope="function")
@allure.title("Register new user with balance and login, navigate to /app")
def authenticated_user_with_balance(page: Page):
    # Use existing page instead of creating new one to avoid blank tabs
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Clear previous state for test isolation
    page.context.clear_cookies()
    # Re-set language cookie after clearing
    _set_language_cookie(page)

    email = UserRegistrationFactory.register_user(
        page,
        user_type="with_balance",
        logout_after=True,
        use_after_register_click=True
    )
    attach_user_info_to_allure(email)
    store_user_info_in_playwright(page, email)
    yield page

    # Teardown
    try:
        page.goto(f"{BASE_URL}/app")
        base_page = BasePage(page)
        base_page.check_and_logout(LOGOUT_BUTTON_TEXT)
    except Exception as e:
        logging.debug(f"Failed to logout during teardown (continuing): {e}")
    finally:
        page.context.clear_cookies()


@pytest.fixture(scope="function")
@allure.title("Register new user with zero balance and login, navigate to /app")
def authenticated_user_zero_balance(page: Page):
    # Use existing page instead of creating new one to avoid blank tabs
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Clear previous state for test isolation
    page.context.clear_cookies()
    # Re-set language cookie after clearing
    _set_language_cookie(page)

    email = UserRegistrationFactory.register_user(page, user_type="zero_balance", logout_after=False)
    attach_user_info_to_allure(email)
    store_user_info_in_playwright(page, email)
    yield page
    page.context.clear_cookies()



@pytest.fixture(scope="session")
@allure.title("Login with existing user and navigate to /app - runs once for all tests")
def auth_user_existing(page: Page):
    base_page = BasePage(page)

    with allure.step("Navigate to /app page"):
        app_url = f"{BASE_URL}/app"
        page.goto(app_url)
        base_page.wait_for_network_idle()

    with allure.step("Check if user is already logged in"):
        logout_btn = page.get_by_text(LOGOUT_BUTTON_TEXT)
        if logout_btn.count() > 0:
            email = "test953+50000++c10++d20@test.com"
            attach_user_info_to_allure(email)
            store_user_info_in_playwright(page, email)
            return page

    with allure.step("Navigate to login page"):
        login_url = f"{BASE_URL}/app/login"
        page.goto(login_url)
        base_page.wait_for_network_idle()

    with allure.step("Fill login form"):
        email = "test953+50000++c10++d20@test.com"
        locators = LoginLocators()

        email_input = page.locator(locators.username_field).first
        expect(email_input).to_be_visible()

        email_input.click()
        email_input.fill(email)

        login_btn = page.locator(locators.login_button).first
        expect(login_btn).to_be_visible()

        base_page.wait_for_network_idle()
        login_btn.click()

    with allure.step("Wait for OTP fields to appear"):
        base_page.wait_for_network_idle()
        otp_pin_1 = page.locator(locators.otp_pin_1).first
        expect(otp_pin_1).to_be_visible(timeout=Timeouts.Registration.OTP_FIELDS_VISIBLE)

    with allure.step("Fill OTP code"):
        pin_fields = [
            locators.otp_pin_1,
            locators.otp_pin_2,
            locators.otp_pin_3,
            locators.otp_pin_4,
            locators.otp_pin_5,
        ]
        base_page.fill_otp_fields(OTP_CODE, pin_fields)

    with allure.step("Submit OTP and handle retries"):
        # Retry logic for HTTP 429
        max_retries = 1

        for attempt in range(max_retries):
            with page.expect_response(
                lambda resp: "/api-v1/auth/login-code" in resp.url,
                timeout=Timeouts.Registration.OTP_SUBMIT_RESPONSE
            ) as resp_info:
                page.locator(locators.otp_send_button).first.click()

            response = resp_info.value

            if response.status == 200:
                break

            elif response.status == 429 and attempt < max_retries - 1:
                # Need guaranteed minimum wait time before retry to respect rate limit
                page.wait_for_timeout(Timeouts.BASE_PAGE_LOAD)
                # Re-fill OTP and retry
                base_page.fill_otp_fields(OTP_CODE, pin_fields)

            else:
                break

        assert response.status == 200, f"Expected status 200, got {response.status}"

    with allure.step("Navigate to /app and verify login"):
        base_page.navigate_to_app_and_verify(BASE_URL, LOGOUT_BUTTON_TEXT)

    with allure.step("Store user information"):
        attach_user_info_to_allure(email)
        store_user_info_in_playwright(page, email)
        return page



@pytest.fixture(scope="function")
@allure.title("Register new user with zero balance, login, and attempt purchase (should fail due to insufficient funds)")
def authenticated_user_zero_balance_with_purchase_attempt(page: Page):
    # Use existing page instead of creating new one to avoid blank tabs
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Clear previous state for test isolation
    page.context.clear_cookies()
    # Re-set language cookie after clearing
    _set_language_cookie(page)

    base_page = BasePage(page)

    try:
        page.goto(f"{BASE_URL}/app")
        base_page.check_and_logout(LOGOUT_BUTTON_TEXT)

    except Exception as e:
        logging.debug(f"Failed to logout before zero balance test (continuing): {e}")

    email = UserRegistrationFactory.register_user(page, user_type="zero_balance", logout_after=True)
    attach_user_info_to_allure(email)
    store_user_info_in_playwright(page, email)

    upload_page = UploadPage(page)

    with allure.step("Attempt purchase with zero balance"):
        upload_page.upload_file("BMW.bin")
        upload_page.select_file_parameters("Car", "BMW, MINI", "Diesel engines", "Bosch EDC16")
        upload_page.search_solutions(wait_time=3)
        upload_page.verify_solutions_found(min_count=1)
        upload_page.select_solution_by_index(3)
        upload_page.apply_order(wait_time=2000)
        page.wait_for_load_state("networkidle")

    yield page

    try:
        page.goto(f"{BASE_URL}/app")
        base_page.check_and_logout(LOGOUT_BUTTON_TEXT)

    except Exception as e:
        logging.debug(f"Failed to logout during teardown (continuing): {e}")

    finally:
        page.context.clear_cookies()


@pytest.fixture(scope="function")
@allure.title("Register new user with balance and discount, login, navigate to /app")
def authenticated_user_with_balance_and_discount(page: Page):
    # Use existing page instead of creating new one to avoid blank tabs
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Clear previous state for test isolation
    page.context.clear_cookies()

    # Re-set language cookie after clearing
    _set_language_cookie(page)

    email = UserRegistrationFactory.register_user(page, user_type="with_balance_and_discount", logout_after=True)
    attach_user_info_to_allure(email)
    store_user_info_in_playwright(page, email)
    yield page

    try:
        page.goto(f"{BASE_URL}/app")
        base_page = BasePage(page)
        base_page.check_and_logout(LOGOUT_BUTTON_TEXT)

    except Exception as e:
        logging.debug(f"Failed to logout during teardown (continuing): {e}")

    finally:
        page.context.clear_cookies()


@pytest.fixture(scope="function")
@allure.title("Register new user with zero balance but 50% cashback, login, navigate to /app")
def authenticated_user_without_balance_but_cashback(page: Page):
    # Use existing page instead of creating new one to avoid blank tabs
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Clear previous state for test isolation
    page.context.clear_cookies()

    # Re-set language cookie after clearing
    _set_language_cookie(page)

    email = UserRegistrationFactory.register_user(page, user_type="without_balance_but_cashback", logout_after=False)
    attach_user_info_to_allure(email)
    store_user_info_in_playwright(page, email)

    yield page
    page.context.clear_cookies()


@pytest.fixture(scope="function")
@allure.title("Register new user with zero balance but discount, login, navigate to /app")
def authenticated_user_without_balance_but_discount(page: Page):
    # Use existing page instead of creating new one to avoid blank tabs
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Clear previous state for test isolation
    page.context.clear_cookies()

    # Re-set language cookie after clearing
    _set_language_cookie(page)

    email = UserRegistrationFactory.register_user(page, user_type="without_balance_but_discount", logout_after=False)
    attach_user_info_to_allure(email)
    store_user_info_in_playwright(page, email)

    yield page
    page.context.clear_cookies()


@pytest.fixture(scope="function")
@allure.title("Register new user with zero balance but 50% cashback and discount, login, navigate to /app")
def authenticated_user_without_balance_but_cashback_and_discount(page: Page):
    # Use existing page instead of creating new one to avoid blank tabs
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Clear previous state for test isolation
    page.context.clear_cookies()

    # Re-set language cookie after clearing
    _set_language_cookie(page)

    email = UserRegistrationFactory.register_user(page, user_type="without_balance_but_cashback_and_discount", logout_after=False)
    attach_user_info_to_allure(email)
    store_user_info_in_playwright(page, email)
    yield page
    page.context.clear_cookies()


@pytest.fixture(scope="session")
@allure.title("Register new user and navigate to /app page for app page tests")
def auth_user_new_for_app_page(page: Page):
    # Use existing page instead of creating new one to avoid blank tabs
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Clear previous state for test isolation
    page.context.clear_cookies()

    # Re-set language cookie after clearing
    _set_language_cookie(page)

    base_page = BasePage(page)

    email = UserRegistrationFactory.register_user(page, user_type="premium", logout_after=True)
    attach_user_info_to_allure(email)
    store_user_info_in_playwright(page, email)

    app_url = f"{BASE_URL}/app"
    page.goto(app_url)
    base_page.wait_for_page_load()

    yield page

    try:
        page.goto(f"{BASE_URL}/app")
        base_page.check_and_logout(LOGOUT_BUTTON_TEXT)

    except Exception as e:
        logging.debug(f"Failed to logout during teardown (continuing): {e}")

    finally:
        page.context.clear_cookies()
