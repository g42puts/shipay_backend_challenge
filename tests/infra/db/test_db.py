from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.infra.db.db import get_session


def test_get_session(engine: Engine):
    original_engine = get_session.__globals__["engine"]
    get_session.__globals__["engine"] = engine

    try:
        session_generator = get_session()
        session = next(session_generator)

        assert isinstance(
            session, Session
        ), "A sessão gerada não é uma instância de sqlalchemy.orm.Session"
        assert (
            session.bind == engine
        ), "A sessão gerada não está vinculada ao engine de teste"

        session.close()

    finally:
        get_session.__globals__["engine"] = original_engine
