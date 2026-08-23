import random
import string


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