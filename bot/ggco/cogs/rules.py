import disnake as discord
from disnake.ext import commands

from config import roles_config


class Rules(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_any_role(roles_config.discord_roles["admin"])
    @commands.slash_command(name="rules", description="Отправляет правила")
    async def rules(self, ctx):
        embed = discord.Embed(title="Общие правила", color=0xE100FF)
        embed.add_field(
            name="\u200b",
            value="```css\n1.1 На этом сервере не допускается расовая нетерпимость или крайняя ненависть любого рода.\n[Бан или предупреждение, в зависимости от содержания]```",
            inline=False,
        )

        embed.add_field(
            name="\u200b",
            value="```css\n1.2 Не будьте токсиком, который портит веселье другим. Это включает в себя нацеливание на одного человека и обсирание его.\n[Бан или предупреждение, в зависимости от содержания]```",
            inline=False,
        )

        embed.add_field(
            name="\u200b",
            value="```css\n1.3 Не сливайте личную информацию о других членах сервера без их разрешения. Это относится и к личке.\n[Предупреждение или бан в зависимости от серьезности утечки]```",
            inline=False,
        )

        embed.add_field(
            name="\u200b",
            value="```css\n1.4 Не публикуйте nsfw-контент вне #nsfw.\n[Бан]```",
            inline=False,
        )

        embed.add_field(
            name="\u200b",
            value="```css\n1.5 Не выдавайте себя за ботов или любого члена сервера. (Через имя, ник или картинку профиля)\n[Предупреждение и бан в случае продолжения]```",
            inline=False,
        )

        embed.add_field(
            name="\u200b",
            value="```css\n1.6 Запрещен спам ЛЮБОГО рода, включая @everyone/@here спам, спам реакции, копирование/вставка текста, @mentions в AFK.\n[Предупреждению и бан в случае продолжения.]```",
            inline=False,
        )

        embed.add_field(
            name="\u200b",
            value="```css\n1.7 Не пингуйте роли без веской причины. Пингуйте роли только в экстренных случаях.\n[Предупреждение]```",
            inline=False,
        )

        embed.add_field(
            name="\u200b",
            value="```css\n1.8 Не выпрашивать роль/звание. Нам это не нужно, и если мы посчитаем, что вы заслуживаете роли, мы вам ее дадим.\n[Предупреждение]```",
            inline=False,
        )

        embed.add_field(
            name="\u200b",
            value="```css\n1.9 Используйте каналы по назначению, (в каналах «музыка» – запускайте музыку и т.д)\n[Устное предупреждение и предупреждение в случае продолжения]```",
            inline=False,
        )

        embed.add_field(
            name="\u200b",
            value="```css\n1.10 Не вступайте в дискуссию с офицерами на сервере после решения о наказании (например, получения предупреждения), если вы считаете, что предупреждение было неправильным, пожалуйста, решите этот вопрос в личке с тем, кто выписал предупредил.\n[Предупреждение]```",
            inline=False,
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Rules(bot))
