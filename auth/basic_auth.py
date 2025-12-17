import base64

from playwright.sync_api import Page

from config.auth_config import PASSWORD, USERNAME


def login(page: Page) -> None:
    # Create Basic Auth header
    credentials = f"{USERNAME}:{PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Set Basic Auth credentials
    page.set_extra_http_headers({'Authorization': f'Basic {encoded_credentials}'})
