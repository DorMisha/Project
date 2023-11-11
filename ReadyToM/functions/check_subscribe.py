# - *- coding: utf- 8 - *-
from loader import dp, bot
from data.sqlite import *

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

async def subscribed(user_id):
    if await get_links() == []:
        return True
    else:
        ids = await get_links()
        check = []
        for data in ids:
            if data[2] == 'channel':
                data = await bot.get_chat_member(chat_id=data[1], user_id=user_id)
                status = str(data.status)
                if status != 'left':
                    check.append(True)
                else:
                    check.append(False)

        if False in check:
            return False
        else:
            return True