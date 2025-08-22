import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from locators.menu_locators import MenuLocators
from pages.base_page import BasePage
import time


class MenuPage(BasePage):
    @allure.step("Открыть меню и выбрать раздел 'Десерты'")
    def select_desserts_from_menu(self):
        # Скроллим в самый верх
        self.browser.find_element(By.TAG_NAME, 'html').send_keys(Keys.HOME)
        time.sleep(1)

        # Находим элемент меню и наводим курсор (одно действие)
        menu_button = self.wait.until(
            EC.element_to_be_clickable(MenuLocators.MENU_BUTTON))
        ActionChains(self.browser).move_to_element(menu_button).perform()

        # Ждем появления выпадающего списка
        self.wait.until(
            EC.visibility_of_element_located(MenuLocators.DROPDOWN))

        # Находим и кликаем 'Десерты'
        desserts_tab = self.wait.until(
            EC.element_to_be_clickable(MenuLocators.DESSERTS_TAB))
        desserts_tab.click()
        return self

    @allure.step("Проверить заголовок Десерты")
    def check_desserts_title(self):
        title = self.wait.until(
            EC.visibility_of_element_located(
                MenuLocators.DESSERTS_TITLE))
        assert "десерты" in title.text.lower(), f"Заголовок '{
            title.text}' не содержит 'Десерты'"
        return self

    @allure.step("Установить максимальную цену")
    def set_max_price(self):
        right_handle = self.browser.find_element(*MenuLocators.MAX_PRICE_INPUT)
        actions = ActionChains(self.browser)
        actions.click_and_hold(
            right_handle).move_by_offset(-200, 0).release().perform()
        time.sleep(1)
        return self

    @allure.step("Применить фильтр")
    def apply_filter(self):
        # Нажимаем кнопку "Применить"
        apply_button = self.wait.until(
            EC.element_to_be_clickable(MenuLocators.APPLY_FILTER_BTN)
        )
        apply_button.click()
        time.sleep(1)
        return self

    @allure.step("Проверить все цены")
    def verify_price_filter(self, max_price=135):
        price_elements = self.browser.find_elements(*MenuLocators.PRICE_AMOUNT)

        for price_element in price_elements:
            # Получаем текст цены (например: "135,00₽")
            price_text = price_element.text

            # Очищаем текст и преобразуем в число
            try:
                price = float(price_text
                              .replace('₽', '')
                              .replace(',', '.')
                              .strip())

                assert price <= max_price, f"Цена {price} превышает максимальную {max_price}"
            except ValueError:
                continue  # Пропускаем элементы, которые не удалось преобразовать

        return self

    @allure.step("Добавить первый десерт в корзину")
    def add_first_dessert(self):
        add_button = self.wait.until(
            EC.element_to_be_clickable(MenuLocators.ADD_FIRST_DESSERT_BTN)
        )
        add_button.click()
        time.sleep(1)
        return self
