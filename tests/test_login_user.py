from generators import GenerateData
import allure
from api_methods.user_methods import UserMethods
from data import Data

class TestLoginUser:

    @allure.title('Тест на вход под существующим пользователем')
    @allure.description('Проверяем, что при корректных данных API возвращает 403 и {"success": false, "message": "Email, password and name are requires fields"}')
    def test_login_success(self, user_cleanup):
        body = user_cleanup
        response = UserMethods.enter_user(body)
        assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"
        assert response.json().get("success") is True

    @allure.title('Тест на вход с некорректными данными (несуществующий пользователь)')
    @allure.description('Проверяем, что при корректных данных API возвращает 401 и {"success": false, "message": "Email, password and name are requires fields"}')
    def test_login_incorrect_credentials(self):
        body = Data.data_for_login()
        response = UserMethods.enter_user(body)
        assert response.status_code == 401, f"Ожидался код 401, но получен {response.status_code}"
        assert response.json().get("success") is False
        assert response.json().get("message") == "email or password are incorrect"