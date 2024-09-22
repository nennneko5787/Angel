import asyncio
import os
import sys
from contextlib import asynccontextmanager

import discord
import dotenv
from discord.ext import commands
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
    await bot.load_extension(f"cogs.level")
    await bot.load_extension(f"cogs.nickname")
    await bot.load_extension(f"cogs.nyans")
    await bot.load_extension(f"cogs.anticommandspam")
    await bot.load_extension(f"cogs.jihanki")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()
    await Database.loadKyash()
    asyncio.create_task(bot.start(os.getenv("discord")))
    yield
    await Database.pool.close()


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=5757)
