from aiogram.dispatcher.filters.state import StatesGroup, State


class balance(StatesGroup):
    amount = State()