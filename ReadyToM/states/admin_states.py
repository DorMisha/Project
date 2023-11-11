# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup

class add_link_st(StatesGroup):
    type = State()
    link = State()
    channel_id = State()

class rem_link_st(StatesGroup):
    channel_id = State()

class add_adlink_st(StatesGroup):
    name = State()

class add_adpost_st(StatesGroup):
    mes = State()

class mailing_st_pic(StatesGroup):
    source_pic = State()
    keyb = State()
    text = State()

class mailing_st(StatesGroup):
    keyb = State()
    text = State()


class add_days(StatesGroup):
    user_id = State()
    count = State()

class rem_days(StatesGroup):
    user_id = State()
    count = State()