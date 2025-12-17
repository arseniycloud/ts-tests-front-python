import pytest

from config.auth_config import BASE_URL
from locators.catalog_locators import CatalogLocators
from pages.catalog_page import CatalogPage


@pytest.fixture(scope="session")
def catalog_brand_page(page):
    """Catalog brand page fixture (shows brand links like BMW, Audi, etc.)"""
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_brand_page("car")
    return catalog_page


@pytest.fixture(scope="session")
def catalog_engine_page(page):
    """Catalog engine page fixture (shows engine types for a specific brand)"""
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_engine_page("car/bmw-mini")
    return catalog_page


@pytest.fixture(scope="session", params=[
    "car/bmw-mini",
    "car/mercedes",
    "car/vag-cars-porsche-audi",
    "car/ford",
    "car/toyota-lexus-scion",
    "car/honda",
])
def catalog_engine_page_param(page, request):
    """Catalog engine page fixture with parametrization for different brands"""
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_engine_page(request.param)
    return catalog_page


@pytest.fixture(scope="session")
def catalog_ecu_page(page):
    """Catalog ECU/block selection page fixture"""
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_ecu_page("car/bmw-mini/diesel")
    return catalog_page


@pytest.fixture(scope="session", params=[
    "car/bmw-mini/diesel",
    "car/bmw-mini/petrol",
    "car/bmw-mini/gearbox",
    "car/mercedes/diesel",
    "car/mercedes/petrol",
    "car/vag-cars-porsche-audi/diesel",
    "car/vag-cars-porsche-audi/petrol",
    "car/vag-cars-porsche-audi/gearbox",
    "car/ford/diesel",
    "car/ford/petrol",
])
def catalog_ecu_page_param(page, request):
    """Catalog ECU/block selection page fixture with parametrization for different brands and engine types"""
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_ecu_page(request.param)
    return catalog_page


@pytest.fixture(scope="session")
def catalog_stock_page(page):
    """Catalog stock list page fixture"""
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_stock_page("car/bmw-mini/diesel/bosch-edc15")
    return catalog_page


@pytest.fixture(scope="session")
def catalog_stock_card_page(page):
    """Catalog stock card page fixture (opened stock item)"""
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_stock_page("car/bmw-mini/diesel/bosch-edc15/15339")
    return catalog_page


@pytest.fixture(scope="session", params=[
    "car/bmw-mini/diesel/bosch-edc15",
    "car/bmw-mini/petrol/bosch-bms46me7m5",
    "car/bmw-mini/gearbox/zf-8hp45hp70hp76",
    "car/mercedes/diesel/bosch-edc17cp10",
    "car/mercedes/petrol/bosch-me2820272",
    "car/vag-cars-porsche-audi/diesel/bosch-edc15vmedc15p",
    "car/vag-cars-porsche-audi/gearbox/dsg-dl501",
    "car/vag-cars-porsche-audi/petrol/bosch-m592m383",
    "car/ford/diesel/bosch-dcu17pc42-43",
    "car/ford/petrol/bosch-me9medg9",
])
def catalog_stock_card_page_param(page, request):
    """Catalog stock card page fixture - opens first stock item from stock list page"""
    catalog_page = CatalogPage(page)
    stock_list_path = request.param

    catalog_page.navigate_to_stock_page(stock_list_path)
    page.wait_for_load_state("networkidle")

    locators = CatalogLocators()
    stock_links = page.locator(locators.stock_link)

    stock_count = stock_links.count()

    if stock_count == 0:
        pytest.fail(f"No stocks found for {stock_list_path}")

    first_link = stock_links.first
    stock_href = first_link.get_attribute("href")

    if not stock_href:
        pytest.fail(f"No stock href found for {stock_list_path}")

    if not stock_href.startswith("http"):
        full_url = f"{BASE_URL}{stock_href}"
        page.goto(full_url)
    else:
        page.goto(stock_href)

    page.wait_for_load_state("networkidle")

    return catalog_page, stock_list_path


@pytest.fixture(scope="session", params=[
    "car/bmw-mini/diesel/bosch-edc15",
    "car/bmw-mini/petrol/bosch-bms46me7m5",
    "car/bmw-mini/gearbox/zf-8hp45hp70hp76",
    "car/mercedes/diesel/bosch-edc17cp10",
    "car/mercedes/petrol/bosch-me2820272",
    "car/vag-cars-porsche-audi/diesel/bosch-edc15vmedc15p",
    "car/vag-cars-porsche-audi/gearbox/dsg-dl501",
    "car/vag-cars-porsche-audi/petrol/bosch-m592m383",
    "car/ford/diesel/bosch-dcu17pc42-43",
    "car/ford/petrol/bosch-me9medg9",
])
def catalog_stock_page_param(page, request):
    """Catalog stock list page fixture with parametrization for different brands and ECU types"""
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_stock_page(request.param)
    return catalog_page


@pytest.fixture(scope="session")
def get_all_brands_from_catalog(page):
    """Fixture to dynamically get all brand links from catalog/car page"""
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_brand_page("car")
    page.wait_for_load_state("networkidle")

    locators = CatalogLocators()
    brand_links = page.locator(locators.brand_links)
    brand_count = brand_links.count()

    brands = []
    for i in range(brand_count):
        link = brand_links.nth(i)
        href = link.get_attribute('href')

        if href and href.startswith('/catalog/'):
            brand_path = href.replace('/catalog/', '')
            brands.append(brand_path)

    return brands
