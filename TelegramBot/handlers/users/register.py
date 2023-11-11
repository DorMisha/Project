from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import IsPrivate
from keyboards.default import kb_menu
from loader import dp

from states import register


@dp.message_handler(IsPrivate(), Command('register'))
async def register_(message: types.Message):

    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    name = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'{message.from_user.first_name}')
            ],
        ],
        resize_keyboard=True
    )

    await message.answer('Привет, ты начал регистрацию,\nВведи своё имя', reply_markup=name)
    await register.test1.set()

@dp.message_handler(state=register.test1)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(test1=answer)
    await message.answer('Сколько тебе лет?')
    await register.test2.set()


@dp.message_handler(state=register.test2)
async def state2(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(test2=answer)
    data = await state.get_data()
    name = data.get('test1')
    years = data.get('test2')
    await message.answer(f'Регистрация успешно завершена\n'
                         f'Твоё имя {name}\n'
                         f'Тебе {years} лет', reply_markup=kb_menu)
    await state.finish()
