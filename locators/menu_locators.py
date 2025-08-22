from selenium.webdriver.common.by import By


class MenuLocators:
    # Основное меню
    MENU_BUTTON = (
        By.CSS_SELECTOR,
        "li.menu-item-has-children > a[href*='product-category/menu']")
    DROPDOWN = (By.CSS_SELECTOR, "ul.sub-menu")
    DESSERTS_TAB = (By.XPATH, "//a[contains(text(), 'Десерты')]")
    DESSERTS_TITLE = (By.XPATH, "//h1[contains(text(), 'Десерты')]")

    # Фильтры
    MAX_PRICE_INPUT = (
        By.CSS_SELECTOR,
        ".ui-slider-handle:last-child")  # Поле "Макс. цена"
    APPLY_FILTER_BTN = (
        By.XPATH,
        # Кнопка "Применить"
        "//button[@type='submit' and contains(@class, 'button') and text()='Применить']")
    PRICE_AMOUNT = (By.CSS_SELECTOR, ".product .price .amount")

    # Десерты
    ADD_FIRST_DESSERT_BTN = (By.CSS_SELECTOR,
                             "li.product:first-child a.add_to_cart_button")
