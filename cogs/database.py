import os

import asyncpg
import dotenv
from aiokyasher import Kyash
from aiopaypaython import PayPay

dotenv.load_dotenv()


class Database:
    pool: asyncpg.Pool = None
    kyash: Kyash = Kyash()
    paypay: PayPay = PayPay()

    @classmethod
    async def loadKyash(cls):
        await cls.kyash.login(
            os.getenv("kyash_email"),
            os.getenv("kyash_password"),
            os.getenv("kyash_client_uuid"),
            os.getenv("kyash_installation_uuid"),
        )

    @classmethod
    async def loadPayPay(cls):
        try:
            await cls.paypay.initialize(access_token=os.getenv("paypay_access_token"))
        except:
            try:
                mae_access_token = os.getenv("paypay_access_token")
                mae_refresh_token = os.getenv("paypay_refresh_token")
                await cls.paypay.token_refresh(os.getenv("paypay_refresh_token"))
                with open(".env", "w", encoding="utf-8") as f:
                    envFile = f.read()
                    envFile = envFile.replace(
                        f"paypay_access_token={mae_access_token}",
                        f'paypay_access_token={os.getenv("paypay_access_token")}',
                    )
                    envFile = envFile.replace(
                        f"paypay_refresh_token={mae_refresh_token}",
                        f'paypay_refresh_token={os.getenv("paypay_refresh_token")}',
                    )
                    f.write(envFile)
                dotenv.load_dotenv()
                await cls.paypay.initialize(
                    access_token=os.getenv("paypay_access_token")
                )
            except:
                await cls.paypay.initialize(
                    phone=os.getenv("paypay_phone"),
                    password=os.getenv("paypay_password"),
                    device_uuid=os.getenv("paypay_device_uuid"),
                    client_uuid=os.getenv("paypay_client_uuid"),
                )

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
