# Justfile for TunService Test Automation Project
#
# DEVICE TESTING
# ==============
# Проект поддерживает запуск тестов на разных устройствах.
# Информация о device автоматически добавляется во все отчеты:
# - Allure отчеты: labels для фильтрации (device, viewport)
# - HTML отчеты: Environment таблица + кастомные колонки (Device, Viewport)
# - JUnit XML: properties для GitHub Actions (device, viewport)
# - Playwright Trace: title, HTTP headers, metadata tab
#
# ДОСТУПНЫЕ УСТРОЙСТВА:
# - desktop: Desktop Chrome (1280x720)
# - mobile: iPhone 15 Pro Max (430x739)
# - tablet: iPad Pro 11 (834x1194)
# - Любое устройство из Playwright: DEVICE="iPhone 14 Pro"
#
# ПРИМЕРЫ:
#   just test-desktop                    # Desktop + Chromium
#   just test-mobile                     # Mobile + Chromium
#   just test-device "iPhone 14 Pro"

# ============================================================================
# CONFIGURATION
# ============================================================================
VENV := ".venv"
PYTEST := VENV + "/bin/pytest"
PYTHON := VENV + "/bin/python"

# Common pytest options
PYTEST_OPTS := "-v --tb=short"
PYTEST_BROWSER := "chromium"
PYTEST_BASE := PYTEST + " tests/ " + PYTEST_OPTS + " --browser " + PYTEST_BROWSER

# Paths
TESTS_DIR := "tests/"
PIXEL_TESTS_DIR := "tests/pixels-tests/"
REPORTS_DIR := "reports/"
ALLURE_RESULTS := REPORTS_DIR + "allure-results"
ALLURE_REPORT := REPORTS_DIR + "allure-report"

# ============================================================================
# VALIDATION
# ============================================================================
_check-root:
    #!/usr/bin/env bash
    if [ ! -f "justfile" ] || [ ! -f "pytest.ini" ]; then
        echo "❌ Error: Must run from project root directory"
        echo "Current directory: $(pwd)"
        echo "Please run 'cd' to project root first"
        exit 1
    fi
    if [ ! -f "{{PYTEST}}" ]; then
        echo "❌ Error: Virtual environment not found at {{VENV}}"
        echo "Please run: python -m venv {{VENV}} && source {{VENV}}/bin/activate && pip install -r requirements.txt"
        exit 1
    fi

# ============================================================================
# HELP
# ============================================================================
default: _check-root
    @echo "🚀 TunService Test Automation - Available Commands"
    @echo ""
    @echo "🧪 Functional Tests:"
    @echo "  just test              - Run all functional tests (Chromium)"
    @echo "  just smoke             - Run smoke tests (supports browser/device)"
    @echo "  just regression        - Run regression tests (supports browser/device)"
    @echo "  just validation        - Run validation tests (supports browser/device)"
    @echo ""
    @echo "💡 Smoke/Regression/Validation Examples:"
    @echo "  just smoke                                    # Smoke tests (Chromium, default)"
    @echo "  just smoke browser=firefox                   # Smoke tests on Firefox"
    @echo "  just smoke device=mobile                     # Smoke tests on mobile"
    @echo "  just smoke browser=webkit device=tablet      # Smoke tests on WebKit tablet"
    @echo "  just regression                              # Regression tests (Chromium, default)"
    @echo "  just regression browser=firefox device=mobile # Regression on Firefox mobile"
    @echo "  just validation                              # Validation tests (Chromium, default)"
    @echo "  just validation browser=firefox device=mobile # Validation on Firefox mobile"
    @echo ""
    @echo "📸 Visual Regression Tests (format: {browser}-{viewport}-{title}.png):"
    @echo "  just test-pixels                    - Run pixel tests (chromium-desktop)"
    @echo "  just test-pixels browser=webkit     - Run pixel tests for WebKit"
    @echo "  just test-pixels-all                - Run pixel tests for all browsers"
    @echo "  just test-pixels-update             - Update snapshots (chromium-desktop)"
    @echo "  just test-pixels-update browser=webkit - Update WebKit snapshots"
    @echo "  just test-pixels-update-all         - Update snapshots for all browsers"
    @echo "  just snapshots-clean                - Clean snapshot failure artifacts"
    @echo ""
    @echo "📝 Pixel Tests Examples:"
    @echo "  just test-pixels                    # Run all Chromium pixel tests"
    @echo "  just test-pixels webkit             # Run WebKit pixel tests"
    @echo "  just test-pixels chromium desktop tests/pixels-tests/test_login_page_pixels.py  # Run specific test"
    @echo "  just test-pixels-update chromium desktop tests/pixels-tests/test_login_page_pixels.py  # Update specific test"
    @echo "  Download reference snapshots from GitHub Actions artifacts (first time setup)"
    @echo ""
    @echo "📱 Device-specific tests (device info added to all reports):"
    @echo "  test-desktop - Desktop Chrome (1280x720)"
    @echo "  test-mobile  - iPhone 15 Pro Max (430x739)"
    @echo "  test-tablet - iPad Pro 11 (834x1194)"
    @echo "  test-device <device> - Any Playwright device"
    @echo "  test-all-devices - All devices (desktop, mobile, tablet)"
    @echo ""
    @echo "🔧 Other commands:"
    @echo "  lint        - Run linting (ruff)"
    @echo "  format      - Format code (black + isort)"
    @echo "  clean       - Clean test artifacts"
    @echo "  allure      - Serve Allure results ({{ALLURE_RESULTS}})"
    @echo ""
    @echo "🐛 Debug & Development:"
    @echo "  test-debug     - Run tests in headed mode (visible browser)"
    @echo "  test-upload     - Run tests with upload marker"
    @echo "  test-authorization - Run tests with authorization marker"
    @echo "  test-marker <marker> - Run tests by marker"

