import traceback

import discord
import dotenv
from discord.ext import commands

from .database import Database

dotenv.load_dotenv()


class NameColorModal(discord.ui.Modal, title="自己紹介"):
    colorHex = discord.ui.TextInput(
        label="名前色(16進数)",
        placeholder="#は含めないでください。",
        min_length=3,
        max_length=6,
    )

    def __init__(
        self,
        title: str = "名前色変更",
        timeout: float = None,
        custom_id: str = "name_color_buy",
    ):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        row = await Database.pool.fetchrow(
            "SELECT * FROM users WHERE id = $1", interaction.user.id
        )
        if row is not None:
            row = dict(row)
        else:
            row = {}
        if "nyans" not in row or row["nyans"] is None:
            row["nyans"] = 30

        if row["nyans"] < 1000:
            await interaction.followup.send("🐱が足りません。", ephemeral=True)
        else:
            role = discord.utils.get(
                interaction.guild.roles, name=f"{interaction.user.id}"
            )
            if not role:
                role = await interaction.guild.create_role(
                    name=f"{interaction.user.id}"
                )
            await interaction.user.add_roles(role)
            await role.edit(
                colour=discord.Colour.from_str(f"#{self.colorHex.value}"),
                position=interaction.guild.get_member(
                    interaction.client.user.id
                ).top_role.position
                - 1,
            )

            row["nyans"] -= 1000

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

            await interaction.followup.send(
                f"名前色を **#{self.colorHex.value}** に変更しました。", ephemeral=True
            )


class RoleColorView(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(
        emoji=discord.PartialEmoji.from_str("🐱"),
        label="名前色変更",
        style=discord.ButtonStyle.blurple,
        custom_id="name_color_buy",
    )
    async def name_color_buy(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(NameColorModal())


class RoleColorCog(commands.Cog):
    def __init__(self, bot: commands.Bot, view: discord.ui.View):
        self.bot = bot
        self.view = view

    @commands.command(name="sendrcjihanki")
    async def sendrcjihanki(
        self, ctx: commands.Context, channel: discord.TextChannel = None
    ):
        if not channel:
            channel = ctx.channel
        if ctx.author.guild_permissions.administrator:
            embed = discord.Embed(
                title="自販機",
                description="**1000🐱** で 名前の色を変えることができます。",
                color=discord.Colour.from_rgb(0, 0, 255),
            )
            await ctx.channel.send(embed=embed, view=self.view)


async def setup(bot: commands.Bot):
    jihankiview = RoleColorView(timeout=None)
    await bot.add_cog(RoleColorCog(bot, jihankiview))
    bot.add_view(jihankiview)
