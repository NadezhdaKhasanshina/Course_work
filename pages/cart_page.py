import allure
from selenium.webdriver.support import expected_conditions as EC
from locators.cart_locators import CartLocators
from pages.base_page import BasePage


class CartPage(BasePage):
    @allure.step("Открыть корзину")
    def open_cart(self):
        self.wait.until(
            EC.element_to_be_clickable(
                CartLocators.CART_ICON)).click()
        return self

    @allure.step("Проверить заголовок корзины")
    def check_cart_title(self):
        title = self.wait.until(
            EC.visibility_of_element_located(
                CartLocators.CART_TITLE))
        assert "Корзина" in title.text
        return self

    @allure.step("Проверить содержимое корзины")
    def verify_cart_contents(self, first_pizza_name, second_pizza_name):
        # Проверяем общее количество
        items = self.wait.until(
            EC.presence_of_all_elements_located(CartLocators.CART_ITEM)
        )
        assert len(items) == 2, f"Ожидалось 2 товара, найдено {len(items)}"

        # Получаем названия всех пицц в корзине
        item_names = [
            item.text for item in self.browser.find_elements(
                *CartLocators.ITEM_NAME)]

        # Для отладки выводим найденные названия
        print(f"Найденные названия в корзине: {item_names}")
        print(f"Ожидаемые названия: {first_pizza_name}, {second_pizza_name}")

        # Проверяем наличие пицц (по частичному совпадению)
        assert self.pizza_in_cart(first_pizza_name, item_names), \
            f"Не найдена пицца '{first_pizza_name}' в корзине. Найдены: {item_names}"

        assert self.pizza_in_cart(second_pizza_name, item_names), \
            f"Не найдена пицца '{second_pizza_name}' в корзине. Найдены: {item_names}"

        # Проверяем сырный бортик ТОЛЬКО у второй пиццы
        second_item = items[1]  # Вторая пицца в корзине
        border_elements = second_item.find_elements(*CartLocators.ITEM_EXTRAS)
        border_texts = [item.text for item in border_elements]

        # Выводим информацию для отладки
        print(f"\nДополнения у второй пиццы: {border_texts}")

        assert border_elements, "Не найдены дополнения у второй пиццы"
        assert any("сырный" in text.lower() for text in border_texts), \
            f"Не найден сырный бортик. Найдены: {border_texts}"

        return self

    def pizza_in_cart(self, expected_name, item_names):
        # Вспомогательный метод для проверки наличия пиццы
        expected_normalized = self.normalize_name(expected_name)
        return any(expected_normalized in self.normalize_name(name)
                   for name in item_names)

    def normalize_name(self, name):
        # Метод для нормализации названия для сравнения
        return (name.lower()
                .replace('пицца', '')
                .replace('«', '')
                .replace('»', '')
                .replace('"', '')
                .strip())

    @allure.step("Получить количество пиццы")
    def get_pizza_quantity(self, index=0):
        # Возвращает количество для пиццы с указанным индексом
        quantities = self.wait.until(
            EC.presence_of_all_elements_located(CartLocators.QUANTITY_INPUT)
        )
        return quantities[index].get_attribute("value")

    @allure.step("Изменить количество пиццы")
    def change_pizza_quantity(self, index, quantity):
        # Устанавливает новое количество для пиццы с указанным индексом
        quantities = self.wait.until(
            EC.presence_of_all_elements_located(CartLocators.QUANTITY_INPUT)
        )
        quantities[index].clear()
        quantities[index].send_keys(str(quantity))
        return self

    @allure.step("Обновить корзину")
    def update_cart(self):
        self.wait.until(
            EC.element_to_be_clickable(
                CartLocators.UPDATE_BUTTON)).click()
        return self

    @allure.step("Удалить товар")
    def remove_item_by_index(self, index):
        # Удаляет товар с указанным индексом из корзины
        delete_buttons = self.wait.until(
            EC.presence_of_all_elements_located(CartLocators.DELETE_BUTTON))
        initial_count = len(
            self.browser.find_elements(
                *CartLocators.CART_ITEM))
        delete_buttons[index].click()

        self.wait.until(
            lambda d: len(d.find_elements(*CartLocators.CART_ITEM)) < initial_count)
        return self

    @allure.step("Проверить что остался 1 товар")
    def verify_single_item_remaining(self, expected_name):
        # Проверяет что в корзине 1 товар с нужным названием
        items = self.wait.until(
            EC.presence_of_all_elements_located(CartLocators.CART_ITEM)
        )
        assert len(items) == 1, "Должен остаться 1 товар"

        item_name = items[0].find_element(*CartLocators.ITEM_NAME).text
        assert self.pizza_in_cart(expected_name, [item_name]), \
            f"Ожидалась пицца '{expected_name}', найдена '{item_name}'"

        extras = items[0].find_elements(*CartLocators.ITEM_EXTRAS)
        assert not extras, "У оставшейся пиццы не должно быть доп. опций"
        return self
