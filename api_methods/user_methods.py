import requests
import allure
from url import URL

class UserMethods:

    @staticmethod
    @allure.step('Создаем пользователя')
    def create_user(body):
        return requests.post(url=URL.CREATE_USER, json=body)
    
    @staticmethod
    @allure.step('Вход пользователя')
    def enter_user(body):
        return requests.post(url=URL.AUTH_USER, json=body)

    @staticmethod
    @allure.step('Удаление пользователя')
    def delete_user(headers):
        return requests.delete(url=URL.DELETE_USER, headers=headers)


