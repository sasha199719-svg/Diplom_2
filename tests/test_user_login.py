import allure
import pytest
import requests

from data import BASE_URL, LOGIN_ENDPOINT


class TestUserLogin:

    @allure.title("Успешный логин существующего пользователя")
    def test_login_existing_user(self, user):
        payload = {
            "email": user["email"],
            "password": user["password"]
        }

        response = requests.post(
            BASE_URL + LOGIN_ENDPOINT,
            json=payload
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @pytest.mark.parametrize(
        "email,password",
        [
            ("wrong_email@yandex.ru", "wrong_password")
        ]
    )
    @allure.title("Нельзя войти с неверным логином и паролем")
    def test_login_with_invalid_credentials(self, email, password):
        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(
            BASE_URL + LOGIN_ENDPOINT,
            json=payload
        )

        assert response.status_code == 401
        assert response.json()["message"] == \
               "email or password are incorrect"