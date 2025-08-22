import allure
from pages.menu_page import MenuPage
import time
import random
from pages.cart_page import CartPage
from pages.auth_page import AuthPage


def generate_random_credentials():
    # Генерация уникальных данных для регистрации нового пользователя
    prefix = random.choice(["user", "test", "qa"])
    username = f"{prefix}_{random.randint(100, 999)}"
    email = f"{username}@example.com"
    password = f"Qwerty{random.randint(100, 999)}"
    return username, email, password


@allure.feature("Основной флоу клиента")
@allure.story("Оформление заказа и регистрация")
class TestAuthFlow:

    @allure.title("TC-13: Оформление заказа без авторизации")
    def test_checkout_without_auth(self, browser, preparing_cart):
        (preparing_cart['cart_page']
         .open_cart()
         .check_cart_title()
         .remove_item_by_index(1))
        menu_page = MenuPage(browser)
        (menu_page.select_desserts_from_menu().add_first_dessert())
        CartPage(browser).open_cart()
        auth_page = AuthPage(browser)
        (auth_page.proceed_to_payment().verify_auth_required())

    @allure.title("ТС-14: Регистрация нового пользователя")
    def test_user_registration(self, browser, preparing_cart):
        # Генерируем данные перед использованием
        username, email, password = generate_random_credentials()
        (preparing_cart['cart_page']
         .open_cart()
         .check_cart_title()
         .remove_item_by_index(1))
        menu_page = MenuPage(browser)
        (menu_page.select_desserts_from_menu().add_first_dessert())
        CartPage(browser).open_cart()
        auth_page = AuthPage(browser)
        (auth_page.proceed_to_payment()
         .go_to_auth_page().click_register_button()
         .fill_registration_form(username, email, password)
         .submit_registration())
        time.sleep(1)
        auth_page.go_to_auth_page()
        auth_page.verify_successful_registration(username)
        time.sleep(1)

    @allure.title("TC-15: Оформление заказа после регистрации с доставкой на завтра")
    def test_complete_order_after_registration(self, browser, preparing_cart):
        # Генерируем данные перед использованием
        username, email, password = generate_random_credentials()
        (preparing_cart['cart_page']
         .open_cart())
        menu_page = MenuPage(browser)
        (menu_page.select_desserts_from_menu().add_first_dessert())
        auth_page = AuthPage(browser)
        (auth_page.go_to_auth_page().click_register_button()
         .fill_registration_form(username, email, password)
         .submit_registration())
        time.sleep(1)
        CartPage(browser).open_cart()
        (auth_page.proceed_to_payment()
         .fill_delivery_details(
            first_name="Иван",
            last_name="Иванов",
            address="ул. Ленина, д. 10, кв. 5",
            city="Москва",
            region="Московская область",
            postcode="101000",
            phone="+79123456789")

         .select_tomorrow_delivery()
         .select_cash_on_delivery()
         .accept_terms())
        time.sleep(3)
        (auth_page.place_order()
         .verify_order_confirmation(email=email))

        # Пауза для визуальной проверки
        time.sleep(3)
