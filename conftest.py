# Main conftest.py - imports all fixtures from fixtures modules
# Pytest will automatically discover all fixtures from imported modules
# Imports may show "unused" warnings, but this is normal - pytest uses them for fixture discovery

import logging
import os
from functools import lru_cache
from pathlib import Path

import allure
import pytest
from _pytest.junitxml import xml_key
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pytest_metadata.plugin import metadata_key
from config.devices_config import DEVICE_NAMES, get_device_config


pytest_plugins = ["pytest_playwright_visual_snapshot"]


# Load environment variables from .env file
load_dotenv()


from fixtures.auth import (  # noqa: F401, E402
    auth_user_existing,
    auth_user_new_for_app_page,
    authenticated_user_new,
    authenticated_user_with_balance,
    authenticated_user_with_balance_and_discount,
    authenticated_user_without_balance_but_cashback,
    authenticated_user_without_balance_but_cashback_and_discount,
    authenticated_user_without_balance_but_discount,
    authenticated_user_zero_balance,
    authenticated_user_zero_balance_with_purchase_attempt,
)
from fixtures.browser import (  # noqa: F401, E402
    browser,
    context,
    device_name,
    page,
    playwright_instance,
)
from fixtures.catalog import (  # noqa: F401, E402
    catalog_brand_page,
    catalog_ecu_page,
    catalog_ecu_page_param,
    catalog_engine_page,
    catalog_engine_page_param,
    catalog_stock_card_page,
    catalog_stock_card_page_param,
    catalog_stock_page,
    catalog_stock_page_param,
    get_all_brands_from_catalog,
)
from fixtures.pages import (  # noqa: F401, E402
    catalog_page,
    contacts_page,
    home_page,
    login_page,
    pricing_page,
    registration_page,
)
from fixtures.visual import (  # noqa: F401, E402
    assert_snapshot_lenient,
    assert_snapshot_strict,
    assert_snapshot_with_threshold,
)

NOT_SPECIFIED = "Not specified"
NOT_SPECIFIED_LABEL = "not_specified"


@lru_cache(maxsize=1)
def _get_device_browser_info(config_browser: str = None) -> dict:
    """Get device and browser information from environment (cached)"""
    device = os.getenv("DEVICE", "")
    browser_type = config_browser or os.getenv("BROWSER", "chromium").lower()

    browser_display_names = {
        "chromium": "Chromium",
        "firefox": "Firefox",
        "webkit": "WebKit"
    }
    browser_display_name = browser_display_names.get(browser_type, "Chromium")

    if device:
        device_display_name = DEVICE_NAMES.get(device, device).replace("_", " ")
        viewport_info = _get_viewport_info(device)
    else:
        device_display_name = NOT_SPECIFIED
        viewport_info = ""

    return {
        "device": device,
        "browser_type": browser_type,
        "device_display_name": device_display_name,
        "browser_display_name": browser_display_name,
        "viewport_info": viewport_info,
    }


@lru_cache(maxsize=10)
def _get_viewport_info(device: str) -> str:
    """Get viewport information for device label (cached)"""
    try:
        with sync_playwright() as p:
            device_config = get_device_config(p, device)
            viewport = device_config.get("viewport", {})
            width = viewport.get("width", "?")
            height = viewport.get("height", "?")
            return f"{width}x{height}"
    except Exception as e:
        logging.debug(f"Failed to get viewport size: {e}")
        return ""


def _get_browser_from_config(config) -> str:
    """Extract browser type from config"""
    try:
        return config.getoption("--browser", default="chromium").lower()
    except (ValueError, AttributeError):
        return "chromium"


