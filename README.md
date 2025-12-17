# TunService Demo

Demo Playwright automation of the TunService website.

## Project Structure

```text
ts-test-front-python/
├── auth/                    # Authentication modules
├── config/                  # Configuration files
├── locators/                # Page locators (dataclasses)
├── pages/                   # Page Object Model classes
├── tests/                   # Test files
│   ├── authenticated/      # Authenticated user tests
│   └── pixels-tests/      # Visual regression tests
├── utils/                   # Utility functions
├── upload/                  # Test files for upload scenarios
├── reports/                 # Test reports and screenshots
├── references/              # Reference screenshots
├── conftest.py             # Pytest fixtures
├── justfile                # Build automation (Just command runner)
├── requirements.txt         # Dependencies
└── pytest.ini              # Pytest configuration
```

## Architecture

**Page Object Model (POM)**:

- **Locators** (`locators/`): Dataclasses with CSS selectors
- **Pages** (`pages/`): Page classes with interaction methods
- **Base Page**: Common functionality (login, navigation, waits)

**Test Organization**:

- `tests/authenticated/`: Tests requiring authentication (uses `auth_user_existing` fixture)
- `tests/pixels-tests/`: Visual regression tests
- `tests/`: Public page tests

## Quick Start

### Setup

```bash
just setup
```

### Run Tests

```bash
# All tests (default: Chromium)
just test

# Smoke and regression tests
just smoke                    # Smoke tests (Chromium, default)
just smoke browser=firefox    # Smoke tests on Firefox
just smoke device=mobile      # Smoke tests on mobile
just regression               # Regression tests (Chromium, default)
just regression browser=webkit device=tablet  # Regression on WebKit tablet

# Device-specific tests
just test-desktop             # Desktop Chrome (1280x720)
just test-mobile              # iPhone 15 Pro Max (430x739)
just test-tablet              # iPad Pro 11 (834x1194)
just test-device "iPhone 14 Pro"  # Any Playwright device
just test-all-devices         # All devices sequentially

# Pixel/Visual regression tests
just test-pixels              # Run all visual regression tests
just test-pixels chromium desktop tests/pixels-tests/test_login_page_pixels.py  # Run specific pixel test
just test-pixels-update       # Update snapshots (all tests)
just test-pixels-update chromium desktop tests/pixels-tests/test_login_page_pixels.py  # Update specific test
just snapshots-clean          # Clean snapshot failure artifacts
```

### Code Quality

```bash
just format      # Format code (black + isort)
just lint        # Lint code (ruff)
just clean       # Clean test artifacts
just allure      # Serve Allure results
```

### Debug & Development

```bash
just test-debug           # Run tests in headed mode (visible browser)
just test-upload           # Run tests with upload marker
just test-authorization    # Run tests with authorization marker
just test-marker <marker>  # Run tests by marker
just health-check          # Check environment status
```

## Key Features

- **Cross-browser Testing** - Chromium, Firefox, WebKit support
- **Pixel Testing** - Visual regression testing with screenshots
- **Allure Reports** - Comprehensive test reporting

## Technologies

- **Playwright** - Web automation and testing
- **Pytest** - Python testing framework
- **Allure** - Test reporting
- **Ruff** - Fast Python linter
- **Black** - Code formatter
- **Just** - Command runner (replaces Make)
