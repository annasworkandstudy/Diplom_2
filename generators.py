from faker import Faker

faker = Faker()
class GenerateData:
    @staticmethod
    def generate_user_login_password():
        unique_login = f"{faker.user_name()}@yandex.ru"

        return {
            "email": unique_login,
            "password": faker.password(),
            "name": faker.first_name()
        }