from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from config import config_file
from data.sqlite import *
from functions.check_subscribe import *

async def user_menu(user_id):
	keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	keyboard.add('✨ Создать Стикеры ✨')
	keyboard.add('⭐️ Мои Стикеры ⭐️')
	keyboard.add('⚡️ Каталог Стикеров ⚡️')

	if user_id in config_file.global_admins:
		keyboard.add('🔧 Панель 🔧')
	else:
		pass

	return keyboard

async def delete_kb():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(*[InlineKeyboardButton(f'✅', callback_data='confirm'),
				   InlineKeyboardButton(f'❌', callback_data='menu')])

	return keyboard

async def cancel_kb():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton(f'📛 Отмена 📛', callback_data='menu'))

	return keyboard

async def st_packs_menu():
	keyboard = InlineKeyboardMarkup(row_width=1)

	keyboard.add(InlineKeyboardButton('✨ Создать Стикеры ✨', callback_data='create_sticker_pack'))
	return keyboard

async def sticker_packs_menu(user_id):
	keyboard = InlineKeyboardMarkup(row_width=3)

	#keyboard.add(InlineKeyboardButton(f'🚛 Создать набор стикеров', callback_data='create_sticker_pack'))
	result = []
	data = await get_sticker_packs(user_id)
	for el in data:
		result.append(InlineKeyboardButton(el[0], callback_data='sticker_pack_'+el[0]+'|'+str(user_id)))

	keyboard.add(*result)
	return keyboard

async def rand_sticker_pack_menu(name):
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(InlineKeyboardButton(f'➕ Добавить стикерсет', url='https://t.me/addstickers/'+name))
	keyboard.add(InlineKeyboardButton('▶ Дальше', callback_data='next_rand_stickerpack'))
	keyboard.add(InlineKeyboardButton('✖ Закрыть', callback_data='close_panel'))

	return keyboard

async def sticker_pack_menu(name, user_id):
	keyboard = InlineKeyboardMarkup(row_width=3)

	data = await get_stickers_from_pack(name, user_id)
	if data != None and len(data) != 0:
		url = await get_sticker_pack(name, user_id)
		keyboard.add(InlineKeyboardButton(f'🖼 Посмотреть набор стикеров', url='https://t.me/addstickers/'+url[2]))

	keyboard.add(InlineKeyboardButton(f'➕ Добавить стикер', callback_data='add_sticker_'+name+'|'+str(user_id)))
	keyboard.add(InlineKeyboardButton(f'🗑 Удалить набор', callback_data='remove_sticker_pack_'+name+'|'+str(user_id)))

	return keyboard

async def stick_menu():
	keyboard = InlineKeyboardMarkup(row_width=2)

	buttons = [InlineKeyboardButton('🖼 Стикер из фото', callback_data='create_photo'),
			   InlineKeyboardButton('🔤 Стикер из текста', callback_data='create_text'),
			   InlineKeyboardButton('🤡 Демотиватор', callback_data='create_dem')]

	keyboard.add(*buttons)
	return keyboard

async def text_menu():
	keyboard = InlineKeyboardMarkup(row_width=2)

	buttons = [InlineKeyboardButton('🔤 С текстом', callback_data='text_text'),
			   InlineKeyboardButton('🖼 С аватаркой', callback_data='text_photo'),
			   InlineKeyboardButton('🔙 Назад', callback_data='back_create')]

	keyboard.add(*buttons)
	return keyboard

async def color_menu():
	keyboard = InlineKeyboardMarkup(row_width=3)

	buttons = [InlineKeyboardButton('⬜️', callback_data='color_⬜️'),
			   InlineKeyboardButton('⬛️', callback_data='color_⬛️'),
			   InlineKeyboardButton('🟦', callback_data='color_🟦'),
			   InlineKeyboardButton('🟩', callback_data='color_🟩'),
			   InlineKeyboardButton('🟨', callback_data='color_🟨'),
			   InlineKeyboardButton('🟥', callback_data='color_🟥')]

	keyboard.add(*buttons)
	return keyboard

async def sub(user_id):
	keyboard = InlineKeyboardMarkup(row_width=2)
	data = []
	links = await get_links()
	i = 0
	for link in links:
		i += 1
		if link[2] == 'channel':
			if await sub_channel(link, user_id) == False:
				data.append(InlineKeyboardButton(f'#{str(i)} Подписаться', url=link[0]))
		elif link[2] == 'channel_fake':
			data.append(InlineKeyboardButton(f'#{str(i)} Подписаться', url=link[0]))
		elif link[2] == 'bot':
			data.append(InlineKeyboardButton(f'#{str(i)} Запустить', url=link[0]))

	keyboard.add(*data)
	keyboard.add(InlineKeyboardButton(f'✅ Я подписался', callback_data='check_sub'))
	
	return keyboard