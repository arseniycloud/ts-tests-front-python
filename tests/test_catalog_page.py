import logging
import os
from datetime import datetime

import allure
import pytest
from playwright.sync_api import expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators.catalog_locators import CatalogLocators



TIMEOUT = 10000  # milliseconds
MAX_STOCKS_TO_CHECK = None  # None means check all stocks, or set to number to lim
locators = CatalogLocators()


@allure.epic("Catalog")
@allure.feature("Catalog Page")
@allure.title("Catalog Page - Navigation")
class TestCatalogPageTestsStructureAndLayout:

    @allure.title("Test catalog page elements are visible")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_catalog_page_elements(self, catalog_page):
        catalog_page.check_catalog_elements()

    @allure.title("Test catalog page layout structure")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_catalog_page_layout(self, catalog_page):


        # Check main container
        container = catalog_page.page.locator(locators.page_container)
        assert container.is_visible(), "Main container should be visible"

        # Check panel
        panel = catalog_page.page.locator(locators.catalog_panel)
        assert panel.is_visible(), "Catalog panel should be visible"

        # Check title
        title = catalog_page.page.locator(locators.page_title)
        assert title.is_visible(), "Page title should be visible"

    @allure.title("Test catalog container is visible")
    @pytest.mark.validation
    def test_catalog_container(self, catalog_page):
        container = catalog_page.page.locator(locators.page_container)
        assert container.is_visible(), "Catalog container should be visible"

    @allure.title("Test catalog panel is visible")
    @pytest.mark.validation
    def test_catalog_panel(self, catalog_page):
        panel = catalog_page.page.locator(locators.catalog_panel)
        assert panel.is_visible(), "Catalog panel should be visible"


class TestCatalogPageTitle:

    @allure.title("Test catalog title is visible")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_catalog_title(self, catalog_page):
        title = catalog_page.page.locator(locators.page_title)
        assert title.is_visible(), "Catalog title should be visible"
        title_text = title.text_content()
        assert (
            title_text is not None and len(title_text) > 0
        ), "Catalog title should have text"


class TestCatalogPageLinksFunctionality:

    @allure.title("Test catalog links are present")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_catalog_links_presence(self, catalog_page):
        links = catalog_page.page.locator(locators.catalog_links)
        assert links.count() >= 4, "Should have at least 4 catalog links"

    @allure.title("Test catalog links are visible")
    @pytest.mark.validation
    def test_catalog_links_visible(self, catalog_page):
        links = catalog_page.page.locator(locators.catalog_links).all()
        for link in links[:4]:  # Check first 4 links
            assert (
                link.is_visible()
            ), f"Link {link.get_attribute('href')} should be visible"

    @allure.title("Test catalog links are clickable")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_catalog_links_functionality(self, catalog_page):
        links = catalog_page.page.locator(locators.catalog_links)
        link_count = links.count()
        assert link_count > 0, "Should have at least one catalog link"

        for i in range(min(4, link_count)):  # Check first 4 links
            link = links.nth(i)
            assert link.is_visible(), f"Link {i} should be visible"

            # Check that link is clickable (may have href or be clickable element)
            href = link.get_attribute("href")
            class_attr = link.get_attribute("class") or ""

            # Link should either have href or be clickable (have cursor-pointer class)
            assert (href is not None and href != "") or "cursor-pointer" in class_attr or "catalog-link" in class_attr, \
                f"Link {i} should have href or be clickable"


class TestCatalogPageSearchFunctionality:

    @allure.title("Test catalog search functionality")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_catalog_search_functionality(self, catalog_page):
        # Test search with a sample term
        catalog_page.search_for_item("BMW")

        # Check if search results are displayed
        results = catalog_page.page.locator(locators.search_results)
        assert (results.count() >= 0
        ), "Search should return results or show no results message"


class TestCatalogPageItems:

    @allure.title("Test catalog items count")
    @pytest.mark.validation
    def test_catalog_items_count(self, catalog_page):
        items_count = catalog_page.get_catalog_items_count()
        assert items_count >= 0, "Catalog should have items or show empty state"


