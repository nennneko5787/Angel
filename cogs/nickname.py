import random
import re
import os
import dotenv

import discord
from discord.ext import commands

from .database import Database

dotenv.load_dotenv()

class NickNameCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="namelock")
    async def namelock(self, ctx: commands.Context, user: discord.Member, lock: bool):
        await ctx.defer()
        if ctx.author.guild_permissions.manage_nicknames:
            await Database.pool.execute(
                """
                INSERT INTO users (id, isnicklocked)
                VALUES ($1, $2)
                ON CONFLICT(id)
                DO UPDATE SET
                    isnicklocked = EXCLUDED.isnicklocked
                """,
                user.id,
                int(lock),
            )
            await ctx.reply("ok")

    @commands.hybrid_command(
        name="nick", description="サーバーでのニックネームを変更します。"
    )
    async def nick(
        self,
        ctx: commands.Context,
        new: str = "",
        randomnick: bool = False,
    ):
        await ctx.defer()
        row = await Database.pool.fetchrow("SELECT * FROM users WHERE id = $1", ctx.author.id)
        if row is not None:
            row = dict(row)
        else:
            row = {}
        if not "isnicklocked" in row or row["isnicklocked"] is None:
            row["isnicklocked"] = False
        member = await ctx.author.edit(nick=new)
        gobi = "。"
        if (
            randomnick
            or row["isnicklocked"]
            or "鯖主" in member.display_name
            or "まんこ" in member.display_name
            or re.match(
                r"(s|S|ｓ|Ｓ)(e|E|ｅ|Ｅ)(x|X|ｘ|Ｘ)", member.display_name
            )
            or re.match(r"ちん(ぽ|こ|ちん)", member.display_name)
            or re.match(
                r"(お|オ|ｵ)(な|ナ|ﾅ)(に|ニ|ﾆ)(ー|-|～)", member.display_name
            )
        ):
            gobi = "（笑）"
            new = random.choice(
                [
                    "Deleted User",
                    "ニーハイが食い込んでるの好き❤",
                    f'{random.choice(["初音ミク", "鏡音リン", "鏡音レン", "巡音ルカ", "MEIKO", "KAITO", "GUMI", "IA"])}大好き❤',
                    "ブルアカは抜ける",
                    "ボカロは神。異論は認めない",
                    "害悪生徒サクッと削除プログラムを起動",
                    self.bot.get_guild(1282708798791745626)
                    .get_member(1261969436232126475)
                    .activity.name,
                    "猫の喫茶店最高！",
                    "おい、抜くなよ。",
                    "初音ミクの胸を盛るな",
                    "everyone",
                    "here",
                    "ゆっくりしていってね",
                    "下ネタは禁止です",
                    "エラー！",
                    "エッチなのはダメ！死刑！！",
                    "(　´∀｀)ｵﾏｴﾓﾅｰ",
                    "I ❤ Iwate",
                    "VSCodeしか勝たん。異論は認めない。",
                ]
            )
        member = await ctx.author.edit(nick=new)
        embed = discord.Embed(
            description=f"ニックネームを`{member.display_name}`に変更しました{gobi}"
        )
        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(NickNameCog(bot))
