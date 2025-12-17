import base64
import logging
import os
from pathlib import Path

import pytest
from playwright.sync_api import expect, sync_playwright

from config.auth_config import PASSWORD, USERNAME, BASE_URL
from config.devices_config import DEVICE_NAMES, get_device_config
from config.timeouts import Timeouts


@pytest.fixture(scope="session")
def playwright_instance():
    """Playwright instance fixture"""
    with sync_playwright() as p:
        yield p


def _get_browser_type_from_config(request=None):
    """Get browser type from pytest config option --browser"""
    browser_type = os.getenv("BROWSER", "chromium").lower()
    if request:
        try:
            browser_option = request.config.getoption("--browser", default=None)

            if browser_option:

                if isinstance(browser_option, list) and len(browser_option) > 0:
                    browser_type = browser_option[0].lower()

                elif isinstance(browser_option, str):
                    browser_type = browser_option.lower()

        except (ValueError, AttributeError, IndexError) as e:
            logging.debug(f"Failed to parse browser option (using default): {e}")

    return browser_type


@pytest.fixture(scope="session")
def browser(playwright_instance, request):
    # Default to headless in CI environments (GitHub Actions, GitLab CI, etc.)
    # or if HEADLESS env var is explicitly set
    is_ci = os.getenv("CI", "false").lower() == "true"
    headless_env = os.getenv("HEADLESS", "").lower()

    if headless_env:
        is_headless = headless_env == "true"

    else:
        # In CI, default to headless; locally, default to headed for debugging
        is_headless = is_ci

    browser_type = _get_browser_type_from_config(request)

    if browser_type == "firefox":
        browser = playwright_instance.firefox.launch(headless=is_headless)

    elif browser_type == "webkit":
        browser = playwright_instance.webkit.launch(headless=is_headless)

    else:
        browser = playwright_instance.chromium.launch(headless=is_headless)

    yield browser
    browser.close()


@pytest.fixture(scope="session")
def device_name():
    """
    Get device name from DEVICE env var.

    If DEVICE is explicitly set, use that value.
    If DEVICE is not set or empty, default to 'desktop' for browser config
    but snapshot names won't have device suffix (handled in visual.py).
    """
    device = os.getenv("DEVICE", "").strip()

    # Default to desktop for browser configuration if not specified
    return device if device else "desktop"


@pytest.fixture(scope="session")
def context(browser, playwright_instance, device_name, request):
    """Browser context fixture with device emulation and optional tracing"""
    device_config = get_device_config(playwright_instance, device_name)
    device_display_name = DEVICE_NAMES.get(device_name, device_name).replace("_", " ")

    browser_type = _get_browser_type_from_config(request)
    browser_display_names = {
        "chromium": "Chromium",
        "firefox": "Firefox",
        "webkit": "WebKit"
    }

    browser_display_name = browser_display_names.get(browser_type, "Chromium")

    viewport = device_config.get("viewport", {})
    viewport_info = f"{viewport.get('width', '?')}x{viewport.get('height', '?')}"

    context = browser.new_context(**device_config)

    # Apply basic authentication for all pages in this context
    credentials = f"{USERNAME}:{PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "X-Test-Device": device_display_name,
        "X-Test-Browser": browser_display_name,
        "X-Test-Viewport": viewport_info,
        "Authorization": f"Basic {encoded_credentials}",
    }

    context.set_extra_http_headers(headers)

    # Store headers in context for later use (to preserve Authorization when updating headers)
    context._base_http_headers = headers.copy()

    enable_tracing = os.getenv("ENABLE_TRACING", "false").lower() == "true"
    trace_on_failure = os.getenv("TRACE_ON_FAILURE", "true").lower() == "true"
    enable_tracing = enable_tracing or trace_on_failure

    base_trace_dir = os.getenv("TRACE_DIR", "reports/trace")
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "")

    if worker_id:
        trace_dir = Path(base_trace_dir) / device_name / browser_type / worker_id

    else:
        trace_dir = Path(base_trace_dir) / device_name / browser_type
    trace_filename = trace_dir / "trace.zip"

    if enable_tracing:
        trace_dir.mkdir(parents=True, exist_ok=True)
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True,
            title=f"{device_display_name} - {browser_display_name} ({viewport_info})"
        )

    # Set language cookie to Russian for all tests
    # This ensures tests run in Russian locale by default in CI
    # Cookie needs to be set after context is created but before pages are used
    try:
        if BASE_URL:
            # Create a temporary page to set cookies (required by Playwright)
            temp_page = context.new_page()
            temp_page.goto(f"{BASE_URL}/", wait_until="domcontentloaded", timeout=5000)
            context.add_cookies([{
                "name": "i18n_redirected",
                "value": "ru",
                "domain": BASE_URL.replace("http://", "").replace("https://", "").split("/")[0],
                "path": "/"
            }])
            temp_page.close()

    except Exception as e:
        # If cookie setting fails, log warning but don't fail tests
        print(f"Warning: Failed to set language cookie: {e}")

    yield context

    if enable_tracing:
        try:
            context.tracing.stop(path=str(trace_filename))

        except Exception as e:
            # Handle tracing errors gracefully - don't fail tests due to tracing issues
            print(f"Warning: Failed to stop tracing: {e}")

    context.close()


@pytest.fixture(scope="session")
def page(context):
    """Page fixture - opens once per test session"""
    page = context.new_page()
    page.set_default_timeout(Timeouts.BASE_PAGE_LOAD)
    page.set_default_navigation_timeout(Timeouts.BASE_PAGE_LOAD)
    expect.set_options(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

    # Ensure language cookie is set (in case it was cleared)
    # Navigate to site to set cookie
    try:
        if BASE_URL:
            page.goto(f"{BASE_URL}/", wait_until="domcontentloaded", timeout=5000)
            context.add_cookies([{
                "name": "i18n_redirected",
                "value": "ru",
                "domain": BASE_URL.replace("http://", "").replace("https://", "").split("/")[0],
                "path": "/"
            }])

    except Exception as e:
        logging.warning(f"Failed to set language cookie: {e}")

    yield page
    page.close()
