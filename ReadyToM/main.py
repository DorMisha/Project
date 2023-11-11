# - *- coding: utf- 8 - *-

async def on_startup(dp):
    import filters
    filters.setup(dp)

    import middlewares
    middlewares.setup(dp)

    from data.sqlite import default_inserts, create_tables
    await create_tables()
    await default_inserts()


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates= True)