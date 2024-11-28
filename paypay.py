import asyncio
import os

import dotenv
from aiopaypaython import PayPay

dotenv.load_dotenv()

paypay = PayPay()


async def main():
    await paypay.initialize(
        phone=os.getenv("paypay_phone"), password=os.getenv("paypay_password")
    )
    print(paypay.client_uuid)
    print(paypay.device_uuid)


asyncio.run(main())
