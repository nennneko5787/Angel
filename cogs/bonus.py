import os
import random
from datetime import timedelta

import asyncpg
import discord
import dotenv
from discord.ext import commands

from .database import Database

dotenv.load_dotenv()


class BonusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await ctx.defer()
        row = await Database.pool.fetchrow(
            "SELECT * FROM users WHERE id = $1", ctx.author.id
        )
        if row is not None:
            row = dict(row)
        else:
            row = {}
        if "nyans" not in row or row["nyans"] is None:
            row["nyans"] = 30

        if random.randint(0, 15) != 1:
            return
        
        row["nyans"] += 1

        embed = discord.Embed(
            title="ボーナスコインを獲得しました。",
            description=f"1🐱増えた！",
            colour=discord.Colour.og_blurple(),
        )
        await message.author.send(embed=embed)
        print(row["nyans"])

        await Database.pool.execute(
            """
            INSERT INTO users (id, nyans)
            VALUES ($1, $2)
            ON CONFLICT(id)
            DO UPDATE SET
                nyans = EXCLUDED.nyans
            """,
            ctx.author.id,
            row["nyans"],
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(BonusCog(bot))
