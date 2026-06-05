import requests
import allure
from url import URL

class OrderMethods:

    @staticmethod
    @allure.step('Создание заказа')
    def create_order(body, headers=None):
        return requests.post(url=URL.CREATE_ORDER, json=body, headers=headers)
    
    @staticmethod
    @allure.step('Получаем список ингридиентов')
    def get_actual_ingredients():
        res = requests.get(url=URL.GET_INGREDIENTS)
        if res.status_code == 200:
            data = res.json().get("data", [])
            return [item["_id"] for item in data[:2]]
        return []