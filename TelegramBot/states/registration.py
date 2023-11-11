from aiogram.dispatcher.filters.state import StatesGroup, State


class registration(StatesGroup):
    name = State()
    phone = State()
    age = State()

class accept(StatesGroup):
    user_id = State()
