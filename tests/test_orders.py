import allure
import requests

from data import (
    BASE_URL,
    LOGIN_ENDPOINT,
    ORDERS_ENDPOINT
)


class TestOrders:

    @allure.title("Можно создать заказ с авторизацией")
    def test_create_order_with_authorization(self, user, ingredient_ids):
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }

        login_response = requests.post(
            BASE_URL + LOGIN_ENDPOINT,
            json=login_data
        )

        access_token = login_response.json()["accessToken"]

        response = requests.post(
            BASE_URL + ORDERS_ENDPOINT,
            json={
                "ingredients": ingredient_ids
            },
            headers={
                "Authorization": access_token
            }
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Можно создать заказ без авторизации")
    def test_create_order_without_authorization(self, ingredient_ids):
        response = requests.post(
            BASE_URL + ORDERS_ENDPOINT,
            json={
                "ingredients": ingredient_ids
            }
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Можно создать заказ с ингредиентами")
    def test_create_order_with_ingredients(self, ingredient_ids):
        response = requests.post(
            BASE_URL + ORDERS_ENDPOINT,
            json={
                "ingredients": ingredient_ids
            }
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self):
        response = requests.post(
            BASE_URL + ORDERS_ENDPOINT,
            json={
                "ingredients": []
            }
        )

        assert response.status_code == 400
        assert response.json()["message"] == (
            "Ingredient ids must be provided"
        )

    @allure.title("Ошибка при создании заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self):
        response = requests.post(
            BASE_URL + ORDERS_ENDPOINT,
            json={
                "ingredients": [
                    "invalid_hash"
                ]
            }
        )

        assert response.status_code == 400