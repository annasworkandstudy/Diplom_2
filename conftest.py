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

@pytest.fixture
def auth_headers():
    body = GenerateData.generate_user_login_password()
    UserMethods.create_user(body)
    
    login_response = UserMethods.enter_user(body)
    token = login_response.json().get("accessToken")
    
    return {"Authorization": token} if token else {}

@pytest.fixture
def user_auth_headers(self, user_cleanup):
    body = user_cleanup
    login_response = UserMethods.enter_user(body)
    token = login_response.json().get("accessToken")
    return {"Authorization": token} if token else {}
