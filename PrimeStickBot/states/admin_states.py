from aiogram.dispatcher.filters.state import State, StatesGroup

class add_list_stick(StatesGroup):
    text = State()

class remove_disactive_users(StatesGroup):
    check = State()

class add_link_st(StatesGroup):
    type = State()
    link = State()
    channel_id = State()

class rem_link_st(StatesGroup):
    channel_id = State()

class add_adlink_st(StatesGroup):
    name = State()

class mailing_st_pic(StatesGroup):
    source_pic = State()
    keyb = State()
    text = State()

class mailing_st(StatesGroup):
    keyb = State()
    text = State()

class mailing_forward(StatesGroup):
    mes = State()

class add_adpost_st(StatesGroup):
    mes = State()
    count = State()

class rem_adpost_st(StatesGroup):
    id = State()