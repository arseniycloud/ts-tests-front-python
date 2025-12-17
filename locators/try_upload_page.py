from dataclasses import dataclass


@dataclass
class TryUploadLocators:
    """Try Upload page locators for unregistered users"""
    # Page structure
    page_title = "title"
    page_container = "#__nuxt"

    # Header navigation (for unregistered users)
    header_container = ".t-header"
    header_logo = "a[href='/'], a[data-test-id='header_logo'], .t-header a[href='/']"
    header_logo_img = ".t-header img[alt='logo'], a[href='/'] img[alt='logo']"
    prices_link = "a[href*='/price'], a:has-text('Цены')"
    catalog_link = "a[href*='/catalog'], a:has-text('Каталог')"
    login_link = "a[href*='/app/login'], a:has-text('Войти')"

    # Language selector
    language_selector = ".relative.flex.items-center.flex-shrink-0.cursor-pointer"
    language_flag = "img[alt='Language flag']"
    language_dropdown = ".iconify.i-ic\\:round-keyboard-arrow-down"

    # Upload form
    upload_form = "[data-test-id='upload-form'], form.upload-f"
    upload_form_container = "[data-test-id='upload-form'] .w-full.lg\\:max-w-\\[768px\\]"
    upload_button = "[data-test-id='upload-btn']"
    upload_label = "[data-test-id='upload-label'], h1[data-test-id='upload-label']"
    file_input = "#file-upload, input[type='file']"
    upload_area = ".uploader-ss"
    upload_icon = ".i-material-symbols\\:upload-file-rounded"
    upload_button_container = "[data-test-id='upload-btn']"

    # Upload form messages
    archive_not_supported = "text='rar, zip, 7zip и другие архивы не поддерживаются'"
    unpacked_files_only = "text='Только распакованные файлы'"

    # Select dropdowns
    select_row = ".select-f-row"
    type_select = "[data-test-id='type-select']"
    type_select_input = "[data-test-id='type-select'] input.search_input, [data-test-id='type-select'] input[type='text']"
    type_select_placeholder = "[data-test-id='type-select'] input[placeholder='Тип']"
    type_select_dropdown = "[data-test-id='type-select'] .arrow-down"
    type_select_box = "[data-test-id='type-select'] .select-box"
    type_select_options_container = "[data-test-id='type-select'] ~ div.p-1.max-h-64, div.p-1.max-h-64:has(> div:has-text('Car'))"

    brand_select = "[data-test-id='brand-select']"
    brand_select_input = "[data-test-id='brand-select'] input.search_input, [data-test-id='brand-select'] input[type='text']"
    brand_select_placeholder = "[data-test-id='brand-select'] input[placeholder='Бренд'], [data-test-id='brand-select'] input[placeholder='Марка']"
    brand_select_dropdown = "[data-test-id='brand-select'] .arrow-down"
    brand_select_box = "[data-test-id='brand-select'] .select-box"
    brand_select_options_container = "[data-test-id='brand-select'] ~ div.p-1.max-h-64"

    engine_select = "[data-test-id='engine-select']"
    engine_select_input = "[data-test-id='engine-select'] input.search_input, [data-test-id='engine-select'] input[type='text']"
    engine_select_placeholder = "[data-test-id='engine-select'] input[placeholder='Двигатель']"
    engine_select_dropdown = "[data-test-id='engine-select'] .arrow-down"
    engine_select_box = "[data-test-id='engine-select'] .select-box"
    engine_select_options_container = "[data-test-id='engine-select'] ~ div.p-1.max-h-64"

    ecu_select = "[data-test-id='ecu-select']"
    ecu_select_input = "[data-test-id='ecu-select'] input.search_input, [data-test-id='ecu-select'] input[type='text']"
    ecu_select_placeholder = "[data-test-id='ecu-select'] input[placeholder='Блок']"
    ecu_select_dropdown = "[data-test-id='ecu-select'] .arrow-down"
    ecu_select_box = "[data-test-id='ecu-select'] .select-box"
    ecu_select_options_container = "[data-test-id='ecu-select'] ~ div.p-1.max-h-64"

    # Search button
    search_button = "[data-test-id='editor-search-btn']"
    search_button_text = "[data-test-id='editor-search-btn']:has-text('Найти')"
    search_button_icon = "[data-test-id='editor-search-btn'] .i-heroicons\\:magnifying-glass"

    # Select states
    select_disabled = ".select-box-disabled"
    select_enabled = ".select-box:not(.select-box-disabled)"

    # Footer
    footer_container = ".bg-\\[\\#101010\\]"
    footer_logo = "img[alt='logo']"
    footer_nav_links = ".nav a"
    footer_policy_link = "a[href*='/policy']"
    footer_agreement_link = "a[href*='/agreement']"

    # Loading states
    loading_spinner = ".i-line-md\\:loading-loop"
    button_disabled = "button[disabled]"

    # Notifications/Toasts
    toast_container = "ol[data-expanded='true'].fixed"
    toast_item = "ol[data-expanded='true'] li"

    # Mobile menu
    mobile_menu_button = ".mobile-menu-btn, .t-vertical-menu-ss"

    # Page structure
    page_body = ".page-body"
    wrap_main = ".wrap_main"
    rows_main_block = ".rows_main_block"

    # Order form and price calculation
    order_form_area = "[data-test-id='order_form_area'], .order-form-area"
    order_form = "[data-test-id='order-form']"
    order_table = ".order-table"
    order_table_row = "tr.o-row"
    order_table_cell = "td[role='cell']"
    order_checkbox = "input[type='checkbox']"
    order_apply_button = "[data-test-id='order-apply-btn']"
    order_total = "[data-test-id='order-total']"
    order_cash = "[data-test-id='order-cash']"
    download_button = "button:has-text('Скачать')"

    # Payment modals
    need_pay_modal = "[data-test-id='need-pay-modal']"
    payment_need_modal_pay_btn = "[data-test-id='payment-need-modal-pay-btn']"
    payment_methods_panel = "[data-test-id='payment-methods-panel']"
    payment_amount = "[data-test-id='payment-amount']"
    payment_pay_btn = "[data-test-id='payment-pay-btn']"

    # Cashback and balance
    cashback_toggle = "label span"
    balance_display = "[data-test-id='page_body'] div"

    # Upload area and icon (data-test-id versions)
    upload_area_data_test_id = "[data-test-id='upload_area']"
    upload_icon_data_test_id = "[data-test-id='upload_icon']"
    uploaded_file_name = "[data-test-id='uploaded-file-name']"

    # History and info
    patch_title = ".patch-title"
    close_icon = ".iconify.i-material-symbols\\:close-rounded"

    # Unregistered user panel
    not_auth_panel = "#not_auth_panel"
    not_auth_panel_text = "#not_auth_panel"
    not_auth_register_link = "#not_auth_panel a[href*='/app/register']"
    not_auth_login_link = "#not_auth_panel a[href*='/app/login']"
