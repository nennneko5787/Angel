import random
import os
import dotenv

import asyncpg
import discord
from discord.ext import commands

from .database import Database

dotenv.load_dotenv()

class LevelCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="profile", description="ユーザーのレベルや経験値などの情報を確認します。"
    )
    async def profileCommand(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            user = ctx.author
        await ctx.defer()
        row = await Database.pool.fetchrow("SELECT * FROM users WHERE id = $1", user.id)
        if row is not None:
            row = dict(row)
        else:
            row = {}

        if "level" not in row or row["level"] is None:
            row["level"] = 0
        if "exp" not in row or row["exp"] is None:
            row["exp"] = 0
        if "nyans" not in row or row["nyans"] is None:
            row["nyans"] = 30

        embed = discord.Embed(
            title=f"{user.display_name} の情報",
            description=f'**レベル**: {row["level"]}\n経験値: {row["exp"]} / {120 * row["level"]}\n🐱(にゃん): {row["nyans"]}',
            color=discord.Colour.og_blurple(),
        ).set_thumbnail(url=user.display_avatar.url)

        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.content.startswith("jesus!"):
            return

        row = await Database.pool.fetchrow("SELECT * FROM users WHERE id = $1", message.author.id)
        if row is not None:
            row = dict(row)
        else:
            row = {}
        if "level" not in row or row["level"] is None:
            row["level"] = 0
        if "exp" not in row or row["exp"] is None:
            row["exp"] = 0
        row["exp"] += random.randint(1, 25)  # Add random experience

        if row["exp"] >= 120 * row["level"]:
            row["level"] += 1
            row["exp"] -= 120 * (
                row["level"] - 1
            )  # Subtract the experience needed for the previous level

            await self.bot.get_channel(1282718839683154008).send(
                f"🥳 **{message.author.mention}** さんのレベルが **{row['level'] - 1}** から **{row['level']}** に上がりました 🎉"
            )

        # Insert or update user data
        await Database.pool.execute(
            """
            INSERT INTO users (id, level, exp)
            VALUES ($1, $2, $3)
            ON CONFLICT(id)
            DO UPDATE SET
                level = EXCLUDED.level,
                exp = EXCLUDED.exp
            """,
            message.author.id, row["level"], row["exp"],
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(LevelCog(bot))
