import pytest
import requests
from jsonschema import validate, ValidationError
from tests.schemas import inventory_schema

BASE_URL = "http://5.181.109.28:9090/api/v3"


@pytest.fixture(scope="function")
def create_pet():
    """Фикстура для создания питомца."""
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="function")
def create_order():
    """Фикстура для создания заказа."""
    payload = {
        "id": 1,
        "petId": 198772,
        "quantity": 7,
        "shipDate": "2025-12-08T00:38:41.580Z",
        "status": "approved",
        "complete": True
    }
    response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
    assert response.status_code == 200
    return response.json()
