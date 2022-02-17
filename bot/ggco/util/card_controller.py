import io
import random
import re

import qrcode as qr
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

from config import roles_config
from config.access_config import settings
from util import ranks_controller


async def get_background_image(self, user, client):
    #  NITRO
    global background_image
    guild = client.get_guild(settings["guildId"])
    # guild = '398857722159824907'
    # #  NITRO
    # if '853942930229559318' in user.roles:
    #     background_image = Image.open(r'bot/assets/images/background/NITRO.png')
    # ##

    #  soldier_roles
    if (
            guild.get_role(ranks_controller.get_rank_id_by_name("OR-1")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OR-2")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OR-3")) in user.roles
    ):
        background_image = Image.open(r"assets/images/background/OR-1-3.png")
    elif (
            guild.get_role(ranks_controller.get_rank_id_by_name("OR-4")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OR-5")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OR-6")) in user.roles
    ):
        background_image = Image.open(r"assets/images/background/OR-4-6.png")
    elif (
            guild.get_role(ranks_controller.get_rank_id_by_name("OR-7")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OR-8")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OR-9")) in user.roles
    ):
        background_image = Image.open(r"assets/images/background/OR-7-9.png")
    ##

    #  officer_roles
    elif (
            guild.get_role(ranks_controller.get_rank_id_by_name("OF-1")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OF-2")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OF-3")) in user.roles
    ):
        background_image = Image.open(r"assets/images/background/OF-1-3.png")
    elif guild.get_role(ranks_controller.get_rank_id_by_name("OF-4")) in user.roles:
        background_image = Image.open(r"assets/images/background/OF-4.png")
    elif (
            guild.get_role(ranks_controller.get_rank_id_by_name("OF-5")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OF-6")) in user.roles
    ):
        background_image = Image.open(r"assets/images/background/OF-5-6.png")
    elif (
            guild.get_role(ranks_controller.get_rank_id_by_name("OF-7")) in user.roles
            or guild.get_role(ranks_controller.get_rank_id_by_name("OF-8")) in user.roles
    ):
        background_image = Image.open(r"assets/images/background/OF-7-8.png")
    elif guild.get_role(ranks_controller.get_rank_id_by_name("OF-9")) in user.roles:
        background_image = Image.open(r"assets/images/background/OF-9.png")
    elif guild.get_role(ranks_controller.get_rank_id_by_name("OF-10")) in user.roles:
        background_image = Image.open(r"assets/images/background/OF-10.png")
    ##
    else:
        background_image = Image.open(r"bot/assets/images/background/OR-1-3.png")
    return background_image


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


async def format_user_nickname(user, card):
    user_name_text_zone = (633, 0)
    W, H = (1600, 1200)

    user_name = f"{user.nick}"
    user_name = user_name.split("]")
    user_name = user_name[1].split("(")
    user_name = user_name[0]

    font_size = 200
    font_size_tmp = float(font_size)
    print(f"Nickname length: {len(user_name)}")
    for i in range(len(user_name)):
        if 9 < len(user_name) <= 12:
            font_size_tmp -= 1.5
            font_size = int(font_size_tmp)
        elif len(user_name) > 12:
            font_size_tmp -= 3.8
            font_size = int(font_size_tmp)
        else:
            pass

    print(f"total font_size = {font_size}")

    font = ImageFont.truetype("arialbd.ttf", font_size, encoding="unic")
    user_name_text_draw = ImageDraw.Draw(card)
    user_name = user_name.replace("_", " ")
    im = Image.new("RGBA", (W, H), "yellow")
    draw = ImageDraw.Draw(im)
    w, h = draw.textsize(user_name, font=font)

    user_name_text_draw.text(
        ((W - w) / 2, user_name_text_zone[1]), user_name, fill="white", font=font
    )


async def get_user_nickname(user):
    nickname = re.search("(?<=\]) (.*?) (?=\()", user).group(0).strip()
    print(f"[INFO] user nickname: {nickname}")
    return nickname


async def get_user_background_image(self, user, client):
    random.seed(None, version=2)
    guild = client.get_guild(settings["guildId"])

    if (
            guild.get_role(roles_config.unit_roles["tanks"]) in user.roles
            and guild.get_role(roles_config.unit_roles["planes"]) in user.roles
    ):
        if random.randint(0, 1) == 1:
            user_path = f"assets/images/user_images/tanks/tank ({random.randint(1, 17)}).jpg"
        else:
            user_path = f"assets/images/user_images/planes/plane ({random.randint(1, 17)}).jpg"

    elif guild.get_role(roles_config.unit_roles["tanks"]) in user.roles:
        user_path = (
            f"assets/images/user_images/tanks/tank ({random.randint(1, 17)}).jpg"
        )
    elif guild.get_role(roles_config.unit_roles["planes"]) in user.roles:
        user_path = (
            f"assets/images/user_images/planes/plane ({random.randint(1, 17)}).jpg"
        )

    user_image = Image.open(user_path).convert("RGBA")
    print(f"[INFO] user_image path: {user_path}")
    # await get_user_medals(self, user)
    user_image = user_image.resize((1090, 615), Image.ANTIALIAS)
    return user_image


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

    print(medals_list)

    medal_zone = [-250, 850]
    medal_width = 223
    medal_length = 237
    pos_x = 0
    offset_x = 210
    pos_y = 855

    print(counter)
    print(counter)
    print(counter)
    print(counter)
    if counter <= 7:
        offset_x = 210
        pos_x = -180
    elif 7 < counter <= 9:
        offset_x = int((1 / counter) * 1400) + 20
        pos_x = int((1 / counter) * -1300) - 50
    elif 10 <= counter <= 15:
        offset_x = int((1 / counter) * 1400) + 20
        pos_x = int((1 / counter) * -1300) - 50
    elif counter >= 16:
        offset_x = 100
        pos_x = -110
    if counter != 6:
        for i in range(counter - 7):
            medal_width = medal_width - 14
            medal_length = medal_length - 14

    medal_placement = Image.new('RGBA', (1600, 1200), (0, 0, 0, 0))
    for medal_id in range(len(medals_list)):
        if medals_list[medal_id] != 0:
            pos_x = pos_x + offset_x
            medal_image = Image.open(f"assets/images/medals/{medal_id + 1}.png", 'r')
            medal_image = medal_image.resize((medal_width, medal_length))
            medal_zone[0] = medal_zone[0] + 250
            print(f"medal_id{medal_id + 1}: {medals_list[medal_id]}")
            medal_placement.paste(medal_image, [int(pos_x), int(pos_y)], medal_image)

    return medal_placement
