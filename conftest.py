import pytest
import requests

from data import (
    BASE_URL,
    REGISTER_ENDPOINT,
    USER_ENDPOINT,
    INGREDIENTS_ENDPOINT
)
from helpers import generate_user_data


@pytest.fixture
def user():
    user_data = generate_user_data()

    response = requests.post(
        BASE_URL + REGISTER_ENDPOINT,
        json=user_data
    )

    yield user_data

    if response.status_code == 200:
        access_token = response.json()["accessToken"]

        requests.delete(
            BASE_URL + USER_ENDPOINT,
            headers={
                "Authorization": access_token
            }
        )


@pytest.fixture
def ingredients():
    response = requests.get(
        BASE_URL + INGREDIENTS_ENDPOINT
    )

    return response.json()["data"]


@pytest.fixture
def ingredient_ids(ingredients):
    return [
        ingredients[0]["_id"],
        ingredients[1]["_id"]
    ]