import io

import disnake as discord
import pymysql
from disnake.ext import commands

from config.access_config import settings
from config.bd_config import CONFIG
from util import card_controller


class CardGenV2(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = pymysql.connect(
            host=CONFIG["host"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=CONFIG["db"])

    @commands.command(pass_context=True)
    async def card_v2(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        nickname = user.nick
        guild = self.client.get_guild(settings["guildId"])
        output = io.BytesIO()
        background_size = (1600, 1200)
        background_zone = (0, 0)

        # background_image = Image.open(r'assets/images/background/OF-1-3.png')
        background_image = await card_controller.get_background_image(
            self, user, self.client
        )
        card = background_image

        qrcode_image, qrcode_image_zone = await card_controller.get_user_qrcode(
            nickname
        )
        try:
            avatar, avatar_zone = await card_controller.get_user_avatar(user)
            card.paste(avatar, avatar_zone, avatar)
        except (AttributeError, TypeError) as e:
            pass

        user_image = await card_controller.get_user_background_image(
            self, user, self.client
        )
        user_image_zone = (255, 190)
        card.paste(user_image, user_image_zone, user_image)

        await card_controller.draw_user_nickname(user, card)

        try:
            medal_image = await card_controller.get_user_medals(self, user)
            card.paste(medal_image, (0, 0), medal_image)
        except Exception:
            print(f"INSERT INTO `UserMedals` (`user_id`) VALUE ('{user.id}');")
            with self.con.cursor() as cursor:
                cursor.execute(f"INSERT INTO `UserMedals` (`user_id`) VALUE ('{user.id}');")
            self.con.commit()

        card.paste(background_image, background_zone, background_image)
        card.paste(qrcode_image, qrcode_image_zone, qrcode_image)

        card.save(output, "png")
        player_card = io.BytesIO(output.getvalue())
        return await ctx.send(file=discord.File(fp=player_card, filename=f"{user}'s_card.png"))


def setup(bot):
    bot.add_cog(CardGenV2(bot))
