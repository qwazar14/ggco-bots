import disnake as discord
import pymysql
from disnake.ext import commands

from config import roles_config
from ggco.config.access_config import settings
from ggco.config.bd_config import CONFIG


async def get_medal_info(medal_id):
    if medal_id == 1:
        return 'Медаль выдается за уничтожение 4 и более наземной техники на наземной технике'
    elif medal_id == 2:
        return 'Медаль выдается за захват трёх точек за бой'
    elif medal_id == 3:
        return 'Медаль выдается за уничтожение 3 и более воздушной техники на наземной технике'
    elif medal_id == 4:
        return 'Медаль выдается за уничтожение 3 и более воздушной техники на наземной технике'
    elif medal_id == 5:
        return 'Медаль выдается за уничтожение 3 и более наземной техники на вертолёте'
    elif medal_id == 6:
        return 'Медаль выдается за оказание помощи в уничтожении техники 4 и более раз'
    elif medal_id == 7:
        return 'Медаль выдается за уничтожение 3 и более наземной техники на воздушной технике'
    elif medal_id == 8:
        return 'Медаль выдается за уничтожение 2 техники противника одной бомбой/ракетой/снарядом'
    elif medal_id == 9:
        return 'Медаль выдается за победу в бою, оставшись последним в команде на воздушной технике'
    elif medal_id == 10:
        return 'Медаль выдается за победу в бою, оставшись последним в команде на наземной технике'
    elif medal_id == 11:
        return 'Медаль выдается за уничтожение техники противника артиллерией'
    elif medal_id == 12:
        return 'Медаль выдается за достижение 1500 и более очков за сезон	'
    elif medal_id == 13:
        return 'Медаль выдается за особые заслуги в жизни полка'
    elif medal_id == 14:
        return 'Мы ещё не придумали описание для этой медали'
    elif medal_id == 14:
        return 'Мы ещё не придумали описание для этой медали'
    elif medal_id == 14:
        return 'Мы ещё не придумали описание для этой медали'


class BDTest(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.has_any_role(roles_config.discord_roles['admin'])
    @commands.slash_command(name="test", description='test')
    async def test(self, ctx, user: discord.Member, medal_id: int):
        embed = discord.Embed(
            title=f"Выдача медали №{medal_id}",
            description=f"Кому: {user.mention}",
            color=0xe100ff)
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/qwazar14/medals-images/master/{medal_id}.png')
        embed.add_field(name=await get_medal_info(medal_id),
                        value="Для выдачи нажмите соответствующую кнопку",
                        inline=True)

        class Buttons(discord.ui.View):
            def __init__(self, client, channel):
                super().__init__()
                self.con = pymysql.connect(
                    host=CONFIG['host'],
                    user=CONFIG['user'],
                    password=CONFIG['password'],
                    database=CONFIG['db'])
                self.client = client
                self.channel = channel

            guild_id = self.client.get_guild(settings['guildId'])

            @discord.ui.button(label='Выдать', style=discord.ButtonStyle.green)
            async def give(self, a, b):
                user_uuid = str(user.id)
                with self.con.cursor() as cursor:
                    cursor.execute(
                        f"INSERT INTO `medals` (`user_id`, `medal_id`) VALUES ('{user_uuid}', '{medal_id}')")
                self.con.commit()
                new_embed = discord.Embed(
                    title=f'Медаль №{medal_id} выдана',
                    description=f"Кому: {user.mention}\n"
                                f"Кем: {ctx.user.mention}",
                    color=0x00ff00
                )
                # new_embed.set_thumbnail(url=f'https://raw.githubusercontent.com/qwazar14/medals-images/master/{medal_id}.png')
                # await info.edit(embed=new_embed)
                # await self.info.add_reaction('✅')
                # await ctx.delete_message(info)
                await ctx.send(embed=new_embed)
                await self.channel.delete()

            @discord.ui.button(label='Отказать', style=discord.ButtonStyle.red)
            async def denied(self, con, medal_id):
                pass

        self.info = await ctx.send(embed=embed)
        buttons = Buttons(self.client, self.info)

        await self.info.edit(view=buttons)


def setup(bot):
    bot.add_cog(BDTest(bot))


async def get_medal_image(medal_id):
    medal_path = f'bot/assets/images/medals/{medal_id}.png'
    return open(medal_path)
