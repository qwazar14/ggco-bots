import io

import disnake as discord
import pymysql
from disnake.ext import commands

from config.access_config import settings
from config.bd_config import CONFIG
from util import card_controller


class CardGen(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = pymysql.connect(
            host=CONFIG["host"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=CONFIG["db"])

    @commands.command(pass_context=True)
    async def card(self, ctx, user: discord.Member = None):
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

        await card_controller.format_user_nickname(user, card)

        # with self.con.cursor() as cursor:
        #     cursor.execute(f"SELECT * FROM `UserMedals` WHERE `user_id` = {user.id};")
        #     medals_tuple = cursor.fetchone()
        # self.con.commit()
        # medals_list = list(medals_tuple)
        # medals_list.pop(0)
        # counter = 0
        # for medal_id in range(len(medals_list)):
        #     if medals_list[medal_id] != 0:
        #         counter = counter + 1
        #
        # print(medals_list)
        #
        # # counter = random.randint(6, 16)
        # medal_zone = [-250, 850]
        # medal_width = 223
        # medal_length = 237
        # pos_x = 0
        # offset_x = 210
        # pos_y = 855
        #
        # print(counter)
        # print(counter)
        # print(counter)
        # print(counter)
        # if counter <= 7:
        #     offset_x = 210
        #     pos_x = -180
        # elif 7 < counter <= 9:
        #     offset_x = int((1 / counter) * 1400) + 20
        #     pos_x = int((1 / counter) * -1300) - 50
        # elif 10 <= counter <= 15:
        #     offset_x = int((1 / counter) * 1400) + 20
        #     pos_x = int((1 / counter) * -1300) - 50
        # elif counter >= 16:
        #     offset_x = 100
        #     pos_x = -110
        # if counter != 6:
        #     for i in range(counter - 7):
        #         medal_width = medal_width - 14
        #         medal_length = medal_length - 14
        #
        # for medal_id in range(len(medals_list)):
        #     if medals_list[medal_id] != 0:
        #         pos_x = pos_x + offset_x
        #         medal_image = Image.open(f"assets/images/medals/{medal_id + 1}.png", 'r')
        #         medal_image = medal_image.resize((medal_width, medal_length))
        #         medal_zone[0] = medal_zone[0] + 250
        #         card.paste(medal_image, [int(pos_x), int(pos_y)], medal_image)
        #         print(f"medal_id{medal_id+1}: {medals_list[medal_id]}")

         # = await card_controller.get_user_medals(self, user)

        medal_image = await card_controller.get_user_medals(self, user)
        card.paste(medal_image, (0, 0), medal_image)

        card.paste(background_image, background_zone, background_image)
        card.paste(qrcode_image, qrcode_image_zone, qrcode_image)

        card.save(output, "png")
        player_card = io.BytesIO(output.getvalue())
        return await ctx.send(file=discord.File(fp=player_card, filename=f"{user}'s_card.png"))


def setup(bot):
    bot.add_cog(CardGen(bot))
