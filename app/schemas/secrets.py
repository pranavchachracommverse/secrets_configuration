from pydantic import BaseModel

class SecretCreateRequest(BaseModel):
    secret_key: str
    secret_value: str  # already MD5-salted by client

class SecretUpdateRequest(BaseModel):
    secret_value: str  # already MD5-salted by client
