from typing import Dict, List, Optional

from app.config.settings import BUCKET_NAME, REGION_NAME, APP_BASE_PATH
from simpledocumentstore.documentstore.simple_document_store_aws import SimpleDocumentStoreAWS

class SecretsStore:
    """
    Persists only secret metadata (key, arn) in S3 via SimpleDocumentStore.
    Folder structure (under bucket):
      {APP_BASE_PATH}/System/Secrets/{secret_key}/data.json
    """

    def __init__(self):
        self.sds = SimpleDocumentStoreAWS(
            store_name=BUCKET_NAME,
            region_name=REGION_NAME,
            base_directory=APP_BASE_PATH,
        )
        self._root = f"{APP_BASE_PATH}/System/Secrets"

    def _key_for_secret(self, secret_key: str) -> str:
        # Each secret has its own folder to keep fetch/get simple
        return f"{self._root}/{secret_key}"

    def _key_for_all(self) -> str:
        return self._root

    def save(self, *, secret_key: str, secret_arn: str) -> None:
        """
        Upsert-like behavior: write the metadata JSON for a secret.
        """
        doc = {"secret_key": secret_key, "secret_arn": secret_arn}
        self.sds.post(key=self._key_for_secret(secret_key), json_data=doc)

    def get(self, *, secret_key: str) -> Optional[Dict]:
        """
        Returns {'secret_key': ..., 'secret_arn': ...} or None.
        """
        result = self.sds.fetch(key=self._key_for_secret(secret_key))
        if isinstance(result, list) and len(result) > 0:
            # Each folder returns merged list; we write a single JSON file so index 0 is fine
            return result[0]
        return None

    def list_all(self) -> List[Dict]:
        """
        Returns list of {'secret_key', 'secret_arn'} across all secrets.
        """
        result = self.sds.fetch(key=self._key_for_all())
        return result if isinstance(result, list) else []
