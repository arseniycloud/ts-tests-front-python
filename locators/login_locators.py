from dataclasses import dataclass


@dataclass
class LoginLocators:
    # Page structure
    page_title = "h1.rf-title"
    page_container = "[data-test-id='page_body']"
    login_form = "[data-test-id='login-form'], .login-container, .auth-form, form"

    # Form fields
    username_field = "[data-test-id='auth_email_input']"
    password_field = "input[type='password'], input[name*='password']"
    remember_me = "input[type='checkbox'], input[name*='remember']"

    # Buttons
    login_button = "[data-test-id='auth_login_btn']"
    forgot_password = "a:has-text('забыли'), a:has-text('forgot'), a:has-text('восстановить')"
    register_link = "a:has-text('регистрация'), a:has-text('register'), a:has-text('создать')"

    # Error messages
    error_message = ".error, .alert-danger, .login-error, [class*='error'], [role='alert']"
    error_title = "text='Ошибка входа в систему!'"
    error_title_otp = "text='Ошибка ввода кода авторизации!'"
    error_user_not_exists = "text=/User .+ doesn't exist/"
    error_token_invalid = "text='token invalid'"
    error_field = ".field-error, .input-error, .validation-error"
    alert = "[role='alert']"

    # Toast/Notification container
    toast_container = "ol[data-expanded='true'].fixed, [role='region'][aria-label*='Notifications']"
    toast_alert_item = "ol[data-expanded='true'] li[role='alert'], [role='region'][aria-label*='Notifications'] li[role='alert'], [role='region'][aria-label*='Notifications'] [role='alert']"

    # Success messages
    success_message = ".success, .alert-success, .login-success"

    # Social login
    social_login = ".social-login, .oauth-login"
    google_login = ".google-login, button:has-text('Google')"
    facebook_login = ".facebook-login, button:has-text('Facebook')"
    vk_login = ".vk-login, button:has-text('VK')"

    # Form validation
    required_field = "[required]"
    field_label = "label"
    field_help = ".help-text, .field-help"

    # Loading states
    loading_spinner = ".loading, .spinner, .loader"
    submit_loading = "button[disabled], input[disabled]"

    # Additional links
    terms_link = "a:has-text('условия'), a:has-text('terms')"
    privacy_link = "a:has-text('конфиденциальность'), a:has-text('privacy')"

    # Language selector
    language_selector = ".language-selector, select[name*='lang']"

    # Captcha
    captcha_container = ".captcha, .recaptcha"
    captcha_image = ".captcha-image, img[alt*='captcha']"
    captcha_input = ".captcha-input, input[name*='captcha']"

    # Two-factor authentication / OTP
    two_factor_code = "input[name*='code'], input[name*='2fa']"
    two_factor_button = "button:has-text('подтвердить'), button:has-text('verify')"
    otp_pin_1 = "[data-test-id='pin-1']"
    otp_pin_2 = "[data-test-id='pin-2']"
    otp_pin_3 = "[data-test-id='pin-3']"
    otp_pin_4 = "[data-test-id='pin-4']"
    otp_pin_5 = "[data-test-id='pin-5']"
    otp_pins = "[data-test-id^='pin-']"
    otp_send_button = "[data-test-id='pin-code-send-btn']"
    otp_resend_button = "[data-test-id='pin-code-resend-btn'], button:has-text('ОТПРАВИТЬ ПОВТОРНО')"

    # Password strength indicator
    password_strength = ".password-strength, .strength-meter"
    strength_weak = ".strength-weak"
    strength_medium = ".strength-medium"
    strength_strong = ".strength-strong"