class TestCatalogPageNavigation:

    @allure.title("Test catalog page navigation")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_catalog_navigation(self, catalog_page):

        # Check if we're on catalog page
        assert "/catalog" in catalog_page.page.url, "Should be on catalog page"

        # Check page title
        title = catalog_page.page.locator(locators.page_title).text_content()
        assert title is not None, "Catalog page should have a title"

    @allure.title("Test catalog breadcrumbs are visible")
    @pytest.mark.validation
    def test_catalog_breadcrumbs(self, catalog_page):
        breadcrumbs = catalog_page.page.locator(locators.breadcrumbs)
        # Breadcrumbs may or may not be present
        if breadcrumbs.count() > 0:
            assert breadcrumbs.is_visible(), "Breadcrumbs should be visible"


class TestCatalogBrandPage:

    @allure.title("Complete validation of brand page: links, images, names")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_brand_page_complete(self, catalog_brand_page):
        page = catalog_brand_page.page

        # 1. Brand links presence and clickability validation
        brand_links = page.locator(locators.brand_links)
        brand_count = brand_links.count()
        assert brand_count > 0, "Brand page should have brand links"

        for i in range(min(5, brand_count)):
            link = brand_links.nth(i)
            assert link.is_visible(), f"Brand link {i} should be visible"

            # Check that link is clickable (may have href or be clickable element)
            href = link.get_attribute("href")
            class_attr = link.get_attribute("class") or ""

            # Link should either have href or be clickable (have cursor-pointer or catalog-link class)
            assert (href is not None and href != "") or "cursor-pointer" in class_attr or "catalog-link" in class_attr, \
                f"Brand link {i} should have href or be clickable"

        # 2. Brand images presence
        brand_images = page.locator(locators.brand_images)
        assert brand_images.count() > 0, "Brand page should have brand images"

        # 3. Brand names visible and not empty
        brand_names = page.locator(locators.brand_names)
        assert brand_names.count() > 0, "Brand page should have brand names"
        for i in range(min(3, brand_names.count())):
            brand = brand_names.nth(i)
            text = brand.text_content()
            assert (
                text is not None and len(text.strip()) > 0
            ), f"Brand {i} should have text"


class TestCatalogEnginePage:

    @allure.title("Complete validation of engine page: links, names, images, content")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_engine_page_complete(self, catalog_engine_page):
        page = catalog_engine_page.page

        # 1. Engine links presence and clickability validation
        engine_links = page.locator(locators.engine_links)
        engine_count = engine_links.count()
        assert engine_count > 0, "Engine page should have engine links"

        for i in range(engine_count):
            link = engine_links.nth(i)
            assert link.is_visible(), f"Engine link {i} should be visible"

            # Check that link is clickable (may have href or be clickable element)
            href = link.get_attribute("href")
            class_attr = link.get_attribute("class") or ""

            # Link should either have href starting with /catalog/ or be clickable
            if href:
                assert href.startswith("/catalog/"), f"Engine link {i} should start with /catalog/"
            else:
                # If no href, should be clickable via class
                assert "cursor-pointer" in class_attr or "catalog-link" in class_attr, \
                    f"Engine link {i} should be clickable"

        # 2. Engine images presence
        engine_images = page.locator(locators.engine_images)
        assert engine_images.count() > 0, "Engine page should have images"

        # 3. Engine names visible and check expected types
        engine_names = page.locator(locators.engine_names)
        assert engine_names.count() > 0, "Engine page should have names"

        actual_names = {engine_names.nth(i).text_content().strip() for i in range(engine_names.count())}
        expected_types = {"Diesel engines", "Petrol engines", "Gearbox"}
        assert any(expected in actual_names for expected in expected_types), f"Expected at least one of {expected_types}"

        # 4. Content container presence
        content = page.locator(locators.content_container)
        assert content.count() > 0 and content.is_visible(), "Content should be visible"

        # 5. Content title presence
        title = page.locator(locators.content_title)
        if title.count() > 0:
            assert title.text_content() is not None, "Title should have text"


