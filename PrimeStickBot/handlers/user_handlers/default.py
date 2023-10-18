# - *- coding: utf- 8 - *-
from loader import dp, bot
from keyboards.user_keyboard import *
from data.sqlite import *
from states.user_states import *
from config.config_file import *

import os, time
import random
from PIL import Image

from functions.check_subscribe import subscribed
from aiogram.utils.exceptions import BotBlocked
from functions.demotivator import Demotivator
from functions.text import BubbleDrawer, get_image_text
from functions.photo import create_sticker_from_picture

from aiogram import types
from aiogram.types import InputFile
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext


stats_text = f"""
<b>Привет!</b> 👋

<b>С помощью этого бота вы можете создать свой набор стикеров, а также найти стикеры в нашем каталоге</b>

<i>Выберите нужную вам кнопку:</i>
"""

async def user_adposted(user_id):
	ids = await get_adpost_ids()
	for id in ids:
		id = id[0]
		user = await user_adposted_check(id, user_id)
		if user is False:
			data = await get_adpost(id)
			if data[1] != 'None':
				await bot.copy_message(user_id, data[2], data[3], parse_mode='Markdown', reply_markup=data[1], allow_sending_without_reply=True)
			else:
				await bot.copy_message(user_id, data[2], data[3], parse_mode='Markdown', allow_sending_without_reply=True)
			result = await add_adpost_seens(id, user_id)
			return None

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.message, state: FSMContext):
	await state.finish()	
	user = await get_user(message.from_user.id)
	uniq = 1
	if user is None:
		if ' ' in message.text:
			code = message.text.replace('/start ', '').strip()
			codes = await get_codes_adlinks()
			ref = code
			if (code, ) in codes:
				await add_count_adlink(code, message.from_user.id, time.time())
				uniq = 0
		
		await register_user(message.from_user.id, time.time(), uniq)
		
	if uniq == 0:
		await op_adlink._.set()
		await state.update_data(code=code)
		await message.answer(await dont_sub_message(), reply_markup=await sub(message.from_user.id))
	else:
		await message.answer(f"{stats_text}",reply_markup=await user_menu(message.from_user.id), disable_web_page_preview=True)


@dp.callback_query_handler(lambda c: 'remove_sticker_pack_' in c.data, state="*")
async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await c.message.delete()
	if await subscribed(c.from_user.id):
		data = c.data.replace('remove_sticker_pack_', '').split('|')
		await state.set_state('delete_sticker')
		await state.update_data(name=data[0])
		await bot.send_message(c.from_user.id, f'📝 <b>Подтвердите удаление набора стикеров <code>{data[0]}</code>:</b>', reply_markup=await delete_kb())
	else:
		await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

@dp.callback_query_handler(lambda c: 'confirm' == c.data, state="*")
async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		name = data['name']
	await state.finish()
	await c.message.delete()
	if await subscribed(c.from_user.id):
		#print(name, c.from_user.id)
		data = await get_sticker_pack(name, c.from_user.id)
		print(data)
		await delete_sticker_pack(data[2], c.from_user.id)
		await c.message.answer('✅<b> Успешно! </b>✅')
		table = await get_sticker_packs(c.from_user.id)
		if table == []:
			await c.message.answer('Для начала создайте набор стикеров')
		else:
			await bot.send_message(c.from_user.id, '🌟 <i>Мои наборы стикеров</i>', reply_markup=await sticker_packs_menu(c.from_user.id))
	else:
		await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

@dp.message_handler(text='⚡️ Каталог Стикеров ⚡️', state="*")
async def rand_stick(message: types.Message, state: FSMContext):
	await state.finish()
	if await subscribed(message.from_user.id):
		try:
			data = await get_sticker_from_rand_pack()
			random_index = random.randint(0, len(data)-1)
			name_pack = data[random_index]
			rack = name_pack[0]
			test_pack = await bot.get_sticker_set(name=rack)
			pack = test_pack.stickers
			await bot.send_sticker(message.from_user.id, pack[0].file_id, reply_markup=await rand_sticker_pack_menu(rack))
			#await add_rand_stickerpack.name.set()

			#await message.answer('Введите название существующего стикерпака')
		except:
			await message.answer('Набор пока пуст, дождитесь пока администратор добавит наборы')
	else:
		await bot.send_message(message.from_user.id, await dont_sub_message(),
							   reply_markup=await sub(message.from_user.id))

@dp.callback_query_handler(lambda c: 'next_rand_stickerpack' == c.data, state='*')
async def next_rand_stick(c: types.CallbackQuery, state: FSMContext):
	await state.finish()

	data = await get_sticker_from_rand_pack()
	random_index = random.randint(0, len(data) - 1)
	name_pack = data[random_index]
	rack = name_pack[0]
	test_pack = await bot.get_sticker_set(name=rack)
	pack = test_pack.stickers
	await bot.send_sticker(c.from_user.id, pack[0].file_id, reply_markup=await rand_sticker_pack_menu(rack))

