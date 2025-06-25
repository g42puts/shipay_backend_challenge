from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.factories.modules.make_auth_router import make_auth_router
from app.factories.modules.make_claim_router import make_claim_router
from app.factories.modules.make_role_router import make_role_router
from app.factories.modules.make_user_router import make_user_router
from app.configs.constants import contact


class AppFactory:
    @staticmethod
    def create_app():
        app = FastAPI(
            contact=contact,
            description="API com rotas customizadas com diversas utilidades",
            docs_url="/docs",
            title="Shipay Backend Challenge",
            version="0.0.1",
            root_path="/api/v1",
        )

        app.include_router(make_auth_router())
        app.include_router(make_claim_router())
        app.include_router(make_role_router())
        app.include_router(make_user_router())

        return app


app = AppFactory.create_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("API Started", app.title, app.description, app.docs_url)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}
