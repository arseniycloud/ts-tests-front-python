from dataclasses import dataclass


@dataclass
class CatalogLocators:
    # Page structure
    page_title = "[data-test-id='catalog_page_title'], .catalog_title-ss"
    page_container = "[data-test-id='page_container'], .catalog-wrapper-ss"
    catalog_panel = "[data-test-id='catalog_panel'], .catalog-list-panel-ss"
    catalog_links = "main a[href*='/catalog/'], .catalog-link.ts_link.link_item"

    # Brand-specific elements
    brand_links = "main a[href*='/catalog/'], .brand_link.catalog-link.ts_link.ts_brand_link"
    brand_images = ".brand_link .ts_img img, main a[href*='/catalog/'] img"
    brand_names = ".brand_link, main a[href*='/catalog/']"

    # Engine/type-specific elements (e.g., diesel, petrol, gearbox)
    engine_links = ".catalog-link.ts_link.ts_engine_link"
    engine_images = ".ts_engine_link img.ts_img_cls"
    engine_names = ".ts_engine_link span"

    # ECU/Block-specific elements (e.g., Bosch EDC15, Bosch EDC16)
    ecu_links = (
        ".catalog-link.ts_link.ts_ecu_link, "
        "main a[href*='/diesel/'], "
        "main a[href*='/petrol/'], "
        "main a[href*='/gearbox/']"
    )
    ecu_names = (
        ".ts_ecu_link, "
        "main a[href*='/diesel/'], "
        "main a[href*='/petrol/'], "
        "main a[href*='/gearbox/']"
    )

    # Stock items specific elements
    stock_list = "ul.catalog-list-panel-ss"
    stock_items = ".ts_original_link.catalog-link"
    stock_link = ".ts_original_link.catalog-link"  # The li itself is clickable
    stock_name = ".ts_original_link.catalog-link span"  # Single span, not nested
    stock_price = ".ts_original_link .catalog-link[itemprop='offers'] span"

    # Stock card elements (when opened)
    product_card = ".product-card"
    product_title = ".product-card .product-title"
    product_info = ".product-card .product-info"
    info_item = ".product-card .info-item"
    info_item_strong = ".product-card .info-item strong"
    info_item_p = ".product-card .info-item p"

    # Content section
    content_container = ".container.bg-white"
    content_title = "h1.font-bold.mb-5"
    content_text = "p.my-5"
    content_heading = "h2"
    content_list = "ul.list-decimal, ul.list-disc"

    # Search functionality
    search_input = "input[type='search'], input[placeholder*='search'], input[placeholder*='поиск']"
    search_button = "button[type='submit'], .search-button"
    search_results = ".search-results, .catalog-items, .products"

    # Catalog items
    catalog_items = ".catalog-item, .product-item, .item"
    item_title = ".item-title, .product-title, h3"
    item_price = ".item-price, .product-price, .price"
    item_image = ".item-image, .product-image, img"
    item_button = ".item-button, .product-button, button"

    # Filters
    filter_container = ".filters, .filter-section"
    category_filter = ".category-filter, select[name*='category']"
    price_filter = ".price-filter, input[name*='price']"
    brand_filter = ".brand-filter, select[name*='brand']"

    # Pagination
    pagination = ".pagination, .page-nav"
    next_page = ".next-page, .pagination-next"
    prev_page = ".prev-page, .pagination-prev"
    page_numbers = ".page-number, .pagination-item"

    # Sorting
    sort_dropdown = ".sort-dropdown, select[name*='sort']"
    sort_by_price = "option[value*='price']"
    sort_by_name = "option[value*='name']"
    sort_by_date = "option[value*='date']"

    # Breadcrumbs
    breadcrumbs = ".breadcrumbs, .breadcrumb"
    breadcrumb_home = ".breadcrumb-home, a[href='/']"
    breadcrumb_catalog = ".breadcrumb-catalog, a[href*='catalog']"
