import asyncio

import boto3
from botocore.exceptions import ClientError


class DynamoDBEventLogger:
    def __init__(
        self,
        region: str,
        access_key: str,
        secret_key: str,
        table_name: str,
    ) -> None:
        self._table_name = table_name

        self._dynamodb = boto3.resource(
            "dynamodb",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        self._table = self._dynamodb.Table(table_name)

    async def log_event(
        self,
        city: str,
        timestamp: str,
        storage_key: str,
    ) -> None:
        item = {
            "city": city,
            "timestamp": timestamp,
            "storage_key": storage_key,
        }

        await asyncio.to_thread(
            self._table.put_item,
            Item=item,
        )

    async def ensure_table_exists(self) -> None:
        """
        Optional: Create table if it doesn't exist.
        Useful for local development with DynamoDB Local.
        """
        client = self._dynamodb.meta.client

        try:
            await asyncio.to_thread(
                client.describe_table,
                TableName=self._table_name,
            )
        except ClientError:
            await asyncio.to_thread(
                client.create_table,
                TableName=self._table_name,
                KeySchema=[
                    {"AttributeName": "city", "KeyType": "HASH"},
                    {"AttributeName": "timestamp", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "city", "AttributeType": "S"},
                    {"AttributeName": "timestamp", "AttributeType": "S"},
                ],
                BillingMode="PAY_PER_REQUEST",
            )
