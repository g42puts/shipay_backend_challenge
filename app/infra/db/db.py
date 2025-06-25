from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session

from app.configs.configs import configs

metadata = MetaData()
engine = create_engine(configs.DATABASE_URL)


def get_session():
    with Session(bind=engine) as session:
        yield session
