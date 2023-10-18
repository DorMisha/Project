from loader import dp, bot
from data.sqlite import *

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

async def sub_channel(link, user_id):
    try:
        data = await bot.get_chat_member(chat_id=link[1], user_id=user_id)
    except:
        return True

    status = str(data.status)
    if status != 'left':
        return True
    else:
        return False

async def subscribed(user_id):
    if await get_links() == []:
        return True
    else:
        ids = await get_links()
        check = []
        for data in ids:
            if data[2] == 'channel':
                print(data[1])
                try:
                    data = await bot.get_chat_member(chat_id=data[1], user_id=user_id)
                except:
                    check.append(True)
                print(data)
                status = str(data.status)
                if status != 'left':
                    check.append(True)
                else:
                    check.append(False)

        if False in check:
            return False
        else:
            return True