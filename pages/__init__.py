"""
Page objects for TunService website
"""
from .catalog_page import CatalogPage
from .contacts_page import ContactsPage
from .home_page import HomePage
from .login_page import LoginPage
from .pricing_page import PricingPage

__all__ = [
    'HomePage',
    'CatalogPage',
    'PricingPage',
    'LoginPage',
    'ContactsPage'
]
