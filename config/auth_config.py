# Authentication configuration
import os

# Credentials for authentication
USERNAME = os.getenv("TEST_USERNAME")
PASSWORD = os.getenv("TEST_PASSWORD")

# Base URL
BASE_URL = os.getenv("BASE_URL")

# Authentication endpoints (if needed)
LOGIN_URL = os.getenv("LOGIN_URL", "/app/login")

# OTP code for testing
OTP_CODE = os.getenv("OTP_CODE")


def _validate_required_config():
    """Validate that all required configuration variables are set"""
    missing = []
    if not USERNAME:
        missing.append("TEST_USERNAME")
    if not PASSWORD:
        missing.append("TEST_PASSWORD")
    if not BASE_URL:
        missing.append("BASE_URL")
    if not OTP_CODE:
        missing.append("OTP_CODE")

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Please set them in your .env file or environment. "
            f"See .env.example for reference."
        )


# Validate configuration on import
_validate_required_config()
