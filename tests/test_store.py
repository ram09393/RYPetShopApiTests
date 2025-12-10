import allure
import jsonschema
import requests
from .schemas.store_schema import STORE_SCHEMA
from .schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:

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

            with allure.step("Отправка запроса на создание заказа"):
                response = requests.post(url=f"{BASE_URL}/store/order/", json=payload)

            with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
                assert response.status_code == 200
                jsonschema.validate(response.json(), STORE_SCHEMA)

            with allure.step("Проверка параметров заказа в ответе"):
                assert response.json()['id'] == payload['id'], "id заказа не совпадает с ожидаемым"
                assert response.json()['petId'] == payload['petId'], "Id питомца не совпадает с ожидаемым"
                assert response.json()['quantity'] == payload['quantity'], "кол-во заказа не совпадает с ожидаемым"
                assert response.json()['shipDate'] == payload['shipDate'], "Дата отправки не совпадает с ожидаемым"
                assert response.json()['status'] == payload['status'], "Статус заказа не совпадает с ожидаемым"
                assert response.json()['complete'] == payload['complete'], "полнота заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        order_id = 1
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Проверка, что ID заказа совпадает с запрашиваемым"):
            order_data = response.json()
            assert order_data['id'] == order_id  # Проверка, что id заказа равен 1
            assert order_data['petId'] == create_order['petId']
            assert order_data['quantity'] == create_order['quantity']
            assert order_data['shipDate'] == create_order['shipDate']
            assert order_data['status'] == create_order['status']
            assert order_data['complete'] == create_order['complete']


    @allure.title("Удаление заказа по ID")
    def test_delete_order(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка DELETE-запроса на удаление заказа"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Отправка GET-запроса для проверки удаления заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе по ID")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации несуществующего заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Проверка получения инвентаря магазина"):
            response = requests.get(f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)
