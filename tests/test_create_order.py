from generators import GenerateData
import allure
from api_methods.order_methods import OrderMethods
from api_methods.user_methods import UserMethods
from data import Data

class TestCreateOrder:    

    @allure.title('Тест на создание заказа под авторизованным пользователем')
    @allure.description('Проверяем, что при корректных данных API возвращает 200')
    def test_create_order_authorize(self):
        body= GenerateData.generate_user_login_password()
        UserMethods.create_user(body)
        login_response = UserMethods.enter_user(body)
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token} if token else {}
        actual_ids = OrderMethods.get_actual_ingredients()
        order_payload = {"ingredients": actual_ids}
        response = OrderMethods.create_order(order_payload, headers=headers)
        assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"

    @allure.title('Тест на создание заказа под не авторизованным пользователем')
    @allure.description('Проверяем, что при не авторизованном пользователем API возвращает 200')
    def test_create_order_unauthorize(self):
        actual_ids = OrderMethods.get_actual_ingredients()
        order_payload = {"ingredients": actual_ids}
        response = OrderMethods.create_order(order_payload)
        assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"
        assert response.json().get("success") is True

    @allure.title('Тест на создание заказа под авторизованным пользователем с ингредиентами')
    @allure.description('Проверяем, что при отправке валидных ингредиентов и токена API возвращает 200')
    def test_create_order_with_ingredients_authorized(self, user_cleanup):
        body = user_cleanup
        login_response = UserMethods.enter_user(body)
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token} if token else {}
        actual_ids = OrderMethods.get_actual_ingredients()
        order_payload = {"ingredients": actual_ids}
        response = OrderMethods.create_order(order_payload, headers=headers)
        assert response.json().get("success") is True
        assert "order" in response.json()
        assert "number" in response.json().get("order", {}), "В объекте 'order' отсутствует номер заказа"

    @allure.title('Тест на ошибку при создании заказа без ингредиентов')
    @allure.description('Проверяем, что при отправке пустого списка ингредиентов API возвращает 400 и текст ошибки')
    def test_create_order_without_ingredients_error(self, user_cleanup):
        body = user_cleanup
        login_response = UserMethods.enter_user(body)
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token} if token else {}
        order_payload = {"ingredients": []}
        response = OrderMethods.create_order(order_payload, headers=headers)
        assert response.status_code == 400, f"Ожидался код 400, но получен {response.status_code}"
        assert response.json().get("success") is False, "Ожидалось success: False в ответе об ошибке"
        assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title('Тест на ошибку при создании заказа с неверным хэшем ингредиентов')
    @allure.description('Проверяем, что при отправке невалидного хэша ингредиента API падает с кодом 500')
    def test_create_order_invalid_ingredient_hash_error(self, user_cleanup):
        body = user_cleanup
        login_response = UserMethods.enter_user(body)
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token} if token else {}
        order_payload = {"ingredients": ["invalid_hash_qa_12345"]}
        response = OrderMethods.create_order(order_payload, headers=headers)
        assert response.status_code == 500, f"Ожидался код 500, но получен {response.status_code}"