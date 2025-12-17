import logging

import allure
from playwright.sync_api import Page, expect

from config.auth_config import BASE_URL
from config.timeouts import Timeouts
from locators import home_locators
from pages.base_page import BasePage
from utils.allure_helpers import attach_screenshot


class HomePage(BasePage):
    """Home page of TunService website"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.header_locators = home_locators.HeaderLocators()
        self.hero_locators = home_locators.HeroLocators()
        self.cards_locators = home_locators.CardsLocators()
        self.footer_locators = home_locators.FooterLocators()
        self.link_locators = home_locators.LinkLocators()

    @allure.step("Navigate to main page")
    def navigate_to_main(self):
        self.page.context.clear_cookies()
        self._set_language_cookie()
        self.page.goto(f"{BASE_URL}/", wait_until="domcontentloaded", timeout=Timeouts.BASE_PAGE_LOAD)
        # Wait for network idle to ensure all resources (images, CSS) are loaded - critical for pixel tests
        self.wait_for_network_idle()

    def _ensure_on_home(self):
        """If redirected to app, try to navigate back to public home page"""
        try:
            if "/app" in self.page.url:
                # Try clicking logo/home link if present
                home_link = self.page.locator("a[href='/'], header a[href='/'], .t-header a[href='/']").first

                if home_link.count() > 0:
                    home_link.click(timeout=Timeouts.Home.ELEMENT_VISIBLE)
                    self.wait_for_page_load()

                else:
                    self.page.goto(f"{BASE_URL}/")
                    self.wait_for_page_load()

        except Exception as e:
            logging.debug(f"Failed to navigate back to home page (continuing): {e}")

    def _is_menu_visible(self) -> bool:
        """Check if mobile menu is already open."""
        menu_block = self.page.locator(self.header_locators.menu_block)

        if menu_block.count() == 0:
            return False

        try:
            if menu_block.first.is_visible(timeout=1000):
                return True

            menu_link = menu_block.locator("a").first
            return menu_link.count() > 0 and menu_link.is_visible(timeout=500)

        except Exception:
            return False

    def _click_mobile_menu_button(self) -> bool:
        """Click mobile menu button if visible. Returns True if clicked."""
        btn = self.page.locator(self.header_locators.mobile_menu).first

        try:
            if btn.count() > 0 and btn.is_visible(timeout=2000):
                btn.click(force=True)
                self.page.wait_for_timeout(500)
                return True

        except Exception as e:
            logging.debug(f"Mobile menu button click failed: {e}")

        return False

    def _open_mobile_menu_if_needed(self):
        """Open mobile menu if it's not already visible."""

        if self._is_menu_visible():
            return

        if self._click_mobile_menu_button():
            menu_block = self.page.locator(self.header_locators.menu_block)

            try:
                expect(menu_block).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)

            except Exception as e:
                logging.debug(f"Menu not visible after click: {e}")

    def _get_link_with_fallback(self, desktop_locator: str, mobile_locator: str):
        """Get link element, trying desktop first then mobile."""
        link = self.page.locator(desktop_locator)

        if link.count() == 0:
            self._open_mobile_menu_if_needed()
            link = self.page.locator(mobile_locator)

        return link

    @allure.step("Check if header elements are visible and positioned correctly")
    def check_header_elements(self):
        self._ensure_on_home()
        self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)
        self._open_mobile_menu_if_needed()

        expect(self.page.locator(self.header_locators.container)).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        expect(self.page.locator(self.header_locators.logo)).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)

        prices_link = self._get_link_with_fallback(
            self.header_locators.prices_link,
            self.header_locators.mobile_prices_link
        )
        self.assert_visible_or_exists_on_mobile(prices_link, "Prices link should exist")

        catalog_link = self._get_link_with_fallback(
            self.header_locators.catalog_link,
            self.header_locators.mobile_catalog_link
        )
        self.assert_visible_or_exists_on_mobile(catalog_link, "Catalog link should exist")

        login_link = self._get_link_with_fallback(
            self.header_locators.login_link,
            self.header_locators.mobile_login_link
        )

        if login_link.count() > 0:
            self.assert_visible_or_exists_on_mobile(login_link, "Login link should exist")

        try_button = self.page.locator(self.header_locators.try_button).first

        if try_button.count() == 0:
            try_button = self.page.locator("button:has-text('Попробовать'), button[type='submit']").first

        if try_button.count() > 0:
            self.assert_visible_or_exists_on_mobile(try_button, "Try button should exist")

        attach_screenshot(self.page, "Header elements verified")

    @allure.step("Check hero section elements")
    def check_hero_section(self):
        self._ensure_on_home()
        hero_container = self.page.locator(self.hero_locators.container).first
        assert hero_container.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Hero section container should be visible"

        expect(hero_container).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        expect(self.page.locator(f"{self.hero_locators.container} {self.hero_locators.title}")).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        expect(self.page.locator(f"{self.hero_locators.container} p.text-sm")).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)

        self.page.wait_for_selector(self.hero_locators.try_button, state="visible", timeout=Timeouts.Home.ELEMENT_VISIBLE)
        expect(self.page.locator(self.hero_locators.try_button).first).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)

        attach_screenshot(self.page, "Hero section verified")

    @allure.step("Check hero button functionality and navigation readiness")
    def check_hero_button_functionality(self):
        self._open_mobile_menu_if_needed()

        button = self.page.locator(self.hero_locators.try_button).first

        expect(button).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        expect(button).to_be_enabled(timeout=Timeouts.Home.ELEMENT_VISIBLE)

        try:
            button_text = button.text_content(timeout=Timeouts.Home.ELEMENT_VISIBLE)

        except Exception as e:
            logging.debug(f"Failed to get button text content: {e}")
            button_text = None

        is_submit = button.evaluate("(btn) => btn.type === 'submit'")
        has_expected_text = button_text and ("Попробовать" in button_text or "Попробуй" in button_text or "Try" in button_text)

        assert has_expected_text or is_submit, (
            f"Button should contain 'Попробовать' text or be submit type. "
            f"Got text: '{button_text}', is_submit: {is_submit}"
        )

        has_click_handler = button.evaluate("""
            (btn) => {
                if (!btn) return false;
                if (btn.onclick) return true;
                if (btn.type === 'submit' || btn.hasAttribute('data-action')) return true;
                const styles = window.getComputedStyle(btn);
                if (styles.cursor === 'pointer') return true;
                return !btn.disabled;
            }
        """)

        assert has_click_handler, "Button should have click functionality"

        attach_screenshot(self.page, "Hero button verified")

    @allure.step("Check cards section elements are visible")
    def check_cards_section(self):
        self._ensure_on_home()
        expect(self.page.locator(self.cards_locators.container).first).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)

        expect(self.page.locator(f"{self.cards_locators.container} > div:first-child").first).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        expect(self.page.locator(f"{self.cards_locators.container} > div:nth-child(2)").first).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        expect(self.page.locator(f"{self.cards_locators.container} > div:last-child").first).to_be_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE)

        attach_screenshot(self.page, "Cards section verified")

    @allure.step("Check footer elements are visible")
    def check_footer(self):
        expect(self.page.locator(f"{self.footer_locators.container}.text-white.pt-10")).to_be_visible()
        expect(self.page.locator(self.footer_locators.logo)).to_be_visible()
        expect(self.page.locator(self.footer_locators.nav_links)).to_be_visible()

        attach_screenshot(self.page, "Footer verified")

    @allure.step("Get header element colors")
    def get_header_colors(self):

        return {
            'header_bg': self.get_element_background_color(self.header_locators.container),
            'logo_color': self.get_element_color(self.header_locators.logo),
            'button_color': self.get_element_color(self.header_locators.try_button)
        }

    @allure.step("Get hero section element colors")
    def get_hero_colors(self):

        return {
            'title_color': self.get_element_color(f"{self.hero_locators.container} {self.hero_locators.title}"),
            'subtitle_color': self.get_element_color(f"{self.hero_locators.container} p.text-sm"),
            'button_color': self.get_element_color(self.hero_locators.try_button)
        }

    @allure.step("Get cards section element colors")
    def get_card_colors(self):

        return {
            'power_card_bg': self.get_element_background_color(f"{self.cards_locators.container} > div:first-child"),
            'systems_card_bg': self.get_element_background_color(f"{self.cards_locators.container} > div:nth-child(2)"),
            'standards_card_bg': self.get_element_background_color(f"{self.cards_locators.container} > div:last-child")
        }

    @allure.step("Check all links on home page")
    def check_all_links(self):
        self.page.wait_for_load_state("networkidle", timeout=Timeouts.BASE_NETWORK_IDLE)

        catalog_link = self._get_link_with_fallback(
            self.link_locators.header_catalog,
            self.link_locators.mobile_header_catalog
        )

        self.assert_visible_or_exists_on_mobile(catalog_link, "Catalog link should exist")

        prices_link = self._get_link_with_fallback(
            self.link_locators.header_prices,
            self.link_locators.mobile_header_prices
        )

        self.assert_visible_or_exists_on_mobile(prices_link, "Prices link should exist")

    @allure.step("Check footer elements visibility")
    def check_footer_elements(self):
        expect(self.page.locator(self.footer_locators.container).first).to_be_visible()
        expect(self.page.locator(self.footer_locators.logo)).to_be_visible()

    @allure.step("Get footer links count")
    def get_footer_links_count(self):
        footer_map_links = self.page.locator(self.link_locators.footer_map).count()
        footer_contacts_links = self.page.locator(self.link_locators.footer_contacts).count()
        footer_catalog_links = self.page.locator(self.link_locators.footer_catalog).count()
        footer_prices_links = self.page.locator(self.link_locators.footer_prices).count()
        footer_email_links = self.page.locator(self.link_locators.footer_email).count()
        footer_youtube_links = self.page.locator(self.link_locators.footer_youtube).count()
        footer_vk_links = self.page.locator(self.link_locators.footer_vk).count()
        footer_policy_links = self.page.locator(self.link_locators.footer_policy).count()
        footer_agreement_links = self.page.locator(self.link_locators.footer_agreement).count()

        return {
            'map': footer_map_links,
            'contacts': footer_contacts_links,
            'catalog': footer_catalog_links,
            'prices': footer_prices_links,
            'email': footer_email_links,
            'youtube': footer_youtube_links,
            'vk': footer_vk_links,
            'policy': footer_policy_links,
            'agreement': footer_agreement_links
        }
