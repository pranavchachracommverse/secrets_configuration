import boto3
from botocore.exceptions import ClientError
from app.config.settings import REGION_NAME, APP_ENV

class SecretsManagerService:
    """
    Thin wrapper over AWS Secrets Manager.
    - We use secret name convention: {ENV}/{secret_key}
    """

    def __init__(self):
        self.client = boto3.client("secretsmanager", region_name=REGION_NAME)

    def _name(self, secret_key: str) -> str:
        return f"{APP_ENV}/{secret_key}"

    def create_secret(self, *, secret_key: str, secret_value: str) -> str:
        """
        Creates a new secret. If a secret already exists with same name, raises HTTP 400 upstream.
        """
        try:
            resp = self.client.create_secret(
                Name=self._name(secret_key),
                SecretString=secret_value
            )
            return resp["ARN"]
        except ClientError as e:
            # Bubble up, router converts to HTTP response
            raise e

    def update_secret(self, *, secret_key: str, secret_value: str) -> None:
        """
        Updates the value for an existing secret.
        """
        try:
            # Prefer put_secret_value if versions exist; update_secret also works but may require perms.
            self.client.put_secret_value(
                SecretId=self._name(secret_key),
                SecretString=secret_value
            )
        except ClientError as e:
            raise e
