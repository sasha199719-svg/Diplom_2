import random
import string

import allure
import requests

from data import (
    BASE_URL,
    REGISTER_ENDPOINT,
    LOGIN_ENDPOINT,
    USER_ENDPOINT,
    INGREDIENTS_ENDPOINT,
    ORDERS_ENDPOINT
)


def generate_random_string(length=10):
    return ''.join(
        random.choices(
            string.ascii_lowercase + string.digits,
            k=length
        )
    )


def generate_user_data():
    random_string = generate_random_string()

    return {
        "email": f"{random_string}@yandex.ru",
        "password": generate_random_string(),
        "name": generate_random_string()
    }


@allure.step("Создать пользователя")
def create_user(user_data):
    return requests.post(
        BASE_URL + REGISTER_ENDPOINT,
        json=user_data
    )


@allure.step("Авторизоваться пользователем")
def login_user(user_data):
    return requests.post(
        BASE_URL + LOGIN_ENDPOINT,
        json={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )


@allure.step("Удалить пользователя")
def delete_user(access_token):
    return requests.delete(
        BASE_URL + USER_ENDPOINT,
        headers={
            "Authorization": access_token
        }
    )


@allure.step("Получить список ингредиентов")
def get_ingredients():
    return requests.get(
        BASE_URL + INGREDIENTS_ENDPOINT
    )


@allure.step("Создать заказ")
def create_order(ingredient_ids, access_token=None):
    headers = {}

    if access_token:
        headers["Authorization"] = access_token

    return requests.post(
        BASE_URL + ORDERS_ENDPOINT,
        json={
            "ingredients": ingredient_ids
        },
        headers=headers
    )