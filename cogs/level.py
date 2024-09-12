import random

import aiosqlite
import discord
from discord.ext import commands


class LevelCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="profile", description="ユーザーのレベルや経験値などの情報を確認します。"
    )
    async def profileCommand(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            user = ctx.author
        async with aiosqlite.connect("level.db") as db:
            async with db.execute(
                "SELECT * FROM users WHERE id = ?", (user.id,)
            ) as cursor:
                row = await cursor.fetchone()

                if not row:
                    row = (ctx.author.id, 0, 0)

                embed = discord.Embed(
                    title=f"{user.display_name} の情報",
                    description=f"**レベル**: {row[1]}\n経験値: {row[2]} / {500 * row[1]}",
                    color=discord.Colour.og_blurple(),
                ).set_thumbnail(url=user.display_avatar.url)

                await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        async with aiosqlite.connect("level.db") as db:
            async with db.execute(
                "SELECT * FROM users WHERE id = ?", (message.author.id,)
            ) as cursor:
                row = await cursor.fetchone()

                if not row:
                    row = [message.author.id, 0, 0]
                else:
                    row = list(row)  # Convert tuple to list to modify values

                row[2] += random.randint(1, 25)  # Add random experience

                if row[2] >= 500 * row[1]:
                    row[1] += 1
                    row[2] = 0

                    await self.bot.get_channel(1282718839683154008).send(
                        f"🥳 **{message.author.mention}** さんのレベルが **{row[1] - 1}** から **{row[1]}** に上がりました 🎉"
                    )

            # Insert or update user data
            await db.execute(
                """
                INSERT INTO users (id, level, exp)
                VALUES (?, ?, ?)
                ON CONFLICT(id)
                DO UPDATE SET
                    level = excluded.level,
                    exp = excluded.exp
                """,
                (message.author.id, row[1], row[2]),
            )
            await db.commit()


async def setup(bot: commands.Bot):
    await bot.add_cog(LevelCog(bot))
