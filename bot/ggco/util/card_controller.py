import io
import random
import re
import cv2 as cv
import placeholder as placeholder
import qrcode as qr
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from colorthief import ColorThief

from config import roles_config
from config.access_config import settings
from util import ranks_controller


# async def get_background_image(self, user, client):
#     #  NITRO
#     global background_image
#     guild = client.get_guild(settings["guildId"])
#     # guild = '398857722159824907'
#     # #  NITRO
#     # if '853942930229559318' in user.roles:
#     #     background_image = Image.open(r'bot/assets/images/background/NITRO.png')
#     # ##
#
#     #  soldier_roles
#     if (
#             guild.get_role(ranks_controller.get_rank_id_by_name("OR-1")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OR-2")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OR-3")) in user.roles
#     ):
#         background_image = Image.open(r"assets/images/background/OR-1-3.png")
#     elif (
#             guild.get_role(ranks_controller.get_rank_id_by_name("OR-4")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OR-5")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OR-6")) in user.roles
#     ):
#         background_image = Image.open(r"assets/images/background/OR-4-6.png")
#     elif (
#             guild.get_role(ranks_controller.get_rank_id_by_name("OR-7")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OR-8")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OR-9")) in user.roles
#     ):
#         background_image = Image.open(r"assets/images/background/OR-7-9.png")
#     ##
#
#     #  officer_roles
#     elif (
#             guild.get_role(ranks_controller.get_rank_id_by_name("OF-1")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OF-2")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OF-3")) in user.roles
#     ):
#         background_image = Image.open(r"assets/images/background/OF-1-3.png")
#     elif guild.get_role(ranks_controller.get_rank_id_by_name("OF-4")) in user.roles:
#         background_image = Image.open(r"assets/images/background/OF-4.png")
#     elif (
#             guild.get_role(ranks_controller.get_rank_id_by_name("OF-5")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OF-6")) in user.roles
#     ):
#         background_image = Image.open(r"assets/images/background/OF-5-6.png")
#     elif (
#             guild.get_role(ranks_controller.get_rank_id_by_name("OF-7")) in user.roles
#             or guild.get_role(ranks_controller.get_rank_id_by_name("OF-8")) in user.roles
#     ):
#         background_image = Image.open(r"assets/images/background/OF-7-8.png")
#     elif guild.get_role(ranks_controller.get_rank_id_by_name("OF-9")) in user.roles:
#         background_image = Image.open(r"assets/images/background/OF-9.png")
#     elif guild.get_role(ranks_controller.get_rank_id_by_name("OF-10")) in user.roles:
#         background_image = Image.open(r"assets/images/background/OF-10.png")
#     ##
#     else:
#         background_image = Image.open(r"bot/assets/images/background/OR-1-3.png")
#     return background_image
from util.ranks_controller import get_member_rank


async def get_user_avatar(user):
    try:
        avatar_size = (190, 190)
        avatar_zone = (0, 0)
        avatar_mask = Image.new("L", avatar_size, 0)
        avatar_draw = ImageDraw.Draw(avatar_mask)
        avatar_draw.rectangle((0, 0) + avatar_size, fill=255)
        avatar_url = str(user.avatar.url)
        resp = requests.get(avatar_url, stream=True)
        resp = Image.open(io.BytesIO(resp.content))
        resp = resp.convert("RGBA")
        resp = resp.resize((190, 190), Image.ANTIALIAS)
        avatar = ImageOps.fit(resp, avatar_mask.size)
        avatar.putalpha(avatar_mask)
        return avatar, avatar_zone
        # card.paste(avatar, avatar_zone, avatar)
    except (AttributeError, TypeError) as e:
        return False


