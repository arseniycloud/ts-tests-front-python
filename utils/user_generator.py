import random
import time
import uuid



def generate_test_email(random_int=None, balance=None, cashback=None, discount=None):
    if random_int is None:
        random_int = random.randint(1000000, 9999999)

    parts = []

    if balance:
        parts.append(f"+{balance}")

    if cashback:
        parts.append(f"+c{cashback}")

    if discount:
        parts.append(f"+d{discount}")

    return f"test{random_int}{''.join(parts)}@test.com"


def generate_basic_user():
    return generate_test_email()


def generate_user_with_zero_balance(balance=0):
    return generate_test_email(balance=balance)


def generate_user_with_balance(balance=10000):
    return generate_test_email(balance=balance)


def generate_user_with_cashback(balance=10000,cashback=10):
    return generate_test_email(balance=balance, cashback=cashback)


def generate_user_with_discount(balance=10000, discount=10):
    return generate_test_email(balance=balance, discount=discount)


def generate_premium_user(balance=50000, cashback=10, discount=20):
    return generate_test_email(balance=balance, cashback=cashback, discount=discount)


def generate_user_with_balance_and_discount(balance=10000, discount=20):
    return generate_test_email(balance=balance, discount=discount)


def generate_user_without_balance_but_cashback(cashback=50):
    return generate_test_email(balance=0, cashback=cashback)


def generate_user_without_balance_but_discount(discount=20):
    return generate_test_email(balance=0, discount=discount)


def generate_user_without_balance_but_cashback_and_discount(cashback=50, discount=20):
    return generate_test_email(balance=0, cashback=cashback, discount=discount)


def generate_unique_email():
    timestamp = int(time.time() * 1000)  # milliseconds
    unique_id = str(uuid.uuid4())[:9]  # First 8 characters of UUID
    return f"test{timestamp}{unique_id}@test.com"
