import allure
import pytest

from helpers import login_user


class TestUserLogin:

    @allure.title("Успешный логин существующего пользователя")
    def test_login_existing_user(self, user):
        response = login_user(user)

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
        response = login_user({
            "email": email,
            "password": password
        })

        assert response.status_code == 401
        assert response.json()["message"] == (
            "email or password are incorrect"
        )