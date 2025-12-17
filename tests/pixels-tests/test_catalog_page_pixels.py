import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts


@allure.epic("Visual Regression")
@allure.feature("Catalog Page")
@allure.story("Visual Components")
@pytest.mark.pixel
class TestCatalogPageVisualRegression:

    @allure.title("Catalog main page snapshot (Level 1)")
    @pytest.mark.pixel_test
    def test_catalog_main_page(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/catalog")
        page.wait_for_load_state("networkidle")

        with allure.step("Capture catalog main page"):
            # Move mouse away to avoid hover/active states (e.g. 'current' element)
            page.mouse.move(0, 0)
            expect(page.locator("body")).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(page.locator("body")).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete before full page screenshot
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)
            # Capture full page screenshot
            assert_snapshot_with_threshold(page.screenshot(full_page=True), threshold=0.15)

    @allure.title("Brand selection page snapshot (Level 2)")
    @pytest.mark.pixel_test
    def test_brand_selection_page(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/catalog/car")
        page.wait_for_load_state("networkidle")

        with allure.step("Capture brand selection page"):
            # Capture catalog panel with brands
            panel = page.locator("[data-test-id='catalog_panel'].catalog-list-panel-ss.ts_wrap").first
            expect(panel).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(panel).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete
            page.wait_for_timeout(1000)
            assert_snapshot_with_threshold(panel.screenshot(), threshold=0.15)

    @allure.title("Engine type selection page snapshot (Level 3)")
    @pytest.mark.pixel_test
    def test_engine_selection_page(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/catalog/car/bmw-mini")
        page.wait_for_load_state("networkidle")

        with allure.step("Capture engine selection page"):
            # Move mouse away so no engine option is in 'current' (hover/active) state
            page.mouse.move(0, 0)
            expect(page.locator("body")).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(page.locator("body")).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete before full page screenshot
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)
            # Capture full page screenshot
            assert_snapshot_with_threshold(page.screenshot(full_page=True), threshold=0.15)

    @allure.title("ECU selection page snapshot (Level 4)")
    @pytest.mark.pixel_test
    def test_ecu_selection_page(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/catalog/car/bmw-mini/diesel")
        page.wait_for_load_state("networkidle")

        with allure.step("Capture ECU selection page"):
            expect(page.locator("body")).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(page.locator("body")).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete before full page screenshot
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)
            # Capture full page screenshot
            assert_snapshot_with_threshold(page.screenshot(full_page=True), threshold=0.15)

    @allure.title("Stock list page snapshot (Level 5)")
    @pytest.mark.pixel_test
    def test_stock_list_page(self, page, assert_snapshot_with_threshold):
        page.goto(f"{BASE_URL}/catalog/car/mazda/diesel/bosch-dcu17pc42")
        page.wait_for_load_state("networkidle")

        with allure.step("Capture stock list page"):
            expect(page.locator("body")).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            expect(page.locator("body")).to_be_visible(timeout=500)
            # Wait for animations and rendering to complete before full page screenshot
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)
            # Capture full page screenshot
            assert_snapshot_with_threshold(page.screenshot(full_page=True), threshold=0.15)

    @allure.title("Product card page snapshot (Level 6)")
    @pytest.mark.pixel_test
    def test_product_card_page(self, page, assert_snapshot_with_threshold):
        # Need to get actual stock ID from Level 5 page
        page.goto(f"{BASE_URL}/catalog/car/bmw-mini/diesel/bosch-edc16")
        page.wait_for_load_state("networkidle")

        with allure.step("Navigate to first product"):
            first_stock = page.locator(".ts_original_link.catalog-link").first
            first_stock.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)

        with allure.step("Capture product card"):
            product_card = page.locator(".product-card").first
            expect(product_card).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            page.wait_for_timeout(500)
            assert_snapshot_with_threshold(product_card.screenshot(), threshold=0.15)
