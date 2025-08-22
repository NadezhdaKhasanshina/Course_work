import allure
from pages.bonus_page import BonusPage
from pages.main_page import MainPage


@allure.feature("Флоу с бонусной системой")
class TestBonusProgram:
    @allure.story("Успешная регистрация в бонусной программе")
    @allure.title("TC-20: Регистрация в бонусной программе")
    def test_bonus_program_registration(self, browser):
        MainPage(browser).open_url()
        bonus_page = BonusPage(browser)
        (bonus_page.open_bonus_page()
         .fill_bonus_field(name="qwe", phone="+71234567891")
         .submit_form()
         .verify_success_registration())

    @allure.story("Валидация полей бонусной программы")
    @allure.title("TC-21: Ввод неверного телефона")
    def test_invalid_phone_validation(self, browser):
        # Проверяет валидацию неверного формата телефона
        MainPage(browser).open_url()
        bonus_page = BonusPage(browser)
        (bonus_page.open_bonus_page()
         .fill_bonus_field(name="Иван", phone="123")  # Неверный формат
         .submit_form()
         .verify_invalid_phone())  # Проверяем ошибку телефона
