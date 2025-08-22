import allure
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.coupon_locators import CouponLocators
import time


class CouponPage(BasePage):

    @allure.step("Получить исходную сумму заказа")
    def get_original_total(self):
        # Получает сумму из поля 'Общая стоимость'
        subtotal = self.wait.until(
            EC.visibility_of_element_located(CouponLocators.CART_TOTAL)
        )
        return self._parse_price(subtotal.text)

    @allure.step("Ввести код купона '{coupon}'")
    def enter_coupon(self, coupon):
        # Находит поле, кликает и вводит код купона
        coupon_field = self.wait.until(
            EC.element_to_be_clickable(CouponLocators.COUPON_INPUT))
        coupon_field.click()
        coupon_field.clear()
        coupon_field.send_keys(coupon)
        return self

    @allure.step("Применить купон")
    def apply_coupon(self):
        # Находит кнопку и нажимает для применения купона
        apply_button = self.wait.until(
            EC.element_to_be_clickable(CouponLocators.APPLY_COUPON_BUTTON))
        apply_button.click()
        # Ждем применения купона
        time.sleep(2)
        return self

    @allure.step("Проверить применение скидки 10%")
    def verify_discount(self, original_total, discount_amount, final_total, coupon="GIVEMEHALYAVA"):
        # Проверяем название купона
        coupon_label = self.wait.until(
            EC.visibility_of_element_located(CouponLocators.COUPON_LABEL)
        )
        assert coupon.upper() in coupon_label.text, \
            f"Ожидался купон {coupon}, найден: {coupon_label.text}"

        # Проверяем что скидка составляет 10%
        expected_discount = round(original_total * 0.1, 2)
        assert abs(discount_amount - expected_discount) < 0.01, \
            f"Ожидалась скидка {expected_discount}₽ (10%), получено {discount_amount}₽"

        # Проверяем итоговую сумму
        expected_final = round(original_total - expected_discount, 2)
        assert abs(final_total - expected_final) < 0.01, \
            f"Ожидалась итоговая сумма {expected_final}₽, получено {final_total}₽"

        return self

    @allure.step("Получить сумму скидки")
    def get_discount_amount(self):
        # Получает сумму скидки из поля купона
        try:
            discount_element = self.wait.until(
                EC.visibility_of_element_located(CouponLocators.COUPON_AMOUNT))
            return self._parse_price(discount_element.text)
        except:
            return 0.0

    @allure.step("Получить итоговую сумму")
    def get_final_total(self):
        # Получает итоговую сумму после скидки
        total_element = self.wait.until(
            EC.visibility_of_element_located(CouponLocators.ORDER_TOTAL))
        return self._parse_price(total_element.text)

    def _parse_price(self, price_text):
        # Парсит цену из текста
        try:
            cleaned = price_text.replace('₽', '').replace('P', '').replace(' ', '').replace(',', '.')
            return float(cleaned)
        except ValueError:
            return 0.0

    @allure.step("Проверить сообщение об ошибке для купона '{coupon}'")
    def verify_error_message(self, coupon):
        # Проверяет что появилось сообщение об ошибке применения купона
        error_message = self.wait.until(
            EC.visibility_of_element_located(CouponLocators.ERROR_MESSAGE))

        # Добавляем в отчет найденное сообщение
        allure.attach(f"Сообщение об ошибке: {error_message.text}", name="Error Message")

        # Проверяем что сообщение содержит ожидаемый текст
        expected_texts = ["неверный купон."]
        message_lower = error_message.text.lower()

        has_error = any(text in message_lower for text in expected_texts)
        assert has_error, f"Ожидалось сообщение об ошибке для купона {coupon}, получено: {error_message.text}"

    @allure.step("Проверить, что купон не применился повторно")
    def verify_coupon_field(self, coupon_code="GIVEMEHALYAVA"):
        self.wait.until(EC.visibility_of_element_located(CouponLocators.COUPON_ROW))
        raise AssertionError(f"Купон '{coupon_code}' применился повторно! Найдена строка купона.")

    @allure.step("Проверить, что купон НЕ применился")
    def verify_coupon_not_applied(self, coupon_code="GIVEMEHALYAVA"):
        # Проверяет что строка с купоном НЕ появилась (для ошибок сервера)
        try:
            # Ждем немного чтобы убедиться
            self.wait.until(EC.visibility_of_element_located(CouponLocators.COUPON_ROW))
            raise AssertionError(f"Купон '{coupon_code}' применился несмотря на ошибку")

        except TimeoutException:
            allure.attach(f"Купон '{coupon_code}' не применился - сервер недоступен",
                          name="Coupon Not Applied")
            return True
