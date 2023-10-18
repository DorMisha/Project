import aiosqlite, logging, traceback, string, random, time
from aiogram import types

path_to_db = 'data/base/fleen_stickers.sqlite'

async def user_link(user_id, first_name):
    text = f"<a href='tg://user?id={user_id}'>{first_name}</a>"
    return text

async def random_word(length):
    letters = string.ascii_letters
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

async def dont_sub_message():
	text = '''
<b>❗️ Что бы создать стикеры
подпишетесь на спонсоров ⬇️</b>
	'''
	return text

############# User #############


async def register_user(user_id, enter_time, uniq):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = (user_id, enter_time, 0, uniq)
			await db.execute("INSERT INTO users VALUES (?, ?, ?, ?)", data)
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def deactivate_user(user_id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute(f"UPDATE users SET deactivated = 1 WHERE user_id = '{user_id}'")
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")
			return None

async def get_user(user_id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			user = await db.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
			return await user.fetchone()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")
			return None

async def get_users():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			users = await db.execute(f"SELECT * FROM users")
			return await users.fetchall()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")
			return None

async def get_disactive_users():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			users = await db.execute(f"SELECT user_id FROM users WHERE deactivated = 1")
			return await users.fetchall()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")
			return None

async def delete_users(users):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			users = ', '.join([us[0] for us in users])
			await db.execute(f"DELETE FROM users WHERE user_id IN ({users})")
			await db.commit()
			await db.execute(f"DELETE FROM adpost_users WHERE user_id IN ({users})")
			await db.commit()
			await db.execute(f"DELETE FROM adlinks_users WHERE user_id IN ({users})")
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def delete_user(user_id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute("DELETE FROM users WHERE user_id = (?)", (user_id, ))
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

############# Info #############


async def get_stats():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			# Все юзеры
			us_all = await db.execute(f"SELECT COUNT(*) FROM users")
			us_all = (await us_all.fetchone())[0]
			# Активные юзеры
			us_act = await db.execute(f"SELECT COUNT(*) FROM users WHERE deactivated = 0")
			us_act = (await us_act.fetchone())[0]

			# За сегодня юзеров
			us_tom = await db.execute(f"SELECT COUNT(0) FROM users WHERE enter_time >= {int(time.time()) - 86400}")
			us_tom = (await us_tom.fetchone())[0]
			# Саморост
			us_samorost = await db.execute(f"SELECT COUNT(1) FROM users WHERE (uniq = 1) IS NOT FALSE and enter_time >= {int(time.time()) - 86400}")
			us_samorost = (await us_samorost.fetchone())[0]
			# За неделю юзеров
			us_wek = await db.execute(f"SELECT count(0) FROM users WHERE enter_time >= {int(time.time()) - 604800}")
			us_wek = (await us_wek.fetchone())[0]
			# Саморост
			us_samorost_wek = await db.execute(f"SELECT COUNT(1) FROM users WHERE (uniq = 1) IS NOT FALSE and enter_time >= {int(time.time()) - 604800}")
			us_samorost_wek = (await us_samorost_wek.fetchone())[0]

			# С рекламных ссылок
			us_ssilka = await db.execute(f"SELECT count(*) FROM adlinks_users")
			us_ssilka = (await us_ssilka.fetchone())[0]
			# С рекламных ссылок ЗА СЕГОДНЯ
			us_ssilka_tom = await db.execute(f"SELECT count(0) FROM adlinks_users WHERE enter_time >= {int(time.time()) - 86400}")
			us_ssilka_tom = (await us_ssilka_tom.fetchone())[0]
			# С рекламных ссылок ЗА НЕДЕЛЮ
			us_ssilka_wek = await db.execute(f"SELECT count(0) FROM adlinks_users WHERE enter_time >= {int(time.time()) - 604800}")
			us_ssilka_wek = (await us_ssilka_wek.fetchone())[0]

			return [us_all, us_act, us_tom, us_samorost, us_wek, us_samorost_wek, us_ssilka, us_ssilka_tom, us_ssilka_wek]

		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")
			return None

async def get_adlinks_stat(_name):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			ad_all = await db.execute(f"SELECT count_subs FROM adlinks WHERE name = '{_name}'")
			ad_all = (await ad_all.fetchone())[0]

			# За сегодня юзеров
			ad_tom = await db.execute(f"SELECT count(0) FROM adlinks_users WHERE name = '{_name}' AND enter_time >= {int(time.time()) - 86400}")
			ad_tom = (await ad_tom.fetchone())[0]

			# За неделю юзеров
			ad_wek = await db.execute(f"SELECT count(0) FROM adlinks_users WHERE name = '{_name}' AND enter_time >= {int(time.time()) - 604800}")
			ad_wek = (await ad_wek.fetchone())[0]

			ad_op = await db.execute(f"SELECT count_op FROM adlinks WHERE name = '{_name}'")
			ad_op = (await ad_op.fetchone())[0]

			return [ad_all, ad_tom, ad_wek, ad_op]

		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")
			return None


############# Links #############


async def get_links():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			links = await db.execute("SELECT * FROM links")
			return await links.fetchall()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def get_link(name):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			link = await db.execute(f"SELECT * FROM links WHERE name = '{name}'")
			return await link.fetchone()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def add_link(link, channel_id, type, name):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = (link, channel_id, type, name)
			await db.execute("INSERT INTO links VALUES (?, ?, ?, ?)", data)
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def remove_link(link):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute("DELETE FROM links WHERE link = (?)", (link, ))
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")


############# ADPOST #############


async def get_adpost(id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			adposts = await db.execute(f"SELECT * FROM adpost WHERE id = {id}")
			return await adposts.fetchone()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def get_adposts():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			adposts = await db.execute("SELECT * FROM adpost")
			return await adposts.fetchall()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def get_adpost_ids():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			adposts = await db.execute("SELECT id FROM adpost WHERE seen != count")
			return await adposts.fetchall()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def user_adposted_check(id, user_id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			adposts = await db.execute(f"SELECT * FROM adpost_users WHERE id = {id} AND user_id = '{user_id}'")
			if await adposts.fetchone() is None:
				return False
			return True
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def add_adpost(rm, uid, mid, count):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = (str(rm), uid, mid, 0, count)
			await db.execute("INSERT INTO adpost (rm, uid, mid, seen, count) VALUES (?, ?, ?, ?, ?)", data)
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def add_adpost_seens(id, user_id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute(f"UPDATE adpost SET seen = seen + 1 WHERE id = {id}")
			await db.commit()
			data = (id, user_id)
			await db.execute("INSERT INTO adpost_users (id, user_id) VALUES (?, ?)", data)
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def rem_adpost(id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute(f"DELETE FROM adpost WHERE id = {id}")
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")


############# AdLinks #############


async def get_adlinks():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			links = await db.execute("SELECT * FROM adlinks")
			return await links.fetchall()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def add_adlink(name, code):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = (name, code, 0, 0)
			await db.execute("INSERT INTO adlinks VALUES (?, ?, ?, ?)", data)
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def get_codes_adlinks():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			links = await db.execute("SELECT code FROM adlinks")
			return await links.fetchall()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def add_count_adlink(code, user_id, enter_time):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute(f"UPDATE adlinks SET count_subs = count_subs + 1 WHERE code = '{code}'")
			await db.commit()
			data = (code, user_id, enter_time)
			await db.execute("INSERT INTO adlinks_users (name, user_id, enter_time) VALUES (?, ?, ?)", data)
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def add_count_adlink_op(code):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute(f"UPDATE adlinks SET count_op = count_op + 1 WHERE code = '{code}'")
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")


async def get_count_adlink(code):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			links = await db.execute(f"SELECT count_subs FROM adlinks WHERE code = '{code}'")
			return await links.fetchone()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def clear_adlinks():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute("DELETE FROM adlinks")
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

########### STICKER PACKS ###########

async def add_sticker_pack(name, user_id, uuid):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = (user_id, name, uuid)
			await db.execute("INSERT INTO sticker_packs VALUES (?, ?, ?)", data)
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def get_sticker_packs(user_id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = await db.execute(f"SELECT name FROM sticker_packs WHERE user_id = '{user_id}'")
			return await data.fetchall()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def get_sticker_pack(name, user_id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = await db.execute(f"SELECT * FROM sticker_packs WHERE user_id = '{user_id}' AND name = '{name}'")
			return await data.fetchone()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def get_sticker_from_rand_pack():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = await db.execute(f"SELECT name FROM rand_stickers")
			return await data.fetchall()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def get_stickers_from_pack(name, user_id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = await db.execute(f"SELECT COUNT(*) FROM stickers WHERE user_id = '{user_id}' AND name = '{name}'")
			return await data.fetchone()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def add_sticker(user_id, name, uuid, emoji, sticker):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = (user_id, name, uuid, emoji, sticker)
			await db.execute("INSERT INTO stickers VALUES (?, ?, ?, ?, ?)", data)
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def add_rand_pack(user_id, name):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			data = (user_id, name)
			await db.execute("INSERT INTO rand_stickers VALUES (?, ?)", data)
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def delete_sticker_pack(uuid, user_id):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute(f"DELETE FROM sticker_packs WHERE uuid = '{uuid}' AND user_id = '{user_id}'")
			await db.commit()
			await db.execute(f"DELETE FROM stickers WHERE uuid = '{uuid}' AND user_id = '{user_id}'")
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

async def delete_rand_stickerpack(name):
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute(f"DELETE FROM rand_stickers WHERE name = '{name}'")
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

############# Settings #############


async def default_inserts(dp):
	print('Bot started!')
	await dp.bot.set_my_commands([
		types.BotCommand("start", "Запустить бота")
	])


async def create_tables():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute("CREATE TABLE IF NOT EXISTS users ("
							"user_id TEXT, enter_time INTEGER,"
							"deactivated BOOLEAN, uniq BOOLEAN)")

			await db.execute("CREATE TABLE IF NOT EXISTS sticker_packs ("
							"user_id TEXT, name TEXT, uuid TEXT)")
			await db.execute("CREATE TABLE IF NOT EXISTS stickers ("
							"user_id TEXT, name TEXT, uuid TEXT,"
							"emoji TEXT, sticker TEXT)")
			await db.execute("CREATE TABLE IF NOT EXISTS rand_stickers ("
							 "user_id TEXT, name TEXT)")

			await db.execute("CREATE TABLE IF NOT EXISTS links ("
							"link TEXT, id TEXT, type TEXT, name TEXT)")
			await db.execute("CREATE TABLE IF NOT EXISTS adlinks ("
							"name TEXT, code TEXT,"
							"count_subs INTEGER, count_op INTEGER)")
			await db.execute("CREATE TABLE IF NOT EXISTS adlinks_users ("
							"name TEXT, user_id TEXT, enter_time INTEGER)")
			await db.execute("CREATE TABLE IF NOT EXISTS adpost ("
							"id INTEGER PRIMARY KEY AUTOINCREMENT,"
							"rm TEXT, uid INTEGER, mid INTEGER,"
							"seen INTEGER, count INTEGER)")
			await db.execute("CREATE TABLE IF NOT EXISTS adpost_users ("
							"id INTEGER, user_id TEXT)")			
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")