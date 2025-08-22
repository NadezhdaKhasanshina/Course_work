from selenium.webdriver.common.by import By


class MainPageLocators:
    PIZZA_SLIDER = (By.CSS_SELECTOR, ".prod1-slider")
    PIZZA_ITEM = (
        By.CSS_SELECTOR,
        '#accesspress_store_product-5 li:nth-child(6)')
    ADD_TO_CART_BUTTON = (
        By.CSS_SELECTOR,
        "#accesspress_store_product-5 li:nth-child(6) .add_to_cart_button")
    NEXT_BUTTON = (By.CSS_SELECTOR, ".slick-next")  # Вправо
    PREV_BUTTON = (By.CSS_SELECTOR, ".slick-prev")  # Влево
    PIZZA_IMAGE = (
        By.CSS_SELECTOR,
        '#accesspress_store_product-5 li:nth-child(6) img')
    DETAILS_TITLE = (By.CSS_SELECTOR, "h1.product_title")
