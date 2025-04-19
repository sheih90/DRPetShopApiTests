from types import NoneType

import allure
import jsonschema
import pytest
import requests
from .schemas.pet_schema import PET_SCHEMA

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
            assert response.text == "Pet deleted", "Текстовое содержимое ответа не совпало с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текстовое содержимое ответа не совпало с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_information_about_a_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпадает с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текстовое содержимое ответа не совпало с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация json-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id ответа не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name ответа не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status ответа не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_with_complete_data(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация json-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id ответа не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name ответа не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "category ответа не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "photoUrls ответа не совпадают с ожидаемыми"
            assert response_json['tags'] == payload['tags'], "tags ответа не совпадают с ожидаемыми"
            assert response_json['status'] == payload['status'], "status ответа не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_information_by_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id

        with allure.step("Подготовка данных для обновления питомца"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на обновление питомца"):
            response = requests.put(f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа и данных обновленного питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id, "id ответа не совпадает с ожидаемым"
            assert response.json()["name"] == payload["name"], "Имя не обновилось"
            assert response.json()["status"] == payload["status"], "Статус не обновился"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_ID(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id

        with allure.step("Отправка запроса на удаление питомца по ID"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"


    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code, expected_error_message",
        [
            ("available", 200, None),  # Корректный статус
            ("pending", 200, None),  # Корректный статус
            ("sold", 200, None),  # Корректный статус
            (None, 400, "No status provided. Try again?"),  # Пустой статус
            ("new", 400, "Input error: query parameter `status value `new` is not in the allowable values `[available, pending, sold]`"),  # Некорректный статус
        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code, expected_error_message):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == expected_status_code, "Статус отличается от ожидаемого"

        with allure.step("Проверка формата данных или наличия ошибки"):
            if expected_error_message:
                # Проверяем, что ответ содержит текстовое сообщение об ошибке
                try:
                    # Попытка получить JSON-ответ
                    error_message = response.json().get("message", "")
                except ValueError:
                    # Если ответ не JSON, используем текст ответа
                    error_message = response.text

                # Проверяем, что текст ошибки соответствует ожидаемому
                assert error_message == expected_error_message, "Текст ошибки не совпал с ожидаемым"
            else:
                # Если ошибки нет, проверяем, что ответ содержит список питомцев
                assert isinstance(response.json(), list), "Ответ должен быть списком питомцев"