import disnake as discord
import pymysql
from disnake import Client
from disnake.ext import commands

from config import roles_config
from config.access_config import settings
from config.bd_config import CONFIG
from util import ranks_controller

client = Client()


async def get_medal_info(medal_id):
    if medal_id == 1:
        return "Медаль выдается за уничтожение 4 и более наземной техники на наземной технике"
    elif medal_id == 2:
        return "Медаль выдается за уничтожение 3 и более воздушной техники на наземной технике"
    elif medal_id == 3:
        return "Медаль выдается за уничтожение 3 и более воздушной техники на воздушной технике"
    elif medal_id == 4:
        return "Медаль выдается за уничтожение 3 и более наземной техники на воздушной технике"
    elif medal_id == 5:
        return "Медаль выдается за оказание 4 и более помощи в уничтожении техники соперника"
    elif medal_id == 6:
        return "Медаль выдается за 4 победы подряд, будучи командиром"
    elif medal_id == 7:
        return "Медаль выдается за уничтожение техники соперника артиллерией"
    elif medal_id == 8:
        return "Медаль выдается за победу в бою, оставшись последним в команде"
    elif medal_id == 9:
        return "Медаль выдается за уничтожение 8 техники соперника"
    elif medal_id == 10:
        return "Медаль выдается за захват трёх точек за бой"
    elif medal_id == 11:
        return "Медаль выдается за уничтожение 2 и более едениц техники соперника одной бомбой/ракетой/снарядом"
    elif medal_id == 12:
        return "Медаль выдается за особые заслуги в жизни полка"
    elif medal_id == 13:
        return "Медаль выдается за достижения к концу сезона 1500 очков и более"
    else:
        return "Такой медали не существует!"