def _add_metadata_to_config(config, info: dict):
    """Add device and browser metadata to config"""
    metadata_dict = {
        "Device": info["device_display_name"],
        "Browser": info["browser_display_name"],
        "Device Type": info["device"] or NOT_SPECIFIED,
        "Browser Type": info["browser_type"] or NOT_SPECIFIED,
    }
    if info["viewport_info"]:
        metadata_dict["Viewport"] = info["viewport_info"]

    # Use pytest-metadata stash (required for pytest-html compatibility)
    # Note: stash should already be initialized in pytest_configure
    try:

        # Ensure stash exists (should already be initialized, but be safe)
        if metadata_key not in config.stash:
            config.stash[metadata_key] = {}
        config.stash[metadata_key].update(metadata_dict)

    except (ImportError, KeyError, AttributeError):

        # If pytest-metadata is not available, skip stash update
        # but still update _metadata for backward compatibility
        pass

    # Also update _metadata attribute for backward compatibility
    if hasattr(config, "_metadata"):
        config._metadata.update(metadata_dict)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure pytest with device/browser info and disable playwright fixtures"""
    # Disable pytest-playwright browser fixtures to use our custom ones
    config.option.plugins = [p for p in config.option.plugins if "pytest_playwright" not in str(p)]

    # Initialize metadata stash EARLY to prevent pytest-html KeyError
    # pytest-html accesses metadata in pytest_sessionstart, so we must initialize it here
    try:

        # Initialize empty dict if not exists - pytest-html expects this
        if metadata_key not in config.stash:
            config.stash[metadata_key] = {}
    except ImportError:
        # pytest-metadata should be installed, but handle gracefully if not
        pass

    # Add metadata for HTML reports
    browser_type = _get_browser_from_config(config)
    info = _get_device_browser_info(browser_type)
    _add_metadata_to_config(config, info)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Ensure metadata stash is initialized before pytest-html tries to access it"""
    # This hook runs before pytest-html's pytest_sessionstart
    # We need to ensure metadata stash exists to prevent KeyError
    try:
        if metadata_key not in session.config.stash:
            session.config.stash[metadata_key] = {}
    except ImportError:
        pass


def _add_allure_labels(info: dict):
    """Add Allure dynamic labels"""
    allure.dynamic.label("device", info["device"] or NOT_SPECIFIED_LABEL)
    allure.dynamic.label("browser", info["browser_type"] or NOT_SPECIFIED_LABEL)
    allure.dynamic.label("device_type", info["device_display_name"])
    allure.dynamic.label("browser_type", info["browser_display_name"])
    if info["viewport_info"]:
        allure.dynamic.label("viewport", info["viewport_info"])


def _add_user_properties(item, info: dict):
    """Add user properties to test item"""
    properties = [
        ("device", info["device"] or NOT_SPECIFIED_LABEL),
        ("browser", info["browser_type"] or NOT_SPECIFIED_LABEL),
        ("device_type", info["device_display_name"]),
        ("browser_type", info["browser_display_name"]),
    ]
    if info["viewport_info"]:
        properties.append(("viewport", info["viewport_info"]))

    item.user_properties.extend(properties)


def _add_xml_properties(item, info: dict):
    """Add XML properties for JUnit reports"""
    try:
        xml = item.config.stash.get(xml_key, None)
        if xml is not None:
            xml.add_global_property("device", info["device"] or NOT_SPECIFIED_LABEL)
            xml.add_global_property("browser", info["browser_type"] or NOT_SPECIFIED_LABEL)
            xml.add_global_property("device_type", info["device_display_name"])
            xml.add_global_property("browser_type", info["browser_display_name"])
            if info["viewport_info"]:
                xml.add_global_property("viewport", info["viewport_info"])
    except (ImportError, AttributeError):
        pass


