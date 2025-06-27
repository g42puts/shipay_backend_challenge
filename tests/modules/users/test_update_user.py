from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models import User


def test_update_user(client: TestClient, admin_user: User, make_login_func):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.put(
        f"/user/{admin_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Leleco",
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_if_admin_can_update_user_with_dif_self_user_id(
    client: TestClient, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.put(
        "/user/1234",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Leleco",
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_if_user_can_update_user_with_dif_self_user_id(
    client: TestClient, normal_user: User, make_login_func
):
    token = make_login_func(normal_user.email, normal_user.clean_password)
    response = client.put(
        "/user/1234",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Leleco",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == "Claim 'user:update' not found"


def test_update_user_with_existent_email(
    client: TestClient, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.post(
        "/user",
        json={
            "name": "John Doe",
            "email": "johndoe53@email.com",
            "password": "random_password",
            "role_id": 1,
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.put(
        f"/user/{admin_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "johndoe53@email.com",
            "password": "new-password",
            "name": "John Doe da Silva",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already exists"


def test_update_user_integrity_error(
    client: TestClient, admin_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.post(
        "/user",
        json={
            "name": "John Doe",
            "email": "johndoe53@email.com",
            "password": "random_password",
            "role_id": 1,
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.put(
        f"/user/{admin_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "johndoe53@email.com",
            "password": "new-password",
            "name": "John Doe da Silva",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already exists"


def test_update_user_name(client: TestClient, admin_user: User, make_login_func):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.put(
        f"/user/{admin_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Novo Nome"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == "Novo Nome"


def test_update_user_email_conflict(
    client: TestClient, admin_user: User, normal_user: User, make_login_func
):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.put(
        f"/user/{admin_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": normal_user.email},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already exists"


def test_update_user_password(client: TestClient, admin_user: User, make_login_func):
    token = make_login_func(admin_user.email, admin_user.clean_password)
    response = client.put(
        f"/user/{admin_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "novasenha123"},
    )
    assert response.status_code == HTTPStatus.OK
    # Não retorna a senha, mas podemos tentar novo login
    new_token = make_login_func(admin_user.email, "novasenha123")
    assert new_token


def test_update_user_not_owner_and_not_admin(
    client: TestClient, admin_user: User, normal_user: User, make_login_func
):
    token = make_login_func(normal_user.email, normal_user.clean_password)
    response = client.put(
        f"/user/{admin_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Hacker"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == "Claim 'user:update' not found"
