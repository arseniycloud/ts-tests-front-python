# Pixel Tests Guide

Visual regression testing с использованием [pytest-playwright-visual-snapshot](https://github.com/iloveitaly/pytest-playwright-visual-snapshot).

## Как это работает

### Принцип работы

1. **Референсы (baselines)** - эталонные скриншоты хранятся в `references/`
2. **При запуске теста** - делается скриншот и сравнивается с референсом
3. **При несовпадении** - тест падает, создаются diff-изображения в `snapshot_failures/`

### Формат именования

```
{browser}-{viewport}-{test_name}.png
```

Примеры:
- `chromium-desktop-test_header.png`
- `webkit-desktop-test_footer.png`

### Структура папок

```
references/
├── test_home_page_pixels/
│   ├── test_header/
│   │   ├── chromium-desktop-test_header.png
│   │   └── webkit-desktop-test_header.png
│   └── test_footer/
│       ├── chromium-desktop-test_footer.png
│       └── webkit-desktop-test_footer.png
└── test_login_page_pixels/
    └── ...

snapshot_failures/           # Создаётся при падении тестов
├── test_home_page_pixels/
│   └── test_header/
│       ├── actual_chromium-desktop-test_header.png    # Что получили
│       ├── expected_chromium-desktop-test_header.png  # Что ожидали
│       └── diff_chromium-desktop-test_header.png      # Различия (красным)
```

---

## Первоначальная настройка

### Шаг 1: Запустить тесты в CI

Референсы должны создаваться в CI, потому что Chrome/WebKit в CI отличаются от локальных версий.

```bash
# Push код и дождаться запуска workflow pixel-tests.yml
git push
```

Или запустить вручную: **Actions → Pixel Tests → Run workflow**

### Шаг 2: Скачать референсы из артефактов

```bash
just snapshots-download
```

Эта команда:
- Находит последний failed run workflow `pixel-tests.yml`
- Скачивает артефакты `test-results-chromium` и `test-results-webkit`
- Копирует референсы в `references/`

### Шаг 3: Закоммитить референсы

```bash
git add references/
git commit -m "Add pixel test baselines from CI"
git push
```

Теперь последующие запуски будут сравнивать с этими референсами.

---

## Локальная работа

### Запуск тестов

```bash
# Chromium (по умолчанию)
just test-pixels

# WebKit
just test-pixels browser=webkit

# Все браузеры
just test-pixels-all
```

### Обновление референсов локально

> ⚠️ **Не рекомендуется** - локальные браузеры отличаются от CI.
> Используйте только для быстрой проверки.

```bash
# Обновить Chromium референсы
just test-pixels-update

# Обновить WebKit референсы
just test-pixels-update browser=webkit

# Обновить все
just test-pixels-update-all
```

### Очистка

```bash
# Очистить только failures
just snapshots-clean

# Очистить всё (failures + references)
just snapshots-clean-all
```

---

## CI Workflow

### Когда запускается

- **По расписанию**: ежедневно в 01:00 MSK (22:00 UTC)
- **Вручную**: Actions → Pixel Tests → Run workflow

### Matrix

| Browser | Viewport |
|---------|----------|
| chromium | desktop (1280x720) |
| webkit | desktop (1280x720) |

### Логика артефактов

| Результат | Артефакты |
|-----------|-----------|
| ✅ Passed | Только `test-reports-{browser}` |
| ❌ Failed | `test-results-{browser}` (references + snapshot_failures) + reports |

**Почему так?**
По дизайну плагина артефакты со снапшотами нужны только при падении - чтобы скачать обновлённые референсы.

---

## Обновление референсов после изменений UI

### Сценарий: UI изменился намеренно

1. **Запустить тесты в CI** - они упадут (скриншоты изменились)

2. **Скачать новые референсы**:
   ```bash
   just snapshots-download
   ```

3. **Проверить diff-изображения** в `snapshot_failures/`:
   - `actual_*.png` - новый скриншот
   - `expected_*.png` - старый референс
   - `diff_*.png` - различия (красным)

4. **Если изменения корректны** - закоммитить:
   ```bash
   git add references/
   git commit -m "Update pixel baselines: [описание изменений]"
   git push
   ```

5. **Очистить failures**:
   ```bash
   just snapshots-clean
   ```

---

## Написание pixel тестов

### Пример теста

```python
import pytest
from playwright.sync_api import expect

@pytest.mark.pixel
@pytest.mark.pixel_test
class TestHomePageVisual:

    def test_header(self, page, assert_snapshot_with_threshold):
        page.goto("/")
        page.wait_for_load_state("networkidle")

        header = page.locator("header").first
        expect(header).to_be_visible()

        # Сравнение с референсом (threshold=15% допустимых различий)
        assert_snapshot_with_threshold(header, threshold=0.15)

    def test_full_page(self, page, assert_snapshot_with_threshold):
        page.goto("/")
        page.wait_for_load_state("networkidle")

        # Скриншот всей страницы
        assert_snapshot_with_threshold(
            page.screenshot(full_page=True),
            threshold=0.15
        )
```

### Доступные fixtures

| Fixture | Threshold | Описание |
|---------|-----------|----------|
| `assert_snapshot_with_threshold` | 0.1 (10%) | Стандартный, настраиваемый threshold |
| `assert_snapshot_strict` | 0.05 (5%) | Строгое сравнение |
| `assert_snapshot_lenient` | 0.2 (20%) | Мягкое сравнение |

### Маскирование динамических элементов

```python
def test_with_masks(self, page, assert_snapshot_with_threshold):
    page.goto("/profile")

    # Маскировать динамические элементы (дата, email, и т.д.)
    assert_snapshot_with_threshold(
        page,
        threshold=0.15,
        mask_elements=[
            ".user-avatar",
            "[data-testid='timestamp']",
            ".dynamic-content"
        ]
    )
```

---

## Troubleshooting

### Тесты падают с "New snapshot(s) created"

**Причина**: Референс не существует.

**Решение**: Первый запуск в CI создаст референсы. Скачайте и закоммитьте их:
```bash
just snapshots-download
git add references/
git commit -m "Add pixel baselines"
```

### Тесты падают с "Snapshots DO NOT match"

**Причина**: Скриншот отличается от референса.

**Решение**:
1. Проверьте `snapshot_failures/` - изучите diff-изображения
2. Если изменение намеренное - обновите референсы (см. выше)
3. Если баг - исправьте код

### Различия в размерах скриншотов

**Причина**: Элемент изменил размер.

**Решение**: Используется `--ignore-size-diff` флаг, diff всё равно генерируется.

### Локальные тесты проходят, CI падает

**Причина**: Браузеры в CI отличаются от локальных (шрифты, рендеринг).

**Решение**: Всегда используйте референсы созданные в CI:
```bash
just snapshots-download
```

---

## Полезные команды

```bash
# Запуск
just test-pixels                    # Chromium desktop
just test-pixels browser=webkit     # WebKit desktop
just test-pixels-all                # Все браузеры

# Обновление (локально)
just test-pixels-update             # Chromium
just test-pixels-update browser=webkit
just test-pixels-update-all

# CI референсы
just snapshots-download             # Скачать из CI

# Очистка
just snapshots-clean                # Только failures
just snapshots-clean-all            # Всё
```