help: default

# ============================================================================
# SETUP
# ============================================================================
setup: _check-root
    @echo "🔧 Setting up project dependencies..."
    pip install -r requirements.txt
    @echo "🎭 Installing Playwright browsers..."
    playwright install
    @echo "✅ Setup completed successfully!"

# ============================================================================
# FUNCTIONAL TESTS
# ============================================================================
test browser="chromium" device="": _check-root
    #!/usr/bin/env bash
    BROWSER_ARG="--browser {{browser}}"
    if [ -n "{{device}}" ]; then
        DEVICE={{device}} {{PYTEST}} {{TESTS_DIR}} {{PYTEST_OPTS}} $BROWSER_ARG
    else
        {{PYTEST}} {{TESTS_DIR}} {{PYTEST_OPTS}} $BROWSER_ARG
    fi

smoke browser="chromium" device="": _check-root
    #!/usr/bin/env bash
    BROWSER_ARG="--browser {{browser}}"
    if [ -n "{{device}}" ]; then
        DEVICE={{device}} {{PYTEST}} {{TESTS_DIR}} {{PYTEST_OPTS}} -m smoke $BROWSER_ARG
    else
        {{PYTEST}} {{TESTS_DIR}} {{PYTEST_OPTS}} -m smoke $BROWSER_ARG
    fi

regression browser="chromium" device="": _check-root
    #!/usr/bin/env bash
    BROWSER_ARG="--browser {{browser}}"
    if [ -n "{{device}}" ]; then
        DEVICE={{device}} {{PYTEST}} {{TESTS_DIR}} {{PYTEST_OPTS}} -m "smoke or regression" $BROWSER_ARG
    else
        {{PYTEST}} {{TESTS_DIR}} {{PYTEST_OPTS}} -m "smoke or regression" $BROWSER_ARG
    fi

validation browser="chromium" device="": _check-root
    #!/usr/bin/env bash
    BROWSER_ARG="--browser {{browser}}"
    if [ -n "{{device}}" ]; then
        DEVICE={{device}} {{PYTEST}} {{TESTS_DIR}} {{PYTEST_OPTS}} -m validation $BROWSER_ARG
    else
        {{PYTEST}} {{TESTS_DIR}} {{PYTEST_OPTS}} -m validation $BROWSER_ARG
    fi

# Marker-based tests
test-upload: _check-root
    @echo "📤 Running tests with upload marker..."
    {{PYTEST_BASE}} -m upload

test-authorization: _check-root
    @echo "🔐 Running tests with authorization marker..."
    {{PYTEST_BASE}} -m authorization

test-marker marker: _check-root
    @echo "🏷️  Running tests with marker: {{marker}}"
    {{PYTEST_BASE}} -m {{marker}}

# Sequential execution (for Docker)
tests: _check-root
    @echo "🐢 Running tests sequentially (for Docker)..."
    {{PYTEST_BASE}} -n 1

