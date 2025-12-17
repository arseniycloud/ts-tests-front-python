from dataclasses import dataclass


@dataclass
class AppLocators:
    # Page structure
    page_title = "title"
    page_container = "#__nuxt"

    # Header navigation
    header_container = "[data-test-id='header_container'], .t-header"
    header_logo = "[data-test-id='header_logo'], a[href='https://ts.tun2.ru/'], a[href*='ts.tun2.ru']"
    header_logo_img = "[data-test-id='header_logo_img'], .t-header img[alt='logo']"

    # Header menu items
    menu_block = "[data-test-id='menu_block'], .menu-block"
    tun_link = "[data-test-id='tun_link'], .menu-block .ts_hover_bg.item-link:has-text('Tun'), span.ts_hover_bg.item-link.h-\\[69px\\]:has-text('Tun')"
    tun_link_data_test_id = "[data-test-id='tun_link']"
    history_link = "[data-test-id='history_link'], a[href*='/app/history'].item-link, a.ts_hover_bg_h.item-link:has-text('История')"
    balance_link = "[data-test-id='balance_link'], a[href*='/app/payment'].item-link, a.ts_hover_bg_h.item-link:has-text('₽')"
    profile_link = "[data-test-id='profile_link'], a[href*='/app/profile'].item-link, a.ts_hover_bg_h.item-link:has-text('@test.com')"
    logout_button = ".menu-block .ts_hover_bg_h.item-void:has-text('Выйти'), span.ts_hover_bg_h.item-void:has-text('Выйти')"

    # Language selector
    language_selector = "[data-test-id='language_selector'], .relative.flex.items-center.flex-shrink-0.cursor-pointer"
    language_flag = "[data-test-id='language_flag'], img[alt='Language flag']"
    language_dropdown = ".iconify.i-ic\\:round-keyboard-arrow-down"

    # Upload form
    upload_form = "[data-test-id='upload-form'], form.upload-f"
    upload_form_container = "[data-test-id='upload-form'] .w-full.lg\\:max-w-\\[768px\\]"
    upload_button = "[data-test-id='upload-btn']"
    upload_label = "[data-test-id='upload-label'], h1[data-test-id='upload-label']"
    file_input = "[data-test-id='file_input'], #file-upload, input[type='file']"
    upload_area = "[data-test-id='upload_area'], .uploader-ss"
    upload_icon = "[data-test-id='upload_icon'], .i-material-symbols\\:upload-file-rounded"
    upload_button_container = "[data-test-id='upload-btn']"

    # Upload form messages
    archive_not_supported = "[data-test-id='archive_not_supported'], text='rar, zip, 7zip и другие архивы не поддерживаются'"
    unpacked_files_only = "[data-test-id='unpacked_files_only'], text='Только распакованные файлы'"

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
    footer_container = "[data-test-id='footer_container'], .bg-\\[\\#101010\\]"
    footer_logo = "[data-test-id='footer_logo'], img[alt='logo']"
    footer_nav_links = "[data-test-id='footer_container'] .nav a, .nav a"
    footer_policy_link = "[data-test-id='footer_policy_link'], a[href*='/policy']"
    footer_agreement_link = "[data-test-id='footer_agreement_link'], a[href*='/agreement']"

    # Loading states
    loading_spinner = ".i-line-md\\:loading-loop"
    button_disabled = "button[disabled]"

    # Notifications/Toasts
    toast_container = "ol[data-expanded='true'].fixed"
    toast_item = "ol[data-expanded='true'] li"

    # Mobile menu
    mobile_menu_button = "[data-test-id='mobile_menu_button'], .mobile-menu-btn, .t-vertical-menu-ss"

    # Page structure
    page_body = "[data-test-id='page_body'], .page-body"
    wrap_main = "[data-test-id='wrap_main'], .wrap_main"
    rows_main_block = "[data-test-id='rows_main_block'], .rows_main_block"

    # Order form and price calculation
    order_form_area = "[data-test-id='order_form_area'], .order-form-area"
    order_form = "[data-test-id='order-form']"
    order_table = "[data-test-id='order-form'] table.order-table, .order-table"
    order_table_row = "[data-test-id='order-form'] tr.o-row, tr.o-row"
    order_table_cell = "[data-test-id='order-form'] td[role='cell'], td[role='cell']"
    order_checkbox = "[data-test-id='order-form'] input[type='checkbox'], tr.o-row input[type='checkbox']"
    order_apply_button = "[data-test-id='order-apply-btn']"
    order_total = "[data-test-id='order-total']"
    order_cash = "[data-test-id='order-cash']"
    download_button = "button:has-text('Скачать')"

    # Task block (file info after upload)
    task_block = ".task-block"
    task_number = ".task-block .task-number"

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
