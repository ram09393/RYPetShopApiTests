import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации несуществующего питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

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

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_full_data(self):
        with allure.step("Подготовка данных для создания питомца c полными данными"):
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

            with allure.step("Отправка запроса на создание питомца c полными данными"):
                response = requests.post(url=f"{BASE_URL}/pet", json=payload)

            with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
                assert response.status_code == 200
                jsonschema.validate(response.json(), PET_SCHEMA)

            with allure.step("Проверка параметров питомца c полными данными в ответе"):
                assert response.json()['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
                assert response.json()['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
                assert response.json()['photoUrls'] == payload['photoUrls'], "фото питомца не совпадает с ожидаемым"
                assert response.json()['tags'] == payload['tags'], "тэг питомца не совпадает с ожидаемым"
                assert response.json()['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

    @allure.title("Обновление информации о питомце")
    def test_update_pet(create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления питомца"):
            updated_payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка PUT-запроса с подготовленными данными о питомце"):
            response = requests.put(url=f"{BASE_URL}/pet", json=updated_payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка ответа о содержании обновленных данных питомца"):
            updated_pet = response.json()
            assert updated_pet["id"] == pet_id
            assert updated_pet["name"] == "Buddy Updated"
            assert updated_pet["status"] == "sold"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet(create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка DELETE-запроса на удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Отправка GET-запроса для проверки удаления питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404
