import pytest
from selenium import webdriver
from pages.main_page import MainPage
from pages.pizza_page import PizzaPage
from pages.cart_page import CartPage
import time

@pytest.fixture(scope='function')
def browser():
    options = webdriver.ChromeOptions()             #в options складываем все настройки Chrome
    #options.add_argument("--headless")             #что бы тести были без визуалки
    browser = webdriver.Chrome(options=options)     #Указываем что будем использовать Chrome и его настройки options
    browser.maximize_window()                       #открыть браузер в полное окно
    yield browser                                   #остановка браузера
    browser.quit()

@pytest.fixture
def preparing_cart(browser):
    """Фикстура подготовливает корзину"""
    main_page = MainPage(browser)
    pizza_page = PizzaPage(browser)
    main_page.open_url()
    main_page.hover_pizza()
    first_pizza_name = main_page.get_pizza_name()
    main_page.click_add_to_cart()
    pizza_page.hover_second_pizza()
    second_pizza_name = pizza_page.get_second_pizza_name()
    pizza_page.click_second_pizza_image()
    pizza_page.select_cheese_border()
    pizza_page.add_pizza_with_cheese_border_to_cart()
    time.sleep(1)
    return {
        'cart_page': CartPage(browser),
        'first_pizza_name': first_pizza_name,
        'second_pizza_name': second_pizza_name
    }
