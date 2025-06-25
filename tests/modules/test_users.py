from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas import UserPublic
from app.models import Claim, Role, User, UserClaim, BlacklistedToken


def makeLogin(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    assert response.status_code == HTTPStatus.OK
    return response.json()["access_token"]


def test_find_many_users(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
    user_schema = UserPublic.model_validate(user).model_dump()
    user_schema["created_at"] = user_schema["created_at"].isoformat()
    if user_schema.get("updated_at"):
        user_schema["updated_at"] = user_schema["updated_at"].isoformat()

    response = client.get("/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_create_user(client: TestClient, user_role):
    response = client.post(
        "/user",
        json={
            "name": "John Doe",
            "email": "johndoe53@email.com",
            "password": "random_password",
            "role_id": user_role.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED


def test_create_user_without_password(client: TestClient, user_role):
    response = client.post(
        "/user",
        json={
            "name": "John Doe",
            "email": "johndoe53@email.com",
            "role_id": user_role.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED


def test_email_already_exists(client: TestClient, user: User, user_role):
    response = client.post(
        "/user",
        json={
            "name": "John Doe",
            "email": user.email,
            "password": "random_password",
            "role_id": user_role.id,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Email already exists"


def test_find_user_by_id(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.get(
        f"/user/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["email"] == user.email


def test_find_user_by_id_return_error(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.get("/user/223", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_update_user(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.put(
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Leleco",
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_if_admin_can_update_user_with_dif_self_user_id(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.put(
        "/user/1234",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Leleco",
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_if_user_can_update_user_with_dif_self_user_id(client: TestClient, user2: User):
    token = makeLogin(client, user2.email, user2.clean_password)
    response = client.put(
        "/user/1234",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Leleco",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == "Claim 'user:update' not found"


def test_update_user_with_existent_email(client: TestClient, user):
    token = makeLogin(client, user.email, user.clean_password)
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
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "johndoe53@email.com",
            "password": "new-password",
            "name": "John Doe da Silva",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already exists"


def test_delete_user(client: TestClient, user: User, session: Session):
    # Remove tokens da blacklist antes de deletar o usuário
    session.query(UserClaim).filter_by(user_id=user.id).delete()
    session.query(Claim).filter(Claim.description.like("user:%")).delete()
    session.query(BlacklistedToken).filter_by(user_id=user.id).delete()
    session.commit()
    token = makeLogin(client, user.email, user.clean_password)
    response = client.delete(
        f"/user/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "User deleted"


def test_delete_user_with_admin_role_should_return_ok(
    client: TestClient, user: User, user2: User
):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.delete(
        f"/user/{user2.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK


def test_delete_user_with_wrong_user_id(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.delete("/user/1234", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "User not found"


def test_delete_user_with_admin_role(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.delete(
        f"/user/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK


def test_update_user_integrity_error(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
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
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "johndoe53@email.com",
            "password": "new-password",
            "name": "John Doe da Silva",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already exists"


def test_update_user_name(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.put(
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Novo Nome"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == "Novo Nome"


def test_update_user_email_conflict(client: TestClient, user: User, user2: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.put(
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": user2.email},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already exists"


def test_update_user_password(client: TestClient, user: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.put(
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "novasenha123"},
    )
    assert response.status_code == HTTPStatus.OK
    # Não retorna a senha, mas podemos tentar novo login
    new_token = makeLogin(client, user.email, "novasenha123")
    assert new_token


def test_update_user_not_owner_and_not_admin(
    client: TestClient, user: User, user2: User
):
    token = makeLogin(client, user2.email, user2.clean_password)
    response = client.put(
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Hacker"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == "Claim 'user:update' not found"


def test_update_user_claim(client: TestClient, user: User, user2: User, session):
    # Cria claim
    claim = Claim(description="test_claim")
    session.add(claim)
    session.commit()
    # user é admin
    token = makeLogin(client, user.email, user.clean_password)
    response = client.post(
        f"/user/claims/{user2.id}/claim/{claim.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Claim added to user."
    # Garante que existe no banco
    user_claim = (
        session.query(UserClaim).filter_by(user_id=user2.id, claim_id=claim.id).first()
    )
    assert user_claim


def test_update_user_claim_already_exists(
    client: TestClient, user: User, user2: User, session: Session
):
    # Cria claim e já associa
    claim = Claim(description="test_claim2")
    session.add(claim)
    session.commit()
    user_claim = UserClaim(user_id=user2.id, claim_id=claim.id)
    session.add(user_claim)
    session.commit()
    token = makeLogin(client, user.email, user.clean_password)
    response = client.post(
        f"/user/claims/{user2.id}/claim/{claim.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert (
        response.status_code == HTTPStatus.BAD_REQUEST
        or response.status_code == HTTPStatus.CONFLICT
    )


def test_delete_user_claim(
    client: TestClient, user: User, user2: User, session: Session
):
    # Cria claim e associa
    claim = Claim(description="test_claim3")
    session.add(claim)
    session.commit()
    user_claim = UserClaim(user_id=user2.id, claim_id=claim.id)
    session.add(user_claim)
    session.commit()
    token = makeLogin(client, user.email, user.clean_password)
    response = client.delete(
        f"/user/claims/{user2.id}/claim/{claim.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "User Claim deleted"
    # Garante que foi removido
    user_claim = (
        session.query(UserClaim).filter_by(user_id=user2.id, claim_id=claim.id).first()
    )
    assert user_claim is None


def test_delete_user_claim_not_found(client: TestClient, user: User, user2: User):
    token = makeLogin(client, user.email, user.clean_password)
    response = client.delete(
        f"/user/claims/{user2.id}/claim/999999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "User Claim not found"
