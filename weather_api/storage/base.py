from typing import Protocol


class Storage(Protocol):
    async def save(self, key: str, data: dict) -> str: ...
