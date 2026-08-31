import pytest

from helpers import (
    create_user,
    delete_user,
    get_ingredients,
    generate_user_data
)


@pytest.fixture
def user():
    user_data = generate_user_data()

    response = create_user(user_data)

    if response.status_code == 200:
        user_data["access_token"] = response.json()["accessToken"]

    yield user_data

    if response.status_code == 200:
        delete_user(user_data["access_token"])


@pytest.fixture
def ingredients():
    response = get_ingredients()

    return response.json()["data"]


@pytest.fixture
def ingredient_ids(ingredients):
    return [
        ingredients[0]["_id"],
        ingredients[1]["_id"]
    ]