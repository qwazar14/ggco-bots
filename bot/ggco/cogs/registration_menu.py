import asyncio

import disnake as discord
from disnake.ext import commands

from config import roles_config
from config.access_config import settings
from util.ranks_controller import get_rank_id_by_name


class RegistrationMenu(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command(pass_context=True)
    @commands.has_any_role(roles_config.discord_roles["admin"])
    @commands.slash_command(
        name="registration_menu",
        description="Создает меню регистрации",
        guild_ids=[398857722159824907],
    )
    async def registration_menu(self, ctx):
        class RegistrationMenuButtons(discord.ui.View):
            def __init__(self, client, *, timeout=None):
                super().__init__(timeout=timeout)
                self.client = client

            guild_id = self.client.get_guild(settings["guildId"])

            @discord.ui.button(
                label="Подать заявку в полк", style=discord.ButtonStyle.green
            )
            async def join_squadron(
                self, button, ctx, timeout_error_call=True, guild_id=guild_id
            ):

                br_user = 1.0
                nickname_user = ""
                name_user = ""
                user = ctx.user
                new_nickname = ""
                await ctx.response.send_message(
                    content="Введите ник в игре *(у вас есть 2 минуты)* ",
                    ephemeral=True,
                )
                try:
                    nickname_user = await get_user_response(self.client, ctx)
                    await ctx.edit_original_message(
                        content="Как Вас зовут? *(у вас есть 2 минуты)*"
                    )
                except asyncio.TimeoutError:
                    timeout_error_call = await timeout_error(ctx)

                if timeout_error_call is not False:
                    try:
                        name_user = await get_user_response(self.client, ctx)
                        await ctx.edit_original_message(
                            content="Введите ваш максимальный БР *(у вас есть 2 минуты)*"
                        )
                    except asyncio.TimeoutError:
                        timeout_error_call = await timeout_error(ctx)

                if timeout_error_call is not False:
                    try:
                        br_msg_content = await get_user_response(self.client, ctx)
                        try:
                            br_user = await replace_comma_to_do(br_msg_content)
                        except ValueError as ve:
                            await ctx.edit_original_message(
                                content="**Используйте только цифры! Начните заново**"
                            )
                            timeout_error_call = False

                        if timeout_error_call is not False:
                            if 1.0 <= br_user <= settings["maxBR"]:
                                new_nickname = (
                                    f"[{br_user}] {nickname_user} ({name_user})"
                                )
                            else:
                                await ctx.edit_original_message(
                                    content="**Боевой рейтинг может быть в диапазоне от 1.0 до 11.0. *Начните заново***"
                                )
                                timeout_error_call = False
                            if timeout_error_call is not False:
                                await finish_registration_if_ok(
                                    user, guild_id, new_nickname, True
                                )
                                await ctx.edit_original_message(
                                    content="*Регистрация завершена*"
                                )

                    except asyncio.TimeoutError:
                        await timeout_error(ctx)

            @discord.ui.button(label="Другой полк", style=discord.ButtonStyle.blurple)
            async def squadron_friend(
                self, button, ctx, timeout_error_call=True, guild_id=guild_id
            ):
                user = ctx.user
                await ctx.response.send_message(
                    content="Введите ник в игре *(у вас есть 2 минуты)* ",
                    ephemeral=True,
                )
                try:
                    nickname_user = await get_user_response(self.client, ctx)
                    await ctx.edit_original_message(
                        content="Как Вас зовут? *(у вас есть 2 минуты)*"
                    )
                except asyncio.TimeoutError:
                    timeout_error_call = await timeout_error(ctx)

                if timeout_error_call is not False:
                    try:
                        name_user = await get_user_response(self.client, ctx)
                    except asyncio.TimeoutError:
                        timeout_error_call = await timeout_error(ctx)

                    class SquadronMenu(discord.ui.View):
                        def __init__(self, client, *, timeout=None):
                            super().__init__(timeout=timeout)
                            self.client = client

                        @discord.ui.button(label="Да", style=discord.ButtonStyle.green)
                        async def get_user_squadron(self, button, interaction):
                            # await interaction.edit_original_message(content='*Введите клантег в формате XXXX')
                            await interaction.response.send_message(
                                content='*Введите клантег без "рамок"', ephemeral=True
                            )
                            try:
                                squadron_user = await get_user_response(
                                    self.client, interaction
                                )
                                if 5 >= len(squadron_user) > 1:
                                    new_nickname = f"[{squadron_user}] {nickname_user} ({name_user})"
                                    # await ctx.send()

                                    await user.edit(nick=new_nickname)
                                    await interaction.edit_original_message(
                                        content="*Регистрация завершена*"
                                    )
                                else:
                                    await interaction.edit_original_message(
                                        content="**ОШИБКА** Клантег должен состоять максимум из 5 символов"
                                    )
                            except asyncio.TimeoutError:
                                await timeout_error(interaction)

                        @discord.ui.button(label="Нет", style=discord.ButtonStyle.red)
                        async def end_user_registration(self, button, interaction):
                            new_nickname = f"[-] {nickname_user} ({name_user})"
                            await user.edit(nick=new_nickname)
                            await finish_registration_if_ok(
                                user, guild_id, new_nickname, False
                            )
                            await edit_final_message_to_finish_registration(
                                self, interaction
                            )

                    if timeout_error_call is not False:
                        view_squadron_buttons = SquadronMenu(self.client)
                        await ctx.edit_original_message(
                            content="*Вы состоите в полку?*", view=view_squadron_buttons
                        )

        buttons = RegistrationMenuButtons(self.client)
        # rank = rank_system.get_member_rank(ctx.author, str=True)

        embed = discord.Embed(
            title="Вы попали на сервер полка GG Company",
            description="**Для вступления в полк - нажмите 'Подать заявку'**",
            color=0xE100FF,
        )
        embed.set_thumbnail(url=settings["logoUrl"])
        embed.add_field(
            name="Если вы хотите зайти на сервер - нажмите кнопку 'Друг полка'",
            value="Нажимая любую кнопку вы автоматически соглашаетесь с правилами в канале <#877276991412379709>",
            inline=False,
        )

        await ctx.send(embed=embed, view=buttons)


async def timeout_error(interaction):
    await interaction.followup.send(
        content="*Извините, вы не ответили вовремя! Повторите попытку*", ephemeral=True
    )
    return False


async def get_user_response(client, interaction):
    msg = await client.wait_for(
        "message",
        timeout=120,
        check=lambda m: m.author == interaction.user
        and m.channel == interaction.channel,
    )
    temp = msg
    await msg.delete()
    return temp.content


async def replace_comma_to_do(br_msg_content):
    replaced_message = max([float(i) for i in br_msg_content.replace(",", ".").split()])
    return replaced_message


async def edit_final_message_to_finish_registration(self, interaction):
    await interaction.response.send_message(
        content="*Регистрация завершена*", ephemeral=True
    )
    return False


async def finish_registration_if_ok(user, guild_id, new_nickname, is_squadron_member):
    await new_nickname_for_user(user, new_nickname)
    await give_user_basic_roles(user, guild_id)
    if is_squadron_member is True:
        await give_user_squadron_roles(user, guild_id)
    else:
        await give_user_friend_roles(user, guild_id)


async def new_nickname_for_user(user, new_nickname):
    await user.edit(nick=new_nickname)


async def give_user_squadron_roles(user, guild_id):
    await user.add_roles(
        guild_id.get_role(roles_config.roles_categories["rank_category"])
    )
    await user.add_roles(
        guild_id.get_role(roles_config.roles_categories["unit_type_category"])
    )
    await user.add_roles(
        guild_id.get_role(roles_config.optional_category_roles["ggco"])
    )
    await user.add_roles(guild_id.get_role(get_rank_id_by_name("OR-1")))


async def give_user_friend_roles(user, guild_id):
    await user.add_roles(
        guild_id.get_role(roles_config.optional_category_roles["squadron_friend"])
    )


async def give_user_basic_roles(user, guild_id):
    await user.remove_roles(
        guild_id.get_role(roles_config.general_category_roles["new_player"])
    )
    await user.add_roles(
        guild_id.get_role(roles_config.general_category_roles["player"])
    )
    await user.add_roles(
        guild_id.get_role(roles_config.roles_categories["optional_category"])
    )
    await user.add_roles(
        guild_id.get_role(roles_config.roles_categories["general_category"])
    )


def setup(bot):
    bot.add_cog(RegistrationMenu(bot))
