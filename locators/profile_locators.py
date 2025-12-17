from dataclasses import dataclass


@dataclass
class ProfileLocators:
    # Page structure
    page_title = "title"
    page_container = "#__nuxt"
    page_body = "[data-test-id='page_body'], .page-body"

    # Profile container
    profile_container = ".profile-container"
    profile_blocks = ".profile-block.profile-block-ss"  # Target inner divs with both classes

    # Profile block elements
    profile_column = ".profile-column, .profile-column.profile-column-ss"
    profile_title = ".profile-title, .profile-title.profile-title-ss"
    profile_subtitle = ".profile-subtitle, .profile-subtitle.profile-subtitle-ss"
    profile_wrapper = ".profile-wrapper.profile-wrapper-ss"  # Target inner divs with both classes
    profile_data = ".profile-data"
    profile_data_in_wrapper = ".profile-wrapper .profile-data, .profile-wrapper.profile-wrapper-ss .profile-data"
    profile_data_value = "div:last-child"

    # Profile data elements
    email_label = ".profile-data div:first-child"
    email_value = ".profile-data div:last-child"
    email_value_container = ".profile-data div.overflow-x-auto"

    # Discount block
    discount_title = ".profile-title:has-text('Ваша скидка'), .profile-title:has-text('Your discount')"
    discount_subtitle = ".profile-subtitle:has-text('Вам предоставлена скидка'), .profile-subtitle:has-text('You have been given a discount')"
    discount_percentage_label = ".profile-data:has-text('Процент скидки') div:first-child, .profile-data:has-text('Discount percentage') div:first-child"
    discount_percentage_value = ".profile-data:has-text('Процент скидки') div:last-child, .profile-data:has-text('Discount percentage') div:last-child"

    # Cashback block
    cashback_title = ".profile-title:has-text('Ваш кэшбэк'), .profile-title:has-text('Your cashback')"
    cashback_subtitle = ".profile-subtitle:has-text('Вам доступна опция кэшбэк'), .profile-subtitle:has-text('Cashback option available to you')"
    cashback_percentage_label = ".profile-data:has-text('Процент кэшбэка') div:first-child, .profile-data:has-text('Cashback percentage') div:first-child"
    cashback_percentage_value = ".profile-data:has-text('Процент кэшбэка') div:last-child, .profile-data:has-text('Cashback percentage') div:last-child"
    cashback_accumulated_label = ".profile-data:has-text('Накоплено кэшбэка') div:first-child, .profile-data:has-text('Cashback accumulated') div:first-child"
    cashback_accumulated_value = ".profile-data:has-text('Накоплено кэшбэка') div:last-child, .profile-data:has-text('Cashback accumulated') div:last-child"
