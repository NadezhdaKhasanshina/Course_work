from selenium.webdriver.common.by import By


class CartLocators:
    CART_ICON = (By.CSS_SELECTOR, ".view-cart")
    CART_TITLE = (By.CSS_SELECTOR, "span.current")
    CART_ITEM = (By.CSS_SELECTOR, "tr.cart_item")  # Строки с товарами
    ITEM_NAME = (By.CSS_SELECTOR, "td.product-name a")  # Названия товаров
    ITEM_EXTRAS = (By.CSS_SELECTOR, "dl.variation dd")  # Доп.опции (бортик)

    QUANTITY_INPUT = (By.CSS_SELECTOR, "input.qty")  # Поле количества
    UPDATE_BUTTON = (By.NAME, "update_cart")  # Кнопка обновления

    DELETE_BUTTON = (By.CSS_SELECTOR, "a.remove")
