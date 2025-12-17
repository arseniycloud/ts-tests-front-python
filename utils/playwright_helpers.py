from playwright.sync_api import Locator


def scroll_to_make_visible(locator: Locator) -> None:
    """Scroll page to make element visible in viewport if it's not already visible"""
    locator.scroll_into_view_if_needed()
