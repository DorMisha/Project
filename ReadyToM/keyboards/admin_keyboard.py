# - *- coding: utf- 8 - *-
from random import randint
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from config import config_file
from data.sqlite import *


async def admin_menu():
	keyboard = InlineKeyboardMarkup(row_width=2)
	a = InlineKeyboardButton('⛓ Линки', callback_data='links')
	b = InlineKeyboardButton('🌊 Рассылка', callback_data='mailing')
	c = InlineKeyboardButton('🍿 Рекламные ссылки', callback_data='adlinks')
	e = InlineKeyboardButton('✖️ Закрыть', callback_data='close_panel')
	keyboard.add(a,b)
	keyboard.add(c)
	keyboard.add(e)

	return keyboard

async def adlink_add_rem():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('➕ Добавить', callback_data='add_adlinked'),
		InlineKeyboardButton('✖️ Очистить', callback_data='clear_adlinked'),
		InlineKeyboardButton('💲 Посмотреть', callback_data='get_adlinked'))
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))

	return keyboard

async def link_add_rem():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('➕ Добавить', callback_data='add_linked'),
		InlineKeyboardButton('✖️ Удалить', callback_data='rem_linked'),
		InlineKeyboardButton('💲 Посмотреть', callback_data='get_linked'))
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))

	return keyboard

async def type_link():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('🖥 Канал', callback_data='channel_add_linked'),
		InlineKeyboardButton('🤖 Бот', callback_data='bot_add_linked'))
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))

	return keyboard

async def adpost_add_rem():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('➕ Добавить', callback_data='add_adposted'),
		InlineKeyboardButton('✖️ Очистить', callback_data='clear_adposted'),
		InlineKeyboardButton('💲 Посмотреть', callback_data='get_adposted'))
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))

	return keyboard

async def mailing_pic_not():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton('🧿 Текст', callback_data='mailing_text'),
				 InlineKeyboardButton('🧬 + Пикча', callback_data='mailing_pic'))
	keyboard.add(InlineKeyboardButton('🔙 Назад', callback_data='backtime'))
	
	return keyboard