@dp.message_handler(state=add_rand_stickerpack.name)
async def add_rand_stickpack(message: types.Message, state: FSMContext):
	test = message.text
	await add_rand_pack(message.from_user.id, test)
	name_test = await get_sticker_from_rand_pack()
	st_pc = await bot.get_sticker_set(name=test)
	st = st_pc.stickers
	await bot.send_sticker(message.from_user.id, st[0].file_id, reply_markup=await rand_sticker_pack_menu(test))

	await state.finish()

@dp.message_handler(text='⭐️ Мои Стикеры ⭐️', state="*")
async def start(message: types.Message, state: FSMContext):
	await state.finish()
	if await subscribed(message.from_user.id):
		table = await get_sticker_packs(message.from_user.id)
		if table == []:
			await message.answer('Для начала создайте стикерпак')
		else:
			await bot.send_message(message.from_user.id, '🌟 <i>Мои наборы стикеров</i>', reply_markup=await sticker_packs_menu(message.from_user.id))
	else:
		await bot.send_message(message.from_user.id, await dont_sub_message(), reply_markup=await sub(message.from_user.id))

@dp.callback_query_handler(lambda c: 'sticker_pack_' in c.data, state="*")
async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await c.message.delete()
	if await subscribed(c.from_user.id):
		data = c.data.replace('sticker_pack_', '').split('|')
		await bot.send_message(c.from_user.id, f'👇🏻 <i>Выберите, что хотите сделать с набором стикеров (<code>{data[0]}</code>):</i>', reply_markup=await sticker_pack_menu(data[0],c.from_user.id))
	else:
		await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

@dp.callback_query_handler(lambda c: 'add_sticker_' in c.data, state="*")
async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await c.message.delete()
	if await subscribed(c.from_user.id):
		data = c.data.replace('add_sticker_', '').split('|')
		await add_sticker_state.sticker.set()
		await state.update_data(name=data[0])
		await bot.send_message(c.from_user.id, f'⚡️<b> Добавляем стикеры</b>\n\n<i>💬 Отправляй мне стикеры или фото, а я добавлю их в твой набор.</i>')
	else:
		await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

# @dp.message_handler(state=add_sticker_state.emoji)
# async def start(message: types.message, state: FSMContext):
# 	async with state.proxy() as data:
# 		data['emoji'] = message.text[0]
#
# 	if await subscribed(message.from_user.id):
# 		await add_sticker_state.next()
# 		await bot.send_message(message.from_user.id, f'📝 <i>Пришлите фото, для создания стикера:</i>')
# 	else:
# 		await bot.send_message(message.from_user.id, await dont_sub_message(), reply_markup=await sub(message.from_user.id))

