import allure
import jsonschema
import requests
from .schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestPet:

    @allure.title("Размещение заказа")
    def test_placement_store_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {

                "id": 1,
                "petId": 1,
                "quantity": 1,
                "shipDate": "2025-12-08T00:24:06.976+00:00",
                "status": "placed",
                "complete": True
            }

            with allure.step("Отправка запроса на создание питомца c полными данными"):
                response = requests.post(url=f"{BASE_URL}/store/order/", json=payload)

            with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
                assert response.status_code == 200
                jsonschema.validate(response.json(), STORE_SCHEMA)

            with allure.step("Проверка параметров питомца c полными данными в ответе"):
                assert response.json()['id'] == payload['id'], "id заказа не совпадает с ожидаемым"
                assert response.json()['petId'] == payload['petId'], "Id питомца не совпадает с ожидаемым"
                assert response.json()['quantity'] == payload['quantity'], "кол-во заказа не совпадает с ожидаемым"
                assert response.json()['shipDate'] == payload['shipDate'], "Дата отправки не совпадает с ожидаемым"
                assert response.json()['status'] == payload['status'], "Статус заказа не совпадает с ожидаемым"
                assert response.json()['complete'] == payload['complete'], "полнота заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        order_id = 1  # ID заказа
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        response_get_order = response.json()
        with allure.step("Проверка, что ID заказа совпадает с запрашиваемым"):
            assert response_get_order["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_pet(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка DELETE-запроса на удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Отправка GET-запроса для проверки удаления питомца"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе по ID")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации несуществующего заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