# ============================================================================
# VISUAL REGRESSION TESTS
# ============================================================================
# Snapshot naming format: {browser}-{viewport}-{title}.png
# Examples: chromium-desktop-test_header.png, webkit-desktop-test_footer.png
#
# CI Workflow:
# 1. First run creates snapshots in CI (Chrome/WebKit differ from local)
# 2. Download snapshots from CI artifacts: just snapshots-download
# 3. Commit to repo: git add references/ && git commit
# 4. Subsequent runs compare against committed snapshots

test-pixels browser="chromium" device="desktop" *args: _check-root
    #!/usr/bin/env bash
    echo "📸 Running visual regression tests ({{browser}} on {{device}})..."
    if [ "$#" -gt 0 ]; then
        HEADLESS=true BROWSER={{browser}} DEVICE={{device}} \
            {{PYTEST}} "$@" {{PYTEST_OPTS}} -m pixel_test --browser {{browser}} --color=yes
    else
        HEADLESS=true BROWSER={{browser}} DEVICE={{device}} \
            {{PYTEST}} {{PIXEL_TESTS_DIR}} {{PYTEST_OPTS}} -m pixel_test --browser {{browser}} --color=yes
    fi

test-pixels-all: _check-root
    #!/usr/bin/env bash
    echo "📸 Running pixel tests for all browsers..."
    echo "🌐 Testing Chromium..."
    HEADLESS=true BROWSER=chromium DEVICE=desktop \
        {{PYTEST}} {{PIXEL_TESTS_DIR}} {{PYTEST_OPTS}} -m pixel_test --browser chromium --color=yes
    echo ""
    echo "🌐 Testing WebKit..."
    HEADLESS=true BROWSER=webkit DEVICE=desktop \
        {{PYTEST}} {{PIXEL_TESTS_DIR}} {{PYTEST_OPTS}} -m pixel_test --browser webkit --color=yes
    echo ""
    echo "✅ All browsers tested!"

test-pixels-update browser="chromium" device="desktop" *args: _check-root
    #!/usr/bin/env bash
    echo "📸 Updating visual snapshots ({{browser}} on {{device}})..."
    if [ "$#" -gt 0 ]; then
        HEADLESS=true BROWSER={{browser}} DEVICE={{device}} \
            {{PYTEST}} "$@" --update-snapshots {{PYTEST_OPTS}} --browser {{browser}} --color=yes
    else
        HEADLESS=true BROWSER={{browser}} DEVICE={{device}} \
            {{PYTEST}} {{PIXEL_TESTS_DIR}} --update-snapshots {{PYTEST_OPTS}} --browser {{browser}} --color=yes
    fi
    echo ""
    echo "✅ Snapshots updated for {{browser}}-{{device}}!"
    echo "📝 Review changes in: references/"
    echo "⚠️  Don't forget to commit: git add references/"
    echo "🧹 Cleaning Allure reports..."
    rm -rf {{ALLURE_RESULTS}}/ {{ALLURE_REPORT}}/

test-pixels-update-all: _check-root
    #!/usr/bin/env bash
    echo "📸 Updating snapshots for all browsers..."
    echo "🌐 Updating Chromium snapshots..."
    HEADLESS=true BROWSER=chromium DEVICE=desktop \
        {{PYTEST}} {{PIXEL_TESTS_DIR}} --update-snapshots {{PYTEST_OPTS}} --browser chromium
    echo ""
    echo "🌐 Updating WebKit snapshots..."
    HEADLESS=true BROWSER=webkit DEVICE=desktop \
        {{PYTEST}} {{PIXEL_TESTS_DIR}} --update-snapshots {{PYTEST_OPTS}} --browser webkit
    echo ""
    echo "✅ All snapshots updated!"
    echo "📝 Review changes in: references/"
    echo "⚠️  Don't forget to commit: git add references/"
    echo "🧹 Cleaning Allure reports..."
    rm -rf {{ALLURE_RESULTS}}/ {{ALLURE_REPORT}}/

# Download snapshots from GitHub Actions UI (simplified workflow)
# 1. Go to GitHub Actions > Pixel Tests workflow run
# 2. Download "references" artifact (contains combined snapshots from all browsers)
# 3. Extract ZIP to project root
# 4. Review and commit: git add references/ && git commit -m 'Update pixel test snapshots'

snapshots-clean: _check-root
    #!/usr/bin/env bash
    echo "🗑️  Cleaning snapshot failure artifacts..."
    rm -rf snapshot_failures/
    echo "✅ Cleaned successfully"

snapshots-clean-all: _check-root
    #!/usr/bin/env bash
    echo "🗑️  Cleaning ALL snapshots (failures + references)..."
    rm -rf snapshot_failures/ references/
    echo "✅ Cleaned successfully"