def _start_trace_if_enabled(item):
    """Start tracing if enabled"""
    if os.getenv("TRACE_ON_FAILURE", "true").lower() == "true":
        browser_context = item.funcargs.get("context")
        if browser_context:
            browser_context.tracing.start_chunk()
            item._trace_chunk_started = True
        else:
            item._trace_chunk_started = False


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Add Allure labels, test metadata, and JUnit XML properties for device and browser"""
    browser_type = _get_browser_from_config(item.config)
    info = _get_device_browser_info(browser_type)

    _add_allure_labels(info)
    _add_user_properties(item, info)
    _add_xml_properties(item, info)
    _start_trace_if_enabled(item)




def _capture_page_artifacts(browser_page, test_name: str, failed_screenshots_dir: Path):
    """Capture page screenshot, HTML, and URL on failure"""
    if not browser_page:
        return

    try:
        with allure.step("Screenshot on failure"):
            try:
                screenshot_bytes = browser_page.screenshot(full_page=True, timeout=5000)
                screenshot_path = failed_screenshots_dir / f"{test_name}.png"
                screenshot_path.write_bytes(screenshot_bytes)
                allure.attach(
                    screenshot_bytes,
                    name="Screenshot on failure",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                allure.attach(
                    f"Failed to capture screenshot: {str(e)}",
                    name="Screenshot Error",
                    attachment_type=allure.attachment_type.TEXT
                )

        with allure.step("HTML on failure"):
            try:
                html_content = browser_page.content()
                allure.attach(
                    html_content,
                    name="Page HTML on failure",
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception as e:
                allure.attach(
                    f"Failed to capture HTML: {str(e)}",
                    name="HTML Error",
                    attachment_type=allure.attachment_type.TEXT
                )

        with allure.step("Page URL on failure"):
            try:
                page_url = browser_page.url
                allure.attach(
                    page_url,
                    name="Page URL",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                allure.attach(
                    f"Failed to capture URL: {str(e)}",
                    name="URL Error",
                    attachment_type=allure.attachment_type.TEXT
                )
    except Exception as e:
        allure.attach(
            f"Failed to capture page artifacts: {str(e)}",
            name="Artifacts Capture Error",
            attachment_type=allure.attachment_type.TEXT
        )


def _save_trace_on_failure(item, info: dict, test_name: str):
    """Save Playwright trace on test failure"""
    browser_context = item.funcargs.get("context")
    if not browser_context or not getattr(item, "_trace_chunk_started", False):
        return

    device = info["device"]
    if not device:
        return

    base_trace_dir = os.getenv("TRACE_DIR", "reports/trace")
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "")

    if worker_id:
        trace_dir = Path(base_trace_dir) / device / info["browser_type"] / worker_id / "failed"
    else:
        trace_dir = Path(base_trace_dir) / device / info["browser_type"] / "failed"

    trace_dir.mkdir(parents=True, exist_ok=True)
    trace_filename = trace_dir / f"{test_name}.zip"
    browser_context.tracing.stop_chunk(path=str(trace_filename))

    if trace_filename.exists():
        allure.attach.file(
            str(trace_filename),
            name="Playwright Trace",
            attachment_type=allure.attachment_type.ZIP
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Generate test report with device/browser info and handle failures"""
    outcome = yield
    rep = outcome.get_result()

    browser_type = _get_browser_from_config(item.config)
    info = _get_device_browser_info(browser_type)

    # Add device/browser info to report
    rep.device = info["device"]
    rep.browser = info["browser_type"]
    rep.viewport = info["viewport_info"]
    rep.device_display = info["device_display_name"]
    rep.browser_display = info["browser_display_name"]

    # Add CTRF fields for github-test-reporter (message, trace, line, filePath, duration)
    if rep.when == "call":
        # Extract file path and line number
        if hasattr(item, "fspath"):
            rep.filePath = str(item.fspath)
        elif hasattr(item, "location") and len(item.location) >= 1:
            rep.filePath = str(item.location[0])

        if hasattr(item, "location") and len(item.location) >= 2:
            rep.line = item.location[1]

        # Store duration for CTRF format (pytest-json-ctrf will handle conversion to milliseconds)
        # Keep rep.duration in seconds (float) for pytest-html compatibility
        # CTRF format requires milliseconds, but pytest-json-ctrf plugin handles the conversion automatically
        # We only store duration if it's not already set, preserving original pytest duration format
        if not hasattr(rep, 'duration') or rep.duration is None:
            if hasattr(call, 'duration') and call.duration is not None:
                rep.duration = call.duration  # Keep in seconds for pytest-html

        # Extract message and trace from longrepr for failed tests
        if rep.failed and rep.longrepr:
            longrepr_str = str(rep.longrepr)
            rep.trace = longrepr_str

            # Extract message (first line with error)
            lines = longrepr_str.split('\n')
            for line in lines:
                if line.strip() and ('AssertionError' in line or 'Error:' in line or 'Failed:' in line):
                    rep.message = line.strip()
                    break
            if not hasattr(rep, 'message') or not rep.message:
                rep.message = lines[0].strip() if lines else None

    trace_on_failure = os.getenv("TRACE_ON_FAILURE", "true").lower() == "true"

    # Stop trace chunk if test passed
    if rep.when == "call" and trace_on_failure and not rep.failed:
        browser_context = item.funcargs.get("context")
        if browser_context and getattr(item, "_trace_chunk_started", False):
            browser_context.tracing.stop_chunk()

    # Handle test failures and teardown errors
    if (rep.when == "call" and rep.failed) or (rep.when == "teardown" and rep.failed):
        failed_screenshots_dir = Path("reports/failed_screenshots")
        failed_screenshots_dir.mkdir(parents=True, exist_ok=True)

        test_name = item.nodeid.replace("::", "_").replace("/", "_").replace(".py", "")
        is_pixel_test = "pixel" in str(item.fspath) or "pixel" in item.nodeid

        # Handle pixel test failures (including teardown failures from pytest-playwright-visual-snapshot)
        if is_pixel_test:
            # Check if this is a visual snapshot error
            if rep.when == "teardown" and "Snapshots DO NOT match" in str(rep.longrepr):
                # Attach visual comparison artifacts for teardown failures
                from utils.allure_helpers import attach_visual_snapshot_comparison

                # Extract module and snapshot names from test
                test_parts = item.nodeid.split("::")
                module_name = test_parts[0].replace("tests/pixels-tests/", "").replace(".py", "")
                if module_name.startswith("test_"):
                    module_name = module_name[5:]  # Remove "test_"
                if module_name.endswith("_pixels"):
                    module_name = module_name[:-7]  # Remove "_pixels"

                snapshot_name = test_parts[-1].split('[')[0] if len(test_parts) >= 2 else test_parts[0].split('[')[0]
                if not snapshot_name.endswith('.png'):
                    snapshot_name = f"{snapshot_name}.png"

                attach_visual_snapshot_comparison(
                    item.nodeid,
                    module_name,
                    snapshot_name,
                    is_failed=True
                )

        # Capture regular artifacts for non-pixel tests
        if not is_pixel_test:
            browser_page = item.funcargs.get("page")
            if browser_page and rep.when != "teardown":  # Skip page artifacts in teardown to avoid closed event loop
                _capture_page_artifacts(browser_page, test_name, failed_screenshots_dir)

        # Save trace on failure
        if trace_on_failure:
            _save_trace_on_failure(item, info, test_name)


try:
    @pytest.hookimpl(optionalhook=True)
    def pytest_html_results_table_header(cells):
        cells.insert(2, "<th>Device</th>")
        cells.insert(3, "<th>Browser</th>")
        cells.insert(4, "<th>Viewport</th>")

    @pytest.hookimpl(optionalhook=True)
    def pytest_html_results_table_row(report, cells):
        device_display = getattr(report, "device_display", "N/A")
        browser_display = getattr(report, "browser_display", "N/A")
        viewport = getattr(report, "viewport", "N/A")

        cells.insert(2, f"<td>{device_display}</td>")
        cells.insert(3, f"<td>{browser_display}</td>")
        cells.insert(4, f"<td>{viewport}</td>")
except ImportError:
    pass
