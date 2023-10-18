# - *- coding: utf- 8 - *-

async def on_startup(dp):
    import filters
    from aiogram import types
    from data.sqlite import default_inserts, create_tables
    filters.setup(dp)
    await create_tables()
    await default_inserts(dp)

if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup)