# - *- coding: utf- 8 - *-
import aiosqlite, logging, traceback, datetime, string, random

path_to_db = 'data/chatbot.sqlite'


async def user_link(user_id, first_name):
    text = f"<a href='tg://user?id={user_id}'>{first_name}</a>"
    return text


async def random_word(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


async def dont_sub_message():
    text = '''
👋🏻 <b>Приветствую!</b>

<i>Чтобы пользоваться данным ботом, подпишись на наши каналы, а затем нажми на кнопку "<b>Проверить подписку</b>"</i>

☺️ <b>Спасибо за понимание</b>
	'''
    return text


############# User #############


async def register_user(user_id):
    async with aiosqlite.connect(path_to_db) as db:
        try:
            data = (user_id, 'True')
            await db.execute("INSERT INTO users VALUES (?, ?)", data)
            await db.commit()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")


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


############# Info #############


async def get_stats():
    async with aiosqlite.connect(path_to_db) as db:
        try:
            info_data = await db.execute("SELECT * FROM info")
            return await info_data.fetchone()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")

async def add_user_in_info():
	async with aiosqlite.connect(path_to_db) as db:
		try:
			await db.execute(f"UPDATE info SET users = users + 1")
			await db.commit()
		except Exception as e:
			stack = traceback.extract_stack()
			print(f"An exception occured in {stack[-2][2]} | {e}")

############# Links #############


async def get_links():
    async with aiosqlite.connect(path_to_db) as db:
        try:
            links = await db.execute("SELECT * FROM links")
            return await links.fetchall()
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
            await db.execute("DELETE FROM links WHERE link = (?)", (link,))
            await db.commit()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")


############# ADLinks #############


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
            data = (name, code, 0)
            await db.execute("INSERT INTO adlinks (name, code, count_subs) VALUES (?, ?, ?)", data)
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


async def add_count_adlink(code):
    async with aiosqlite.connect(path_to_db) as db:
        try:
            await db.execute(f"UPDATE adlinks SET count_subs = count_subs + 1 WHERE code = '{code}'")
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


############# AdPost #############


async def get_adpost():
    async with aiosqlite.connect(path_to_db) as db:
        try:
            links = await db.execute("SELECT * FROM adpost")
            return await links.fetchone()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")


async def add_adpost(rm, uid, mid):
    async with aiosqlite.connect(path_to_db) as db:
        try:
            data = (str(rm), uid, mid, 0)
            await db.execute("INSERT INTO adpost (rm, uid, mid, seen) VALUES (?, ?, ?, ?)", data)
            await db.commit()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")


async def add_adpost_seens(paramter):
    async with aiosqlite.connect(path_to_db) as db:
        try:
            await db.execute(f"UPDATE adpost SET seen = seen + {paramter}")
            await db.commit()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")


async def clear_adpost():
    async with aiosqlite.connect(path_to_db) as db:
        try:
            await db.execute("DELETE FROM adpost")
            await db.commit()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")


############# Settings #############

async def get_private_link_text():
    async with aiosqlite.connect(path_to_db) as db:
        try:
            link = await db.execute(f"SELECT text FROM private_link")
            return await link.fetchone()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")


async def edit_private_link_text(text, tf):
    async with aiosqlite.connect(path_to_db) as db:
        try:
            if tf == True:
                await db.execute("DELETE FROM private_link")
                await db.commit()
                await db.execute("INSERT INTO private_link (text) VALUES (?)", (text,))
                await db.commit()
            else:
                await db.execute("INSERT INTO private_link (text) VALUES (?)", (text,))
                await db.commit()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")

async def get_user_sub(user_id):
    async with aiosqlite.connect(path_to_db) as db:
        try:
            user = await db.execute(f"SELECT sub FROM users WHERE user_id = '{user_id}'")
            data = await user.fetchone()
            if data[0] != 'Отсутствует':
                return datetime.datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S.%f')
            else:
                return data[0]
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")
            return None

async def default_inserts():
    async with aiosqlite.connect(path_to_db) as db:
        try:
            info_data = await db.execute("SELECT * FROM info")
            info_data = await info_data.fetchone()
            if info_data is None:
                data = (0, 0)
                await db.execute("INSERT INTO info VALUES (?, ?)", data)
                await db.commit()
                print("Settings are set")
            else:
                print("Settings already applied")
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")


async def create_tables():
    async with aiosqlite.connect(path_to_db) as db:
        try:
            await db.execute("CREATE TABLE IF NOT EXISTS users ("
                             "user_id TEXT, first_time TEXT)")
            await db.execute("CREATE TABLE IF NOT EXISTS info ("
                             "users INTEGER, count_alive INTEGER)")
            await db.execute("CREATE TABLE IF NOT EXISTS adlinks ("
                             "name TEXT, code TEXT,"
                             "count_subs INTEGER)")
            await db.execute("CREATE TABLE IF NOT EXISTS adpost ("
                             "rm TEXT, uid INTEGER, mid INTEGER, seen INTEGER)")
            await db.execute("CREATE TABLE IF NOT EXISTS links ("
                             "link TEXT, id TEXT, type TEXT, name TEXT)")
            await db.execute("CREATE TABLE IF NOT EXISTS private_link ("
                             "text TEXT)")
            await db.commit()
        except Exception as e:
            stack = traceback.extract_stack()
            print(f"An exception occured in {stack[-2][2]} | {e}")
