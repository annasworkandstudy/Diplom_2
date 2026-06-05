import allure
from api_methods.order_methods import OrderMethods


class TestCreateOrder:    

    @allure.title('Тест на создание заказа под авторизованным пользователем')
    @allure.description('Проверяем, что при корректных данных API возвращает 200')
    def test_create_order_authorize(self, auth_headers):
        actual_ids = OrderMethods.get_actual_ingredients()
        order_payload = {"ingredients": actual_ids}
        response = OrderMethods.create_order(order_payload, headers=auth_headers)
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
    def test_create_order_with_ingredients_authorized(self, user_auth_headers):
        actual_ids = OrderMethods.get_actual_ingredients()
        order_payload = {"ingredients": actual_ids}
        response = OrderMethods.create_order(order_payload, headers=user_auth_headers)
        assert response.json().get("success") is True
        assert "order" in response.json()
        assert "number" in response.json().get("order", {}), "В объекте 'order' отсутствует номер заказа"

    @allure.title('Тест на ошибку при создании заказа без ингредиентов')
    @allure.description('Проверяем, что при отправке пустого списка ингредиентов API возвращает 400 и текст ошибки')
    def test_create_order_without_ingredients_error(self, user_auth_headers):
        order_payload = {"ingredients": []}
        response = OrderMethods.create_order(order_payload, headers=user_auth_headers)
        assert response.status_code == 400, f"Ожидался код 400, но получен {response.status_code}"
        assert response.json().get("success") is False, "Ожидалось success: False в ответе об ошибке"
        assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title('Тест на ошибку при создании заказа с неверным хэшем ингредиентов')
    @allure.description('Проверяем, что при отправке невалидного хэша ингредиента API падает с кодом 500')
    def test_create_order_invalid_ingredient_hash_error(self, user_auth_headers):
        order_payload = {"ingredients": ["invalid_hash_qa_12345"]}
        response = OrderMethods.create_order(order_payload, headers=user_auth_headers)
        assert response.status_code == 500, f"Ожидался код 500, но получен {response.status_code}"