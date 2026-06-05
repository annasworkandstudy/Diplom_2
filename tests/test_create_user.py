from generators import GenerateData
import allure
from api_methods.user_methods import UserMethods
from data import Data

class TestCreateUser:

    @allure.title('Тест на создание уникального пользователя')
    @allure.description('Проверяем, что при корректных данных API возвращает 200 и {"success": true"}')
    def test_create_user(self):
        body= GenerateData.generate_user_login_password()
        response= UserMethods.create_user(body)
        token = response.json().get("accessToken")
        if token:
            headers = {"Authorization": token}
            UserMethods.delete_user(headers)
        assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"
        assert response.json().get("success") is True

    @allure.title('Тест на ошибку при создании дубликата пользователя')
    @allure.description('Проверяем, что повторный запрос с тем же логином возвращает 403 Conflict')
    def test_create_duplicate_user_conflict(self, user_cleanup):
        body = user_cleanup
        duplicate_response = UserMethods.create_user(body)
        assert duplicate_response.status_code == 403, f"Ожидался код 403, но получен {duplicate_response.status_code}"
        assert duplicate_response.json().get("success") is False
        assert duplicate_response.json().get("message") == "User already exists"

    @allure.title('Тест на ошибку при отсутствии одного из полей')
    @allure.description('Проверяем, что при отсутствии одного из полей регистрация невозможна')
    def test_create_user_without_first_name(self):
        body = Data.data_for_login()
        response = UserMethods.create_user(body)
        assert response.status_code == 403, f"Ожидался код 403, но получен {response.status_code}"
        assert response.json().get("message") == f'{"Email, password and name are required fields"}'