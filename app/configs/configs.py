from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Configs(BaseSettings):
    MYSQL_HOST: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_TCP_PORT: str
    PORT: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_IN_MINUTES: int
    mysql_user: str | None = None
    database_url: str | None = None
    database_url_override: str | None = None
    DEFAULT_ADMIN_EMAIL: str | None = None
    DEFAULT_ADMIN_PASSWORD: str | None = None

    @property
    def DATABASE_URL(self):
        """Returns the database URL."""
        if self.database_url_override:
            return self.database_url_override
        return f"mysql+pymysql://root:{self.MYSQL_ROOT_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_TCP_PORT}/{self.MYSQL_DATABASE}"

    model_config = ConfigDict(
        extra="forbid", env_file=".env", env_file_encoding="utf-8"
    )


configs = Configs()
