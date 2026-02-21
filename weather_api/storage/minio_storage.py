import asyncio
import json
from typing import Any

import boto3
from botocore.exceptions import ClientError


class MinioStorage:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
    ) -> None:
        self._bucket = bucket
        self._s3 = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    async def save(self, key: str, data: dict[str, Any]) -> str:
        body = json.dumps(data).encode("utf-8")
        await asyncio.to_thread(
            self._s3.put_object,
            Bucket=self._bucket,
            Key=key,
            Body=body,
            ContentType="application/json",
        )
        return key

    async def ensure_bucket_exists(self) -> None:
        try:
            await asyncio.to_thread(self._s3.head_bucket, Bucket=self._bucket)
        except ClientError:
            await asyncio.to_thread(self._s3.create_bucket, Bucket=self._bucket)
