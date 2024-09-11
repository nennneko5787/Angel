import random
import re

import discord
from discord.ext import commands


class NickNameCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="nick", description="サーバーでのニックネームを変更します。"
    )
    async def nick(
        self,
        ctx: commands.Context,
        new: str = None,
        randomnick: bool = False,
    ):
        gobi = "。"
        if (
            randomnick
            or ctx.author.id == 1282293322060271690
            or ctx.author.id == 1067038360654336000
            or ctx.author.id == 967716693474418739
            or "鯖主" in f"{new}"
            or "まんこ" in f"{new}"
            or re.match(r"(s|S|ｓ|Ｓ)(e|E|ｅ|Ｅ)(x|X|ｘ|Ｘ)", new)
            or re.match(r"ちん(ぽ|こ|ちん)", new)
            or re.match(r"(お|オ|ｵ)(な|ナ|ﾅ)(に|ニ|ﾆ)(ー|-|～)", new)
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
        embed = discord.Embed(description=f"ニックネームを`{member.display_name}`に変更しました{gobi}")
        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(NickNameCog(bot))
