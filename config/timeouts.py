class Timeouts:

    # Base timeouts (milliseconds)
    BASE_PAGE_LOAD = 15000
    BASE_ELEMENT_VISIBLE = 10000
    BASE_ELEMENT_ENABLED = 10000
    BASE_NETWORK_IDLE = 15000
    BASE_RESPONSE_WAIT = 20000

    # Page-specific timeouts
    class Registration:
        PAGE_LOAD_AFTER_NAVIGATION = 2000
        STANDARD_PAUSE = 1000
        EMAIL_INPUT_VISIBLE = 4000
        EMAIL_INPUT_ENABLED = 4000
        EMAIL_VALIDATION_WAIT = 2000  # Optimized from 3000
        CHECKBOX_CHECKED = 2000
        REGISTER_BUTTON_ENABLED = 8000
        OTP_FIELDS_VISIBLE = 10000  # Increased from 5000
        OTP_SUBMIT_RESPONSE = 5000
        AFTER_OTP_FILL = 5000  # Optimized from 20000
        RESEND_OTP_WAIT = 45000  # KEPT AS IS

    class Upload:
        FILE_INPUT_ATTACHED = 10000  # File input attached state (increased from 5000 per requirements)
        FILE_UPLOADED_VISIBLE = 15000  # File name visible in upload area after upload
        AFTER_FILE_UPLOAD = 3000  # Wait after file upload (animation)
        TYPE_SELECT_ENABLED = 4000  # Type select enabled (per requirements: activation of selects)
        SEARCH_BUTTON_ENABLED = 2000  # Search button enabled (per requirements: activation of selects)
        # Kept for backward compatibility
        SEARCH_SOLUTIONS_WAIT = 3000  # Wait for search results (in milliseconds, was in seconds)
        SOLUTION_ROW_VISIBLE = 10000  # Solution row visibility (increased for reliability with slow network)
        ORDER_TOTAL_VISIBLE = 5000  # Order total visibility (per requirements: appearance of order form)
        AFTER_APPLY_ORDER = 3000  # Wait after applying order
        ERROR_CODE_INPUT_VISIBLE = 3000  # Error code input visibility
        AFTER_ERROR_CODE_CHECK = 2000  # Wait after error code check
        MODAL_CLOSE_WAIT = 2000  # Wait for modal close animation (optimized from 3000)
        FILE_DELETE_WAIT = 2000  # Wait after file delete action

    class App:
        HEADER_LOGO_VISIBLE = 5000  # Header logo visibility
        UPLOAD_AREA_VISIBLE = 5000  # Upload area visibility (large file support)
        AFTER_UPLOAD_CLICK = 1000  # Wait after upload click (animation)
        AFTER_FILE_SET = 1000  # Wait after file set (animation)
        DROPDOWN_SELECT_DELAY = 2000  # Dropdown select animation delay
        PROFILE_LINK_VISIBLE = 3000  # Profile link visibility
        PROFILE_LINK_CLICK = 5000  # Profile link click timeout
        AFTER_NAVIGATION = 2000  # Wait after navigation

    class History:
        HISTORY_LINK_VISIBLE = 2000  # History link visibility
        HISTORY_TABLE_VISIBLE = 4000  # History table visibility
        EMPTY_STATE_VISIBLE = 3000  # Empty state visibility
        PAGINATION_VISIBLE = 4000  # Pagination visibility
        DOWNLOAD_LINK_VISIBLE = 3000  # Download link visibility
        FILE_ROW_VISIBLE = 4000  # File row visibility
        AFTER_ACTION = 1000  # Wait after action (animation)
        AFTER_PAGE_LOAD = 2000  # Wait after page load
        FILE_LINK_VISIBLE = 25000  # File link visibility in history (optimized from 30000)
        ROW_VISIBLE = 8000  # History row visibility (optimized from 10000)
        DTC_BUTTON_VISIBLE = 8000  # DTC disable button visibility (optimized from 10000)

    class Home:
        ELEMENT_VISIBLE = 3000  # Standard element visibility (reduced from 10000)
        HEADER_LOGO_VISIBLE = 3000  # Header logo visibility (reduced from 10000)

    class Balance:
        ELEMENT_VISIBLE = 3000  # Standard element visibility
        BALANCE_DISPLAY_VISIBLE = 3000  # Balance display visibility
        PAYMENT_REQUEST_WAIT = 30000  # Wait for payment API request
        PAYMENT_RESPONSE_WAIT = 200000  # Wait for payment API response (yoomoney/gateline) - 3.33 minutes

    class Profile:
        ELEMENT_VISIBLE = 8000  # Standard element visibility (increased for reliability)
        PROFILE_BLOCKS_LOAD = 10000  # Wait for profile blocks to load

    # Animation waits (milliseconds)
    # DEPRECATED for use in tests: Use expect().to_be_visible() instead of wait_for_timeout
    # Used in page objects via wait_short/medium/standard/long methods (this is fine)
    # Use ONLY for real UI animations or client-side validations in page objects
    # Minimize usage - prefer explicit waits where possible
    class Animation:
        SHORT = 3500  # Short animation (dropdown, tooltip) - used in page objects
        MEDIUM = 5000  # Medium animation (modal fade, button state) - used in page objects
        STANDARD = 4500  # Standard animation (page transition) - used in page objects
        LONG = 8000  # Long animation (complex transitions) - used in page objects
        VERY_LONG = 10000  # Very long animation (heavy UI updates) - used in page objects

    # Modal windows timeouts
    class Modal:
        APPEAR = 8000  # Modal window appearance
        BUTTON_VISIBLE = 4000  # Button visibility in modal
        CONTENT_VISIBLE = 8000  # Modal content visibility
        CLOSE = 3000  # Modal close animation
        TITLE_VISIBLE = 8000  # Modal title visibility
        NOT_VISIBLE = 4000  # Wait for modal to disappear

    # Toast/Alert notifications timeouts
    class Toast:
        APPEAR = 3000  # Toast appearance
        VISIBLE = 12000  # Toast visibility for verification (increased for reliability)

    # Download operations timeouts
    class Download:
        FILE_DOWNLOAD = 25000  # File download timeout
        FILE_DOWNLOAD_FAST = 15000  # Fast file download timeout
        BUTTON_VISIBLE = 10000  # Download button visibility

    # API response timeouts
    class Api:
        LOGIN_CODE_RESPONSE = 20000  # Login code API response
        AUTH_RESPONSE = 15000  # Authentication API response

    # Short wait timeouts
    # DEPRECATED for use in tests: Use expect().to_be_visible() instead of wait_for_timeout
    # Used in page objects (this is fine)
    class ShortWaits:
        SHORT_PAUSE = 1500  # DEPRECATED for tests - used in page objects
        VERY_SHORT_PAUSE = 1000  # Used in page objects
        MEDIUM_PAUSE = 2000  # Used in page objects

    # Page load specific timeouts
    class PageLoad:
        DOMCONTENTLOADED = 5000  # DOMContentLoaded state
        DOMCONTENTLOADED_LONG = 30000  # Long DOMContentLoaded for history
        NETWORKIDLE = 30000  # NetworkIdle state for history

    # Fixture-specific timeouts
    class Fixture:
        PAGE_LOAD_AFTER_GOTO = 3000  # Wait after page.goto()
        EMAIL_FILL_WAIT = 5000  # Wait after email fill (validation)
        CHECKBOX_CHECK_WAIT = 3000  # Wait after checkbox check
        BEFORE_REGISTER_CLICK = 5000  # Wait before register button click
        AFTER_REGISTER_CLICK = 5000  # Wait after register button click (for some fixtures)
