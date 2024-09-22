import os

import asyncpg
import dotenv
from aiokyasher import Kyash

dotenv.load_dotenv()


class Database:
    pool: asyncpg.Pool = None
    kyash: Kyash = Kyash()

    @classmethod
    async def loadKyash(cls):
        await cls.kyash.login(
            os.getenv("kyash_email"),
            os.getenv("kyash_password"),
            os.getenv("kyash_client_uuid"),
            os.getenv("kyash_installation_uuid"),
        )

    @classmethod
    async def connect(cls):
        cls.pool = await asyncpg.create_pool(os.getenv("dsn"), statement_cache_size=0)
