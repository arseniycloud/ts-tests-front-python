from dataclasses import dataclass


@dataclass
class HeaderLocators:
    container = "[data-test-id='header_container']"
    logo = "[data-test-id='header_logo_img']"
    try_button = "[data-test-id='header_container'] button:has-text('Попробовать'), [data-test-id='header_container'] button[type='submit']"
    prices_link = "[data-test-id='menu_block'] a[href*='price']"
    catalog_link = "[data-test-id='menu_block'] a[href*='catalog']"
    login_link = "[data-test-id='menu_block'] a[href*='/app/login']"
    language_selector = "[data-test-id='language_selector']"
    language_flag = "[data-test-id='language_flag']"
    mobile_menu = "[data-test-id='mobile_menu_button'], .mobile-menu-btn"
    menu_block = "[data-test-id='menu_block']"
    # Mobile menu locators (without data-test-id)
    mobile_prices_link = "a[href*='price']"
    mobile_catalog_link = "a[href*='catalog']"
    mobile_login_link = "a[href*='/app/login']"


@dataclass
class HeroLocators:
    container = ".f-block-gradient"
    title = "h1"
    subtitle = "p"
    try_button = ".f-block-gradient .btn-primary--mainPage"
    hero_image = "img[alt='Blue cloud']"
    hero_car_image = "img[alt='Car']"
    badge_1 = ".badge-1"
    badge_2 = ".badge-2"
    logos_container = ".f-block-gradient .flex.space-x-2"
    bitbox_logo = "img[alt='BitBox logo']"
    winols_logo = "img[alt='WinOls logo']"
    pcm_logo = "img[alt='PCM logo']"
    autotuner_logo = "img[alt='Autotuner logo']"


@dataclass
class PageBodyLocators:
    container = "[data-test-id='page_body']"


@dataclass
class CardsLocators:
    container = ".container.flex.flex-col.gap-5"
    power_card = ".container.flex.flex-col.gap-5 > div:first-child, .cards > div:first-child"
    systems_card = ".container.flex.flex-col.gap-5 > div:nth-child(2), .cards > div:nth-child(2)"
    standards_card = ".container.flex.flex-col.gap-5 > div:last-child, .cards > div:last-child"


@dataclass
class AboutLocators:
    container = ".mt-10.flex.flex-col.overflow-hidden"
    title = ".section-heading"
    text = ".flex.flex-col.gap-2.text-sm"
    stats_container = ".mt-8.grid.grid-cols-2.gap-4"
    years_stat = ".font-bold:has-text('15+')"
    solutions_stat = ".font-bold:has-text('60+')"


@dataclass
class WhyLocators:
    container = "section.why-are-we, .why-are-we"
    title = "section.why-are-we h2.section-heading, .why-are-we h2.section-heading"
    items = ".space-y-4"
    car_icon = "img[alt='car-icon']"
    add_doc_icon = "img[alt='add-icon']"
    community_icon = "img[alt='community-icon']"
    wallet_icon = "img[alt='wallet-icon']"


@dataclass
class ServicesLocators:
    container = ".overflow-x-hidden"
    title = ".overflow-x-hidden h2.section-heading"
    diesel_card = ".t-service-card.bg-lightGray, .t-service-card:first-of-type"
    gasoline_card = ".t-service-card.bg-gradient-to-br, .t-service-card:last-of-type"
    diesel_title = ".t-service-card.bg-lightGray h3, .t-service-card:first-of-type h3"
    gasoline_title = ".t-service-card.bg-gradient-to-br h3, .t-service-card:last-of-type h3"
    card_title = "h3"
    section_title = "h4"
    list_items = ".t-list-item"
    list_item_span = ".t-list-item span"
    diesel_engine_img = "img[alt='Diesel engine']"
    gasoline_engine_img = "img[alt='Engine']"
    car_img = "img[alt='Car']"
    diesel_systems = ["DPF", "EGR", "VSA", "TVA", "SCR", "Start/stop", "AGS", "MAF", "EGP", "LSU", "IMMO"]
    gasoline_systems = ["E2, CAT", "SAP", "CAT HEAT", "EVAP", "VSA", "Start/stop",
                       "GPF/OPF/PPF", "NOX", "AGS", "EGR", "IMMO", "Misfare"]


@dataclass
class FAQLocators:
    container = ".container.my-14.bg-white"
    title = ".section-heading.text-center"
    first_question = "button:has-text('Как происходит проверка файла?')"
    second_question = "button:has-text('Что делать если сервис не выдал никаких решений?')"
    third_question = "button:has-text('Как происходит редактирование файла?')"
    fourth_question = "button:has-text('Необходимо ли принудительно удалять коды DTC при покупке решения?')"
    items = "button:has-text('Как происходит проверка файла?'), button:has-text('Что делать если сервис не выдал никаких решений?'), button:has-text('Как происходит редактирование файла?'), button:has-text('Необходимо ли принудительно удалять коды DTC при покупке решения?')"


