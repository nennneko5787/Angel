import traceback

import discord
import dotenv
from discord.ext import commands

from .database import Database

dotenv.load_dotenv()


class JihankiModal(discord.ui.Modal, title="自己紹介"):
    kyashLink = discord.ui.TextInput(label="Kyashの送金リンク")

    def __init__(
        self,
        title: str = "Kyashで🐱を購入",
        timeout: float = None,
        custom_id: str = "buy_with_kyash",
    ):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            linkData = await Database.kyash.link_check(self.kyashLink.value)
            print(linkData)
            await Database.kyash.link_recieve(url=self.kyashLink.value)

            row = await Database.pool.fetchrow(
                "SELECT * FROM users WHERE id = $1", interaction.user.id
            )
            if row is not None:
                row = dict(row)
            else:
                row = {}
            if "nyans" not in row or row["nyans"] is None:
                row["nyans"] = 30

            row["nyans"] += linkData["result"]["data"]["transaction"]["amount"] / 0.0001

            await Database.pool.execute(
                """
                INSERT INTO users (id, nyans)
                VALUES ($1, $2)
                ON CONFLICT(id)
                DO UPDATE SET
                    nyans = EXCLUDED.nyans
                """,
                interaction.user.id,
                row["nyans"],
            )

            embed = discord.Embed(
                title="自販機を使ったユーザーが居るらしい",
                description=f'ユーザー: {interaction.user.mention}\n購入した🐱の数: {linkData["result"]["data"]["transaction"]["amount"] / 0.0001}',
                colour=discord.Colour.og_blurple(),
            )
            await interaction.guild.get_channel(1286652743959707680).send(embed=embed)

            embed = discord.Embed(
                title="購入が完了しました",
                description="購入できていない場合は、管理者 <@1048448686914551879> までお問い合わせください。",
                colour=discord.Colour.og_blurple(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            traceback.print_exc()
            exception = traceback.format_exc()
            embed = discord.Embed(
                title="自販機でのエラー",
                description=f"```py\n{exception}\n```",
                colour=discord.Colour.red(),
            )
            await interaction.guild.get_channel(1286652743959707680).send(embed=embed)
            embed = discord.Embed(
                title="エラーが発生しました",
                description=f"{e}\n-# エラー内容は管理者に送信されました。修正までしばらくお待ち下さい。",
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)


class JihankiView(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(
        emoji=discord.PartialEmoji.from_str("<:kyash:1287303826575065089>"),
        label="Kyashで購入",
        style=discord.ButtonStyle.blurple,
        custom_id="buy_with_kyash",
    )
    async def ok(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(JihankiModal())


class JikankiCog(commands.Cog):
    def __init__(self, bot: commands.Bot, view: discord.ui.View):
        self.bot = bot
        self.view = view

    @commands.command(name="sendjihanki")
    async def sendjihanki(
        self, ctx: commands.Context, channel: discord.TextChannel = None
    ):
        if not channel:
            channel = ctx.channel
        if ctx.author.guild_permissions.administrator:
            embed = discord.Embed(
                title="自販機",
                description="1 Kyashバリュー / 1 Kyashマネー で 10000コインを購入することができます",
                color=discord.Colour.from_rgb(0, 0, 255),
            )
            await ctx.channel.send(embed=embed, view=self.view)


async def setup(bot: commands.Bot):
    jihankiview = JihankiView(timeout=None)
    await bot.add_cog(JikankiCog(bot, jihankiview))
    bot.add_view(jihankiview)