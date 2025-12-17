"""Utility modules for testing"""
from utils.playwright_helpers import scroll_to_make_visible
from utils.user_generator import (
    generate_basic_user,
    generate_premium_user,
    generate_test_email,
    generate_unique_email,
    generate_user_with_cashback,
    generate_user_with_discount,
    generate_user_with_zero_balance,
)

__all__ = [
    'generate_test_email',
    'generate_basic_user',
    'generate_user_with_zero_balance',
    'generate_user_with_cashback',
    'generate_user_with_discount',
    'generate_premium_user',
    'generate_unique_email',
    'scroll_to_make_visible',
]
