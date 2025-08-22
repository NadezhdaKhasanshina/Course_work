import allure
from pages.main_page import MainPage
from pages.pizza_page import PizzaPage
import time


@allure.feature("Основной флоу клиента")
@allure.story("Дополнительные опции пиццы")
class TestPizzaOptions:
    @allure.title("TC-06: Выбор сырного борта")
    def test_add_pizza_with_cheese_border(self, browser):
        # Инициализируем страницы
        main_page = MainPage(browser)
        pizza_page = PizzaPage(browser)

        # Добавляем первую пиццу
        main_page.open_url()
        main_page.hover_pizza()
        main_page.click_add_to_cart()

        pizza_page.hover_second_pizza()
        pizza_page.click_second_pizza_image()

        # Выбираем сырный бортик
        pizza_page.select_cheese_border()
        time.sleep(2)

        # Добавляем в корзину
        pizza_page.add_pizza_with_cheese_border_to_cart()
        time.sleep(3)
        # Проверяем сброс выбора
        pizza_page.check_border_reset()
