from http import HTTPStatus

from fastapi.testclient import TestClient


def teste_root_should_return_ok_and_hello_world(client: TestClient):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}
