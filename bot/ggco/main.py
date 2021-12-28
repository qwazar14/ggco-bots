import os

import disnake
from disnake.ext import commands

from config import roles_config
from config.access_config import settings
from config.roles_config import discord_roles

client = commands.Bot(command_prefix=settings['botPrefix'])
guild_id = client.get_guild(settings['guildId'])


@client.event
async def on_ready():
    print('[INFO] GGCo bot ready')
    # client.add_cog()


@client.event
async def on_member_joined(member):
    # add roles
    print(f'[INFO] {member} was given default roles')


@client.event
async def on_command(ctx):
    print(f'[INFO] {ctx.author} called command {ctx.command}:\nArgs: {ctx.args}\nKwargs: {ctx.kwargs}')


@commands.has_any_role(discord_roles['admin'])
@client.slash_command(name="reload", description='Перезагружает модули', guild_ids=guild_id)
async def reload(ctx, extension):
    result = ""
    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "db.py":
                try:
                    client.unload_extension(f"cogs.{filename[:-3]}")
                    client.load_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    result += f"[ERROR] reload **{filename}:** {e}\n"
                else:
                    result += f"**{filename[:-3]}** reloaded!\n"
    else:
        try:
            client.unload_extension(f"cogs.{extension}")
            client.load_extension(f"cogs.{extension}")
        except Exception as e:
            result += f"Error reload **{extension}:** {e}\n\n"
        else:
            await ctx.send(f"**{extension}** reloaded!")
    if result != "":
        await ctx.send(result)


@commands.has_any_role(roles_config.discord_roles['admin'])
@client.slash_command(name="unload", description='Отключает модули')
async def unload(ctx, extension):
    result = ""
    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "db.py":
                try:
                    client.unload_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    result += f"[ERROR] unload **{filename}:** {e}\n"
                else:
                    result += f"**{filename[:-3]}** unloaded!\n"
    else:
        try:
            client.unload_extension(f"cogs.{extension}")
        except Exception as e:
            result += f"[ERROR] unload **{extension}:** {e}\n\n"
        else:
            await ctx.send(f"**{extension}** unloaded!")
    if result != "":
        await ctx.send(result)


@commands.has_any_role(roles_config.discord_roles['admin'])
@client.slash_command(name="load", description='Загружает модули')
async def load(ctx, extension):
    result = ""
    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "db.py":
                try:
                    client.load_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    result += f"[ERROR] load **{filename}:** {e}\n\n"
                else:
                    await ctx.send(f"**{filename[:-3]}** loaded!")
    else:
        try:
            client.load_extension(f"cogs.{extension}")
        except Exception as e:
            result += f"[ERROR] load **{extension}:** {e}\n\n"
        else:
            await ctx.send(f"**{extension}** loaded!")
    if result != "":
        await ctx.send(result)


@commands.has_any_role(roles_config.discord_roles['admin'])
@client.slash_command(name="rules", description='Отправляет правила')
async def rules(ctx):
    embed = disnake.Embed(title='Общие правила', color=0xe100ff)
    embed.add_field(name="\u200b",
                    value='```css\n1.1 На этом сервере не допускается расовая нетерпимость или крайняя ненависть любого рода.\n[Бан или предупреждение, в зависимости от содержания]```',
                    inline=False)

    embed.add_field(name="\u200b",
                    value='```css\n1.2 Не будьте токсиком, который портит веселье другим. Это включает в себя нацеливание на одного человека и обсирание его.\n[Бан или предупреждение, в зависимости от содержания]```',
                    inline=False)

    embed.add_field(name="\u200b",
                    value='```css\n1.3 Не сливайте личную информацию о других членах сервера без их разрешения. Это относится и к личке.\n[Предупреждение или бан в зависимости от серьезности утечки]```',
                    inline=False)

    embed.add_field(name="\u200b", value='```css\n1.4 Не публикуйте nsfw-контент вне #nsfw.\n[Бан]```', inline=False)

    embed.add_field(name="\u200b",
                    value='```css\n1.5 Не выдавайте себя за ботов или любого члена сервера. (Через имя, ник или картинку профиля)\n[Предупреждение и бан в случае продолжения]```',
                    inline=False)

    embed.add_field(name="\u200b",
                    value='```css\n1.6 Запрещен спам ЛЮБОГО рода, включая @everyone/@here спам, спам реакции, копирование/вставка текста, @mentions в AFK.\n[Предупреждению и бан в случае продолжения.]```',
                    inline=False)

    embed.add_field(name="\u200b",
                    value='```css\n1.7 Не пингуйте роли без веской причины. Пингуйте роли только в экстренных случаях.\n[Предупреждение]```',
                    inline=False)

    embed.add_field(name="\u200b",
                    value='```css\n1.8 Не выпрашивать роль/звание. Нам это не нужно, и если мы посчитаем, что вы заслуживаете роли, мы вам ее дадим.\n[Предупреждение]```',
                    inline=False)

    embed.add_field(name="\u200b",
                    value='```css\n1.9 Используйте каналы по назначению, (в каналах «музыка» – запускайте музыку и т.д)\n[Устное предупреждение и предупреждение в случае продолжения]```',
                    inline=False)

    embed.add_field(name="\u200b",
                    value='```css\n1.10 Не вступайте в дискуссию с офицерами на сервере после решения о наказании (например, получения предупреждения), если вы считаете, что предупреждение было неправильным, пожалуйста, решите этот вопрос в личке с тем, кто выписал предупредил.\n[Предупреждение]```',
                    inline=False)

    await ctx.send(embed=embed)


try:
    client.run(settings['botToken'])
except Exception as e:
    print(f'[ERROR] Failed to start bot GGCo \nInfo: {e}')
