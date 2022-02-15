import datetime

import disnake
import disnake as discord
from disnake.components import SelectOption
from disnake.ext import commands
from disnake.ui import view

from util import ranks_controller


class RankManager(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.slash_command(
        name="down",
        description="Запрашивает понижение конкретного игрока в звании на 1",
        guild_ids=[398857722159824907],
    )
    async def down(self, ctx, user: discord.Member):
        class View(discord.ui.View):
            @discord.ui.select(
                placeholder="Выберите ранг",
                min_values=1,
                max_values=1,
                options=[SelectOption(label="Lol"), SelectOption(label="Kek")],
            )
            async def select_rank(self, select, interaction):
                self.down_rank = select.values[0]

            @discord.ui.button(label="Потвердить", style=discord.ButtonStyle.red)
            async def confirm(self, button, interaction):
                """if interaction.user == ctx.author:
                    await interaction.response.send_message(content='Вы не можете понизить самого себя!',ephemeral=True)
                    return
                if not RankSystem.if_member_can_up_officers(interaction.user):
                    await interaction.response.send_message(content='Вы не можете понижать офицеров!',ephemeral=True)
                    return
                if not RankSystem.if_rank_member1_above_member2(interaction.user, ctx.author):
                    await interaction.response.send_message(content='Вы не можете понижать игроков, у которых ранг выше вашего!',ephemeral=True)
                    return"""
                await ctx.author.remove_roles(
                    ctx.guild.get_role(ranks_controller.get_rank_id_by_name(user_rank))
                )
                await ctx.author.add_roles(
                    ctx.guild.get_role(
                        ranks_controller.get_rank_id_by_name(self.down_rank)
                    )
                )
                await ctx.author.send(f"Ваc позизили в ранге до {self.down_rank}.")
                self.clear_items()
                embed = message.embeds[0]
                embed.color = 0xC03537
                embed.title = "Потверждение"
                embed.add_field(
                    name="Понижен:",
                    value=interaction.user.mention + f"\n||{interaction.user}||",
                    inline=False,
                )
                await message.edit(embed=embed, view=self)
                self.stop()

            @discord.ui.button(label="Отмена", style=discord.ButtonStyle.grey)
            async def cancel(self, button, interaction):
                await message.delete()

        view = View()

        rank_list = []
        user_rank = ranks_controller.get_member_rank(user, str=True)
        ranks = ranks_controller.get_all_ranks_name()
        index = ranks.index(user_rank) - 1
        embed = discord.Embed(title="Понижение", color=0xF2930D)
        embed.add_field(
            name=f"Вы собираетесь понизить {ctx.author.nick} в ранге",
            value=f"Ранг на момент понижения: {user_rank}\n\nУпоминание: {ctx.author.mention}",
            inline=True,
        )

        for i in range(index, -1, -1):
            rank_list.append(SelectOption(label=ranks[i]))

        view.children[0].options = rank_list

        message = await ctx.send(embed=embed, view=view)

    @commands.slash_command(
        name="up",
        description="Запрашивает повышение вызвавшего игрока в звании на 1",
        guild_ids=[398857722159824907],
    )
    async def up(self, ctx):
        class View(disnake.ui.View):
            @discord.ui.button(label="Повысить", style=disnake.ButtonStyle.green)
            async def rank_up(self, button, interaction):
                new_rank = ranks_controller.get_next_member_rank(ctx.author)
                if interaction.user == ctx.author:
                    await interaction.response.send_message(
                        content="Вы не можете повысить самого себя!", ephemeral=True
                    )
                    return
                if new_rank in ranks_controller.get_officers_ranks_id():
                    if not ranks_controller.if_member_can_up_officers(interaction.user):
                        await interaction.response.send_message(
                            content="Вы не можете повышать офицеров!", ephemeral=True
                        )
                        return
                if not ranks_controller.if_rank_member1_above_member2(
                    ctx.author, interaction.user
                ):
                    await interaction.response.send_message(
                        content="Вы не можете повышать игроков, у которых ранг выше вашего!",
                        ephemeral=True,
                    )
                    return
                await ctx.author.remove_roles(
                    ctx.guild.get_role(ranks_controller.get_rank_id_by_name(rank))
                )
                await ctx.author.add_roles(ctx.guild.get_role(new_rank))
                await ctx.author.send("Ваc повысили.")
                self.clear_items()
                embed = message.embeds[0]
                embed.color = 0x38A22A
                embed.title = "Принято"
                embed.add_field(
                    name="Повышен:",
                    value=interaction.user.mention + f"\n||{interaction.user}||",
                    inline=False,
                )
                await message.edit(embed=embed, view=self)
                self.stop()

            @discord.ui.button(label="Отказ", style=disnake.ButtonStyle.red)
            async def deny(self, button, interaction):
                if interaction.user == ctx.author:
                    await interaction.response.send_message(
                        content="Вы не можете повысить самого себя!", ephemeral=True
                    )
                    return
                if not ranks_controller.if_member_can_up_officers(interaction.user):
                    await interaction.response.send_message(
                        content="Вы не можете повышать офицеров!", ephemeral=True
                    )
                    return
                if not ranks_controller.if_rank_member1_above_member2(
                    interaction.user, ctx.author
                ):
                    await interaction.response.send_message(
                        content="Вы не можете повышать игроков, у которых ранг выше вашего!",
                        ephemeral=True,
                    )
                    return
                await ctx.author.send(
                    "Вам отказали в повышение. Следующий запрос возможен через неделю."
                )
                self.clear_items()
                embed = message.embeds[0]
                embed.color = 0xDE3B3B
                embed.title = "Отказ"
                await message.edit(embed=embed, view=self)
                self.stop()

        view = View()
        rank = ranks_controller.get_member_rank(ctx.author, str=True)
        now = datetime.datetime.now(datetime.timezone.utc)

        if rank in ["OF-8", "OF-9", "OF-10"]:
            await ctx.author.send(
                "Вы заняли максимальное ранг в нашем полке. Подача заявки на повышение для вас закрыта."
            )
            return

        timedelta = now - ctx.author.joined_at
        seconds = timedelta.total_seconds()
        days = seconds // 86400
        month = days // 30
        days = days - (month * 30)

        datestr = f"{int(month)} месяцев и {int(days)} дней"

        embed = discord.Embed(title="Запрос на повышение", color=0xF2930D)
        embed.add_field(
            name=f"Игрок {ctx.author.nick} запрашивает повышение.",
            value=f"Ранг на момент подачи заявки: {rank}\n\nУпоминание: {ctx.author.mention}",
            inline=True,
        )
        embed.set_footer(text=f"На сервере {datestr}")
        message = await ctx.send(embed=embed, view=view)


def setup(client):
    client.add_cog(RankManager(client))
