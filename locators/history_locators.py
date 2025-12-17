from dataclasses import dataclass


@dataclass
class HistoryLocators:
    """History page locators"""
    # Page structure
    page_title = "title"
    page_container = "#__nuxt"
    page_body = ".page-body"

    # Header navigation (same as app page)
    header_container = ".t-header"
    header_logo = "a[href='https://ts.tun2.ru/'], a[href*='ts.tun2.ru']"
    header_logo_img = ".t-header img[alt='logo']"
    menu_block = ".menu-block"
    history_link = "a[href*='/app/history'].item-link, a.ts_hover_bg_h.item-link:has-text('История')"

    # History page specific elements
    history_container = ".history-container, .history-wrapper"
    history_table = ".history-table, table"
    history_table_row = "tr.history-row, tr[data-test-id='history-row']"
    history_table_header = "thead, .history-table-header"
    history_table_body = "tbody, .history-table-body"

    # History item elements
    history_item = ".history-item, [data-test-id='history-item']"
    history_item_date = ".history-item-date, [data-test-id='history-date']"
    history_item_status = ".history-item-status, [data-test-id='history-status']"
    history_item_price = ".history-item-price, [data-test-id='history-price']"
    history_item_download = ".history-item-download, [data-test-id='history-download']"
    history_item_time = ".history-item-time, [data-test-id='history-time']"
    history_item_task = ".history-item-task, [data-test-id='history-task']"
    history_item_info_button = "button:has-text('Инфо'), button:has-text('INFO'), button[aria-label*='Инфо'], button[aria-label*='Info']"
    history_item_disable_button = "button:has-text('Отключить'), button:has-text('Disable'), button[aria-label*='Отключить'], button[aria-label*='Disable']"
    history_download_link = "a:has-text('Скачать'), a:has-text('Download'), a[href*='download'], a[aria-label*='Скачать'], a[aria-label*='Download']"

    # Empty state
    empty_state = ".history-empty, [data-test-id='history-empty']"
    empty_state_message = ".history-empty-message, [data-test-id='history-empty-message']"

    # Pagination
    pagination = ".pagination, [data-test-id='pagination'], .page-nav"
    pagination_container = ".pagination-container, .pagination-wrapper"
    pagination_first = "button:has(.i-lucide\\:chevrons-left), button[aria-label*='Первая'], button[aria-label*='First']"
    pagination_prev = "button:has(.i-lucide\\:chevron-left), button[aria-label*='Предыдущая'], button[aria-label*='Previous']"
    pagination_next = "button:has(.i-lucide\\:chevron-right), button[aria-label*='Следующая'], button[aria-label*='Next']"
    pagination_last = "button:has(.i-lucide\\:chevrons-right), button[aria-label*='Последняя'], button[aria-label*='Last']"
    pagination_page_number = ".pagination-page, [data-test-id='pagination-page'], button.pagination-page"
    pagination_current_page = ".pagination-page-active, [data-test-id='pagination-current'], button[aria-current='page']"
    pagination_info = ".pagination-info, [data-test-id='pagination-info'], .page-info"
