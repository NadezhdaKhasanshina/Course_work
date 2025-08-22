import allure
from pages.coupon_page import CouponPage
from pages.auth_page import AuthPage
from pages.cart_page import CartPage
from pages.main_page import MainPage
import time


@allure.feature("Флоу с кодом купона")
class TestCouponFlow:
    @allure.story("Успешное применение купона")
    @allure.title("TC-16: Применение валидного кода купона")
    def test_valid_coupon(self, browser, preparing_cart):
        coupon_page = CouponPage(browser)
        # Перейти в корзину
        preparing_cart['cart_page'].open_cart()

        # Получить исходную сумму заказа
        original_total = coupon_page.get_original_total()
        allure.attach(
            f"Исходная сумма: {original_total}₽",
            name="Original Total")

        # Ввести код купона GIVEMEHALYAVA и применить
        (coupon_page
         .enter_coupon("GIVEMEHALYAVA")
         .apply_coupon())
        # Получить данные после применения купона
        discount_amount = coupon_page.get_discount_amount()
        final_total = coupon_page.get_final_total()

        # Добавляем вложения в отчет
        allure.attach(
            f"Сумма скидки: {discount_amount}₽",
            name="Discount Amount")
        allure.attach(f"Итоговая сумма: {final_total}₽", name="Final Total")

        # Проверить применение скидки 10%
        coupon_page.verify_discount(
            original_total, discount_amount, final_total)

    @allure.story("Неуспешное применение купона")
    @allure.title("TC-17: Применение невалидного кода купона")
    def test_invalid_coupon(self, browser, preparing_cart):
        coupon_page = CouponPage(browser)
        preparing_cart['cart_page'].open_cart()
        original_total = coupon_page.get_original_total()
        allure.attach(
            f"Исходная сумма: {original_total}₽",
            name="Original Total")

        # Ввести код купона DC120 и применить
        (coupon_page
         .enter_coupon("DC120")
         .apply_coupon())

        # Проверить сообщение об ошибке
        coupon_page.verify_error_message("DC120")

        # Проверить что суммы не изменились
        final_total = coupon_page.get_final_total()
        allure.attach(f"Итоговая сумма: {final_total}₽", name="Final Total")

    @allure.story("Неуспешное применение купона")
    @allure.title("TC-18: Повторное применение купона")
    def test_reuse_coupon(self, browser, preparing_cart):
        coupon_page = CouponPage(browser)
        auth_page = AuthPage(browser)
        preparing_cart['cart_page'].open_cart()
        (auth_page.go_to_auth_page()
         .fill_login_form("qweqwe123", "123")
         .submit_login())
        CartPage(browser).open_cart()
        coupon_page.enter_coupon("GIVEMEHALYAVA").apply_coupon()
        (auth_page.proceed_to_payment())
        time.sleep(3)
        auth_page.accept_terms()
        auth_page.place_order()
        main_page = MainPage(browser)
        main_page.open_url()
        main_page.hover_pizza()
        main_page.click_add_to_cart()
        CartPage(browser).open_cart()
        coupon_page.enter_coupon("GIVEMEHALYAVA").apply_coupon()
        coupon_page.verify_coupon_field("GIVEMEHALYAVA")

    @allure.story("Неуспешное применение купона")
    @allure.title("TC-19: Применение купона при ошибке сервера")
    def test_valid_coupon_server_error(self, browser, preparing_cart):
        coupon_page = CouponPage(browser)
        # Перейти в корзину
        preparing_cart['cart_page'].open_cart()

        # Получить исходную сумму заказа
        original_total = coupon_page.get_original_total()
        allure.attach(
            f"Исходная сумма: {original_total}₽",
            name="Original Total")

        try:
            # Включаем управление сетью
            browser.execute_cdp_cmd('Network.enable', {})

            # Блокируем запросы apply_coupon
            browser.execute_cdp_cmd('Network.setBlockedURLs', {
                'urls': ['*apply_coupon*', '*wc-ajax=apply_coupon*']
            })

            allure.attach(
                "Заблокированы запросы apply_coupon",
                name="Requests Blocked")

        except Exception as e:
            allure.attach(
                f"Не удалось настроить блокировку: {
                    str(e)}", name="CDP Warning")

        (coupon_page
         .enter_coupon("GIVEMEHALYAVA")
         .apply_coupon())
        coupon_page.verify_coupon_not_applied("GIVEMEHALYAVA")
