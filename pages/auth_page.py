import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from locators.auth_locators import AuthLocators
from datetime import datetime, timedelta


class AuthPage(BasePage):
    @allure.step("Перейти к оплате")
    def proceed_to_payment(self):
        self.browser.find_element(*AuthLocators.PAYMENT_BTN).click()
        return self

    @allure.step("Проверить запрос авторизации")
    def verify_auth_required(self):
        prompt = self.wait.until(
            EC.visibility_of_element_located(AuthLocators.LOGIN_PROMPT)
        ).text
        assert "авторизуйтесь" in prompt.lower(), "Не появился запрос на авторизацию"
        return self

    @allure.step("Перейти в 'Мой аккаунт'")
    def go_to_auth_page(self):
        self.browser.find_element(*AuthLocators.MY_ACCOUNT).click()
        return self

    @allure.step("Перейти к регистрации")
    def click_register_button(self):
        self.wait.until(
            EC.element_to_be_clickable(
                AuthLocators.REGISTER_BUTTON)).click()
        return self

    @allure.step("Заполнить форму регистрации")
    def fill_registration_form(self, username: str, email: str, password: str):
        self.wait.until(EC.visibility_of_element_located(
            AuthLocators.REG_USERNAME)).send_keys(username)
        self.wait.until(
            EC.visibility_of_element_located(
                AuthLocators.REG_EMAIL)).send_keys(email)
        self.wait.until(EC.visibility_of_element_located(
            AuthLocators.REG_PASSWORD)).send_keys(password)
        return self

    @allure.step("Нажать кнопку регистрации")
    def submit_registration(self):
        self.wait.until(
            EC.element_to_be_clickable(
                AuthLocators.REGISTER_BTN)).click()
        return self

    @allure.step("Проверить успешную регистрацию")
    def verify_successful_registration(self, username=None):
        # Проверяем приветствие с именем пользователя
        WELCOME_MSG = (
            By.XPATH,
            f"//p[contains(., 'Привет') and contains(., '{username}')]")
        self.wait.until(EC.visibility_of_element_located(WELCOME_MSG))
        allure.attach(
            self.browser.get_screenshot_as_png(),
            name="registration_result",
            attachment_type=allure.attachment_type.PNG
        )
        return self

    @allure.step("Заполнить данные доставки")
    def fill_delivery_details(self, first_name: str, last_name: str, address: str,
                              city: str, region: str, postcode: str, phone: str):
        # Заполняем все обязательные поля
        self.wait.until(
            EC.visibility_of_element_located(
                AuthLocators.BILLING_FIRST_NAME))
        self.browser.find_element(
            *AuthLocators.BILLING_FIRST_NAME).send_keys(first_name)
        self.browser.find_element(
            *AuthLocators.BILLING_LAST_NAME).send_keys(last_name)
        self.browser.find_element(
            *AuthLocators.BILLING_ADDRESS).send_keys(address)
        self.browser.find_element(*AuthLocators.BILLING_CITY).send_keys(city)
        self.browser.find_element(
            *AuthLocators.BILLING_STATE).send_keys(region)
        self.browser.find_element(
            *AuthLocators.BILLING_POSTCODE).send_keys(postcode)
        self.browser.find_element(*AuthLocators.BILLING_PHONE).send_keys(phone)

        return self

    @allure.step("Выбрать оплату при доставке")
    def select_cash_on_delivery(self):
        self.wait.until(
            EC.element_to_be_clickable(
                AuthLocators.PAYMENT_CASH)).click()
        return self

    @allure.step("Принять условия соглашения")
    def accept_terms(self):
        # Проверяем подтверждение
        checkbox = self.wait.until(
            EC.visibility_of_element_located(
                AuthLocators.CHECKBOX_AGREEMENT))
        if not checkbox.is_selected():
            checkbox.click()
        return self

    @allure.step("Выбрать дату доставки - завтра")
    def select_tomorrow_delivery(self):
        self.tomorrow_date = (
            datetime.now() +
            timedelta(
                days=1)).strftime("%d.%m.%Y")
        self.browser.find_element(*AuthLocators.ORDER_DATE).clear()
        self.browser.find_element(
            *
            AuthLocators.ORDER_DATE).send_keys(
            self.tomorrow_date)
        return self

    @allure.step("Подтвердить заказ")
    def place_order(self):
        self.wait.until(
            EC.element_to_be_clickable(
                AuthLocators.PLACE_ORDER_BTN)).click()
        return self

    @allure.step("Проверить подтверждение заказа")
    def verify_order_confirmation(
            self, email, payment_method="Оплата при доставке"):
        # Проверяем заголовок/сообщение о успешном заказе
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,
             "//p[contains(@class, 'woocommerce-notice') and contains(., 'Ваш заказ был получен')]")
        ))

        # Проверяем email
        email_element = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//li[contains(., 'Почта:')]/strong")))
        assert email.lower() in email_element.text.lower(
        ), f"Email не совпадает. Ожидалось: {email}, Фактически: {email_element.text}"

        # Проверяем метод оплаты
        payment_element = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//li[contains(., 'Метод оплаты:')]/strong")))
        assert payment_method in payment_element.text, f"Метод оплаты не совпадает. Ожидалось: {payment_method}, Фактически: {
            payment_element.text}"

        # Проверяем дату (должна быть завтра)

        date_element = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//li[contains(., 'Дата:')]/strong")))
        assert self.tomorrow_date in date_element.text, f"Дата доставки не совпадает. Ожидалось: {
            self.tomorrow_date}, Фактически: {
            date_element.text}"
        # Добавляем скриншот в отчет
        allure.attach(
            self.browser.get_screenshot_as_png(),
            name="order_confirmation_details",
            attachment_type=allure.attachment_type.PNG
        )
        return self

    @allure.step("Авторизоваться пользователем qweqwe123")
    def fill_login_form(self, username: str, password: str):
        # Заполняет поля логина и пароля
        self.wait.until(EC.visibility_of_element_located(
            AuthLocators.LOGIN_USERNAME)).send_keys(username)
        self.wait.until(EC.visibility_of_element_located(
            AuthLocators.LOGIN_PASSWORD)).send_keys(password)
        return self

    @allure.step("Нажать кнопку входа")
    def submit_login(self):
        self.wait.until(
            EC.element_to_be_clickable(
                AuthLocators.LOGIN_BUTTON)).click()
        return self