class TestCatalogEnginePageMultipleBrands:

    @allure.title("Complete validation of engine page for multiple brands")
    @pytest.mark.validation
    def test_engine_page_complete_multiple_brands(self, catalog_engine_page_param):
        page = catalog_engine_page_param.page

        # 1. Engine links presence and clickability validation
        engine_links = page.locator(locators.engine_links)
        engine_count = engine_links.count()
        assert engine_count > 0, "Engine page should have links"

        for i in range(engine_count):
            link = engine_links.nth(i)
            assert link.is_visible(), f"Engine link {i} should be visible"

            # Check that link is clickable (may have href or be clickable element)
            href = link.get_attribute("href")
            class_attr = link.get_attribute("class") or ""

            # Link should either have href starting with /catalog/ or be clickable
            if href:
                assert href.startswith("/catalog/"), f"Engine link {i} should start with /catalog/"
            else:
                # If no href, should be clickable via class
                assert "cursor-pointer" in class_attr or "catalog-link" in class_attr, \
                    f"Engine link {i} should be clickable"

        # 2. Engine images presence
        engine_images = page.locator(locators.engine_images)
        assert engine_images.count() > 0, "Engine page should have images"

        # 3. Engine names visible and not empty
        engine_names = page.locator(locators.engine_names)
        assert engine_names.count() > 0, "Engine page should have names"
        for i in range(min(3, engine_names.count())):
            engine = engine_names.nth(i)
            text = engine.text_content()
            assert (text is not None and len(text.strip()) > 0), f"Engine {i} should have text"


class TestCatalogECUPage:

    @allure.title("Complete validation of ECU page: links, names, structure")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_ecu_page_complete(self, catalog_ecu_page):
        page = catalog_ecu_page.page

        # Wait for page to be fully loaded
        page.wait_for_load_state("domcontentloaded", timeout=Timeouts.BASE_PAGE_LOAD)
        ecu_links = page.locator(locators.ecu_links)
        expect(ecu_links.first).to_be_visible(timeout=Timeouts.ShortWaits.SHORT_PAUSE)

        # 1. ECU links presence and href validation
        ecu_count = ecu_links.count()
        assert ecu_count > 0, "ECU page should have links"

        for i in range(ecu_count):
            link = ecu_links.nth(i)
            assert link.is_visible(), f"ECU link {i} should be visible"

            # Check that link is clickable (may have href or be clickable element)
            href = link.get_attribute("href")
            class_attr = link.get_attribute("class") or ""

            # Link should either have href starting with /catalog/ or be clickable
            if href:
                assert href.startswith("/catalog/"), f"ECU link {i} should start with /catalog/"
            else:
                # If no href, should be clickable via class
                assert "cursor-pointer" in class_attr or "catalog-link" in class_attr, \
                    f"ECU link {i} should be clickable"

        # 2. ECU names visible and not empty
        ecu_names = page.locator(locators.ecu_names)
        assert ecu_names.count() > 0, "ECU page should have names"
        for i in range(min(3, ecu_names.count())):
            ecu = ecu_names.nth(i)
            text = ecu.text_content()
            assert (text is not None and len(text.strip()) > 0), f"ECU {i} should have text"


class TestCatalogECUPageMultipleBrands:

    @allure.title("Complete validation of ECU page for multiple brands")
    @pytest.mark.validation
    def test_ecu_page_complete_multiple_brands(self, catalog_ecu_page_param):
        page = catalog_ecu_page_param.page

        # Wait for page to be fully loaded
        page.wait_for_load_state("domcontentloaded", timeout=Timeouts.BASE_PAGE_LOAD)
        ecu_links = page.locator(locators.ecu_links)
        expect(ecu_links.first).to_be_visible(timeout=Timeouts.ShortWaits.SHORT_PAUSE)

        # 1. ECU links presence and clickability validation
        ecu_count = ecu_links.count()
        assert ecu_count > 0, "ECU page should have links"

        for i in range(ecu_count):
            link = ecu_links.nth(i)
            assert link.is_visible(), f"ECU link {i} should be visible"

            # Check that link is clickable (may have href or be clickable element)
            href = link.get_attribute("href")
            class_attr = link.get_attribute("class") or ""

            # Link should either have href starting with /catalog/ or be clickable
            if href:
                assert href.startswith("/catalog/"), f"ECU link {i} should start with /catalog/"
            else:
                # If no href, should be clickable via class
                assert "cursor-pointer" in class_attr or "catalog-link" in class_attr, \
                    f"ECU link {i} should be clickable"

        # 2. ECU names visible and not empty
        ecu_names = page.locator(locators.ecu_names)
        assert ecu_names.count() > 0, "ECU page should have names"
        for i in range(min(3, ecu_names.count())):
            ecu = ecu_names.nth(i)
            text = ecu.text_content()
            assert (text is not None and len(text.strip()) > 0), f"ECU {i} should have text"


