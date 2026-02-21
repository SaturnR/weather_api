import asyncio
import json
from typing import Any

import boto3
from botocore.exceptions import ClientError


class S3Storage:
    def __init__(
        self,
        region: str,
        access_key: str,
        secret_key: str,
        bucket: str,
    ) -> None:
        self._bucket = bucket

        self._s3 = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    async def save(self, key: str, data: dict[str, Any]) -> str:
        """
        Save JSON data to AWS S3 bucket.
        Returns object key.
        """
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
        """
        Ensure bucket exists.
        In AWS this typically isn't auto-created,
        but we include safe check for completeness.
        """
        try:
            await asyncio.to_thread(self._s3.head_bucket, Bucket=self._bucket)
        except ClientError:
            await asyncio.to_thread(self._s3.create_bucket, Bucket=self._bucket)
