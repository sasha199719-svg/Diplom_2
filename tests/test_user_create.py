import allure
import pytest
import requests

from data import BASE_URL, REGISTER_ENDPOINT
from helpers import generate_user_data


class TestUserCreate:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self):
        user_data = generate_user_data()

        response = requests.post(
            BASE_URL + REGISTER_ENDPOINT,
            json=user_data
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Нельзя создать уже существующего пользователя")
    def test_create_existing_user(self):
        user_data = generate_user_data()

        requests.post(
            BASE_URL + REGISTER_ENDPOINT,
            json=user_data
        )

        response = requests.post(
            BASE_URL + REGISTER_ENDPOINT,
            json=user_data
        )

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

        response = requests.post(
            BASE_URL + REGISTER_ENDPOINT,
            json=user_data
        )

        assert response.status_code == 403
        assert response.json()["message"] == (
            "Email, password and name are required fields"
        )