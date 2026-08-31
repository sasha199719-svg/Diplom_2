import allure
import pytest

from helpers import (
    create_user,
    generate_user_data
)


class TestUserCreate:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self):
        user_data = generate_user_data()

        response = create_user(user_data)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Нельзя создать уже существующего пользователя")
    def test_create_existing_user(self):
        user_data = generate_user_data()

        create_user(user_data)
        response = create_user(user_data)

        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @pytest.mark.parametrize(
        "missing_field",
        [
            "email",
            "password",
            "name"
        ]
    )
    @allure.title("Нельзя создать пользователя без обязательного поля")
    def test_create_user_without_required_field(self, missing_field):
        user_data = generate_user_data()
        del user_data[missing_field]

        response = create_user(user_data)

        assert response.status_code == 403
        assert response.json()["message"] == (
            "Email, password and name are required fields"
        )