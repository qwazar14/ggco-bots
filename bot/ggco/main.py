import os
import platform
import time

import disnake as discord
from disnake.ext import commands

from config import roles_config
from config.access_config import settings
from config.roles_config import discord_roles

intents = discord.Intents.all()
client = commands.Bot(command_prefix=settings['botPrefix'], intents=intents, test_guilds=[398857722159824907])
guild_id = client.get_guild(settings['guildId'])


@client.event
async def on_ready():
    await load_all_cogs()
    await get_system_info()
    print('[INFO] GGCo bot ready')



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
        for filename in os.listdir("bot/ggco/cogs"):
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
        for filename in os.listdir("bot/ggco/cogs"):
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
# @client.command()
async def load(ctx, extension):
    result = ""
    if extension == "all":
        for filename in os.listdir("bot/ggco/cogs"):
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


async def load_all_cogs():
    embed = discord.Embed(
        title=f"**LOADING ALL COGS**",
        color=0xe100ff)
    print('[INFO] Loading all cogs')
    for filename in os.listdir("bot/ggco/cogs"):
        if filename.endswith(".py") and filename != "db.py":
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
            except Exception as exception:
                embed.add_field(name=f'{filename}',
                                value=f"```css\n[{exception}]```",
                                inline=False)

                print(f'[ERROR] load {filename}: {exception}')
            else:
                embed.add_field(name=f'{filename}',
                                value=f"```ini\n[loaded!]```",
                                inline=True)
                print(f'...{filename[:-3]} loaded!')

    embed.add_field(name=f"```{time.strftime('%d %b %Y')}```",
                    value=f"```fix\n{time.strftime('%H:%M:%S')}```",
                    inline=False)
    await client.get_channel(929338243563003944).send(embed=embed)


async def get_system_info():
    os_name = platform.system()
    print("[INFO] OS : ", os_name)


try:
    client.run(settings['botToken'])
except Exception as e:
    print(f'[ERROR] Failed to start bot GGCo \nInfo: {e}')
