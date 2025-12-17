import allure
import pytest
from playwright.sync_api import expect

from config.timeouts import Timeouts
from locators.balance_locators import (
    INTERNATIONAL_CARDS,
    RUSSIAN_CARDS,
    BalanceLocators,
)
from pages.balance_page import BalancePage


@allure.epic("Visual Regression")
@allure.feature("Balance Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestBalancePageVisualRegression:

    @allure.title("Payment methods - Russian cards snapshot (full page)")
    @pytest.mark.pixel_test
    def test_payment_methods_russian_cards(self, auth_user_existing, assert_snapshot_with_threshold):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            expect(page.locator(balance_page.locators.page_container)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)

        with allure.step("Select Russian cards payment method"):
            balance_page.select_payment_method(RUSSIAN_CARDS)
            expect(page.locator(balance_page.locators.payment_methods_select_button)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)

        with allure.step("Capture payment methods select snapshot with Russian cards"):
            locators = BalanceLocators()
            page_body = page.locator(locators.page_body)
            expect(page_body).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            # Scroll element into view, aligning to top of viewport
            page_body.scroll_into_view_if_needed()
            # Scroll a bit higher to ensure the form is fully visible with some padding
            page.evaluate("window.scrollBy(0, -500)")
            expect(page_body).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            # Capture screenshot of the full page body
            assert_snapshot_with_threshold(page_body, threshold=0.15)

    @allure.title("Payment methods - International cards snapshot (full page)")
    @pytest.mark.pixel_test
    def test_payment_methods_international_cards(self, auth_user_existing, assert_snapshot_with_threshold):
        page = auth_user_existing
        balance_page = BalancePage(page)

        with allure.step("Navigate to balance page"):
            balance_page.navigate_to_balance()
            expect(page.locator(balance_page.locators.page_container)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)

        with allure.step("Select international cards payment method"):
            balance_page.select_payment_method(INTERNATIONAL_CARDS)
            expect(page.locator(balance_page.locators.payment_methods_select_button)).to_be_visible(timeout=Timeouts.ShortWaits.VERY_SHORT_PAUSE)

        with allure.step("Capture payment methods select snapshot with International cards"):
            locators = BalanceLocators()
            page_body = page.locator(locators.page_body)
            expect(page_body).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            # Scroll element into view, aligning to top of viewport
            page_body.scroll_into_view_if_needed()
            # Scroll a bit higher to ensure the form is fully visible with some padding
            page.evaluate("window.scrollBy(0, -500)")
            expect(page_body).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(3000)
            # Capture screenshot of the full page body
            assert_snapshot_with_threshold(page_body, threshold=0.15)