async def get_user_qrcode(user):
    thunderskill_link = "https://thunderskill.com/ru/stat/"
    nickname = await get_user_nickname(user)
    qrcode_image = qr.make(f"{thunderskill_link}{str(nickname)}")
    qrcode_image_zone = (1410, 0)
    qrcode_image_size = (190, 190)
    qrcode_image_mask = Image.new("L", qrcode_image_size, 0)
    qrcode_image_draw = ImageDraw.Draw(qrcode_image_mask)
    qrcode_image_draw.rectangle((0, 0) + qrcode_image_size, fill=255)
    qrcode_image = ImageOps.fit(qrcode_image, qrcode_image_mask.size)
    return qrcode_image, qrcode_image_zone


async def get_user_nickname(user):
    nickname = re.search("(?<=\]) (.*?) (?=\()", user).group(0).strip()
    # print(f"[INFO] user nickname: {nickname}")
    return nickname


async def draw_user_nickname(user, card):
    user_name_text_zone = (30, 630)
    W, H = (1600, 1200)

    user_name = f"{user.nick}"
    user_name = user_name.split("]")
    user_name = user_name[1].split("(")
    user_name = user_name[0]

    font_size = 100
    font = ImageFont.truetype(
        "assets/fonts/Montserrat-ExtraLight.ttf", font_size, encoding="unic"
    )
    user_name_text_draw = ImageDraw.Draw(card)
    user_name = user_name.replace("_", " ")
    user_name_text_draw.text(
        (user_name_text_zone[0] + 3, user_name_text_zone[1] + 3),
        user_name,
        fill="black",
        font=font,
    )
    user_name_text_draw.text(user_name_text_zone, user_name, fill="white", font=font)


async def draw_user_rank(user, card):
    user_rank_text_zone = (1415, 655)
    user_rank = get_member_rank(user, str=True)
    font_size = 50
    font = ImageFont.truetype(
        "assets/fonts/Montserrat-ExtraLight.ttf", font_size, encoding="unic"
    )
    user_rank_text_draw = ImageDraw.Draw(card)
    user_rank_text_draw.text(
        (user_rank_text_zone[0] + 3, user_rank_text_zone[1] + 3),
        user_rank,
        fill="black",
        font=font,
    )
    user_rank_text_draw.text(user_rank_text_zone, user_rank, fill="white", font=font)


async def get_user_background_image(self, user, client):
    global image_path
    random.seed(None, version=2)
    guild = client.get_guild(settings["guildId"])

    # if (
    #         guild.get_role(roles_config.unit_roles["tanks"]) in user.roles
    #         and guild.get_role(roles_config.unit_roles["planes"]) in user.roles
    # ):
    #     if random.randint(0, 1) == 1:
    #         image_path = f"assets/images/user_images/tanks/tank ({random.randint(1, 17)}).jpg"
    #     else:
    #         image_path = f"assets/images/user_images/planes/plane ({random.randint(1, 17)}).jpg"
    #
    # elif guild.get_role(roles_config.unit_roles["tanks"]) in user.roles:
    #     image_path = (
    #         f"assets/images/user_images/tanks/tank ({random.randint(1, 17)}).jpg"
    #     )
    # elif guild.get_role(roles_config.unit_roles["planes"]) in user.roles:
    #     image_path = (
    #         f"assets/images/user_images/planes/plane ({random.randint(1, 17)}).jpg"
    #     )
    image_path = f"assets/images/test_set/plane ({random.randint(1, 51)}).jpg"
    user_image = Image.open(image_path).convert("RGBA")
    # await create_gradient(user_path)
    print(f"[INFO] user_image path: {image_path}")
    # await get_user_medals(self, user)
    user_image = user_image.resize((1580, 580), Image.ANTIALIAS)

    gradient = await create_gradient(image_path)
    return user_image, gradient


