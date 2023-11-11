from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram .dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from data.config import admins
from filters import IsPrivate
from keyboards.default import kb_menu

from loader import dp
from states import registration, accept
from utils.db_api import register_commands


@dp.message_handler(text='Отменить регистрацию', state=[registration.name, registration.phone, registration.age])
async def quit(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Регистрация отменена', reply_markup=kb_menu)


@dp.message_handler(IsPrivate(), Command('register'))
async def bot_register(message: types.Message):
    name = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'{message.from_user.first_name}')
            ],
            [
                KeyboardButton(text='Отменить регистрацию')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(f'Привет\n'
                         f'Для регистрации введи свое имя:',
                         reply_markup=name)

    await registration.name.set()

@dp.message_handler(IsPrivate(), state=registration.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    phone = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f'<b>{message.text}</b>, теперь пришли мне свой номер телефона для связи',
                         reply_markup=phone)

    await registration.phone.set()


@dp.message_handler(IsPrivate(), state=registration.phone)
async def get_phone(message: types.Message, state: FSMContext):
    answer = message.text
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ]
        ],
        resize_keyboard=True
    )
    try:
        if answer.replace('+', '').isnumeric():
            await state.update_data(phone=answer)

            await message.answer(f'Теперь пришли мне свой возраст (целым числом)',
                                 reply_markup=markup)
            await registration.age.set()
        else:
            await message.answer('Введите корректный номер', reply_markup=markup)
    except Exception:
        await message.answer('Введите корректный номер', reply_markup=markup)



@dp.message_handler(IsPrivate(), state=registration.age)
async def get_age(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isnumeric():
        if int(answer) < 150:
            await state.update_data(age=answer)
            data = await state.get_data()
            name = data.get('name')
            phone = data.get('phone')
            age = data.get('age')
            await register_commands.new_registration(user_id=message.from_user.id,
                                                     tg_first_name=message.from_user.first_name,
                                                     tg_last_name=message.from_user.last_name,
                                                     name=name,
                                                     phone=phone,
                                                     age=age,
                                                     status='created')
            await message.answer(f'Регистрация успешно завершена\n'
                                 f'Имя: {name}\n'
                                 f'Номер телефона: {phone}\n'
                                 f'Возраст: {age}',
                                 reply_markup=kb_menu)
            await state.finish()
        else:
            await message.answer('Введите корректный возраст')
    else:
        await message.answer('Введите корректный возраст (целым числом)')


@dp.message_handler(IsPrivate(), text='/registrations', user_id=admins)
async def get_reg(message: types.Message):
    reg = await register_commands.select_registration()
    ikb = InlineKeyboardMarkup(row_width=1,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text='Accept',
                                                            callback_data='Accept')
                                   ]
                               ])
    await message.answer(f'Дата создания: {reg.created_at}\n'
                         f'Id: {reg.user_id}\n'
                         f'First name: {reg.tg_first_name}\n'
                         f'Last name: {reg.tg_last_name}\n'
                         f'Name: {reg.name}\n'
                         f'Phone: {reg.phone}\n'
                         f'Age: {reg.age}\n'
                         f'Status: {reg.status}\n',
                         reply_markup=ikb)


@dp.callback_query_handler(text='Accept')
async def accept_reg(call: types.CallbackQuery):
    await call.message.answer(f'Введите айди для подтверждения')
    await accept.user_id.set()

@dp.message_handler(state=accept.user_id)
async def accept_reg(message: types.Message, state: FSMContext):
    await register_commands.accept_registration(message.text)
    await message.answer(f'Подтвержден: {message.text}')
    await state.finish()


