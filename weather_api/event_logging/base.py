from typing import Protocol


class EventLogger(Protocol):
    async def log_event(
        self,
        city: str,
        timestamp: str,
        storage_key: str,
    ) -> None: ...
