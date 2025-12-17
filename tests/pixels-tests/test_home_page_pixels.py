import logging

import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.home_locators import AboutLocators, HeaderLocators, ServicesLocators
from utils.playwright_helpers import scroll_to_make_visible


def wait_for_page_ready(page) -> None:
    page.wait_for_load_state("networkidle")

    # Wait for images to load
    try:
        page.wait_for_function(
            "() => Array.from(document.images).every(img => img.complete)",
            timeout=5000
        )
    except Exception as e:
        logging.debug(f"Failed to wait for all images to load (continuing): {e}")
        pass

    # Wait for lazy-loaded content
    expect(page.locator("main, .main-content, [role='main']").first).to_be_visible(timeout=2000)

    # Ensure page is scrolled to top
    page.evaluate("() => window.scrollTo(0, 0)")
    expect(page.locator("body")).to_be_visible(timeout=500)


def wait_for_element_ready(page, element=None) -> None:
    if element:
        expect(element).to_be_visible(timeout=500)
    else:
        expect(page.locator("body")).to_be_visible(timeout=500)


@allure.epic("Visual Regression")
@allure.feature("Home Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestHomePageVisualRegression:

    @allure.title("Header section snapshot")
    @pytest.mark.pixel_test
    def test_header(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/")
        wait_for_page_ready(page)

        with allure.step("Capture header section"):
            header = page.locator(HeaderLocators.container).first
            expect(header).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(header).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(header, threshold=0.15)

    @allure.title("Main content snapshot")
    @pytest.mark.pixel_test
    def test_main_content(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/")
        wait_for_page_ready(page)

        with allure.step("Capture main content section"):
            # Wait for main content before capturing full page screenshot
            expect(page.locator("main, .main-content, [role='main']").first).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete before full page screenshot
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(page.screenshot(full_page=True), threshold=0.15)

    @allure.title("Footer section snapshot")
    @pytest.mark.pixel_test
    def test_footer(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/")
        wait_for_page_ready(page)

        with allure.step("Capture footer section"):
            copyright_text = page.locator("text=2022-2025 © TUN SERVICE")
            expect(copyright_text).to_be_visible(timeout=5000)
            footer = copyright_text.locator(
                "xpath=ancestor::footer | ancestor::div[contains(@class, 'footer')] | ancestor::div[position()=last()-2]"
            ).first
            expect(footer).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            scroll_to_make_visible(footer)
            wait_for_element_ready(page, footer)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(footer, threshold=0.15)

    @allure.title("Hero section snapshot")
    @pytest.mark.pixel_test
    def test_hero_section(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/")
        wait_for_page_ready(page)

        with allure.step("Capture hero section"):
            hero = page.locator(".f-block-gradient").first
            expect(hero).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(hero).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(hero, threshold=0.15)

    @allure.title("Cards section snapshot (Power, Systems, Standards)")
    @pytest.mark.pixel_test
    def test_cards_section(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/")
        wait_for_page_ready(page)

        with allure.step("Capture cards section"):
            cards_container = page.locator(".container.flex.flex-col.gap-5").first
            expect(cards_container).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            scroll_to_make_visible(cards_container)
            wait_for_element_ready(page, cards_container)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(cards_container, threshold=0.15)

    @allure.title("About section snapshot (Кто мы?)")
    @pytest.mark.pixel_test
    def test_about_section(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/")
        wait_for_page_ready(page)

        with allure.step("Find and capture about section"):
            about_section = page.locator(AboutLocators.container).first
            expect(about_section).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            scroll_to_make_visible(about_section)
            wait_for_element_ready(page, about_section)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(about_section, threshold=0.15)

    @allure.title("Why section snapshot (Почему мы?)")
    @pytest.mark.pixel_test
    def test_why_section(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/")
        wait_for_page_ready(page)

        with allure.step("Capture why section"):
            why_section = page.locator("section.why-are-we").first
            expect(why_section).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            scroll_to_make_visible(why_section)
            wait_for_element_ready(page, why_section)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(why_section, threshold=0.15)

    @allure.title("Services section snapshot (Diesel + Gasoline)")
    @pytest.mark.pixel_test
    def test_services_section(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/")
        wait_for_page_ready(page)

        with allure.step("Find and capture services section"):
            services_section = page.locator(ServicesLocators.container).first
            expect(services_section).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            scroll_to_make_visible(services_section)
            wait_for_element_ready(page, services_section)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(services_section, threshold=0.15)
