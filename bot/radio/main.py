import disnake
from disnake.ext import commands, tasks

from cog.radio import Radio
from config.access_config import settings
from util.radio_api import get_current_song

client = commands.Bot(command_prefix=settings["botPrefix"])
radio_ulitka = "http://air.radioulitka.ru:8000/ulitka_128"


@client.event
async def on_ready():
    client.add_cog(Radio(client, radio_ulitka))
    print(
        f"[INFO] Bot with url {radio_ulitka} is ready! PREFIX = '{client.command_prefix}'"
    )
    await update_status.start()


@tasks.loop(seconds=10.0)
async def update_status():
    current_song = await get_current_song()
    await client.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.listening, name=current_song, timestamps=1000
        )
    )


# Setting `Streaming ` status

try:
    client.run(settings["botToken"])
except Exception as e:
    print(f"[ERROR] Failed to start bot Radio \nInfo: {e}")
