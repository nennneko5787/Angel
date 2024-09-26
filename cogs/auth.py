import io
import random, string

import discord
import dotenv
from discord.ext import commands
from multicolorcaptcha import CaptchaGenerator

dotenv.load_dotenv()


class CaptchaSelect(discord.ui.Select["CaptchaView"]):
    def __init__(self, characters: str):
        super().__init__()
        self.characters = characters
        options = [
            discord.SelectOption(label=self.randomChars(4).upper()) for i in range(9)
        ]
        options.append(discord.SelectOption(label=self.characters.upper()))
        random.shuffle(options)
        self.options = options

    def randomChars(self, n) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=n))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        assert self.view is not None
        if self.values[0] == self.characters:
            await interaction.user.add_roles(
                interaction.guild.get_role(1288776710673797173)
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="認証が完了しました。",
                    description="引き続き、猫の喫茶店でおくつろぎください！",
                    colour=discord.Colour.og_blurple(),
                ),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="認証に失敗しました。",
                    description="もう一度「**captchaで認証**」ボタンを押して認証するか、「**簡単に認証**」ボタンを押してください。",
                    colour=discord.Colour.red(),
                ),
                ephemeral=True,
            )
        return True


class CaptchaView(discord.ui.View):
    def __init__(self, characters: str, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(CaptchaSelect(characters))


class AuthPanelView(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)
        self.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.blurple,
                label="簡単に認証",
                url="https://discord.com/oauth2/authorize?client_id=1096727990655778876&response_type=code&redirect_uri=https%3A%2F%2Fbedrock.aa-bot.com%2F&scope=identify%20guilds.join&state=11CD18DB3E40005A",
            )
        )

    @discord.ui.button(
        label="captchaで認証",
        style=discord.ButtonStyle.gray,
        custom_id="auth_with_captcha",
    )
    async def captcha(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        generator = CaptchaGenerator(2)
        captcha = generator.gen_captcha_image(difficult_level=3, chars_mode="ascii")
        image = captcha.image
        characters = captcha.characters

        fileio = io.BytesIO()
        image.save(fileio, format="png")
        fileio.seek(0)
        file = discord.File(fileio, filename="captcha.png")
        embed = discord.Embed(
            title="Angel Captcha v1",
            description="**3分以内に**、この画像に表示されている文字列を下のセレクトメニューより選択してください。",
        ).set_image(url="attachment://captcha.png")
        await interaction.response.send_message(
            embed=embed, file=file, view=CaptchaView(characters), ephemeral=True
        )


class AuthCog(commands.Cog):
    def __init__(self, bot: commands.Bot, view: discord.ui.View):
        self.bot = bot
        self.view = view

    @commands.command(name="sendauth")
    async def sendauth(
        self, ctx: commands.Context, channel: discord.TextChannel = None
    ):
        if not channel:
            channel = ctx.channel
        if ctx.author.guild_permissions.administrator:
            embed = discord.Embed(
                title="認証",
                description="「**captchaで認証**」ボタン、または「**簡単に認証**」ボタンを押してください",
                color=discord.Colour.og_blurple(),
            )
            await ctx.channel.send(embed=embed, view=self.view)


async def setup(bot: commands.Bot):
    authpanelView = AuthPanelView(timeout=None)
    await bot.add_cog(AuthCog(bot, authpanelView))
    bot.add_view(authpanelView)
