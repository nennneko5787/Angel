import asyncio
import enum
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import discord
import dotenv
from discord.ext import commands


dotenv.load_dotenv()


class UPType(enum.Enum):
    DICOALL = "DICOALL"
    DCAFE = "DCAFE"
    DISSOKU = "DISSOKU"
    DISBOARD = "DISBOARD"


class UPSiroCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.upCommands: dict[UPType, str] = {
            UPType.DICOALL: "</up:935190259111706754>",
            UPType.DCAFE: "</up:980136954169536525>",
            UPType.DISSOKU: "</dissoku up:828002256690610256>",
            UPType.DISBOARD: "</bump:947088344167366698>",
        }

    async def replyUP(message: discord.Message, *, upType: UPType, hours: int):
        now = datetime.now(ZoneInfo("Asia/Tokyo")) + timedelta(hours=1)
        embed = discord.Embed(
            title="UPを検知しました！",
            description=f"{message.interaction_metadata.user.mention} さん、UPありがとうございます！\n<t:{int(now.timestamp())}> にまた通知をお送りします。\n\n- できれば <#1282980401668816969> もご利用いただけると助かります！",
            color=discord.Colour.og_blurple(),
        )
        await message.reply(embed=embed)
        await asyncio.sleep(hours * 60 * 60)
        embed = discord.Embed(
            title="UPの時間です！",
            description=f"{upType} コマンドを使用して、今すぐUPしましょう！！",
            color=discord.Colour.og_blurple(),
        )
        await message.reply(content="<@&1297475872852414494>", embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        match message.author.id:
            # DICOALL
            case 903541413298450462:
                try:
                    if "成功" in message.embeds[0].description:
                        await self.replyUP(message, upType=UPType.DICOALL, hours=1)
                except:
                    pass
            # DCAFE
            case 850493201064132659:
                try:
                    if "上げました" in message.embeds[0].description:
                        await self.replyUP(message, upType=UPType.DCAFE, hours=1)
                except:
                    pass
            # DISSOKU
            case 761562078095867916:
                try:
                    if "アップ" in message.embeds[0].description:
                        await self.replyUP(message, upType=UPType.DISSOKU, hours=1)
                except:
                    pass
            # DISBOARD
            case 302050872383242240:
                try:
                    if "アップ" in message.embeds[0].description:
                        await self.replyUP(message, upType=UPType.DISBOARD, hours=2)
                except:
                    pass


async def setup(bot: commands.Bot):
    await bot.add_cog(UPSiroCog(bot))
