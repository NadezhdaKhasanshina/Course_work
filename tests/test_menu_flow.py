import allure
from pages.menu_page import MenuPage
from pages.main_page import MainPage


@allure.feature("Основной флоу клиента")
@allure.story("Выбор десерта")
class TestDessertSelection:
    @allure.title("TC-10: Выбор раздела Десерты во вкладке Меню")
    def test_select_section(self, browser, preparing_cart):
        (preparing_cart['cart_page']
         .open_cart()
         .check_cart_title()
         .remove_item_by_index(1))
        # Переходим в меню дессертов
        menu_page = MenuPage(browser)
        menu_page.select_desserts_from_menu()
        menu_page.check_desserts_title()

    @allure.title("TC-11: Установить фильтр цены")
    def test_set_max_price(self, browser, preparing_cart):
        (preparing_cart['cart_page']
         .open_cart()
         .check_cart_title()
         .remove_item_by_index(1))
        menu_page = MenuPage(browser)
        (menu_page.select_desserts_from_menu()
         .set_max_price()
         .apply_filter()
         .verify_price_filter(135))

    @allure.title("TC-12: Добавление первого десерта в корзину")
    def test_add_dessert_to_cart(self, browser, preparing_cart):
        (preparing_cart['cart_page']
         .open_cart()
         .check_cart_title()
         .remove_item_by_index(1))
        menu_page = MenuPage(browser)
        main_page = MainPage(browser)
        (menu_page.select_desserts_from_menu()
         .set_max_price()
         .apply_filter()
         .add_first_dessert())
        main_page.product_added()
