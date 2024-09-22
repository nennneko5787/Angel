import os
import random
from datetime import timedelta

import asyncpg
import discord
import dotenv
from discord.ext import commands

from .database import Database

dotenv.load_dotenv()


class NyansCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="roulette", description="5🐱を消費しルーレットを引きます"
    )
    async def roulette(self, ctx: commands.Context):
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

        if row["nyans"] < -100:
            embed = discord.Embed(
                title="借金のし過ぎです！！",
                description="精算し、5分のタイムアウトを開始します。",
                colour=discord.Colour.red(),
            )
            await ctx.author.timeout(timedelta(minutes=5))
            row["nyans"] = 0
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
            return
        elif row["nyans"] < 5:
            embed = discord.Embed(
                title="🐱が足りません！",
                description="借金を開始 または 利息が増えます",
                colour=discord.Colour.red(),
            )
            await ctx.reply(embed=embed)
            row["nyans"] -= 2

        amount = random.randint(random.randint(-5, 0), random.randint(0, 15))
        row["nyans"] += amount

        embed = discord.Embed(
            title="抽選の結果",
            description=f"{amount}🐱増えた！",
            colour=discord.Colour.og_blurple(),
        )
        await ctx.reply(embed=embed)
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
    await bot.add_cog(NyansCog(bot))
