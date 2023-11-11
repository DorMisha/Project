from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType

from filters import IsPrivate
from loader import dp
from utils.db_api import quick_commands as commands
from states import bot_mailing

from data.config import admins


@dp.message_handler(IsPrivate(), text='/mailing', chat_id=admins)
async def start_mailing(message: types.Message):
    await message.answer(f'Введите текст рассылки')
    await bot_mailing.text.set()

@dp.message_handler(IsPrivate(), state=bot_mailing.text, chat_id=admins)
async def mailing_text(message: types.Message, state: FSMContext):
    answer = message.text
    murkup = InlineKeyboardMarkup(row_width=3,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo'),
                                          InlineKeyboardButton(text='Далее', callback_data='next'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=murkup)
    await bot_mailing.state.set()


@dp.callback_query_handler(text='next', state=bot_mailing.state, chat_id=admins)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user.user_id, text=text)
            await sleep(0.33)
        except Exception:
            pass
    await call.message.answer('Рассылка выполнена')


@dp.callback_query_handler(text='add_photo', state=bot_mailing.state, chat_id=admins)
async def add_photo(call: types.CallbackQuery):
    await call.message.answer('Пришлите фото')
    await bot_mailing.photo.set()

@dp.message_handler(IsPrivate(), state=bot_mailing.photo, content_types=ContentType.PHOTO, chat_id=admins)
async def mailing_text(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Далее', callback_data='next'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)

@dp.callback_query_handler(text='next', state=bot_mailing.photo, chat_id=admins)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user.user_id, photo=photo, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await call.message.answer('Рассылка выполнена')


@dp.message_handler(IsPrivate(), state=bot_mailing.photo, chat_id=admins)
async def no_photo(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer('Пришли мне фотографию', reply_markup=markup)

@dp.callback_query_handler(text='quit', state=[bot_mailing.text, bot_mailing.photo, bot_mailing.state], chat_id=admins)
async def quit(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Рассылка отменена')

