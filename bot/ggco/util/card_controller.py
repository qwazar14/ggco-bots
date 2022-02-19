import fnmatch
import io
import os
import random
import re

import qrcode as qr
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from colorthief import ColorThief

from config import roles_config
from config.access_config import settings
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


async def count_jpg_files_in_folder(path):
    return len(fnmatch.filter(os.listdir(path), "*.jpg"))


async def get_background_image_path(user, guild):
    try:
        background_images_path = f"assets/images/background/user_images/{user.id}"
        random_last_index = await count_jpg_files_in_folder(path=background_images_path)
    except FileNotFoundError:
        if (
            guild.get_role(roles_config.unit_roles["tanks"]) in user.roles
            and guild.get_role(roles_config.unit_roles["planes"]) in user.roles
        ):
            if random.randint(0, 1) == 1:
                background_images_path = f"assets/images/background/tanks_images"
            else:
                background_images_path = f"assets/images/background/planes_images"
        elif guild.get_role(roles_config.unit_roles["tanks"]) in user.roles:
            background_images_path = f"assets/images/background/tanks_images"
        elif guild.get_role(roles_config.unit_roles["planes"]) in user.roles:
            background_images_path = f"assets/images/background/planes_images"
        random_last_index = await count_jpg_files_in_folder(path=background_images_path)
    image_path = (
        f"{background_images_path}/({random.randint(1, random_last_index)}).jpg"
    )
    return image_path


async def get_user_background_image(self, user, client):
    random.seed(None, version=2)
    guild = client.get_guild(settings["guildId"])

    image_path = await get_background_image_path(user, guild)
    user_image = Image.open(image_path).convert("RGBA")
    # print(f"[INFO] user_image path: {image_path}")
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
            # medal_path = await get_medals_images(medal_id, medals_list[medal_id])
            # medal_image = Image.open(medal_path, "r").convert(("RGBA"))
            medal_image = await get_medals_images(medal_id + 1, medals_list[medal_id])
            medal_image = medal_image.resize((400, 400))
            medal_zone[0] = medal_zone[0] + 250
            # print(f"medal_id{medal_id + 1}: {medals_list[medal_id]}")
            medal_placement.paste(medal_image, [int(pos_x), int(pos_y)], medal_image)
            await get_medal_info(medals_list[medal_id], pos_x + 180, medal_placement)
    return medal_placement


async def get_medal_info(medal_count, pos_x, medal_placement):
    font = ImageFont.truetype(
        "assets/fonts/Montserrat-ExtraLight.ttf", 50, encoding="unic"
    )
    medal_info = ImageDraw.Draw(medal_placement)
    medal_info.text((pos_x + 3, 1080 + 3), str(medal_count), fill="black", font=font)
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


async def get_medals_images(medal_id, medal_count):
    image = Image.open(f"assets/images/medals/medal ({medal_id}).png").convert("RGBA")
    if medal_id in range(1, 5):
        if medal_count >= 16:
            image = Image.open(
                f"assets/images/medals/additional_medals/medal{medal_id}_2.png"
            ).convert("RGBA")
        elif medal_count >= 4:
            image = Image.open(
                f"assets/images/medals/additional_medals/medal{medal_id}_1.png"
            ).convert("RGBA")

    elif medal_id == 6 or medal_id == 8 and medal_count >= 5:
        image = Image.open(
            f"assets/images/medals/additional_medals/medal{medal_id}_1.png"
        ).convert("RGBA")

    elif medal_id == 13:
        for i in range(5):
            if medal_count == 5 - i + 1:
                image = Image.open(
                    f"assets/images/medals/additional_medals/medal{medal_id}_{i}.png"
                ).convert("RGBA")

    return image


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
