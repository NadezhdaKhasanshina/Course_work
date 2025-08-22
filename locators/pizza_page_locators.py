from selenium.webdriver.common.by import By


class PizzaPageLocators:
    SECOND_PIZZA_ITEM = (
        By.CSS_SELECTOR,
        '#accesspress_store_product-5 li:nth-child(5)')
    SECOND_PIZZA_IMAGE = (
        By.CSS_SELECTOR,
        '#accesspress_store_product-5 li:nth-child(5) img')
    BORDER_SELECT = (By.CSS_SELECTOR, "select[name='board_pack']")
    ADD_TO_CART_BUTTON_SINGLE = (
        By.CSS_SELECTOR,
        'button.single_add_to_cart_button')
