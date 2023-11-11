import asyncio

from data import config
from utils.db_api import quick_commands as commands
from utils.db_api.db_gino import db


async def db_test():
    await db.set_bind(config.POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    await commands.add_user(1, 'Mike', 'Net')
    await commands.add_user(253464, 'Rostya', 'Yes')
    await commands.add_user(23, 'Dota', 'Имя')
    await commands.add_user(256, 'telegram', 'g5')
    await commands.add_user(538, 'ddd', 'dd')

    users = await commands.select_all_users()
    print(users)

    count = await commands.count_users()
    print(count)

    user = await commands.select_user(1)
    print(user)

    await commands.update_user_name(1, 'MishaD')
    user = await commands.select_user(1)
    print(user)

loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
