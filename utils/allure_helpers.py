"""
Allure reporting utilities for Playwright tests
Provides helper functions for attaching screenshots, HTML, and logs to Allure reports
"""

import os
import re
from pathlib import Path
from typing import Optional
import logging
import json


import allure
from playwright.sync_api import Locator, Page


def _get_device_suffix() -> str:
    """Get device suffix for snapshot naming based on DEVICE env var."""
    device = os.getenv("DEVICE", "").lower()

    if device in ("mobile", "iphone", "phone", "smartphone"):
        return "_mobile"

    elif device in ("tablet", "ipad", "pad"):
        return "_tablet"

    elif device in ("desktop", "pc", "laptop"):
        return "_desktop"

    return ""


def attach_screenshot(page: Page, name: str = "Screenshot", full_page: bool = True, timeout: int = 30000) -> None:
    """
    Attach screenshot to Allure report.
    This function attaches screenshot to the current active Allure step.
    Should be called within 'with allure.step(...)' context to attach to that step.

    Args:
        page: Playwright Page object
        name: Name for the attachment in Allure report
        full_page: Whether to capture full page or viewport only
        timeout: Timeout for screenshot capture in milliseconds (default: 30000)
    """
    try:
        screenshot_bytes = page.screenshot(full_page=full_page, timeout=timeout)
        allure.attach(
            screenshot_bytes,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    except Exception as e:
        # Silently fail - don't create separate step or attachment for errors
        # The error will be visible in test logs if needed
        logging.warning(f"Failed to capture screenshot '{name}': {str(e)}")


def attach_element_screenshot(page_or_locator, selector_or_name=None, name="Element Screenshot"):
    """
    Attach screenshot of specific element to Allure report.
    This function attaches screenshot to the current active Allure step.
    Should be called within 'with allure.step(...)' context to attach to that step.

    Args:
        page_or_locator: Playwright Page object or Locator object
        selector_or_name: CSS selector string (if page_or_locator is Page) or name (if page_or_locator is Locator)
        name: Name for the attachment in Allure report
    """
    try:
        if isinstance(page_or_locator, Locator):
            element = page_or_locator

            if selector_or_name:
                name = selector_or_name

        else:
            if not selector_or_name:
                raise ValueError("Selector is required when page_or_locator is Page")

            element = page_or_locator.locator(selector_or_name).first

        if element.count() > 0:
            screenshot_bytes = element.screenshot()
            allure.attach(
                screenshot_bytes,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )

        else:
            allure.attach(
                "Element not found",
                name=f"{name} (Element Not Found)",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        allure.attach(
            f"Failed to capture element screenshot: {str(e)}",
            name=f"{name} (Error)",
            attachment_type=allure.attachment_type.TEXT
        )


def attach_html(page: Page, name: str = "Page HTML") -> None:
    """
    Attach page HTML to Allure report

    Args:
        page: Playwright Page object
        name: Name for the attachment in Allure report
    """
    try:
        html_content = page.content()
        allure.attach(
            html_content,
            name=name,
            attachment_type=allure.attachment_type.HTML
        )

    except Exception as e:
        allure.attach(
            f"Failed to capture HTML: {str(e)}",
            name=f"{name} (Error)",
            attachment_type=allure.attachment_type.TEXT
        )


def attach_text(content: str, name: str = "Text Attachment") -> None:
    """
    Attach text content to Allure report

    Args:
        content: Text content to attach
        name: Name for the attachment in Allure report
    """
    allure.attach(
        content,
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )


def attach_json(data: dict, name: str = "JSON Attachment") -> None:
    """
    Attach JSON data to Allure report

    Args:
        data: Dictionary to serialize as JSON
        name: Name for the attachment in Allure report
    """

    json_content = json.dumps(data, indent=2, ensure_ascii=False)
    allure.attach(
        json_content,
        name=name,
        attachment_type=allure.attachment_type.JSON
    )


def attach_file(file_path: Path, name: Optional[str] = None) -> None:
    """
    Attach file to Allure report

    Args:
        file_path: Path to the file to attach
        name: Optional name for the attachment (defaults to filename)
    """
    if not file_path.exists():
        allure.attach(
            f"File not found: {file_path}",
            name=f"{name or file_path.name} (Not Found)",
            attachment_type=allure.attachment_type.TEXT
        )
        return

    try:
        with open(file_path, "rb") as f:
            file_content = f.read()

        attachment_type = allure.attachment_type.TEXT

        suffix = file_path.suffix.lower()
        if suffix == ".png":
            attachment_type = allure.attachment_type.PNG
        elif suffix in [".jpg", ".jpeg"]:
            attachment_type = allure.attachment_type.JPG
        elif suffix == ".gif":
            attachment_type = allure.attachment_type.GIF

        elif file_path.suffix.lower() == ".json":
            attachment_type = allure.attachment_type.JSON

        elif file_path.suffix.lower() in [".html", ".htm"]:
            attachment_type = allure.attachment_type.HTML

        elif file_path.suffix.lower() == ".xml":
            attachment_type = allure.attachment_type.XML

        allure.attach(
            file_content,
            name=name or file_path.name,
            attachment_type=attachment_type
        )

    except Exception as e:
        allure.attach(
            f"Failed to attach file: {str(e)}",
            name=f"{name or file_path.name} (Error)",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.step("Attach page state: {name}")
def attach_page_state(page: Page, name: str = "Page State") -> None:
    attach_screenshot(page, name=f"{name} - Screenshot")

    attach_html(page, name=f"{name} - HTML")
    attach_text(page.url, name=f"{name} - URL")


def _sanitize_name(name: str) -> str:
    """Clean name for filesystem usage."""
    return re.sub(r'\W', '_', name)


def _clean_module_name(module_name: str) -> str:
    """Clean module name for references directory lookup."""
    # For references directory, we need the full module name with test_ and _pixels
    # because that's how pytest-playwright-visual-snapshot creates the structure
    if not module_name.startswith("test_"):
        module_name = f"test_{module_name}"

    if not module_name.endswith("_pixels"):
        module_name = f"{module_name}_pixels"

    return _sanitize_name(module_name)


def _attach_file_to_allure(file_path: Path, attachment_name: str) -> bool:
    """Safely attach file to Allure report."""
    if not file_path.exists():
        return False

    try:
        with open(file_path, "rb") as f:
            allure.attach(
                f.read(),
                name=attachment_name,
                attachment_type=allure.attachment_type.PNG
            )
        return True

    except Exception:
        return False


def _find_expected_snapshot(snapshots_dir: Path, module_name: str, snapshot_name: str) -> Optional[Path]:
    """Find expected snapshot file in references directory."""
    clean_module = _clean_module_name(module_name)

    # Remove .png extension and device suffix from snapshot_name to get directory name
    snapshot_base_name = snapshot_name.replace('.png', '')

    for suffix in ('_desktop', '_mobile', '_tablet'):
        if snapshot_base_name.endswith(suffix):
            snapshot_dir_name = snapshot_base_name[:-len(suffix)]
            break

    else:
        snapshot_dir_name = snapshot_base_name

    snapshot_dir = snapshots_dir / clean_module / snapshot_dir_name

    if not snapshot_dir.exists():
        return None


    # Try to find exact match with device suffix first
    device_suffix = _get_device_suffix()
    if device_suffix:
        exact_file = snapshot_dir / f"{snapshot_dir_name}{device_suffix}.png"

        if exact_file.exists():
            return exact_file

    # Fall back to file without device suffix
    base_file = snapshot_dir / f"{snapshot_dir_name}.png"
    if base_file.exists():
        return base_file

    # Find any matching snapshot file as last resort
    matching_files = list(snapshot_dir.glob(f"{snapshot_dir_name}*.png"))
    return matching_files[0] if matching_files else None


def _find_visual_failure_directory(failures_dir: Path, test_name: str) -> Optional[Path]:
    """Find visual failure directory for test in snapshot_failures structure."""
    if not failures_dir.exists():
        return None

    # Extract test parts from node ID
    # e.g., "tests/pixels-tests/test_profile_page_pixels.py::TestClass::test_method[chromium]"
    test_parts = test_name.split("::")
    if len(test_parts) < 2:
        return None

    # Get module name (e.g., "test_profile_page_pixels")
    module_path = test_parts[0]  # "tests/pixels-tests/test_profile_page_pixels.py"
    module_name = Path(module_path).stem  # "test_profile_page_pixels"

    # Get test function name with parameters
    test_function = test_parts[-1]  # "test_method[chromium]"

    # Look for test directory in module directory
    module_dir = failures_dir / module_name

    if not module_dir.exists():
        return None

    # Find directories that match the test function (with browser/platform params)
    # e.g., "test_method[chromium][darwin]"
    # Extract base function name without parameters for more flexible matching
    base_function = test_function.split('[')[0]  # "test_profile_block"
    matching_dirs = list(module_dir.glob(f"{base_function}*"))

    return matching_dirs[0] if matching_dirs else None


def _attach_expected_snapshot(snapshots_dir: Path, module_name: str, snapshot_name: str) -> None:
    """Attach expected snapshot to Allure if found."""
    if not snapshots_dir.exists():
        return

    expected_file = _find_expected_snapshot(snapshots_dir, module_name, snapshot_name)
    if expected_file:
        _attach_file_to_allure(expected_file, "Expected Screenshot (Reference)")



def attach_visual_snapshot_comparison(
    test_name: str,
    module_name: str,
    snapshot_name: str,
    is_failed: bool = False
) -> None:
    """
    Attach visual snapshot comparison artifacts to Allure report within Visual comparison step.

    Args:
        test_name: Full test node ID (e.g., "tests/pixels-tests/test_file.py::TestClass::test_func[param]")
        module_name: Module name without test_ prefix and _pixels suffix (e.g., "home_page")
        snapshot_name: Snapshot name (test function name)
        is_failed: Whether the test failed
    """

    # Always attach expected snapshot from references
    _attach_expected_snapshot(Path("references"), module_name, snapshot_name)

    if is_failed:
        # For failed tests, also attach Diff from snapshot_failures directory
        visual_failures_dir = Path("snapshot_failures")

        # Find the test failure directory
        failure_dir = _find_visual_failure_directory(visual_failures_dir, test_name)
        if failure_dir:
            # Look for diff file in the failure directory
            diff_files = list(failure_dir.glob("diff_*.png"))
            
            if diff_files:
                _attach_file_to_allure(diff_files[0], "Visual Diff (Pixel Differences)")
