from disnake import FFmpegPCMAudio, PCMVolumeTransformer
from disnake.ext import commands
from config.roles_config import discord_roles


class Radio(commands.Cog):

    def __init__(self, client, radio_url):
        self.client = client
        self.radio_url = radio_url
        self.player = None
        super().__init__()

    @commands.has_any_role(discord_roles['admin'])
    @commands.command(aliases=['radio'], pass_context=True)
    async def play(self, ctx):
        channel = ctx.message.author.voice.channel
        self.player = await channel.connect()
        ffmpeg_source = FFmpegPCMAudio(self.radio_url)
        volume_manager = PCMVolumeTransformer(ffmpeg_source, volume=0.033)
        self.player.play(volume_manager)

    @commands.has_any_role(discord_roles['admin'])
    @commands.command(aliases=['stop_radio'], pass_context=True)
    async def stop(self, ctx):
        self.player.stop()


def setup(client, url):
    client.add_cog(Radio(client, url))
