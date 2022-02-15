import disnake as discord
import pymysql
from disnake import Client
from disnake.ext import commands

from config import roles_config as rc
from config.access_config import settings
from config.bd_config import CONFIG
from util import ranks_controller
from util.ranks_controller import get_officers_ranks_name

client = Client()


async def get_medal_info(medal_id):
    if medal_id == 1:
        return "Медаль выдается за уничтожение 4 и более наземной техники на наземной технике"
    elif medal_id == 2:
        return "Медаль выдается за захват трёх точек за бой"
    elif medal_id == 3:
        return "Медаль выдается за уничтожение 3 и более воздушной техники на наземной технике"
    elif medal_id == 4:
        return "Медаль выдается за уничтожение 3 и более воздушной техники на наземной технике"
    elif medal_id == 5:
        return "Медаль выдается за уничтожение 3 и более наземной техники на вертолёте"
    elif medal_id == 6:
        return "Медаль выдается за оказание помощи в уничтожении техники 4 и более раз"
    elif medal_id == 7:
        return "Медаль выдается за уничтожение 3 и более наземной техники на воздушной технике"
    elif medal_id == 8:
        return "Медаль выдается за уничтожение 2 техники противника одной бомбой/ракетой/снарядом"
    elif medal_id == 9:
        return "Медаль выдается за победу в бою, оставшись последним в команде на воздушной технике"
    elif medal_id == 10:
        return "Медаль выдается за победу в бою, оставшись последним в команде на наземной технике"
    elif medal_id == 11:
        return "Медаль выдается за уничтожение техники противника артиллерией"
    elif medal_id == 12:
        return "Медаль выдается за достижение 1500 и более очков за сезон	"
    elif medal_id == 13:
        return "Медаль выдается за особые заслуги в жизни полка"
    elif medal_id == 14:
        return "Мы ещё не придумали описание для этой медали"
    elif medal_id == 15:
        return "Мы ещё не придумали описание для этой медали"
    elif medal_id == 16:
        return "Мы ещё не придумали описание для этой медали"
    else:
        return "Такой медали не существует"


class BDTest(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = pymysql.connect(
            host=CONFIG["host"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=CONFIG["db"],
        )

    @commands.has_any_role(rc.discord_roles["admin"])
    @commands.slash_command(
        name="medal",
        description="Выдать медаль @Пользователь №Медали",
        guild_ids=[398857722159824907],
    )
    async def medal(
            self,
            ctx: discord.ApplicationCommandInteraction,
            user: discord.Member,
            medal_id: int,
    ):
        print(get_officers_ranks_name())
        embed = discord.Embed(
            title=f"Выдача медали №{medal_id}",
            description=f"Кому: {user.mention}",
            color=0xE100FF,
        )
        embed.set_thumbnail(
            url=f"https://raw.githubusercontent.com/qwazar14/medals-images/master/{medal_id}.png"
        )
        embed.add_field(
            name=await get_medal_info(medal_id),
            value="Для выдачи нажмите соответствующую кнопку",
            inline=True,
        )

        class Buttons(discord.ui.View):
            def __init__(self, client, con):
                super().__init__()
                self.client = client
                self.con = con

            guild_id = self.client.get_guild(settings["guildId"])

            @discord.ui.button(
                label="Выдать", style=discord.ButtonStyle.green, custom_id="give"
            )
            async def give(
                    self, button: discord.ui.Button, interaction: discord.MessageInteraction
            ):
                if interaction.user == ctx.author:
                    await interaction.response.send_message(
                        content="Вы не можете выдать медаль самому себе!",
                        ephemeral=True,
                    )
                    return
                user_rank = ranks_controller.get_member_rank
                if user_rank in ranks_controller.get_officers_ranks_id():
                    await interaction.response.edit_message(view=None)
                    user_uuid = str(user.id)
                    with self.con.cursor() as cursor:
                        # cursor.execute(
                        #     f"INSERT INTO `medals` (`user_id`, `medal_id`, `medal_count`) VALUES ('{user_uuid}', '{medal_id}', {medal_count}),")
                        cursor.execute(
                            f"INSERT INTO `MedalsDB` (`user_id`, `medal_id`) VALUES ('{user_uuid}', '{medal_id}')"
                        )
                    self.con.commit()
                    new_embed = discord.Embed(
                        title=f"Медаль №{medal_id} выдана",
                        description=f"Кому выдана: {user.mention}\n"
                                    f"Кем выдана: {interaction.user.mention}",
                        color=settings["okColor"],
                    )
                    await ctx.send(embed=new_embed)
                else:
                    await interaction.response.send_message(
                        content="У вас недостаточно прав для выдачи медали.",
                        ephemeral=True,
                    )

            @discord.ui.button(
                label="Отказать", style=discord.ButtonStyle.red, custom_id="deny"
            )
            async def deny(
                    self, button: discord.ui.Button, interaction: discord.MessageInteraction
            ):
                if interaction.user == ctx.author:
                    await interaction.response.send_message(
                        content="Вы не можете выдать медаль самому себе!",
                        ephemeral=True,
                    )
                    return
                user_rank = ranks_controller.get_member_rank
                if user_rank in ranks_controller.get_officers_ranks_id():
                    await interaction.response.edit_message(view=None)
                    new_embed = discord.Embed(
                        title=f"Отказано в выдачи медали №{medal_id}",
                        description=f"Кому отказано: {user.mention}\n"
                                    f"Кем отказано: {interaction.user.mention}",
                        color=settings["noOkColor"],
                    )
                    await ctx.send(embed=new_embed)
                else:
                    await interaction.response.send_message(
                        content="У вас недостаточно прав для выдачи медали.",
                        ephemeral=True,
                    )

        Buttons.disabled = True
        buttons = Buttons(self.client, self.con)

        # buttons.add_item(button1)
        #
        # async def button_callback(button_inter: discord.MessageInteraction):
        #     print("buttons.disabled = True")
        #     buttons.disabled = True
        #     await button_inter.send(embed=embed)
        #     await ctx.edit_original_message(view=buttons)
        #
        # buttons.callback = button_callback

        await ctx.send(embed=embed, view=buttons)

    # @commands.has_any_role(roles_config.discord_roles['admin'])
    # @commands.slash_command(name="view", description='view all records', guild_ids=[398857722159824907])
    # async def view(self, ctx, user: discord.Member):
    #     embed = discord.Embed(
    #         description=f"Медали игрока {user.mention} ||{user.id}||",
    #         color=0xe871ff
    #     )
    #
    #     for medal_id in range(16):
    #         embed.add_field(
    #             name=f"\u200b",
    #             value=f"Medal **#{medal_id + 1}**, count: **{await self.get_medal_count(user, medal_id + 1)}**",
    #             inline=False
    #         )
    #
    #     await ctx.send(embed=embed)
    #
    # async def get_medal_count(self, user, medal_id):
    #     with self.con.cursor() as cursor:
    #         cursor.execute("SELECT `medal_id` FROM `MedalsDB` WHERE `user_id`=%s", user.id)
    #         rows = cursor.fetchall()
    #         count = 0
    #         for row in rows:
    #             if row[0] == medal_id:
    #                 count += 1
    #     # print(count)
    #     return count


def setup(bot):
    bot.add_cog(BDTest(bot))


async def get_medal_image(medal_id):
    medal_path = f"bot/assets/images/medals/{medal_id}.png"
    return open(medal_path)
