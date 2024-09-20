import asyncio
from collections import defaultdict
from datetime import timedelta

import discord
from discord.ext import commands

class AntiSlashCommandSpamCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.messageList: dict[int, list[discord.Message]] = defaultdict(list)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.interaction_metadata:
            return
        
        if len(self.messageList[message.author.id]) >= 5:
            await message.guild.get_member(message.interaction_metadata.user.id).timeout(timedelta(minutes=2))
            for m in self.messageList[message.author.id]:
                await m.delete()
                self.messageList[message.author.id].remove(m)
            embed = discord.Embed(title="Already supported", description=f"User: {message.interaction_metadata.user.mention} `{message.interaction_metadata.user.name}`")
            await self.bot.get_channel(1286652743959707680).send(embed=embed)

        self.messageList[message.author.id].append(message)
        await asyncio.sleep(10)
        self.messageList[message.author.id].remove(message)
        


async def setup(bot: commands.Bot):
    await bot.add_cog(AntiSlashCommandSpamCog(bot))
