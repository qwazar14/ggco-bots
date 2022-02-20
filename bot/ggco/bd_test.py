import pymysql
import disnake as discord
from config.bd_config import CONFIG


def __init__(self, client):
    self.client = client
    self.con = pymysql.connect(
        host=CONFIG["host"],
        user=CONFIG["user"],
        password=CONFIG["password"],
        database=CONFIG["db"])


async def add(self, ctx, user, medal_id):
    with self.con.cursor() as cursor:
        if user is None:
            user = ctx.author
        cursor.execute(
            f"INSERT INTO `MedalsDB` (`user_id`, `medal_id`) VALUES ('{user.id}', '{medal_id}')"
        )
    self.con.commit()
