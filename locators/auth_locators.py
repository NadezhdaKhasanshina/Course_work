from selenium.webdriver.common.by import By


class AuthLocators:
    PAYMENT_BTN = (By.CSS_SELECTOR, "a.checkout-button")
    LOGIN_PROMPT = (By.CSS_SELECTOR, "div.woocommerce-info")

    MY_ACCOUNT = (By.CSS_SELECTOR, "li.menu-item-30 > a")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button.custom-register-button")
    # Поле имени пользователя для регистрации
    REG_USERNAME = (By.ID, "reg_username")
    REG_EMAIL = (By.ID, "reg_email")  # Поле email
    REG_PASSWORD = (By.ID, "reg_password")  # Поле пароля для регистрации
    REGISTER_BTN = (By.CSS_SELECTOR, "button[name='register']")

    # Локаторы для оформления заказа
    BILLING_FIRST_NAME = (By.ID, "billing_first_name")
    BILLING_LAST_NAME = (By.ID, "billing_last_name")
    BILLING_ADDRESS = (By.ID, "billing_address_1")
    BILLING_CITY = (By.ID, "billing_city")
    BILLING_STATE = (By.ID, "billing_state")
    BILLING_POSTCODE = (By.ID, "billing_postcode")
    BILLING_PHONE = (By.ID, "billing_phone")
    BILLING_EMAIL = (By.ID, "billing_email")
    ORDER_DATE = (By.ID, "order_date")
    PAYMENT_CASH = (By.ID, "payment_method_cod")
    PLACE_ORDER_BTN = (By.ID, "place_order")
    CHECKBOX_AGREEMENT = (By.ID, "terms")

    # Локаторы для авторизации
    LOGIN_USERNAME = (By.ID, "username")
    LOGIN_PASSWORD = (By.ID, "password")  # Поле пароля для авторизации
    LOGIN_BUTTON = (By.NAME, "login")
