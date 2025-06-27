import os
from http import HTTPStatus
from datetime import datetime
from typing import Callable

import pytest
from alembic.config import Config
from alembic import command
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.mysql import MySqlContainer

from app.factories.infra.auth.make_password_helper import make_password_helper
from app.main import app
from app.infra.db.db import get_session
from app.models import Claim, User, Role, UserClaim


@pytest.fixture(scope="session")
def engine():
    with MySqlContainer("mysql:8.4") as mysql:
        url = mysql.get_connection_url().replace("mysql://", "mysql+pymysql://")
        from app.configs.configs import configs

        configs.database_url_override = url
        engine = create_engine(url)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alembic_ini_path = os.path.join(base_dir, "alembic.ini")
        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("sqlalchemy.url", url)
        command.upgrade(alembic_cfg, "head")
        yield engine


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    with TestClient(app, root_path="/api/v1") as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
        app.dependency_overrides.clear()


@pytest.fixture(name="session")
def session_fixture(engine: Engine):
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        try:
            with engine.connect() as connection:
                connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
                for table in ["user_claims", "users", "claims", "roles"]:
                    connection.execute(text(f"TRUNCATE TABLE {table};"))
                connection.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
                connection.commit()
        except Exception as e:
            print(f"Erro ao truncar tabelas: {e}")


@pytest.fixture(name="make_login_func")
def make_login_func_fixture(client: TestClient) -> Callable[[str, str], str]:
    def _make_login(email: str, password: str) -> str:
        response = client.post(
            "/auth/login", data={"username": email, "password": password}
        )
        assert response.status_code == HTTPStatus.OK
        return response.json()["access_token"]

    return _make_login


@pytest.fixture(name="admin_user")
def first_user_fixture(session: Session):
    password = "testtest"
    admin_role = session.query(Role).filter_by(description="admin").first()
    if not admin_role:
        admin_role = Role(description="admin")
        session.add(admin_role)
        session.commit()
    user = session.query(User).filter_by(email="teste@teste.com").first()
    if not user:
        user = User(
            name="Gilmar",
            password=make_password_helper().hash(password=password),
            email="teste@teste.com",
            created_at=datetime.now(),
            role_id=admin_role.id,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        claims = session.query(Claim).all()
        admin_claim_ids = {
            uc.claim_id for uc in session.query(UserClaim).filter_by(user_id=user.id)
        }
        new_user_claims = [
            UserClaim(user_id=user.id, claim_id=claim.id)
            for claim in claims
            if claim.id not in admin_claim_ids
        ]
        if new_user_claims:
            session.bulk_save_objects(new_user_claims)
            session.commit()

    user.clean_password = password
    return user


@pytest.fixture(name="normal_user")
def second_user_fixture(session: Session):
    password = "testtest"
    role = session.query(Role).filter_by(description="user").first()
    if not role:
        role = Role(description="user")
        session.add(role)
        session.commit()
    user = session.query(User).filter_by(email="teste2@teste.com").first()
    if not user:
        user = User(
            name="Gilmar",
            password=make_password_helper().hash(password=password),
            email="teste2@teste.com",
            created_at=datetime.now(),
            role_id=role.id,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    user.clean_password = password
    return user


@pytest.fixture(name="admin_role")
def admin_role_fixture(session: Session):
    role = session.query(Role).filter_by(description="admin").first()
    if not role:
        role = Role(description="admin")
        session.add(role)
        session.commit()
    return role


@pytest.fixture(name="user_role")
def user_role_fixture(session: Session):
    role = session.query(Role).filter_by(description="user").first()
    if not role:
        role = Role(description="user")
        session.add(role)
        session.commit()
    return role


@pytest.fixture(name="user_create_claim")
def user_create_claim_fixture(session: Session):
    claim = session.query(Claim).filter_by(description="user_create").first()
    if not claim:
        claim = Claim(description="user_create")
        session.add(claim)
        session.commit()
    return claim
