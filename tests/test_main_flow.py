import allure
import time
from pages.main_page import MainPage


@allure.feature("Основной флоу клиента")
@allure.story("Главная страница и слайдер с пиццами")
class TestMenuFlow:
    @allure.title("TC-01: Отображение главной страницы")
    def test_main_page_loaded(self, browser):
        page = MainPage(browser)
        page.open_url()
        assert "Pizzeria" in browser.title

    @allure.title("TC-02: Наведение на пиццу в слайдере")
    def test_pizza(self, browser):
        page = MainPage(browser)
        page.open_url()
        assert page.hover_pizza()

    @allure.title("TC-03: Переключение слайдера")
    def test_slider_navigation(self, browser):
        page = MainPage(browser)
        page.open_url()
        time.sleep(5)
        page.click_next()
        page.click_prev()
        time.sleep(3)

    @allure.title("TC-04: Добавление пиццы в корзину")
    def test_add_pizza_to_cart(self, browser):
        page = MainPage(browser)
        page.open_url()
        page.hover_pizza()
        page.click_add_to_cart()
        page.product_added()

    @allure.title("TC-05: Просмотр деталей пиццы")
    def test_view_pizza_details(self, browser):
        page = MainPage(browser)
        page.open_url()
        page.hover_pizza()
        page.click_pizza_image()
        assert page.pizza_details_opened(), "Страница с описанием не открылась"