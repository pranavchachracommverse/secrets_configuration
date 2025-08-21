from fastapi import FastAPI

from app.api.secrets_router import secrets_router

app = FastAPI(
    title="Trader Market Intel Platform API",
    docs_url="/Platform/Api/docs",
    openapi_url="/Platform/Api/openapi.json"
)

app.include_router(secrets_router, prefix="/Platform/Admin/secrets", tags=["Secrets"])

