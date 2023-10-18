from random import randint
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from config import config_file
from data.sqlite import *


async def admin_menu():
	keyboard = InlineKeyboardMarkup(row_width=2)
	a = InlineKeyboardButton('📊 Статистика', callback_data='stats')
	st = InlineKeyboardButton('🎭 Стикеры', callback_data='adm_stick')
	b = InlineKeyboardButton('⛓ Линки', callback_data='links')
	c = InlineKeyboardButton('🌊 Рассылка', callback_data='mailing')
	d = InlineKeyboardButton('🍿 Рекламные ссылки', callback_data='adlinks')
	e = InlineKeyboardButton('🖼 Рекламные посты', callback_data='adpost')
	f = InlineKeyboardButton('📚 Скачать юзеров', callback_data='download_users')
	g = InlineKeyboardButton('💀 Удалить мёртвых', callback_data='delete_disactive_users')
	_ = InlineKeyboardButton('✖️ Закрыть', callback_data='close_panel')
	keyboard.add(a, st)
	keyboard.add(b,c,d,e)
	keyboard.add(f,g)
	keyboard.add(_)

	return keyboard

async def adm_list_stikers(user_id):
	keyboard = InlineKeyboardMarkup(row_width=3)

	keyboard.add(InlineKeyboardButton(f'➕ Добавить набор стикеров', callback_data='new_stikerpack'))
	res = []
	data = await get_sticker_from_rand_pack()

	for el in data:
		res.append(InlineKeyboardButton(el[0], callback_data='set_'+el[0]))

	keyboard.add(*res)
	return keyboard

async def list_stikers_in_set(name):
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('👀 Посмотреть набор', url='https://t.me/addstickers/'+name))
	keyboard.add(InlineKeyboardButton('❌ Удалить', callback_data='delete_rand_pack_'+name))

	return keyboard

async def confirm_kb():
	keyboard = InlineKeyboardMarkup(row_width=1)
	keyboard.add(InlineKeyboardButton('✅ Подтвердить', callback_data='confirm'),
				 InlineKeyboardButton('Отклонить', callback_data='backtime'))

	return keyboard


async def adlink_add_rem(data, row=3):
	keyboard = InlineKeyboardMarkup(row_width=row)
	keyboard.add(InlineKeyboardButton('➕ Добавить', callback_data='add_adlinked'),
		InlineKeyboardButton('✖️ Очистить', callback_data='clear_adlinked'))

	result = []
	for i in data:
		result.append(InlineKeyboardButton(i[0], callback_data='adlink_'+i[0]))

	keyboard.add(*result)
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))

	return keyboard

async def back_adlinks_kb():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backadlinks'))

	return keyboard

async def adpost_add_rem(data, row=3):
	keyboard = InlineKeyboardMarkup(row_width=row)
	keyboard.add(InlineKeyboardButton('➕ Добавить', callback_data='add_adposted'))

	result = []
	for i in data:
		result.append(InlineKeyboardButton('ID-'+str(i[0]), callback_data='adpost_'+str(i[0])))

	keyboard.add(*result)
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))

	return keyboard

async def rem_adpost_kb():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('Удалить пост', callback_data='remove_adpost'))

	return keyboard


async def link_add_rem(data, row=3):
	keyboard = InlineKeyboardMarkup(row_width=row)
	result = []

	keyboard.add(InlineKeyboardButton('➕ Добавить', callback_data='add_linked'))
	for i in data:
		result.append(InlineKeyboardButton(i[3], callback_data='l1nk_'+i[3]))

	keyboard.add(*result)
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))

	return keyboard

async def remove_link_kb():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('Удалить линку', callback_data='remove_link'))

	return keyboard


async def type_link():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('🖥 Канал', callback_data='channel_add_linked'),
				 InlineKeyboardButton('🤖 Бот', callback_data='bot_add_linked'),
				 InlineKeyboardButton('🖥 Канал (Без проверки)', callback_data='channel_fake_add_linked'))
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))

	return keyboard

async def mailing_pic_not():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('🧿 Текст', callback_data='mailing_text'),
		InlineKeyboardButton('🧬 + Пикча', callback_data='mailing_pic'),
		InlineKeyboardButton('🚛 Пересылка', callback_data='mailing_forw'))
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))
	
	return keyboard

async def back_panel():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))

	return keyboard