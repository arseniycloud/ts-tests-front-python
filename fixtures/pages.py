import pytest

from pages.catalog_page import CatalogPage
from pages.contacts_page import ContactsPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.pricing_page import PricingPage
from pages.registration_page import RegistrationPage


@pytest.fixture(scope="function")
def home_page(page):
    home_page = HomePage(page)
    home_page.navigate_to_main()
    home_page.wait_for_network_idle()
    return home_page


@pytest.fixture(scope="session")
def catalog_page(page):
    catalog_page = CatalogPage(page)
    catalog_page.navigate_to_catalog()
    catalog_page.wait_for_network_idle()
    return catalog_page


@pytest.fixture(scope="session")
def pricing_page(page):
    pricing_page = PricingPage(page)
    pricing_page.navigate_to_pricing()
    pricing_page.wait_for_network_idle()
    return pricing_page


@pytest.fixture(scope="session")
def login_page(page):
    login_page = LoginPage(page)
    login_page.navigate_to_login()
    login_page.wait_for_network_idle()
    return login_page


@pytest.fixture(scope="session")
def registration_page(page):
    registration_page = RegistrationPage(page)
    registration_page.navigate_to_registration()
    registration_page.wait_for_network_idle()
    return registration_page


@pytest.fixture(scope="session")
def contacts_page(page):
    contacts_page = ContactsPage(page)
    contacts_page.navigate_to_contacts()
    contacts_page.wait_for_network_idle()
    return contacts_page
