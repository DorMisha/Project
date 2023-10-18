from aiogram.dispatcher.filters.state import State, StatesGroup

class global_state(StatesGroup):
    what = State()
    text = State()
    color = State()
    thing = State()

class add_sticker_state(StatesGroup):
    name = State()
    emoji = State()
    sticker = State()

class op_adlink(StatesGroup):
    code = State()
    _ = State()

class add_rand_stickerpack(StatesGroup):
    name = State()