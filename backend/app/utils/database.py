import aiomysql
from aiomysql import Pool, Connection, Cursor


class Database:
    def __init__(self, host: str, user: str, password: str, db: str, port=3306, loop=None):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.loop = loop

    async def connect(self):
        self.pool: Pool = await aiomysql.create_pool(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            port=self.port,
            loop=self.loop
        )

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            conn: Connection
            async with conn.cursor() as cur:
                cur: Cursor
                await cur.execute(query, args)
                await conn.commit()
                return cur.lastrowid

    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            conn: Connection
            async with conn.cursor() as cur:
                cur: Cursor
                await cur.execute(query, args)
                return await cur.fetchall()

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()