@dp.message_handler(state=add_sticker_state.sticker, content_types=[ContentType.STICKER])
async def start_stick(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		name = data['name']
		uuid = (await get_sticker_pack(name, message.from_user.id))[2]
	await state.finish()

	if await subscribed(message.from_user.id):
		data = await get_stickers_from_pack(name, message.from_user.id)
		sticker = message.sticker.file_id
		if data != None and data[0] == 0:
			await bot.create_new_sticker_set(
				user_id=message.from_user.id,
				name=uuid,
				title=f'{name} (via @{bot_user})',
				png_sticker=sticker,
				emojis='🌚')
		else:
			await bot.add_sticker_to_set(user_id=message.from_user.id, name=uuid, png_sticker=sticker, emojis='🌚')
		await add_sticker(message.from_user.id, name, uuid, '🌚', sticker)

		await message.answer('✅<b> Успешно! </b>✅')
		await bot.send_message(message.from_user.id,
							   f'👇🏻 <i>Выберите, что хотите сделать с набором стикеров (<code>{name}</code>):</i>',
							   reply_markup=await sticker_pack_menu(name, message.from_user.id))

	else:
		await bot.send_message(message.from_user.id, await dont_sub_message(),
							   reply_markup=await sub(message.from_user.id))


@dp.message_handler(state=add_sticker_state.sticker, content_types=[ContentType.PHOTO])
async def start(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		name = data['name']
		#emoji = data['emoji']
		#emoji = '🌚'
		uuid = (await get_sticker_pack(name, message.from_user.id))[2]
	await state.finish()


	if await subscribed(message.from_user.id):
		data = await get_stickers_from_pack(name, message.from_user.id)

		res_rand = f'data/temp/sticker_{message.from_user.id}.png'
		await message.photo[-1].download(destination_file=res_rand)
		sticker_test = InputFile(await create_sticker_from_picture(res_rand))

		sticker_res = await bot.send_sticker(message.from_user.id, sticker_test)
		sticker = sticker_res.sticker.file_id
		await bot.delete_message(message.from_user.id, sticker_res.message_id)
		os.remove(res_rand)


		#try:
		if data != None and data[0] == 0:
			await bot.create_new_sticker_set(
							  	user_id=message.from_user.id,
							  	name=uuid,
							  	title=f'{name} (via @{bot_user})',
							  	png_sticker=sticker,
							  	emojis='🌚')
		else:
			await bot.add_sticker_to_set(user_id=message.from_user.id, name=uuid, png_sticker=sticker, emojis='🌚')
		await add_sticker(message.from_user.id, name, uuid, '🌚', sticker)


		await message.answer('✅<b> Успешно! </b>✅')
		await bot.send_message(message.from_user.id, f'👇🏻 <i>Выберите, что хотите сделать с набором стикеров (<code>{name}</code>):</i>', reply_markup=await sticker_pack_menu(name,message.from_user.id))
		#except:
			#await message.answer('Были введены некорректные данные, повторите попытку', reply_markup=await sticker_packs_menu(message.from_user.id))
	else:
		await bot.send_message(message.from_user.id, await dont_sub_message(), reply_markup=await sub(message.from_user.id))



@dp.message_handler(text='✨ Создать Стикеры ✨', state="*")
async def start(message: types.message, state: FSMContext):
	await state.finish()
	if await subscribed(message.from_user.id):
		await bot.send_message(message.from_user.id, '<i>Нажмите на кнопку ниже</i> 👇', reply_markup=await st_packs_menu())
	else:
		await bot.send_message(message.from_user.id, await dont_sub_message(), reply_markup=await sub(message.from_user.id))


@dp.callback_query_handler(lambda c: 'create_' in c.data)
async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	await c.message.delete()
	if await subscribed(c.from_user.id):
		text = 'Отправь фото с подписью' if c.data == 'create_dem' else 'Отправь фото' if c.data == 'create_photo' else 'Выбери, как будет выглядеть твой стикер' if c.data == 'create_text' else '⚡️<b> Cоздание набора</b>\n\n<i>💬 Отправь мне название своих новых стикеров</i>'
		kb = await text_menu() if c.data == 'create_text' else await cancel_kb()
		if c.data == 'create_text':
			await global_state.text.set()
		else:
			await global_state.thing.set()
		await state.update_data(what=c.data.replace('create_', ''))
		await bot.send_message(c.from_user.id, f'<i>{text}</i>', reply_markup = kb)
	else:
		await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

@dp.callback_query_handler(lambda c: 'text_' in c.data, state=global_state.text)
async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['text'] = c.data.replace('text_','',1)

	await c.message.delete()
	if await subscribed(c.from_user.id):
		if 'photo' in c.data:
			await state.finish()
			await global_state.thing.set()
			await state.update_data(what='text_photo')
			await bot.send_message(c.from_user.id, '📝 <i>Отправь текст:</i>')
		else:
			await global_state.next()
			await bot.send_message(c.from_user.id, '📝 <i>Выбери цвет текста:</i>', reply_markup = await color_menu())
	else:
		await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

#@dp.callback_query_handler(lambda c: 'color_' in c.data, state=global_state.color)
#async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	# colors = {
	# 	'⬜️': [(255, 255, 255), (200, 200, 200)],
	# 	'⬛️': [(0, 0, 0), (50, 50, 50)],
	# 	'🟦': [(0, 0, 255), (0, 0, 200)],
	# 	'🟩': [(0, 255, 0), (0, 200, 0)],
	# 	'🟨': [(255, 194, 0), (255, 170, 0)],
	# 	'🟥': [(255, 0, 0), (200, 0, 0)]
	# }
	# async with state.proxy() as data:
	# 	data['color'] = colors[c.data.replace('color_', '')]
	#
	# await c.message.delete()
	# if await subscribed(c.from_user.id):
	# 	await global_state.next()
	# 	await bot.send_message(c.from_user.id, '📝 <i>Отправь текст:</i>')
	# else:
	# 	await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

@dp.message_handler(state=global_state.thing, content_types=[ContentType.PHOTO, ContentType.TEXT])
async def global_state_st(message: types.message, state: FSMContext):
	async with state.proxy() as data:
		what = data['what']
		try:
			color = data['color']
		except:
			pass
	await state.finish()

	if await subscribed(message.from_user.id):
		if what == 'sticker_pack':
			if len(await get_sticker_packs(message.from_user.id)) <= 12:
				name = message.text
				await add_sticker_pack(name, message.from_user.id, await random_word(8)+'_by_'+bot_user)
				#await message.answer('👇🏻 <i>Выберите, что хотите сделать с вашими стикерпаками:</i>', reply_markup=await sticker_packs_menu(message.from_user.id))
				await add_sticker_state.sticker.set()
				await state.update_data(name=name)
				await bot.send_message(message.from_user.id, f'⚡️<b> Добавляем стикеры</b>\n\n<i>💬 Отправляй мне стикеры или фото, а я добавлю их в твой набор.</i>', reply_markup=await cancel_kb())
			else:
				await message.answer('⛔️ <b>Вы пытаетесь превысить доступное количество стикерпаков (<code>12</code>)</b> ⛔️')

		elif what == 'dem':
			src_rand = f'data/temp/{message.from_user.id}.jpg'
			res_rand = f'data/temp/demotivator_{message.from_user.id}.jpg'
			await message.photo[-1].download(destination_file=src_rand)

			data = []
			try:
				data.append(message.caption.split('\n')[0])
				data.append(message.caption.split('\n')[1])
			except:
				data = [message.caption]

			dem = Demotivator(*data) # 2 строчки
			dem.create(src_rand, result_filename=res_rand, watermark=bot_user, delete_file=True, arrange=True) # Название изображения, которое будет взято за основу демотиватора

			await bot.send_photo(message.from_user.id, photo=InputFile(res_rand), caption=f'<b>Сделано с помощью: @{bot_user}</b>')
			os.remove(res_rand)

		elif what == 'photo':
			res_rand = f'data/temp/sticker_{message.from_user.id}.png'
			await message.photo[-1].download(destination_file=res_rand)
			await bot.send_sticker(message.from_user.id, InputFile(await create_sticker_from_picture(res_rand)))
			os.remove(res_rand)

		elif what == 'text':
			res_rand = f"data/temp/text_{message.from_user.id}.png"
			await bot.send_sticker(message.from_user.id, InputFile(await get_image_text(res_rand, color, message.text)))

		elif what == 'text_photo':
			sticker_set_name = f"data/temp/quote_{message.from_user.id}.png"
			profile_photo = f"data/temp/profile_{message.from_user.id}.jpg"
		
			b = BubbleDrawer(message)

			result = await bot.get_user_profile_photos(message.from_user.id,limit=1)
			if result.total_count > 0:
				file = await bot.get_file(result.photos[0][0].file_id)
				await file.download(destination_file=profile_photo)
				b.set_avatar(profile_photo)

			b.draw()
			b.save(sticker_set_name)
			await bot.send_sticker(message.from_user.id, InputFile(sticker_set_name))
			os.remove(profile_photo)
			os.remove(sticker_set_name)
	else:
		await bot.send_message(message.from_user.id, await dont_sub_message(), reply_markup=await sub(message.from_user.id))

@dp.callback_query_handler(lambda c: c.data == 'check_sub', state = op_adlink._)
async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	await c.message.delete()
	if await subscribed(c.from_user.id):
		async with state.proxy() as data:
			code = data['code']
		await add_count_adlink_op(code)
		await bot.send_message(c.from_user.id, stats_text, reply_markup = await user_menu(c.from_user.id), disable_web_page_preview=True)
	else:
		await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

@dp.callback_query_handler(lambda c: c.data == 'check_sub', state = '*')
async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	await state.finish()
	user = await get_user(c.from_user.id)
	if user is None:
		await register_user(c.from_user.id, time.time())

	if await subscribed(c.from_user.id):
		await c.message.delete()
		await bot.send_message(c.from_user.id, stats_text, reply_markup = await user_menu(c.from_user.id), disable_web_page_preview=True)
	else:
		await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

@dp.callback_query_handler(lambda c: c.data == 'menu', state = '*')
async def check_sub_handler(c: types.CallbackQuery, state: FSMContext):
	await state.finish()
	if await subscribed(c.from_user.id):
		await c.message.delete()
		await c.message.answer(f"{stats_text}",reply_markup=await user_menu(c.from_user.id), disable_web_page_preview=True)
	else:
		await bot.send_message(c.from_user.id, await dont_sub_message(), reply_markup=await sub(c.from_user.id))

@dp.message_handler(text = "/chat_id", state = "*")
async def chat_id(message: types.Message, state: FSMContext):
	await message.answer(f'🌀 <b>Chat ID is:</b> <code>{message.chat.id}</code>')

@dp.chat_join_request_handler()
async def echo(message: types.Message):
	try:
		await bot.approve_chat_join_request(message.chat.id, message.from_user.id)
		user = await get_user(message.from_user.id)
		if user is None:
			await register_user(message.from_user.id, time.time())
		try:
			await bot.send_message(message.from_user.id, stats_text, reply_markup=await inline_menu(), disable_web_page_preview=True)
		except Exception as e:
			#print(e)
			pass
	except:
		pass