async def get_user_medals(self, user):

    with self.con.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `UserMedals` WHERE `user_id` = {user.id};")
        medals_tuple = cursor.fetchone()
    self.con.commit()
    medals_list = list(medals_tuple)
    medals_list.pop(0)
    counter = 0
    for medal_id in range(len(medals_list)):
        if medals_list[medal_id] != 0:
            counter = counter + 1

    medal_zone = [-250, 800]

    pos_x = -400
    offset_x = 250
    pos_y = 730
    if counter == 1:
        pos_x = 365
    elif counter == 2:
        pos_x = 220
    elif counter == 3:
        pos_x = 110
    elif counter == 4:
        pos_x = -10
    elif counter == 5:
        pos_x = -135
    elif counter == 6:
        pos_x = -280

    medal_placement = Image.new("RGBA", (1600, 1200), (0, 0, 0, 0))
    for medal_id in range(len(medals_list)):
        if medals_list[medal_id] != 0:
            pos_x = pos_x + offset_x
            medal_image = Image.open(
                f"assets/images/medals/medal ({medal_id + 1}).png", "r"
            ).convert(("RGBA"))
            medal_image = medal_image.resize((400, 400))
            medal_zone[0] = medal_zone[0] + 250
            # print(f"medal_id{medal_id + 1}: {medals_list[medal_id]}")
            medal_placement.paste(medal_image, [int(pos_x), int(pos_y)], medal_image)
            await get_medal_info(medals_list[medal_id], pos_x+180, medal_placement)
    return medal_placement


async def get_medal_info(medal_count, pos_x, medal_placement):
    font = ImageFont.truetype("assets/fonts/Montserrat-ExtraLight.ttf", 50, encoding="unic")
    medal_info = ImageDraw.Draw(medal_placement)
    medal_info.text((pos_x + 3, 1080+3), str(medal_count), fill="black", font=font)
    medal_info.text((pos_x, 1080), str(medal_count), fill="white", font=font)


async def get_color_scheme(image_path):
    # image = Image.open(image_path)
    # color_scheme = ColorThief(image_path)
    color_pallete = ColorThief(image_path).get_palette(color_count=4)
    print(f"get_palette: {color_pallete}")
    return color_pallete


async def create_gradient(image_path):
    full_gradient = Image.new("RGBA", (1600, 600), (0, 0, 0, 255))
    # placeholder = Image.new('RGBA', (1600, 600), (127, 127, 127, 255))
    colors = await get_color_scheme(image_path)
    gradient_zone_width = 0
    gradient_zone_height = 0
    # full_gradient.paste(placeholder,(800,500),placeholder)
    for i in range(4):
        gradient = Image.new("RGB", (800, 300), (colors[i]))
        if i == 2:
            gradient_zone_height = gradient_zone_height + 300
            gradient_zone_width = gradient_zone_width - 1600
        full_gradient.paste(gradient, (gradient_zone_width, gradient_zone_height))
        gradient_zone_width = gradient_zone_width + 800
    new_gradient = full_gradient.filter(ImageFilter.GaussianBlur(radius=200))
    # new_gradient = full_gradient
    new_gradient = new_gradient.resize((1580, 580))
    return new_gradient


def create_rounded_rectangle_mask(size, radius, alpha=255):
    factor = (
        5  # Factor to increase the image size that I can later antialiaze the corners
    )
    radius = radius * factor
    image = Image.new("RGBA", (size[0] * factor, size[1] * factor), (0, 0, 0, 0))

    # create corner
    corner = Image.new("RGBA", (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    # added the fill = .. you only drew a line, no fill
    draw.pieslice(
        (0, 0, radius * 2, radius * 2), 180, 270, fill=(50, 50, 50, alpha + 55)
    )

    # max_x, max_y
    mx, my = (size[0] * factor, size[1] * factor)

    # paste corner rotated as needed
    # use corners alpha channel as mask
    image.paste(corner, (0, 0), corner)
    image.paste(corner.rotate(90), (0, my - radius), corner.rotate(90))
    image.paste(corner.rotate(180), (mx - radius, my - radius), corner.rotate(180))
    image.paste(corner.rotate(270), (mx - radius, 0), corner.rotate(270))

    # draw both inner rects
    draw = ImageDraw.Draw(image)
    draw.rectangle([(radius, 0), (mx - radius, my)], fill=(50, 50, 50, alpha))
    draw.rectangle([(0, radius), (mx, my - radius)], fill=(50, 50, 50, alpha))
    image = image.resize(size, Image.ANTIALIAS)  # Smooth the corners

    return image
