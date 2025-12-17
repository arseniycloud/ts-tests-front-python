import allure
import pytest

from config.timeouts import Timeouts
from locators.home_locators import (
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
    ServicesLocators,
    WhyLocators,
)
from utils.allure_helpers import attach_element_screenshot, attach_screenshot


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Header")
class TestHomePageTestsHeaderSection:

    @allure.title("Test header elements are visible and functional")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_header_elements(self, home_page):
        with allure.step("Check header elements visibility"):
            home_page.check_header_elements()
            attach_screenshot(home_page.page, "Header section visible")

        header_locators = HeaderLocators()

        with (allure.step("Verify header background color")):
            assert home_page.validate_element_background_color(header_locators.container, Colors.HEADER_BG),f"Header background color should be {Colors.HEADER_BG}"
            attach_element_screenshot(home_page.page, header_locators.container, "Header with background")

        with allure.step("Verify logo visibility"):
            assert home_page.validate_element_visibility(header_locators.logo), "Logo should be visible"
            attach_element_screenshot(home_page.page, header_locators.logo, "Logo element")


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Hero")
class TestHeroSection:

    @allure.title("Test complete hero section including title, subtitle, images, badges, and logos")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_hero_section(self, home_page):
        home_page.check_hero_section()

        hero_locators = HeroLocators()

        # Verify hero title is visible
        assert home_page.validate_element_visibility(
            f"{hero_locators.container} {hero_locators.title}"), "Hero title should be visible"

        # Verify hero subtitle is visible
        assert home_page.validate_element_visibility(
            f"{hero_locators.container} p.text-sm"),"Subtitle should be visible"

        # Verify badge 1 is visible
        badge_1 = home_page.page.locator(hero_locators.badge_1)
        assert badge_1.is_visible(), "Badge 1 should be visible"

        # Verify badge 2 is visible
        badge_2 = home_page.page.locator(hero_locators.badge_2)
        assert badge_2.is_visible(), "Badge 2 should be visible"

        # Verify all program logos are visible
        logos = [
            hero_locators.bitbox_logo,
            hero_locators.winols_logo,
            hero_locators.pcm_logo,
            hero_locators.autotuner_logo,
        ]
        for logo in logos:
            assert home_page.validate_element_visibility(logo), f"{logo} should be visible"


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Buttons")
class TestButtonsFunctionality:

    @allure.title("Test button functionality")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_buttons(self, home_page):
        home_page.check_hero_button_functionality()
        home_page.wait_for_page_load("load")

        button_locators = ButtonLocators()

        header_button = home_page.page.locator(button_locators.header_try_button)
        home_page.assert_visible_or_exists_on_mobile(header_button, "Header button should exist")

        hero_button = home_page.page.locator(button_locators.hero_try_button)
        home_page.assert_visible_or_exists_on_mobile(hero_button, "Hero button should exist")


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Cards")
class TestCardsSection:

    @allure.title("Test all cards in the cards section")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_cards_section(self, home_page):
        home_page.check_cards_section()

        cards_locators = CardsLocators()

        # Verify power card
        power_card = home_page.page.locator(f"{cards_locators.container} > div:first-child")
        assert power_card.is_visible(), "Power card should be visible"

        # Verify systems card
        systems_card = home_page.page.locator(f"{cards_locators.container} > div:nth-child(2)")
        assert systems_card.is_visible(), "Systems card should be visible"

        # Verify standards card
        standards_card = home_page.page.locator(f"{cards_locators.container} > div:last-child")
        assert standards_card.is_visible(), "Standards card should be visible"


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("About")
class TestAboutSection:

    @allure.title("Test complete about section including text and statistics")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_about_section(self, home_page):
        about_locators = AboutLocators()

        # Verify section title (use first() to handle multiple matches)
        title = home_page.page.locator(about_locators.title).first
        assert title.is_visible(), "About section title should be visible"
        assert title.text_content().strip() == "Кто мы?", "Title should be 'Кто мы?'"

        # Verify text blocks
        text_blocks = home_page.page.locator(about_locators.text)
        assert text_blocks.first.is_visible(), "About text should be visible"

        # Verify statistics
        stats = home_page.page.locator(about_locators.stats_container)
        assert stats.is_visible(), "Statistics section should be visible"


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Why Section")
class TestWhySection:

    @allure.title("Test complete why section with all icons")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_why_section(self, home_page):
        why_locators = WhyLocators()

        # Verify why section container is visible
        why_section = home_page.page.locator(why_locators.container).first
        assert why_section.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Why section should be visible"

        # Verify title within the section
        title = why_section.locator("h2.section-heading").first
        assert title.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Why section title should be visible"
        assert "Почему" in title.text_content(), "Title should contain 'Почему'"

        # Verify all icons within the section
        icons = [
            why_locators.car_icon,
            why_locators.add_doc_icon,
            why_locators.community_icon,
            why_locators.wallet_icon,
        ]
        for icon in icons:
            icon_element = why_section.locator(icon).first
            assert icon_element.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), f"{icon} should be visible"


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Services")
class TestServicesSection:

    @allure.title("Test services section structure including title and cards")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_services_section_structure(self, home_page):
        services_locators = ServicesLocators()

        # Verify services section title - use locator with container to be more specific
        services_title = home_page.page.locator(services_locators.title).first
        assert services_title.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Services section title should be visible"

        title_text = services_title.text_content(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        assert ("С нашим сервисом вы можете" in title_text), f"Title should contain correct text, got: {title_text}"

        # Verify diesel card
        diesel_card = home_page.page.locator(services_locators.diesel_card)
        assert diesel_card.is_visible(), "Diesel card should be visible"

        # Verify gasoline card
        gasoline_card = home_page.page.locator(services_locators.gasoline_card)
        assert gasoline_card.is_visible(), "Gasoline card should be visible"

    @allure.title("Test diesel card content including systems list")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_diesel_card_content(self, home_page):
        services_locators = ServicesLocators()

        # Find diesel card - first card with bg-lightGray
        diesel_card = home_page.page.locator(".t-service-card.bg-lightGray").first
        assert diesel_card.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Diesel card should be visible"

        # Verify card title
        title = diesel_card.locator("h3").first
        assert title.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Diesel card title should be visible"

        title_text = title.text_content(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        assert ("дизельных двигателей" in title_text), f"Diesel card should be for diesel engines, got: {title_text}"

        # Verify "Отключить" section
        section_title = diesel_card.locator("h4").first
        assert section_title.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Disable section should be visible"
        section_title_text = section_title.text_content(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        assert (
            section_title_text.strip() == "Отключить"
        ), f"Section title should be 'Отключить', got: {section_title_text}"

        # Verify systems list - check first item is visible, then count all
        systems = diesel_card.locator(".t-list-item")
        first_system = systems.first
        assert first_system.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "First system item should be visible"

        systems_count = systems.count()
        assert systems_count >= 11, f"Should have at least 11 systems for diesel, got {systems_count}"

        # Check for specific systems
        systems_text = diesel_card.locator(".t-list-item span").all_text_contents()
        for system in services_locators.diesel_systems[:5]:  # Check first 5 systems
            assert any(system.upper() in text.upper() for text in systems_text
            ), f"System {system} should be in the list. Found: {systems_text[:3]}"

    @allure.title("Test gasoline card content including systems list")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_gasoline_card_content(self, home_page):
        services_locators = ServicesLocators()
        # Find gasoline card - card with bg-gradient-to-br
        gasoline_card = home_page.page.locator(".t-service-card.bg-gradient-to-br").first
        assert gasoline_card.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Gasoline card should be visible"

        # Verify card title
        title = gasoline_card.locator("h3").first
        assert title.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Gasoline card title should be visible"
        title_text = title.text_content(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        assert ("бензиновых двигателей" in title_text
        ), f"Gasoline card should be for gasoline engines, got: {title_text}"

        # Verify "Отключить" section
        section_title = gasoline_card.locator("h4").first
        assert section_title.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Disable section should be visible"
        section_title_text = section_title.text_content(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        assert (
            section_title_text.strip() == "Отключить"
        ), f"Section title should be 'Отключить', got: {section_title_text}"

        # Verify systems list - check first item is visible, then count all
        systems = gasoline_card.locator(".t-list-item")
        first_system = systems.first
        assert first_system.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "First system item should be visible"
        systems_count = systems.count()
        assert systems_count >= 11, f"Should have at least 11 systems for gasoline, got {systems_count}"

        # Check for specific systems
        systems_text = gasoline_card.locator(".t-list-item span").all_text_contents()
        for system in services_locators.gasoline_systems[:5]:  # Check first 5 systems
            assert any(system.upper() in text.upper() for text in systems_text
            ), f"System {system} should be in the list. Found: {systems_text[:3]}"

    @allure.title("Test gasoline card has temperature reduction section")
    @pytest.mark.validation
    def test_gasoline_card_temperature_section(self, home_page):
        services_locators = ServicesLocators()
        gasoline_card = home_page.page.locator(services_locators.gasoline_card)

        # Verify "Понизить температуру" section
        temp_section = gasoline_card.locator(services_locators.section_title).nth(1)
        assert temp_section.is_visible(), "Temperature section should be visible"
        assert (temp_section.text_content().strip() == "Понизить температуру"
        ), "Section title should be 'Понизить температуру'"

        # Verify temperature items
        temp_items = temp_section.locator("..").locator("li")
        assert temp_items.count() >= 2, "Should have at least 2 temperature items"

    @allure.title("Test services section images are visible")
    @pytest.mark.validation
    def test_services_section_images(self, home_page):
        services_locators = ServicesLocators()

        # Verify engine images in cards
        diesel_engine = home_page.page.locator(services_locators.diesel_engine_img)
        assert diesel_engine.is_visible(), "Diesel engine image should be visible"

        gasoline_engine = home_page.page.locator(services_locators.gasoline_engine_img)
        assert gasoline_engine.is_visible(), "Gasoline engine image should be visible"

        # Verify car image in services section (third Car image)
        services_car = home_page.page.locator(services_locators.car_img).nth(2)
        assert services_car.is_visible(), "Services car image should be visible"


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("FAQ")
class TestFAQSection:

    @allure.title("Test FAQ section with all questions")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_faq_section(self, home_page):
        faq_locators = FAQLocators()

        # Verify FAQ section is visible
        assert home_page.validate_element_visibility(faq_locators.container), "FAQ section should be visible"

        # Verify title
        assert home_page.validate_element_visibility(
            f"{faq_locators.container} {faq_locators.title}"), "FAQ title should be visible"

        # Verify all FAQ items (FAQ is now represented as h2 headings, not .faq-item)
        faq_items = home_page.page.locator(faq_locators.items)
        assert faq_items.count() >= 3, f"Should have at least 3 FAQ items, got {faq_items.count()}"


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Footer")
class TestFooterSection:

    @allure.title("Test footer elements")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.validation
    def test_footer_elements(self, home_page):
        home_page.check_footer_elements()
        footer_locators = FooterLocators()

        # Footer container might match header too, so use first
        assert home_page.page.locator(footer_locators.container).first.is_visible(), "Footer should be visible"
        assert home_page.validate_element_visibility(footer_locators.logo), "Footer logo should be visible"

        # Verify navigation sections (first() to handle multiple matches)
        about_section = home_page.page.locator(footer_locators.about_section).first
        assert about_section.is_visible(), "Footer about section should be visible"

        services_section = home_page.page.locator(footer_locators.services_section).first
        assert (services_section.is_visible()), "Footer services section should be visible"

        contacts_section = home_page.page.locator(footer_locators.contacts_section).first
        assert (contacts_section.is_visible()), "Footer contacts section should be visible"

        # Verify copyright text
        copyright_text = home_page.page.locator(footer_locators.copyright)
        assert copyright_text.is_visible(), "Footer copyright should be visible"
        assert ("TUN SERVICE" in copyright_text.text_content()), "Copyright should mention TUN SERVICE"


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Links")
class TestLinksFunctionality:

    @allure.title("Test header and footer links are visible")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_header_and_footer_links(self, home_page):
        home_page.check_all_links()
        link_locators = LinkLocators()

        # Footer links (always visible on both platforms)
        assert home_page.validate_element_visibility(link_locators.footer_map), "Map link should be visible"
        assert home_page.validate_element_visibility(link_locators.footer_contacts), "Contacts link should be visible"
        assert home_page.validate_element_visibility(link_locators.footer_email), "Email link should be visible"
        assert home_page.validate_element_visibility(link_locators.footer_youtube), "YouTube link should be visible"
        assert home_page.validate_element_visibility(link_locators.footer_vk), "VK link should be visible"
        assert home_page.validate_element_visibility(link_locators.footer_policy), "Policy link should be visible"
        assert home_page.validate_element_visibility(link_locators.footer_agreement), "Agreement link should be visible"

    @allure.title("Test all footer links have valid href attributes")
    @pytest.mark.validation
    def test_footer_links_have_href(self, home_page):
        link_locators = LinkLocators()

        # Check footer navigation links
        footer_map = home_page.page.locator(link_locators.footer_map).first
        href = footer_map.get_attribute("href")
        assert href is not None and href != "", "Footer map link should have href"

        footer_contacts = home_page.page.locator(link_locators.footer_contacts).first
        href = footer_contacts.get_attribute("href")
        assert href is not None and href != "", "Footer contacts link should have href"

        # Check social links
        footer_youtube = home_page.page.locator(link_locators.footer_youtube).first
        href = footer_youtube.get_attribute("href")
        assert href is not None and href != "", "Footer YouTube link should have href"
        assert "youtube" in href, "YouTube link should contain 'youtube'"

        footer_vk = home_page.page.locator(link_locators.footer_vk).first
        href = footer_vk.get_attribute("href")
        assert href is not None and href != "", "Footer VK link should have href"
        assert "vk" in href, "VK link should contain 'vk'"

        # Check email link
        footer_email = home_page.page.locator(link_locators.footer_email).first
        href = footer_email.get_attribute("href")
        assert href is not None and href != "", "Footer email link should have href"
        assert "mailto:" in href, "Email link should contain 'mailto:'"


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Images")
class TestImagesVisibility:

    @allure.title("Test all images are loaded and visible")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_all_images_loading(self, home_page):
        image_locators = ImageLocators()

        # Header and footer logos - use .first and explicit timeouts
        header_logo = home_page.page.locator(image_locators.header_logo).first
        assert header_logo.is_visible(timeout=Timeouts.Home.HEADER_LOGO_VISIBLE), "Header logo should be visible"
        footer_logo = home_page.page.locator(image_locators.footer_logo).first
        assert footer_logo.is_visible(timeout=Timeouts.Home.HEADER_LOGO_VISIBLE), "Footer logo should be visible"

        # Hero images - use .first and explicit timeouts
        hero_image = home_page.page.locator(image_locators.hero_image).first
        assert hero_image.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Hero image should be visible"
        hero_car_image = home_page.page.locator(image_locators.hero_car_image).first
        assert hero_car_image.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Hero car image should be visible"
        badge_1_image = home_page.page.locator(image_locators.hero_badge_1_image).first
        assert badge_1_image.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Badge1 image should be visible"
        badge_2_image = home_page.page.locator(image_locators.hero_badge_2_image).first
        assert badge_2_image.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Badge2 image should be visible"

        # Program logos
        logos = [image_locators.bitbox_logo,image_locators.winols_logo,image_locators.pcm_logo,image_locators.autotuner_logo]

        for logo in logos:
            assert home_page.validate_element_visibility(logo), f"{logo} should be visible"

        # Social icons
        assert home_page.validate_element_visibility(image_locators.youtube_icon), "YouTube icon should be visible"
        assert home_page.validate_element_visibility(image_locators.vk_icon), "VK icon should be visible"


@allure.epic("Home")
@allure.feature("Home Page")
@allure.story("Text Content")
class TestTextContentVisibility:

    @allure.title("Test all text blocks are visible and have content")
    @pytest.mark.regression
    @pytest.mark.validation
    def test_text_content(self, home_page):

        # Check hero text
        hero_title = home_page.page.locator(".f-block-gradient h1").first
        assert hero_title.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Hero title should be visible"

        hero_title_text = hero_title.text_content(timeout=Timeouts.Home.ELEMENT_VISIBLE)
        assert hero_title_text is not None and hero_title_text.strip() != "", \
            f"Hero title should have text, got: {hero_title_text}"

        hero_subtitle = home_page.page.locator(".f-block-gradient p.text-sm").first
        assert hero_subtitle.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Hero subtitle should be visible"

        # Check cards text - find container with flex flex-col gap-5 classes (it can have additional classes)
        # CSS selector .container.flex.flex-col.gap-5 works even with additional classes
        cards_container = home_page.page.locator("div.container.flex.flex-col.gap-5").first
        assert cards_container.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "Cards container should be visible"

        cards = cards_container.locator("> div")

        # Check first card is visible instead of waiting for all cards
        first_card = cards.first
        assert first_card.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "First card should be visible"

        cards_count = cards.count()
        assert cards_count >= 3, f"Should have at least 3 cards, got {cards_count}"

        for i in range(min(3, cards_count)):
            card = cards.nth(i)
            assert card.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), f"Card {i+1} should be visible"

            card_text = card.text_content(timeout=Timeouts.Home.ELEMENT_VISIBLE)
            assert (card_text is not None and len(card_text.strip()) > 0), \
                f"Card {i+1} should have text, got: {card_text[:50]}"

        # Check FAQ questions
        faq_locators = FAQLocators()
        faq_questions = home_page.page.locator(faq_locators.items)

        first_faq = faq_questions.first
        assert first_faq.is_visible(timeout=Timeouts.Home.ELEMENT_VISIBLE), "First FAQ question should be visible"

        faq_count = faq_questions.count()
        assert faq_count >= 3, f"Should have at least 3 FAQ questions, got {faq_count}"
