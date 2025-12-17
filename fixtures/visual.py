"""Visual regression testing fixtures and utilities for pytest-playwright-visual-snapshot"""

import logging
import os
import time

import allure
import pytest

from utils.allure_helpers import attach_visual_snapshot_comparison


def _get_browser_name() -> str:
    """Get browser name from BROWSER env var."""
    browser = os.getenv("BROWSER", "chromium").strip().lower()
    return browser


def _get_viewport_name() -> str:
    """
    Get viewport name from DEVICE env var.
    Returns 'desktop' by default if not specified.
    """
    device = os.getenv("DEVICE", "desktop").strip().lower()
    if not device:
        return "desktop"
    return device


def _generate_snapshot_name_from_test(test_name: str) -> str:
    """Generate snapshot name from test name."""
    test_parts = test_name.split("::")
    if len(test_parts) >= 2:
        return test_parts[-1].split("[")[0]
    return test_name.split("[")[0]


def _build_snapshot_name(title: str) -> str:
    """
    Build snapshot name in format: {browser}-{viewport}-{title}.png

    Examples:
        chromium-desktop-test_header.png
        webkit-desktop-test_footer.png
    """
    browser = _get_browser_name()
    viewport = _get_viewport_name()

    # Clean up title
    clean_title = title
    if clean_title.endswith('.png'):
        clean_title = clean_title[:-4]

    # Remove any existing browser/viewport prefixes to avoid duplication
    for prefix in ['chromium-', 'webkit-', 'firefox-', 'desktop-', 'mobile-', 'tablet-']:
        if clean_title.startswith(prefix):
            clean_title = clean_title[len(prefix):]

    return f"{browser}-{viewport}-{clean_title}.png"


def _ensure_png_extension(name: str) -> str:
    """Ensure snapshot name has .png extension."""
    if not name.endswith('.png'):
        return f"{name}.png"
    return name


def _extract_module_name(test_name: str) -> str:
    """Extract module name from test name for snapshot path."""
    test_parts = test_name.split("::")
    module_name = test_parts[0].replace("tests/pixels-tests/", "").replace(".py", "")

    if module_name.startswith("test_"):
        module_name = module_name[5:]

    if module_name.endswith("_pixels"):
        module_name = module_name[:-7]

    return module_name


def _get_screenshot_bytes(screenshot) -> bytes | None:
    """Extract screenshot bytes from screenshot object."""
    if isinstance(screenshot, bytes):
        return screenshot

    try:
        if hasattr(screenshot, 'screenshot'):
            return screenshot.screenshot()
    except Exception as e:
        logging.debug(f"Failed to get screenshot bytes from object: {e}")

    return None


def _attach_current_screenshot(screenshot_bytes: bytes | None) -> None:
    """Attach current screenshot to Allure report."""
    if screenshot_bytes:
        allure.attach(
            screenshot_bytes,
            name="Current Screenshot (Actual)",
            attachment_type=allure.attachment_type.PNG
        )


def _handle_snapshot_assertion(assert_snapshot_func, screenshot, name: str, threshold, fail_fast, mask_elements,
                              test_name: str, module_name: str):
    """Handle snapshot assertion with error handling and Allure attachments."""
    try:
        result = assert_snapshot_func(
            screenshot,
            name=name,
            threshold=threshold,
            fail_fast=fail_fast,
            mask_elements=mask_elements
        )

        attach_visual_snapshot_comparison(
            test_name,
            module_name,
            name,
            is_failed=False
        )
        return result

    except (AssertionError, ValueError):
        # Wait for snapshot artifacts to be written before attaching
        time.sleep(0.5)
        attach_visual_snapshot_comparison(
            test_name,
            module_name,
            name,
            is_failed=True
        )
        raise


def _add_allure_support(assert_snapshot_func, request, threshold_value=None):
    """Helper function to add Allure attachments to any assert_snapshot fixture."""

    def _assert_with_allure(screenshot, name=None, threshold=None, fail_fast=False, mask_elements=None):
        if threshold is None and threshold_value is not None:
            threshold = threshold_value

        test_name = request.node.nodeid

        if name is None:
            name = _generate_snapshot_name_from_test(test_name)

        # Build snapshot name with browser-viewport-title format
        name = _build_snapshot_name(name)

        module_name = _extract_module_name(test_name)

        with allure.step(f"Visual comparison: {name}"):
            screenshot_bytes = _get_screenshot_bytes(screenshot)
            _attach_current_screenshot(screenshot_bytes)

            return _handle_snapshot_assertion(
                assert_snapshot_func,
                screenshot,
                name,
                threshold,
                fail_fast,
                mask_elements,
                test_name,
                module_name
            )

    return _assert_with_allure


@pytest.fixture
def assert_snapshot_with_threshold(assert_snapshot, request):
    """
    Wrapper for snapshot assertions with configurable threshold and Allure support.

    Snapshot naming format: {browser}-{viewport}-{title}.png
    Examples:
        chromium-desktop-test_header.png
        webkit-desktop-test_footer.png

    Usage:
        def test_component(page, assert_snapshot_with_threshold):
            page.goto("/component")
            assert_snapshot_with_threshold(
                page.screenshot(),
                threshold=0.15  # 15% pixel difference allowed
            )
    """
    def _assert(screenshot, name=None, threshold=0.1, fail_fast=False, mask_elements=None):
        """
        Assert screenshot matches baseline snapshot with Allure attachments.

        Args:
            screenshot: Screenshot bytes from page.screenshot() or Page/Locator object
            name: Optional snapshot name (title part). Auto-generated if not provided
            threshold: Allowed pixel difference (0.0-1.0). Default 0.1 (10%)
            fail_fast: Fail immediately on first pixel difference
            mask_elements: List of CSS selectors to mask during screenshot

        Returns:
            None if match, raises AssertionError if mismatch
        """
        return _add_allure_support(assert_snapshot, request)(screenshot, name, threshold, fail_fast, mask_elements)

    return _assert


@pytest.fixture
def assert_snapshot_strict(assert_snapshot, request):
    """
    Strict snapshot matching (threshold=0.05) with Allure support.
    Use for critical UI components where precision is important.

    Snapshot naming format: {browser}-{viewport}-{title}.png
    """
    def _assert(screenshot, name=None, threshold=None, fail_fast=False, mask_elements=None):
        # Use strict threshold if not overridden
        if threshold is None:
            threshold = 0.05

        return _add_allure_support(assert_snapshot, request, threshold_value=0.05)(screenshot, name, threshold, fail_fast, mask_elements)

    return _assert


@pytest.fixture
def assert_snapshot_lenient(assert_snapshot, request):
    """
    Lenient snapshot matching (threshold=0.2) with Allure support.
    Use for components where pixel-perfect is not critical.

    Snapshot naming format: {browser}-{viewport}-{title}.png
    """
    def _assert(screenshot, name=None, threshold=None, fail_fast=False, mask_elements=None):
        # Use lenient threshold if not overridden
        if threshold is None:
            threshold = 0.2

        return _add_allure_support(assert_snapshot, request, threshold_value=0.2)(screenshot, name, threshold, fail_fast, mask_elements)

    return _assert
