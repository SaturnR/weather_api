import asyncio
import sqlite3


class SQLiteEventLogger:
    def __init__(self, db_path: str = "events.db") -> None:
        self._db_path = db_path
        self._initialize_db()

    def _initialize_db(self) -> None:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                storage_key TEXT NOT NULL
            )
            """
        )

        conn.commit()
        conn.close()

    async def log_event(
        self,
        city: str,
        timestamp: str,
        storage_key: str,
    ) -> None:
        await asyncio.to_thread(
            self._insert_event,
            city,
            timestamp,
            storage_key,
        )

    def _insert_event(self, city: str, timestamp: str, storage_key: str) -> None:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO weather_events (city, timestamp, storage_key)
            VALUES (?, ?, ?)
            """,
            (city, timestamp, storage_key),
        )

        conn.commit()
        conn.close()
