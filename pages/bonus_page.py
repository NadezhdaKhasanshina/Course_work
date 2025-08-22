import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.bonus_locators import BonusLocators
from pages.base_page import BasePage


class BonusPage(BasePage):
    @allure.step("Перейти на страницу бонусной программы")
    def open_bonus_page(self):
        self.browser.find_element(*BonusLocators.BONUS_PAGE).click()
        return self

    @allure.step("Заполнить поля имя и телефон")
    def fill_bonus_field(self, name: str, phone: str):
        self.browser.find_element(*BonusLocators.BONUS_NAME).send_keys(name)
        self.browser.find_element(*BonusLocators.BONUS_PHONE).send_keys(phone)
        return self

    @allure.step("Отправить форму регистрации")
    def submit_form(self):
        # Нажимает кнопку Оформить карту
        self.wait.until(
            EC.element_to_be_clickable(
                BonusLocators.BONUS_BUTTON)).click()
        return self

    @allure.step("Проверить успешное оформление карты")
    def verify_success_registration(self):
        # Проверяет alert с сообщением об успешной отправке заявки
        try:
            # Ждем появления alert
            WebDriverWait(self.browser, 10).until(EC.alert_is_present())

            # Переключаемся на alert
            alert = self.browser.switch_to.alert
            alert_text = alert.text

            # Проверяем текст alert
            assert "Заявка отправлена" in alert_text, f"Ожидалось 'Заявка отправлена', а получено: {alert_text}"

            # Принимаем alert (нажимаем OK)
            alert.accept()

            allure.attach(
                f"Успешная регистрация: {alert_text}",
                name="Registration Success")
            return True

        except Exception as e:
            allure.attach(
                "Не появилось alert-окно с подтверждением",
                name="Alert Missing")
            raise AssertionError(f"Регистрация не прошла успешно: {str(e)}")

    @allure.step("Проверить ошибку валидации телефона")
    def verify_invalid_phone(self):
        try:
            phone_error = self.wait.until(
                EC.visibility_of_element_located(BonusLocators.PHONE_ERROR))
            error_text = phone_error.text.strip()
            expected_error = "Введен неверный формат телефона"
            assert expected_error in error_text, f"Ожидалась ошибка '{expected_error}', а получено: '{error_text}'"
            allure.attach(
                f"Ошибка валидации телефона: {error_text}",
                name="Phone Validation Error")
            return self
        except Exception:
            allure.attach(
                "Не найдена ошибка валидации телефона",
                name="No Phone Error")
            raise AssertionError(
                "Ожидалась ошибка 'Введен неверный формат телефона'")
