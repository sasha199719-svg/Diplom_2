import allure

from helpers import create_order


class TestOrders:

    @allure.title("Можно создать заказ с авторизацией")
    def test_create_order_with_authorization(self, user, ingredient_ids):
        response = create_order(
            ingredient_ids,
            user["access_token"]
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Можно создать заказ без авторизации")
    def test_create_order_without_authorization(self, ingredient_ids):
        response = create_order(ingredient_ids)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Можно создать заказ с ингредиентами")
    def test_create_order_with_ingredients(self, ingredient_ids):
        response = create_order(ingredient_ids)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self):
        response = create_order([])

        assert response.status_code == 400
        assert response.json()["message"] == (
            "Ingredient ids must be provided"
        )

    @allure.title("Ошибка при создании заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self):
        response = create_order(["invalid_hash"])

        assert response.status_code == 400