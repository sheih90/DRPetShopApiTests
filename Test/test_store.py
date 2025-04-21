import allure
import jsonschema
import pytest
import requests

from .conftest import create_order
from .schemas.pet_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа на питомца")
    def test_place_an_order_for_a_pet(self):
        with allure.step("Подготовка данных для запроса на размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(f"{BASE_URL}/store/order", json=payload)

        with allure.step("Проверка статуса ответа и данных по заказу"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == payload["id"], "id ответа не совпадает с ожидаемым"
            assert response.json()["petId"] == payload["petId"], "petId не совпадает с ожидаемым"
            assert response.json()["quantity"] == payload["quantity"], "quantity не совпадает с ожидаемым"
            assert response.json()["status"] == payload["status"], "status не совпадает с ожидаемым"
            assert response.json()["complete"] == payload["complete"], "complete не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_information_by_ID(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_ID(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == order_id

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_information_by_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Текстовое содержимое ответа не совпало с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_shop(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Валидация json-схемы инвентаря"):
            jsonschema.validate(response_json, INVENTORY_SCHEMA)