# ============================================================================
# DEVICE-SPECIFIC TEST COMMANDS
# ============================================================================
# Все команды автоматически добавляют device информацию в отчеты:
# - Allure: labels (device, viewport)
# - HTML: Environment таблица + колонки (Device, Viewport)
# - JUnit XML: properties (device, viewport) для GitHub Actions
# - Trace: title, HTTP headers, metadata

test-desktop: _check-root
    @echo "🖥️  Running tests on desktop..."
    DEVICE=desktop {{PYTEST_BASE}}

test-mobile: _check-root
    @echo "📱 Running tests on mobile..."
    DEVICE=mobile {{PYTEST_BASE}}

test-tablet: _check-root
    @echo "📱 Running tests on tablet..."
    DEVICE=tablet {{PYTEST_BASE}}

test-device device: _check-root
    @echo "📱 Running tests on device: {{device}}"
    DEVICE="{{device}}" {{PYTEST_BASE}}

test-all-devices: _check-root
    #!/usr/bin/env bash
    echo "📱 Running all devices on Chromium..."
    echo "🖥️  Testing desktop..."
    DEVICE=desktop {{PYTEST_BASE}} && \
    echo "📱 Testing mobile..." && \
    DEVICE=mobile {{PYTEST_BASE}} && \
    echo "📱 Testing tablet..." && \
    DEVICE=tablet {{PYTEST_BASE}} && \
    echo "✅ All devices tested successfully!"

# ============================================================================
# DEBUG & DEVELOPMENT
# ============================================================================
test-debug: _check-root
    @echo "🐛 Running tests in debug mode (headed browser)..."
    {{PYTEST_BASE}} --headed

tracing device test_file: _check-root
    #!/usr/bin/env bash
    echo "🔍 Running test with tracing enabled..."
    ENABLE_TRACING=true DEVICE={{device}} {{PYTEST}} {{test_file}} {{PYTEST_OPTS}} --browser {{PYTEST_BROWSER}}
    echo "✅ Trace saved. Check trace.zip file"

# ============================================================================
# CODE QUALITY
# ============================================================================
lint:
    @echo "🔍 Running linter (ruff)..."
    ruff check .
    @echo "✅ Linting completed"

format:
    @echo "✨ Formatting code with black and isort..."
    black .
    isort .
    @echo "✅ Code formatting completed"

clean:
    #!/usr/bin/env bash
    echo "🧹 Cleaning test artifacts..."
    find {{REPORTS_DIR}} -type f -delete 2>/dev/null || true
    rm -rf .ruff_cache/ .pytest_cache/
    rm -f trace.zip trace-*.zip
    rm -rf {{ALLURE_RESULTS}}/ {{ALLURE_REPORT}}/
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f \( -name "*.pyc" -o -name ".DS_Store" -o -name "*.pyo" -o -name "*.pyd" \) -delete 2>/dev/null || true
    echo "✅ Cleanup completed"

# ============================================================================
# ALLURE REPORTS
# ============================================================================
allure: _check-root
    #!/usr/bin/env bash
    echo "🌐 Opening Allure report..."
    allure serve {{ALLURE_RESULTS}}

allure-clean: _check-root
    #!/usr/bin/env bash
    echo "🧹 Cleaning Allure reports..."
    rm -rf {{ALLURE_RESULTS}}/ {{ALLURE_REPORT}}/ {{REPORTS_DIR}}junit.xml {{REPORTS_DIR}}failed_screenshots/*.png
    echo "✅ Allure reports cleaned"

allure-open: _check-root
    #!/usr/bin/env bash
    echo "🌐 Opening Allure report..."
    if [ -d "{{ALLURE_REPORT}}" ]; then
        allure open {{ALLURE_REPORT}}
    else
        echo "⚠️  Allure report not found. Generating from results..."
        allure generate {{ALLURE_RESULTS}} -o {{ALLURE_REPORT}} --clean
        allure open {{ALLURE_REPORT}}
    fi

# ============================================================================
# UTILITIES
# ============================================================================
health-check: _check-root
    @echo "🏥 Health Check - Environment Status"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo "🐍 Python version:"
    @{{PYTHON}} --version
    @echo "🧪 Pytest version:"
    @{{PYTEST}} --version
    @echo "🎭 Playwright version:"
    @{{VENV}}/bin/playwright --version
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo "✅ Health check completed"
