import allure


@allure.feature("Основной флоу клиента")
@allure.story("Работа с корзиной")
class TestCartFlow:
    @allure.title("TC-07: Переход в корзину")
    def test_go_to_cart(self, browser, preparing_cart):
        # Проверка перехода в корзину и отображения товаров
        (preparing_cart['cart_page'].open_cart().check_cart_title()
         .verify_cart_contents(
            first_pizza_name=preparing_cart['first_pizza_name'],
            second_pizza_name=preparing_cart['second_pizza_name']
        ))

    @allure.title("TC-08: Изменение количества пицц в корзине")
    def test_change_pizza_quantity(self, browser, preparing_cart):
        # Увеличение количества пицц и обновление корзины
        cart_page = preparing_cart['cart_page']
        (cart_page.open_cart().check_cart_title()
         .change_pizza_quantity(0, 2)
         .update_cart())

        updated_quantity = cart_page.get_pizza_quantity(0)
        assert updated_quantity == "2", \
            f"Ожидалось количество 2, получено {updated_quantity}"

    @allure.title("TC-09: Удаление пиццы в корзине")
    def test_remove_item(self, browser, preparing_cart):
        (preparing_cart['cart_page']
         .open_cart()
         .check_cart_title()
         .remove_item_by_index(1)
         .verify_single_item_remaining(preparing_cart['first_pizza_name']))
