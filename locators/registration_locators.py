from dataclasses import dataclass


@dataclass
class RegistrationLocators:
    """Registration page locators"""
    # Page structure
    page_title = "h1.rf-title"
    page_container = "#__nuxt"
    registration_form = ".register-container, .auth-form, [data-testid='register-form'], form, .form"

    # Form fields
    email_field = "[data-test-id='auth_email_input']"
    password_field = "input[type='password'], input[name*='password'], input[placeholder*='пароль']"
    confirm_password_field = "input[name*='confirm'], input[name*='confirm_password'], input[placeholder*='подтвердить']"
    name_field = "input[name*='name'], input[placeholder*='имя']"
    phone_field = "input[type='tel'], input[name*='phone']"

    # Buttons
    register_button = "button:has-text('зарегистрироваться'), button:has-text('Зарегистрироваться'), button:has-text('ЗАРЕГИСТРИРОВАТЬСЯ')"
    login_link = "a:has-text('войти'), a:has-text('login'), a:has-text('уже есть аккаунт')"

    # Error messages
    error_message = ".error, .alert-danger, .register-error, [class*='error'], [role='alert']"
    error_email_empty = "text='Email не может быть пустым!'"
    error_email_invalid = "text='Email не корректный!'"
    error_email_title = "text='Ошибка ввода email!'"
    error_password_weak = "text=/Пароль .* слабый/"
    error_password_confirm = "text=/Пароль.* не совпадает/"
    error_field = ".field-error, .input-error, .validation-error"
    alert = "[role='alert']"

    # Toast/Notification container
    toast_container = "ol[data-expanded='true'].fixed"
    toast_alert_item = "ol[data-expanded='true'] li[role='alert']"

    # Success messages
    success_message = ".success, .alert-success, .register-success"

    # Terms and conditions
    terms_checkbox = "input[type='checkbox']"
    terms_link = "a:has-text('условия'), a:has-text('terms')"
    privacy_link = "a:has-text('конфиденциальность'), a:has-text('privacy')"

    # Form validation
    required_field = "[required]"
    field_label = "label"
    field_help = ".help-text, .field-help"

    # OTP/Verification code fields (same as login)
    otp_pin_1 = "[data-test-id='pin-1']"
    otp_pin_2 = "[data-test-id='pin-2']"
    otp_pin_3 = "[data-test-id='pin-3']"
    otp_pin_4 = "[data-test-id='pin-4']"
    otp_pin_5 = "[data-test-id='pin-5']"
    otp_pins = "[data-test-id^='pin-']"
    otp_send_button = "[data-test-id='pin-code-send-btn']"
    otp_resend_button = "[data-test-id='pin-code-resend-btn'], button:has-text('ОТПРАВИТЬ ПОВТОРНО')"

    # OTP page elements
    otp_title = ".auth-code-block__title"
    otp_inputs_container = ".auth-code-block__inputs"
    otp_info_email = ".auth-code-block__info b"
    otp_info_text = ".auth-code-block__info p"
    otp_check_email_text = "text='Проверьте почту'"
    otp_code_sent_text = "text='Вам выслано письмо с кодом подтверждения.'"
    otp_spam_text = "text='Если письмо не приходит, проверьте папку Спам.'"