class BDTest(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = pymysql.connect(
            host=CONFIG["host"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=CONFIG["db"],
        )

    # @commands.command()
    @commands.slash_command(
        name="medal",
        description="Выдать медаль @Пользователь №Медали",
        guild_ids=[398857722159824907],
    )
    async def medal(
            self,
            ctx: discord.ApplicationCommandInteraction,
            # user: discord.Member,
            medal_id: int,
    ):
        # user = ctx.user
        user = ctx.author
        embed = discord.Embed(
            title=f"Выдача медали №{medal_id}",
            description=f"Кому: {user.mention}",
            color=0xE100FF,
        )
        embed.set_thumbnail(
            url=f"https://raw.githubusercontent.com/qwazar14/medals-images/master/medal%20({medal_id}).png"
        )
        embed.add_field(
            name=await get_medal_info(medal_id),
            value="Для выдачи нажмите соответствующую кнопку",
            inline=True,
        )
        if 0 < medal_id <= 13:
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
                    # if interaction.user is user:
                    #     await interaction.response.send_message(
                    #         content="Вы не можете выдать медаль самому себе!",
                    #         ephemeral=True,
                    #     )
                    #     return
                    user_rank = ranks_controller.get_member_rank(interaction.user)
                    if user_rank in ranks_controller.get_real_officers_ranks_id():
                        with self.con.cursor() as cursor:
                            cursor.execute(
                                f"SELECT `medal{medal_id}` FROM `UserMedals` WHERE `user_id` = {user.id};"
                            )
                            medal_count = cursor.fetchall()
                        self.con.commit()
                        print(f"medal_count: {medal_count}")
                        if str(medal_count) != "()":
                            medal_counter = medal_count[0][0]
                            print(f"medal_counter: {medal_counter}")
                            await interaction.response.edit_message(view=None)
                            print(
                                f"UPDATE `UserMedals` SET `medal{str(medal_id)}` = {medal_counter + 1} WHERE `user_id` = {user.id};")
                            with self.con.cursor() as cursor:
                                cursor.execute(
                                    f"UPDATE `UserMedals` SET `medal{str(medal_id)}` = {medal_counter + 1} WHERE `user_id` = {user.id};")
                            self.con.commit()
                        else:
                            await interaction.response.edit_message(view=None)
                            print(f"INSERT INTO `UserMedals` (`user_id`, `medal{medal_id}`) VALUES ('{user.id}', '1');")
                            with self.con.cursor() as cursor:
                                cursor.execute(
                                    f"INSERT INTO `UserMedals` (`user_id`, `medal{medal_id}`) VALUES ('{user.id}', '1');"
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

                    if interaction.user is user:
                        await interaction.response.send_message(
                            content="Вы не можете выдать медаль самому себе!",
                            ephemeral=True,
                        )
                        return
                    user_rank = ranks_controller.get_member_rank(interaction.user)
                    if user_rank in ranks_controller.get_real_officers_ranks_id():
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

            await ctx.send(embed=embed, view=buttons)
        else:
            await ctx.response.send_message(
                content=await get_medal_info(medal_id),
                ephemeral=True,
            )

    @commands.has_any_role(roles_config.discord_roles["admin"])
    @commands.slash_command(
        name="view",
        description="Посмотреть все медали игрока",
        guild_ids=[398857722159824907],
    )
    async def view(self, ctx, user: discord.Member):
        embed = discord.Embed(
            description=f"Медали игрока {user.mention} ||{user.id}||", color=0xE871FF
        )

        for medal_id in range(16):
            embed.add_field(
                name=f"\u200b",
                value=f"Medal **#{medal_id + 1}**, count: **{await self.get_medal_count(user, medal_id + 1)}**",
                inline=False,
            )

        await ctx.send(embed=embed)

    @commands.has_any_role(roles_config.discord_roles["admin"])
    # @commands.slash_command(
    #     name="remove_medal",
    #     description="Удалить медаль у игрока",
    #     guild_ids=[398857722159824907],
    # )
    @commands.command()
    async def remove_medal(
            self,
            ctx: discord.ApplicationCommandInteraction,
            user: discord.Member,
            medal_id: int,
    ):
        embed = discord.Embed(
            title=f"Удалить медаль №{medal_id}",
            description=f"У кого: {user.mention}",
            color=0xE100FF,
        )
        embed.set_thumbnail(
            url=f"https://raw.githubusercontent.com/qwazar14/medals-images/master/{medal_id}.png"
        )
        embed.add_field(
            name=await get_medal_info(medal_id),
            value="Для удаление медали нажмите соответствующую кнопку",
            inline=True,
        )

        class Buttons(discord.ui.View):
            def __init__(self, client, con):
                super().__init__()
                self.client = client
                self.con = con

            guild_id = self.client.get_guild(settings["guildId"])

            @discord.ui.button(
                label="Удалить", style=discord.ButtonStyle.green, custom_id="remove"
            )
            async def remove(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
                user_rank = ranks_controller.get_member_rank(interaction.user)
                if user_rank in ranks_controller.get_real_officers_ranks_id():
                    await interaction.response.edit_message(view=None)

                    with self.con.cursor() as cursor:
                        cursor.execute(
                            f"SELECT `medal{medal_id}` FROM `UserMedals` WHERE `user_id` = {user.id};"
                        )
                        medal_count = cursor.fetchall()
                    self.con.commit()
                    print(f"medal_count: {medal_count}")
                    if str(medal_count) != "()":
                        medal_counter = medal_count[0][0]
                        if medal_counter <= 0:
                            new_embed = discord.Embed(
                                title=f"Медаль №{medal_id} не удалена",
                                description=f"У {user.mention} нет медали №{medal_id}.\n",
                                color=settings["noOkColor"],
                            )

                        else:
                            print(f"medal_counter: {medal_counter}")
                            print(
                                f"UPDATE `UserMedals` SET `medal{str(medal_id)}` = {medal_counter - 1} WHERE `user_id` = {user.id};")
                            with self.con.cursor() as cursor:
                                cursor.execute(
                                    f"UPDATE `UserMedals` SET `medal{str(medal_id)}` = {medal_counter - 1} WHERE `user_id` = {user.id};")
                            self.con.commit()
                            new_embed = discord.Embed(
                                title=f"Медаль №{medal_id} удалена",
                                description=f"У кого удалена: {user.mention}\n"
                                            f"Кем удалена: {interaction.user.mention}",
                                color=settings["noOkColor"],
                            )
                        await ctx.send(embed=new_embed)
                    else:
                        print(f"INSERT INTO `UserMedals` (`user_id`) VALUE ('{user.id}');")
                        with self.con.cursor() as cursor:
                            cursor.execute(f"INSERT INTO `UserMedals` (`user_id`) VALUE ('{user.id}');")
                        self.con.commit()

                        new_embed = discord.Embed(
                            title=f"Медаль №{medal_id} не удалена",
                            description=f"У {user.mention} нет медали №{medal_id}.\n",
                            color=settings["noOkColor"],
                        )
                        await ctx.send(embed=new_embed)
                else:
                    await interaction.response.send_message(
                        content="У вас недостаточно прав для выдачи медали.",
                        ephemeral=True,
                    )

        buttons = Buttons(self.client, self.con)

        await ctx.send(embed=embed, view=buttons)

    async def get_medal_count(self, user, medal_id):
        with self.con.cursor() as cursor:
            cursor.execute(
                "SELECT `medal_id` FROM `MedalsDB` WHERE `user_id`=%s", user.id

            )
            rows = cursor.fetchall()
            count = 0
            for row in rows:
                if row[0] == medal_id:
                    count += 1
        # print(count)
        return count


def setup(bot):
    bot.add_cog(BDTest(bot))


async def get_medal_image(medal_id):
    medal_path = f"bot/assets/images/medals/{medal_id}.png"
    return open(medal_path)
