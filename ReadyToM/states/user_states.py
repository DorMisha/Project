# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup

class StickerSet(StatesGroup):
    name = State()
    emodji = State()

class Chat(StatesGroup):
    chat_gpt = State()

class Generate(StatesGroup):
    gen = State()
    var_gen = State()