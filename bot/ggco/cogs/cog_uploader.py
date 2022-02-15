from disnake.ext import commands

from config import roles_config


class CogUploader(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.slash_command(name="upload_cog", description='Загружает когу в папку с когами')
    @commands.has_any_role(roles_config.discord_roles["admin"])
    @commands.command()
    async def upload_cog(self, ctx):
        try:
            for attach in ctx.message.attachments:
                await attach.save(f"/cogs/{attach.filename}")
                await ctx.message.add_reaction("✅")
        except Exception as e:
            await ctx.message.add_reaction("❌")


def setup(bot):
    bot.add_cog(CogUploader(bot))