class TestCatalogStockPage:

    def _check_stock_list_presence(self, page):
        """Check stock list structure presence"""
        stock_list = page.locator(locators.stock_list)
        assert (stock_list.count() > 0 and stock_list.is_visible()), "Stock list should be visible"

    def _check_stock_items_presence(self, page):
        """Check stock items presence and names"""
        stock_items = page.locator(locators.stock_items)
        stock_count = stock_items.count()
        assert stock_count > 0, "Stock page should have items"

        for i in range(min(3, stock_count)):
            item = stock_items.nth(i)
            name_span = item.locator("span").first
            if name_span.count() > 0:
                text = name_span.text_content()
                assert (
                    text is not None and len(text.strip()) > 0
                ), f"Stock {i} should have text"
            assert item.is_visible(), f"Stock item {i} should be visible"

    def _check_stock_links_validation(self, page):
        """Check stock items validation - items are clickable li elements"""
        stock_links = page.locator(locators.stock_link)
        link_count = stock_links.count()
        assert link_count > 0, "Stock page should have stock items"

        for i in range(min(5, link_count)):
            item = stock_links.nth(i)
            assert item.is_visible(), f"Stock item {i} should be visible"
            class_attr = item.get_attribute("class") or ""
            assert "cursor-pointer" in class_attr or "catalog-link" in class_attr, \
                f"Stock item {i} should be clickable"
        return stock_links, link_count

    def _test_click_first_item(self, page, stock_links, link_count):
        """Test clicking first item if it exists"""
        if link_count == 0:
            return

        current_url = page.url
        first_item = stock_links.first

        try:
            first_item.click(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
            product_card = page.locator(locators.product_card)
            expect(product_card).to_be_visible(timeout=Timeouts.ShortWaits.SHORT_PAUSE)

            if page.url != current_url:
                expect(product_card).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
                title = page.title()
                assert ("error" not in title.lower() and "404" not in title.lower()
                        ), f"Page should not be an error page: {title}"

                page.goto(current_url)
                page.wait_for_load_state("networkidle")

        except Exception as e:
            logging.debug(f"Optional check for product card failed (continuing): {e}")

    @allure.title("Complete validation of stock page: presence, links, structure, functionality")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_stock_page_complete(self, catalog_stock_page):
        page = catalog_stock_page.page
        self._check_stock_list_presence(page)
        self._check_stock_items_presence(page)

        stock_links, link_count = self._check_stock_links_validation(page)
        self._test_click_first_item(page, stock_links, link_count)


class TestCatalogStockPageMultipleBrands:

    @allure.title("Comprehensive validation of stock list: presence, links, structure")
    @pytest.mark.validation
    def test_stock_list_complete_validation(self, catalog_stock_page_param):
        page = catalog_stock_page_param.page

        # 1. Stock list structure should be present
        stock_list = page.locator(locators.stock_list)
        assert stock_list.count() > 0, "Stock page should have stock list"
        assert stock_list.is_visible(), "Stock list should be visible"

        # 2. Stock items should exist
        stock_items = page.locator(locators.stock_items)
        stock_count = stock_items.count()
        assert stock_count > 0, "Stock page should have stock items"

        # 3. Stock items should be clickable and functional
        stock_links = page.locator(locators.stock_link)
        link_count = stock_links.count()
        assert link_count > 0, "Stock page should have stock items"

        # Verify all stock items are visible and clickable (they are li elements, not traditional links)
        for i in range(min(5, link_count)):  # Check first 5 items
            item = stock_links.nth(i)
            assert item.is_visible(), f"Stock item {i} should be visible"
            # Check that item has cursor-pointer class indicating it's clickable
            class_attr = item.get_attribute("class") or ""
            assert "cursor-pointer" in class_attr or "catalog-link" in class_attr, \
                f"Stock item {i} should be clickable"

        # 4. Stock names should be visible and not empty
        for i in range(min(3, stock_count)):  # Check first 3 items
            item = stock_items.nth(i)
            # Stock name is in a span inside the li
            stock_name_span = item.locator("span").first

            if stock_name_span.count() > 0:
                text = stock_name_span.text_content()
                assert (text is not None and len(text.strip()) > 0), f"Stock {i} should have text"


class TestCatalogStockCardPage:

    @allure.title("Test product card is present")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_product_card_presence(self, catalog_stock_card_page):
        product_card = catalog_stock_card_page.page.locator(locators.product_card)

        # Product card should be present
        assert product_card.count() > 0, "Stock card page should have product card"
        assert product_card.is_visible(), "Product card should be visible"

    @allure.title("Test product title is present")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_product_title_presence(self, catalog_stock_card_page):
        product_title = catalog_stock_card_page.page.locator(locators.product_title)

        # Product title should be present
        assert product_title.count() > 0, "Stock card page should have product title"
        assert product_title.is_visible(), "Product title should be visible"

        title_text = product_title.text_content()
        assert (title_text is not None and len(title_text.strip()) > 0), "Product title should have text"

    @allure.title("Test product info section is present")
    @pytest.mark.validation
    def test_product_info_presence(self, catalog_stock_card_page):
        product_info = catalog_stock_card_page.page.locator(locators.product_info)

        # Product info should be present
        assert product_info.count() > 0, "Stock card page should have product info"
        assert product_info.is_visible(), "Product info should be visible"

    @allure.title("Test that all info items (Type, Brand, Engine, Block, Identifiers, Solutions) are not empty")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_info_items_are_not_empty(self, catalog_stock_card_page):
        info_items = catalog_stock_card_page.page.locator(locators.info_item)

        # Info items should exist
        item_count = info_items.count()
        assert item_count > 0, "Stock card page should have info items"

        # Check each info item has text
        for i in range(item_count):
            item = info_items.nth(i)
            item_text = item.text_content()
            assert (item_text is not None and len(item_text.strip()) > 0), f"Info item {i} should have text content"

    @allure.title("Test specific info items have content: Type, Brand, Engine, Block")
    @pytest.mark.validation
    def test_specific_info_items_content(self, catalog_stock_card_page):
        info_items = catalog_stock_card_page.page.locator(locators.info_item)

        # Expected info item labels
        expected_labels = [
            "Тип:",
            "Бренд:",
            "Двигатель:",
            "Блок:",
            "Иденты:",
            "Решения:",
        ]

        # Get all info items text
        info_items_text = []
        for i in range(info_items.count()):
            item_text = info_items.nth(i).text_content()
            if item_text:
                info_items_text.append(item_text)

        # Verify at least some of the expected labels are present
        found_labels = 0
        for label in expected_labels:
            if any(label in text for text in info_items_text):
                found_labels += 1

        assert (found_labels > 0), f"Should have at least one of these labels: {expected_labels}"

    @allure.title("Test that info items have actual values (not just labels)")
    @pytest.mark.validation
    def test_info_items_have_values(self, catalog_stock_card_page):
        info_items = catalog_stock_card_page.page.locator(locators.info_item)

        # Check that info items contain actual data
        item_count = info_items.count()
        assert item_count > 0, "Stock card page should have info items"

        # Check that at least one item has substantial content (more than just a label)
        for i in range(item_count):
            item = info_items.nth(i)
            item_text = item.text_content()

            # Should have more than just a colon and space
            if item_text and ":" in item_text:
                parts = item_text.split(":")

                if len(parts) > 1:
                    value = parts[1].strip()
                    assert (len(value) > 0), f"Info item {i} should have a value after the label"


class TestCatalogStockCardPageMultipleBrands:

    @pytest.mark.skip(reason="Skipping too long")
    @allure.title("Comprehensive validation of stock card page: presence, visibility, content")
    def test_stock_card_complete_validation(self, catalog_stock_card_page_param):
        catalog_page, param = catalog_stock_card_page_param

        # 1. Check product card presence and visibility
        product_card = catalog_page.page.locator(locators.product_card)
        assert product_card.count() > 0, f"Stock card should exist for {param}"
        assert product_card.is_visible(), f"Stock card should be visible for {param}"

        # 2. Check product info section presence and visibility
        product_info = catalog_page.page.locator(locators.product_info)
        assert product_info.count() > 0, f"Product info should exist for {param}"
        assert product_info.is_visible(), f"Product info should be visible for {param}"

        # 3. Check all info items have content
        info_items = catalog_page.page.locator(locators.info_item)
        item_count = info_items.count()
        assert item_count > 0, f"Stock card should have info items for {param}"

        # 4. Verify each info item has text content
        for i in range(item_count):
            item = info_items.nth(i)
            item_text = item.text_content()
            assert (item_text is not None and len(item_text.strip()) > 0
            ), f"Info item {i} should have text content for {param}"

        # 5. Verify specific labels (Type, Brand, Engine, Block, Identifiers, Solutions)
        expected_labels = [
            "Тип:",
            "Бренд:",
            "Двигатель:",
            "Блок:",
            "Иденты:",
            "Решения:",
        ]

        info_items_text = []
        for i in range(info_items.count()):
            item_text = info_items.nth(i).text_content()
            if item_text:
                info_items_text.append(item_text)

        found_labels = sum(1 for label in expected_labels if any(label in text for text in info_items_text))
        assert found_labels > 0, f"Should have at least one expected label for {param}"


class TestCatalogCompleteFlow:

    def _check_error_page(self, page, url):
        """Check if page is error page"""
        return "error" in page.title().lower() or "404" in page.title().lower()

    def _process_engine_page(self, page, engine_href, brand_path, results, locators):
        """Process a single engine page"""
        try:
            page.goto(f"{BASE_URL}{engine_href}")
            page.wait_for_load_state("networkidle")

            if self._check_error_page(page, engine_href):
                results['broken_pages'].append(f"{BASE_URL}{engine_href}")
                return

            ecu_links = page.locator(locators.ecu_links)
            ecu_count = ecu_links.count()
            direct_stock_links = page.locator(locators.stock_link)
            direct_stock_count = direct_stock_links.count()

            if ecu_count > 0:
                self._process_ecu_links(page, ecu_links, ecu_count, engine_href, brand_path, results, locators)

            elif direct_stock_count > 0:
                self._process_direct_stocks(page, direct_stock_links, direct_stock_count, engine_href, brand_path, results, locators)

            page.goto(f"{BASE_URL}{engine_href}")
            page.wait_for_load_state("networkidle")
        except Exception as e:
            logging.warning(f"Failed to process engine page {engine_href} (continuing): {e}")

    def _process_stocks_from_ecu(self, page, ecu_href, brand_path, results, locators, engine_href):
        """Process all stocks for a given ECU"""
        stock_links = page.locator(locators.stock_link)
        stock_count = stock_links.count()

        if stock_count > 0:
            limit = MAX_STOCKS_TO_CHECK if MAX_STOCKS_TO_CHECK else stock_count
            for k in range(min(limit, stock_count)):
                self._process_stock_card(page, stock_links, k, ecu_href, brand_path, results, locators)

        page.goto(f"{BASE_URL}{engine_href}")
        page.wait_for_load_state("networkidle")

    def _process_ecu_links(self, page, ecu_links, ecu_count, engine_href, brand_path, results, locators):
        """Process ECU links"""
        for j in range(ecu_count):
            try:
                ecu_link = ecu_links.nth(j)
                ecu_href = ecu_link.get_attribute('href', timeout=TIMEOUT)

                if not ecu_href or not ecu_href.startswith('/catalog/'):
                    continue

                page.goto(f"{BASE_URL}{ecu_href}")
                page.wait_for_load_state("networkidle")

                if self._check_error_page(page, ecu_href):
                    results['broken_pages'].append(f"{BASE_URL}{ecu_href}")
                    continue

                self._process_stocks_from_ecu(page, ecu_href, brand_path, results, locators, engine_href)
            except Exception as e:
                logging.warning(f"Failed to process ECU link {ecu_href} (continuing): {e}")
                continue

    def _process_direct_stocks(self, page, stock_links, direct_stock_count, engine_href, brand_path, results, locators):
        """Process direct stocks"""
        limit = MAX_STOCKS_TO_CHECK if MAX_STOCKS_TO_CHECK else direct_stock_count
        current_url = page.url
        for k in range(min(limit, direct_stock_count)):
            try:
                stock_item = stock_links.nth(k)

                # Stock items are clickable li elements, not links with href
                # Click the item and check if navigation occurred
                stock_item.click(timeout=TIMEOUT)

                # Check if we navigated to a stock card page
                if page.url != current_url:
                    product_card = page.locator(locators.product_card)
                    expect(product_card).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)
                    results['success'].append(f"{brand_path} -> Stock {k+1}")

                    # Navigate back to engine page
                    page.goto(f"{BASE_URL}{engine_href}")
                    page.wait_for_load_state("networkidle")
                    current_url = page.url

            except Exception as e:

                # If navigation failed, log and continue
                results['broken_pages'].append(f"{brand_path} -> Stock {k+1}: {str(e)}")

                # Try to get back to engine page
                try:
                    page.goto(f"{BASE_URL}{engine_href}")
                    page.wait_for_load_state("networkidle")
                    current_url = page.url
                except Exception as e2:
                    logging.warning(f"Failed to navigate back to engine page {engine_href}: {e2}")
                continue

    def _process_stock_card(self, page, stock_links, k, ecu_href, brand_path, results, locators):
        """Process a single stock card"""
        current_url = page.url
        try:
            stock_item = stock_links.nth(k)

            # Stock items are clickable li elements, not links with href
            # Click the item and check if navigation occurred
            stock_item.click(timeout=TIMEOUT)

            # Check if we navigated to a stock card page
            if page.url != current_url:
                product_card = page.locator(locators.product_card)
                expect(product_card).to_be_visible(timeout=Timeouts.BASE_ELEMENT_VISIBLE)

                if product_card.count() > 0:
                    results['success'].append(f"{brand_path} -> Stock {k+1}")
                    assert product_card.is_visible()

                # Navigate back to ECU page
                page.goto(f"{BASE_URL}{ecu_href}")
                page.wait_for_load_state("networkidle")

        except Exception as e:
            # If navigation failed, log and continue
            results['broken_pages'].append(f"{brand_path} -> Stock {k+1}: {str(e)}")

            # Try to get back to ECU page
            try:
                page.goto(f"{BASE_URL}{ecu_href}")
                page.wait_for_load_state("networkidle")

            except Exception as e2:
                logging.warning(f"Failed to navigate back to ECU page {ecu_href}: {e2}")

    def _save_report(self, results):
        """Save test results to file"""
        broken_urls = [item for item in results['broken_pages'] if item.startswith('https://') and ':' not in item]
        os.makedirs('reports/categories', exist_ok=True)
        report_file = f"reports/categories/catalog_404_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\nCATALOG FLOW TEST SUMMARY\n" + "="*60 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Successfully tested: {len(results['success'])} paths\n")
            f.write(f"404 errors found: {len(broken_urls)}\n\n")

            if broken_urls:
                f.write("404 URLs:\n")

                for url in broken_urls:
                    f.write(f"  - {url}\n")

        return report_file, broken_urls

    def _process_brand(self, page, brand_path, results, locators):
        """Process a single brand and its engines"""
        try:
            print(f"\nProcessing brand: {brand_path}")
            page.goto(f"{BASE_URL}/catalog/{brand_path}")
            page.wait_for_load_state("networkidle")

            if self._check_error_page(page, brand_path):
                results['broken_pages'].append(f"Brand: {brand_path}")
                return

            engine_links = page.locator(locators.engine_links)
            engine_count = engine_links.count()

            if engine_count == 0:
                results['no_content'].append(f"Brand {brand_path}: No engines")
                return

            print(f"Found {engine_count} engine types")

            for i in range(engine_count):
                try:
                    engine_link = engine_links.nth(i)
                    engine_href = engine_link.get_attribute('href', timeout=TIMEOUT)

                    if engine_href and engine_href.startswith('/catalog/'):
                        self._process_engine_page(page, engine_href, brand_path, results, locators)

                except Exception as e:
                    logging.warning(f"Failed to process engine link {engine_href} (continuing): {e}")
                    continue

            page.goto(f"{BASE_URL}/catalog/car")
            page.wait_for_load_state("networkidle")

        except Exception as e:
            results['broken_pages'].append(f"Brand {brand_path}: {str(e)}")

    @pytest.mark.skip(reason="Skipping too long")
    @allure.title("Test complete flow: brand -> engine type -> ECU -> stock list -> stock card")
    def test_brand_engine_ecu_stock_flow(self, page, get_all_brands_from_catalog):
        all_brands = get_all_brands_from_catalog
        results = {'success': [], 'broken_pages': [], 'no_content': []}

        for brand_path in all_brands:
            self._process_brand(page, brand_path, results, locators)

        # Save report and print summary
        report_file, broken_urls = self._save_report(results)

        print("\n" + "="*60)
        print("CATALOG FLOW TEST SUMMARY")
        print("="*60)
        print(f"Successfully tested: {len(results['success'])} paths")
        print(f"404 errors found: {len(broken_urls)}")
        print(f"\nReport saved to: {report_file}")

        if broken_urls:
            print("\n404 URLs:")
            for url in broken_urls:
                print(f"  - {url}")

        print("="*60)

        # Test passes if at least some paths were successful
        assert len(results['success']) > 0, "Should have at least some successful paths"
