from aiogram import types

from keyboards.default import kb_test
from loader import dp

@dp.message_handler(text='Любой текст')
async def test(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}! \n'
                         f'Тут должен быть какой-то текст', reply_markup=kb_test)