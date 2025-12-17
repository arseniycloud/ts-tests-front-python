"""
Locators package for TunService website
"""
from .app_locators import AppLocators
from .balance_locators import BalanceLocators
from .catalog_locators import CatalogLocators
from .contacts_locators import ContactsLocators
from .home_locators import (
    AboutLocators,
    ButtonLocators,
    CardsLocators,
    Colors,
    FAQLocators,
    FooterLocators,
    HeaderLocators,
    HeroLocators,
    ImageLocators,
    LinkLocators,
    Positions,
    ServicesLocators,
    WhyLocators,
)
from .login_locators import LoginLocators
from .pricing_locators import PricingLocators
from .registration_locators import RegistrationLocators

__all__ = [
    # Home page locators
    'HeaderLocators',
    'HeroLocators',
    'CardsLocators',
    'FooterLocators',
    'ButtonLocators',
    'LinkLocators',
    'ImageLocators',
    'FAQLocators',
    'AboutLocators',
    'WhyLocators',
    'ServicesLocators',
    'Colors',
    'Positions',

    # Other page locators
    'CatalogLocators',
    'PricingLocators',
    'LoginLocators',
    'RegistrationLocators',
    'ContactsLocators',
    'AppLocators',
    'BalanceLocators'
]
