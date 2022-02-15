import disnake as discord
from disnake.ext import commands

from config import roles_config
from config.access_config import settings


class UserMenu(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_any_role(roles_config.discord_roles["admin"])
    @commands.slash_command(
        name="user_menu",
        description="Создает меню регистрации",
        guild_ids=[398857722159824907],
    )
    async def user_menu(self, ctx):
        class UserMenuButtons(discord.ui.View):
            @discord.ui.button(label="Обновить БР", style=discord.ButtonStyle.green)
            async def change_battle_rating(self):
                pass

            @discord.ui.button(
                label="Запросить повышение", style=discord.ButtonStyle.green
            )
            async def request_up(self):
                pass

            @discord.ui.button(label="Выбрать войска", style=discord.ButtonStyle.green)
            async def request_up(self):
                pass

            @discord.ui.button(label="Выбрать войска", style=discord.ButtonStyle.link)
            async def request_up(self):
                pass

        buttons = UserMenuButtons()
        embed = discord.Embed(title="test", color=0xE100FF)
        embed.set_thumbnail(url=settings["logoUrl"])

        await ctx.send(embed=embed, view=buttons)


def setup(bot):
    bot.add_cog(UserMenu(bot))
