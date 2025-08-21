from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.models.generic_response_model import GenericApiResponse

from app.schemas.secrets import SecretCreateRequest, SecretUpdateRequest
from app.services.secrets_manager import SecretsManagerService
from app.services.secrets_store import SecretsStore

secrets_router = APIRouter()

_secrets_mgr = SecretsManagerService()
_store = SecretsStore()

@secrets_router.post("/")
def create_secret(payload: SecretCreateRequest):
    """
    Create Secret:
    - Body contains secret_key, secret_value (already MD5-salted by client).
    - Creates/Registers secret in AWS Secrets Manager.
    - Stores {secret_key, secret_arn} in simpledocumentstore (S3) under APP_BASE_PATH.
    """
    try:
        # Check if metadata already exists
        existing = _store.get(secret_key=payload.secret_key)
        if existing:
            raise HTTPException(status_code=400, detail="Secret already exists")

        arn = _secrets_mgr.create_secret(secret_key=payload.secret_key, secret_value=payload.secret_value)
        _store.save(secret_key=payload.secret_key, secret_arn=arn)

        return JSONResponse(
            content=GenericApiResponse.success_response(
                {"secret_key": payload.secret_key, "secret_arn": arn}
            ).model_dump()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))


@secrets_router.post("/fetch")
def list_secrets():
    """
    List Secrets:
    - Returns list of {secret_key, secret_arn}.
    - Never returns the secret value.
    """
    try:
        items = _store.list_all()
        return JSONResponse(
            content=GenericApiResponse.success_response(items).model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))


@secrets_router.get("/{secret_key}")
def view_secret(secret_key: str):
    """
    View Secret (metadata only):
    - Returns {secret_key, secret_arn}.
    - Never returns the secret value.
    """
    try:
        item = _store.get(secret_key=secret_key)
        if not item:
            raise HTTPException(status_code=404, detail="Secret not found")
        return JSONResponse(
            content=GenericApiResponse.success_response(item).model_dump()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))


@secrets_router.put("/{secret_key}")
def modify_secret(secret_key: str, payload: SecretUpdateRequest):
    """
    Modify Secret:
    - Body contains secret_value (MD5 salted).
    - Updates value in AWS Secrets Manager. Metadata (ARN) remains same.
    """
    try:
        # Ensure secret exists in our metadata store
        item = _store.get(secret_key=secret_key)
        if not item:
            raise HTTPException(status_code=404, detail="Secret not found")

        _secrets_mgr.update_secret(secret_key=secret_key, secret_value=payload.secret_value)
        return JSONResponse(
            content=GenericApiResponse.success_response("Secret updated successfully").model_dump()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))
