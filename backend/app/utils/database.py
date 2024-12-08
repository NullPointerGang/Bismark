import os
import aiosqlite
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv("DB_PATH", "database.db")  # Set the default DB path
        self.db = None

    async def connect(self):
        self.db = await aiosqlite.connect(self.db_path)

    async def execute(self, query, *args):
        async with self.db.cursor() as cur:
            await cur.execute(query, args)
            await self.db.commit()
            return cur.lastrowid

    async def fetch(self, query, *args):
        async with self.db.cursor() as cur:
            await cur.execute(query, args)
            return await cur.fetchall()

    async def close(self):
        await self.db.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()


class DatabaseTables:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv("DB_PATH", "database.db")
        self.db = None

    async def create_tables(self):
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )
                """)
                await conn.commit()