@dataclass
class FooterLocators:
    container = "[data-test-id='footer_container']"
    logo = "[data-test-id='footer_logo']"
    nav_links = "[data-test-id='footer_container'] .nav"
    about_section = "[data-test-id='footer_container'] .nav div:first-of-type"
    services_section = "[data-test-id='footer_container'] .nav div:nth-of-type(2)"
    contacts_section = "[data-test-id='footer_container'] .nav div:nth-of-type(3)"
    language_selector = "[data-test-id='footer_container'] [data-test-id='language_selector']"
    social_links = "[data-test-id='footer_container'] .flex.space-x-2"
    youtube_link = "[data-test-id='footer_container'] a[href*='youtube']"
    vk_link = "[data-test-id='footer_container'] a[href*='vk.com']"
    copyright = "[data-test-id='footer_container'] .text-\\[10px\\].lg\\:text-xs.xl\\:text-sm.text-center.block"
    policy_link = "[data-test-id='footer_policy_link']"
    agreement_link = "[data-test-id='footer_agreement_link']"


@dataclass
class ButtonLocators:
    header_try_button = "[data-test-id='header_container'] button:has-text('Попробовать'), [data-test-id='header_container'] button[type='submit']"
    hero_try_button = ".f-block-gradient button, .f-block-gradient .btn-primary--mainPage, button:has-text('Попробовать')"
    faq_buttons = "button[type='button']:has-text('Как происходит'), button:has-text('Что делать'), button:has-text('Необходимо')"
    mobile_menu_button = "[data-test-id='mobile_menu_button'], .mobile-menu-btn"


@dataclass
class LinkLocators:
    header_prices = "[data-test-id='menu_block'] a[href*='price']"
    header_catalog = "[data-test-id='menu_block'] a[href*='catalog']"
    header_login = "[data-test-id='menu_block'] a[href*='/app/login']"
    footer_map = "[data-test-id='footer_container'] a[href*='map']"
    footer_contacts = "[data-test-id='footer_container'] a[href*='contacts']"
    footer_catalog = "[data-test-id='footer_container'] a[href*='catalog']"
    footer_prices = "[data-test-id='footer_container'] a[href*='price']"
    footer_email = "[data-test-id='footer_container'] a[href^='mailto:']"
    footer_youtube = "[data-test-id='footer_container'] a[href*='youtube']"
    footer_vk = "[data-test-id='footer_container'] a[href*='vk.com']"
    footer_policy = "[data-test-id='footer_policy_link']"
    footer_agreement = "[data-test-id='footer_agreement_link']"
    # Mobile menu locators (without data-test-id)
    mobile_header_prices = "a[href*='price']"
    mobile_header_catalog = "a[href*='catalog']"
    mobile_header_login = "a[href*='/app/login']"


@dataclass
class ImageLocators:
    header_logo = "[data-test-id='header_logo_img']"
    footer_logo = "[data-test-id='footer_logo']"
    hero_image = "img[alt='Blue cloud']"
    hero_car_image = ".f-block-gradient img[alt='Car']"
    hero_badge_1_image = "img[alt='ecu']"
    hero_badge_2_image = "img[alt='kess']"
    bitbox_logo = "img[alt='BitBox logo']"
    winols_logo = "img[alt='WinOls logo']"
    pcm_logo = "img[alt='PCM logo']"
    autotuner_logo = "img[alt='Autotuner logo']"
    about_man_image = "img[alt='Man in front of monitors']"
    why_car_icon = "img[alt='car-icon']"
    why_add_icon = "img[alt='add-icon']"
    why_community_icon = "img[alt='community-icon']"
    why_wallet_icon = "img[alt='wallet-icon']"
    services_car_image = ".overflow-x-hidden img[alt='Car']"
    services_gasoline_engine = "img[alt='Engine']"
    services_diesel_engine = "img[alt='Diesel engine']"
    language_flag = "[data-test-id='language_flag']"
    youtube_icon = "[data-test-id='footer_container'] img[alt='Youtube logo']"
    vk_icon = "[data-test-id='footer_container'] img[alt='VK logo']"


# Color constants for validation
class Colors:
    HEADER_BG = "rgb(16, 16, 16)"
    WHITE = "rgb(255, 255, 255)"
    BLACK = "rgb(0, 0, 0)"
    GRAY_900 = "rgb(17, 24, 39)"
    GRAY_800 = "rgb(31, 41, 55)"
    PRIMARY_TEXT = "rgb(0, 0, 0)"  # Primary text color
    SECONDARY_TEXT = "rgb(107, 114, 128)"  # Secondary text color


# Position constants for validation
class Positions:
    HEADER_HEIGHT_MIN = 54
    HEADER_HEIGHT_MAX = 69
    LOGO_WIDTH_MIN = 190
    LOGO_WIDTH_MAX = 262
    LOGO_HEIGHT_MIN = 17
    LOGO_HEIGHT_MAX = 25
