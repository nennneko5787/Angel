import asyncio
import os
import sys

import discord
import dotenv
from discord.ext import commands

dotenv.load_dotenv()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

bot = commands.Bot("jesus!", intents=discord.Intents.all())


@bot.command("sync")
async def sync(ctx: commands.Context):
    await bot.tree.sync()
    await ctx.message.delete()


@bot.event
async def setup_hook():
    await asyncio.gather(
        *[
            bot.load_extension(f"cogs.{cog[:-3]}")
            for cog in os.listdir("cogs")
            if cog.endswith(".py")
        ]
    )


bot.run(os.getenv("discord"))
