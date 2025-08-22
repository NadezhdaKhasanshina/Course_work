from selenium.webdriver.common.by import By


class BonusLocators:
    # Страница бонусной программы
    BONUS_PAGE = (By.CSS_SELECTOR, "li.menu-item-363 > a")

    # Форма регистрации
    BONUS_NAME = (By.NAME, "username")
    BONUS_PHONE = (By.ID, "bonus_phone")
    BONUS_BUTTON = (By.CSS_SELECTOR, "button[name='bonus']")

    PHONE_ERROR = (By.ID, "bonus_content")
