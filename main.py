import asyncio
import os
import sys
from contextlib import asynccontextmanager

import discord
import dotenv
from discord.ext import commands, tasks
from fastapi import FastAPI

from cogs.database import Database

dotenv.load_dotenv()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

discord.utils.setup_logging()

bot = commands.Bot("jesus!", intents=discord.Intents.all())


@bot.command("sync")
async def sync(ctx: commands.Context):
    await bot.tree.sync()
    await ctx.message.delete()


@bot.event
async def setup_hook():
    await bot.load_extension("cogs.level")
    await bot.load_extension("cogs.nickname")
    await bot.load_extension("cogs.nyans")
    await bot.load_extension("cogs.anticommandspam")
    await bot.load_extension("cogs.jihanki")
    await bot.load_extension("cogs.auth")
    await bot.load_extension("cogs.rolecolor")
    await bot.load_extension("cogs.bonus")


@tasks.loop(minutes=2)
async def paypayAlive():
    await Database.paypay.alive()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()
    await Database.loadKyash()
    await Database.loadPayPay()
    asyncio.create_task(bot.start(os.getenv("discord")))
    yield
    await Database.pool.close()


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=5757)
