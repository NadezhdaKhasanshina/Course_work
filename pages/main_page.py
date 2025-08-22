import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    @allure.step("Открыть домашнюю страницу")
    def open_url(self):
        self.browser.get('https://pizzeria.skillbox.cc/')

    @allure.step("Навести курсор на пиццу и проверить кнопку 'В корзину'")
    def hover_pizza(self):
        # Прокручиваем к слайдеру (если он не в зоне видимости)
        self.wait.until(
            EC.presence_of_element_located(MainPageLocators.PIZZA_SLIDER))

        # Находим карточку пиццы и наводим курсор
        pizza_item = self.wait.until(
            EC.element_to_be_clickable(MainPageLocators.PIZZA_ITEM)
        )
        ActionChains(self.browser).move_to_element(
            pizza_item).pause(1).perform()

        # Ждём появления кнопки "В корзину"
        self.wait.until(
            EC.visibility_of_element_located(
                MainPageLocators.ADD_TO_CART_BUTTON)
        )
        return self

    @allure.step("Кликнуть стрелку 'Вправо'")
    def click_next(self):
        next_btn = self.wait.until(
            EC.presence_of_element_located(MainPageLocators.NEXT_BUTTON))
        # Наводим курсор и кликаем
        ActionChains(self.browser).move_to_element(
            next_btn).pause(0.5).click().perform()

    @allure.step("Кликнуть стрелку 'Влево'")
    def click_prev(self):
        prev_btn = self.wait.until(
            EC.presence_of_element_located(MainPageLocators.PREV_BUTTON))
        # Наводим курсор и кликаем
        ActionChains(self.browser).move_to_element(
            prev_btn).pause(0.5).click().perform()

    @allure.step("Нажать 'В корзину'")
    def click_add_to_cart(self):
        self.wait.until(
            EC.element_to_be_clickable(
                MainPageLocators.ADD_TO_CART_BUTTON)).click()
        return self

    @allure.step("Проверить обновление корзины")
    def product_added(self):
        # Проверяем, что кнопка "В корзину" стала "добавленной"
        add_button = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a.ajax_add_to_cart.added"))
        )
        assert "added" in add_button.get_attribute(
            "class"), "Товар не добавился в корзину"
        # Ищем кнопку "Подробнее" и проверяем её текст
        view_cart_button = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "a.added_to_cart.wc-forward"))
        )
        assert "Подробнее" in view_cart_button.get_attribute(
            "title"), "Неверный title кнопки"
        return True

    @allure.step("Нажать на картинку")
    def click_pizza_image(self):
        self.wait.until(
            EC.element_to_be_clickable(
                MainPageLocators.PIZZA_IMAGE)).click()
        self.wait.until(
            EC.url_contains("/product/"))
        return self

    @allure.step("Проверить, что страница с описанием пиццы открыта")
    def pizza_details_opened(self):
        # Проверка заголовка
        details_title = self.wait.until(
            EC.visibility_of_element_located(
                MainPageLocators.DETAILS_TITLE))
        assert details_title.is_displayed(), "Заголовок не отображается"
        return True

    @allure.step("Получить название пиццы")
    def get_pizza_name(self):
        element = self.wait.until(
            EC.visibility_of_element_located(MainPageLocators.PIZZA_ITEM)
        )
        # Получаем title из первой ссылки внутри элемента
        return element.find_element(By.TAG_NAME, "a").get_attribute("title")
