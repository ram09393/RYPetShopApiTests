import allure
import jsonschema
import requests
from .schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Inventory")
class TestPet:
    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Проверка получения инвентаря магазина"):
            response = requests.get(f"{BASE_URL}/store/inventory")
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, dict)
        expected_data = {"approved": 50}
        assert response_data == expected_data, f"Expected {expected_data}, but got {response_data}"
