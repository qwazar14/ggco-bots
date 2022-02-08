import os
import platform
import time

import disnake as discord
from disnake.ext import commands, tasks

from config import roles_config
from config.access_config import settings
from config.roles_config import discord_roles, channels_roles

intents = discord.Intents.all()
client = commands.Bot(command_prefix=settings['botPrefix'], intents=intents)
guild_id = client.get_guild(settings['guildId'])


@client.event
async def on_ready():
    await load_all_cogs()
    await get_system_info()
    print('[INFO] GGCo bot ready')


@client.event
async def on_member_join(member):
    print(f"[INFO] {member} joined")
    await user_join_left_controller(member, True)


@client.event
async def on_member_remove(member):
    print(f"[INFO] {member} left")
    await user_join_left_controller(member, False)


@client.event
async def on_voice_state_update(member, before, after):
    guild = client.get_guild(settings['guildId'])

    if after.channel is not None:
        if after.channel.id != settings['squadron_battle_channel_1'] \
                and after.channel.id != settings['squadron_battle_channel_2'] \
                and after.channel.id != settings['waiting_channel']:
            await member.remove_roles(guild.get_role(channels_roles['squad_1']))
            await member.remove_roles(guild.get_role(channels_roles['squad_2']))
            await member.remove_roles(guild.get_role(channels_roles['waiting_role']))
        else:
            if after.channel.id == settings['squadron_battle_channel_1']:
                await member.add_roles(guild.get_role(channels_roles['squad_1']))
                await member.remove_roles(guild.get_role(channels_roles['squad_2']))
                await member.remove_roles(guild.get_role(channels_roles['waiting_role']))
            elif after.channel.id == settings['squadron_battle_channel_2']:
                await member.add_roles(guild.get_role(channels_roles['squad_2']))
                await member.remove_roles(guild.get_role(channels_roles['squad_1']))
                await member.remove_roles(guild.get_role(channels_roles['waiting_role']))
            elif after.channel.id == settings['waiting_channel']:
                await member.add_roles(guild.get_role(channels_roles['waiting_role']))
                await member.remove_roles(guild.get_role(channels_roles['squad_1']))
                await member.remove_roles(guild.get_role(channels_roles['squad_2']))
    else:
        await member.remove_roles(guild.get_role(channels_roles['squad_1']))
        await member.remove_roles(guild.get_role(channels_roles['squad_2']))
        await member.remove_roles(guild.get_role(channels_roles['waiting_role']))
    if before.channel is not None:
        print(f"[INFO] {member} left {before.channel}")
    if after.channel is not None:
        print(f"[INFO] {member} joined {after.channel}")


@client.event
async def on_command(ctx):
    print(f'[INFO] {ctx.author} called command {ctx.command}:\nArgs: {ctx.args}\nKwargs: {ctx.kwargs}')


@commands.has_any_role(discord_roles['admin'])
@client.slash_command(name="reload", description='Перезагружает модули', guild_ids=[398857722159824907])
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
@client.slash_command(name="unload", description='Отключает модули', guild_ids=[398857722159824907])
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
@client.slash_command(name="load", description='Загружает модули', guild_ids=[398857722159824907])
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
    await send_embed_to_channel(settings['logsChannelId'], embed)


async def user_join_left_controller(member, mode):
    if mode:
        embed = discord.Embed(
            title=f"{member} зашёл на сервер",
            color=settings['okColor'])
    else:
        embed = discord.Embed(
            title=f"{member} покинул сервер",
            color=settings['noOkColor'])
    embed.add_field(name="\u200b",
                    value=f"Ник: {member.mention}")
    embed.add_field(name="\u200b",
                    value=f"Время: {time.strftime('%H:%M:%S %d %b %Y')}")
    try:
        embed.set_thumbnail(member.avatar)
        await send_embed_to_channel(settings['memberJoinedForOfficerChannelId'], embed)
    except:
        embed.set_thumbnail(member.default_avatar)
        await send_embed_to_channel(settings['memberJoinedForOfficerChannelId'], embed)


async def give_user_basic_roles(member):
    role = discord.utils.get(member.server.roles, id=roles_config.general_category_roles['new_player'])
    await member.add_roles(member, role)
    # await member.add_roles(roles_config.roles_categories['general_category'])
    print(f"[INFO] {member} was given basic roles")


async def send_embed_to_channel(channel_id, embed):
    await client.get_channel(channel_id).send(embed=embed)


async def get_system_info():
    os_name = platform.system()
    print("[INFO] OS : ", os_name)


try:
    client.run(settings['botToken'])
except Exception as e:
    print(f'[ERROR] Failed to start bot GGCo \nInfo: {e}')
