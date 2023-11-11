from aiogram import types

from data import config
from filters import IsGroup
from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=0, key='groups')
@dp.message_handler(IsGroup())
async def check_messages(message: types.Message):
    print(message.chat.id)
    text = message.text.lower().replace(' ', '')

    for banned_message in config.banned_messages:
        if banned_message in text:
            await message.delete()
