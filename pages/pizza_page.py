import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from locators.pizza_page_locators import PizzaPageLocators
from pages.base_page import BasePage


class PizzaPage(BasePage):
    @allure.step("Навести курсор на вторую пиццу")
    def hover_second_pizza(self):
        second_pizza = self.wait.until(
            EC.element_to_be_clickable(PizzaPageLocators.SECOND_PIZZA_ITEM)
        )
        ActionChains(self.browser).move_to_element(
            second_pizza).pause(1).perform()
        return self

    @allure.step("Нажать на картинку")
    def click_second_pizza_image(self):
        self.wait.until(
            EC.element_to_be_clickable(
                PizzaPageLocators.SECOND_PIZZA_IMAGE)).click()
        self.wait.until(
            EC.url_contains("/product/"))
        return self

    @allure.step("Выбрать сырный бортик")
    def select_cheese_border(self):
        border_select = self.wait.until(
            EC.presence_of_element_located(PizzaPageLocators.BORDER_SELECT))

        select = Select(border_select)

        # Выбираем опцию по видимому тексту
        select.select_by_visible_text("Сырный - 55.00 р.")

    @allure.step("Добавить пиццу с сырным бортиком в корзину")
    def add_pizza_with_cheese_border_to_cart(self):
        self.wait.until(
            EC.element_to_be_clickable(
                PizzaPageLocators.ADD_TO_CART_BUTTON_SINGLE)
        ).click()
        return self

    @allure.step("Проверить сброс выбора бортика")
    def check_border_reset(self):
        select = self.wait.until(
            EC.presence_of_element_located(PizzaPageLocators.BORDER_SELECT)
        )
        selected_option = Select(select).first_selected_option
        assert selected_option.text == "Обычный", "Выбор бортика не сбросился"
        return True

    @allure.step("Получить название второй пиццы")
    def get_second_pizza_name(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                PizzaPageLocators.SECOND_PIZZA_ITEM)
        )
        # Получаем title из второй ссылки внутри элемента
        return element.find_element(By.TAG_NAME, "a").get_attribute("title")
