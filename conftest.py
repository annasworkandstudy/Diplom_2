import pytest
from api_methods.user_methods import UserMethods
from generators import GenerateData

@pytest.fixture
def user_cleanup():
    body = GenerateData.generate_user_login_password()
    response = UserMethods.create_user(body)
    token = response.json().get("accessToken")
    headers = {"Authorization": token} if token else {}
    yield body
    if token:
        UserMethods.delete_user(headers)
