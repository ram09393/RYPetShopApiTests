import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA
from .schemas.pet_schema import PET_SCHEMA_1

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

#Создаю еще один пулл реквест, предыдущий удалился при закрытии PR#

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json()['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response.json()['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response.json()['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet_1(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {

                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
        }

            with allure.step("Отправка запроса на создание питомца"):
                response = requests.post(url=f"{BASE_URL}/pet", json=payload)

            with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
                assert response.status_code == 200
                jsonschema.validate(response.json(), PET_SCHEMA_1)

            with allure.step("Проверка параметров питомца в ответе"):
                assert response.json()['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
                assert response.json()['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
                assert response.json()['photoUrls'] == payload['photoUrls'], "фото питомца не совпадает с ожидаемым"
                assert response.json()['tags'] == payload['name'], "тэг питомца не совпадает с ожидаемым"
                assert response.json()['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"