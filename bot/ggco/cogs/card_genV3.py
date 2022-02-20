import io

import disnake as discord
import pymysql
from PIL import Image
from disnake.ext import commands

from config.bd_config import CONFIG
from util import card_controller


class CardGenV3(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = pymysql.connect(
            host=CONFIG["host"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=CONFIG["db"],
        )

    # @commands.command(pass_context=True)
    @commands.slash_command(
        name="card",
        description="Показать карточку игрока",
        guild_ids=[398857722159824907],
    )
    async def card(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        output = io.BytesIO()

        card = Image.new("RGBA", (1600, 1200), (0, 0, 0, 0))

        user_image, gradient = await card_controller.get_user_background_image(
            user, self.client
        )

        user_image_mask = card_controller.create_rounded_rectangle_mask(
            (1580, 580), 50, 255
        )


        gradient_mask = card_controller.create_rounded_rectangle_mask(
            (1580, 580), 50, 255
        )

        card.paste(gradient, (10, 610), gradient_mask)
        card.paste(user_image, (10, 10), user_image_mask)
        await card_controller.draw_user_nickname(user, card)
        await card_controller.draw_user_rank(user, card)

        try:
            medal_image = await card_controller.get_user_medals(self, user)
            card.paste(medal_image, (0, 0), medal_image)
        except Exception:
            print(f"INSERT INTO `UserMedals` (`user_id`) VALUE ('{user.id}');")
            with self.con.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO `UserMedals` (`user_id`) VALUE ('{user.id}');"
                )
            self.con.commit()

        card.save(output, "png")
        player_card = io.BytesIO(output.getvalue())
        return await ctx.send(
            file=discord.File(fp=player_card, filename=f"{user}'s_card.png")
        )


def setup(bot):
    bot.add_cog(CardGenV3(bot))
