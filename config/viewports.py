"""
Viewport configurations for visual regression tests.

This module provides standardized viewport sizes for different device types
to ensure consistency across all pixel tests.

Device specifications:
- Desktop: Desktop Chrome (1280x720)
- Mobile: iPhone 15 Pro Max (430x739)
- Tablet: iPad Pro 11 (834x1194)

To add a new viewport, simply add it to VIEWPORTS dictionary.
"""

from typing import Dict

# Viewport configurations for Playwright set_viewport_size()
# To add a new viewport, add a new entry here
VIEWPORTS: Dict[str, Dict[str, int]] = {
    "desktop": {"width": 1280, "height": 720},
    "mobile": {"width": 430, "height": 739},  # iPhone 15 Pro Max
    "tablet": {"width": 834, "height": 1194},  # iPad Pro 11
    # Add new viewports here, for example:
    # "mobile_small": {"width": 375, "height": 667},  # iPhone SE
}

# Convenience constants for direct use in tests
DESKTOP_VIEWPORT = VIEWPORTS["desktop"]
MOBILE_VIEWPORT = VIEWPORTS["mobile"]
TABLET_VIEWPORT = VIEWPORTS["tablet"]

# Width and height constants for parametrize decorators
DESKTOP_WIDTH, DESKTOP_HEIGHT = DESKTOP_VIEWPORT["width"], DESKTOP_VIEWPORT["height"]
MOBILE_WIDTH, MOBILE_HEIGHT = MOBILE_VIEWPORT["width"], MOBILE_VIEWPORT["height"]
TABLET_WIDTH, TABLET_HEIGHT = TABLET_VIEWPORT["width"], TABLET_VIEWPORT["height"]
