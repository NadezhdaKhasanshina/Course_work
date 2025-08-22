from selenium.webdriver.common.by import By


class CouponLocators:
    # Элементы сумм
    CART_TOTAL = (
        By.CSS_SELECTOR,
        "tr.cart-subtotal span.woocommerce-Price-amount.amount")  # Общая стоимость

    # Поле ввода купона
    COUPON_INPUT = (By.ID, "coupon_code")

    # Кнопка применения купона
    APPLY_COUPON_BUTTON = (By.NAME, "apply_coupon")

    COUPON_ROW = (By.CSS_SELECTOR, "tr.cart-discount")  # Строка с купоном
    COUPON_LABEL = (By.CSS_SELECTOR, "tr.cart-discount th")  # Название купона
    COUPON_AMOUNT = (
        By.CSS_SELECTOR,
        "tr.cart-discount td span.woocommerce-Price-amount.amount")  # Сумма скидки
    ORDER_TOTAL = (
        By.CSS_SELECTOR,
        "tr.order-total span.woocommerce-Price-amount.amount")  # Итоговая сумма

    # Сообщения
    ERROR_MESSAGE = (By.CLASS_NAME, "woocommerce-error")
