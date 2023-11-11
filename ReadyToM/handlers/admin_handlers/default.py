# - *- coding: utf- 8 - *-
import os
from loader import dp, bot
from keyboards.admin_keyboard import *
from keyboards.user_keyboard import *
from filters.admin_filter import IsAdmin
from data.sqlite import *
from states.admin_states import *
from config.config_file import *

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext

async def panel_text(data):
    text = f"""
🔧 <b><u>Панель:</u></b>

👥 <i>Юзеров:</i> <code>{len(await get_users())}</code>

<b>/getids</b> - Получить базу айди
    """
    # <b>/private_link_see</b> - Посмотреть текст, который бот отписывает при принятии заявки
    # <b>/private_link TEXT</b> - Изменить текст, который бот отписывает при принятии заявки
    return text

@dp.message_handler(IsAdmin(), text = "🔧 Панель 🔧", state = "*")
async def helpomation(message: types.Message, state: FSMContext):
    await state.finish()
    data = await get_stats()
    await message.answer(text=await panel_text(data), reply_markup= await admin_menu())

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'close_panel')
async def call_close_panel(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(c.from_user.id, c.message.message_id)
    await bot.send_message(chat_id=c.from_user.id, text=f'👋🏻 <b>Добро пожаловать!</b>\n <i>Используй кнопку:</i>', reply_markup= await user_menu(c.from_user.id))

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'backtime')
async def call_links(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    data = await get_stats()
    await bot.edit_message_text(chat_id=c.from_user.id, text=await panel_text(data), message_id=c.message.message_id, reply_markup=await admin_menu())

@dp.message_handler(IsAdmin(), text = "/getids", state = "*")
async def panel_menu(message: types.Message, state: FSMContext):
    a = await message.answer(f"<i>Собираю ...</i>")
    
    users = await get_users()
    with open("data/users.txt", "w") as f:
        pass
    for us in users:
        with open("data/users.txt", "a+") as f:
            f.write(us[0]+'\n')

    await bot.delete_message(a.chat.id, a.message_id)
    await bot.send_document(message.from_user.id, open("data/users.txt", "rb"))
    os.remove('data/users.txt')
    
@dp.message_handler(IsAdmin(), text = "/private_link_see", state = "*")
async def private_link_see(message: types.Message, state: FSMContext):
    text = await get_private_link_text()
    if text != None:
        await message.answer('<b>Текст:</b>')
        await message.answer(text[0])
    else:
        await message.answer('<b>Текст отсутствует</b>')


@dp.message_handler(IsAdmin(), lambda message: "/private_link" in message.text, state = "*")
async def private_link(message: types.Message, state: FSMContext):
    text = message.text.replace('/private_link ', '', 1)
    text_link = await get_private_link_text()
    if text_link != None:
        await edit_private_link_text(text, True)
        await message.answer('✔️ <b>Успешно</b>')
    else:
        await edit_private_link_text(text, False)
        await message.answer('✔️ <b>Успешно</b>')



################# AD POST #################

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'adpost')
async def call_links(c: types.CallbackQuery):
    await bot.edit_message_text(chat_id=c.from_user.id, text=f'➕<i>Выбери что сделать:</i>', message_id=c.message.message_id, reply_markup=await adpost_add_rem())

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'clear_adposted', state = '*')
async def adlinks_rem(c: types.CallbackQuery, state: FSMContext):
    await clear_adpost()
    await bot.send_message(c.from_user.id, '✔️ <b>Успешно</b>', reply_markup = await user_menu(c.from_user.id))

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'get_adposted', state = '*')
async def adlinks_rem(c: types.CallbackQuery, state: FSMContext):
    data = await get_adpost()
    if data != None:
        if data[0] != 'None':
            await bot.copy_message(c.from_user.id, data[1], data[2], parse_mode='Markdown', reply_markup=data[0], allow_sending_without_reply=True)
            await bot.send_message(c.from_user.id, f'👁 <b>Пост просмотрен:</b> <code>{data[3]}</code> раз(а)')
        else:
            await bot.copy_message(c.from_user.id, data[1], data[2], parse_mode='Markdown', allow_sending_without_reply=True)
            await bot.send_message(c.from_user.id, f'👁 <b>Пост просмотрен:</b> <code>{data[3]}</code> раз(а)')
    else:
        await bot.send_message(c.from_user.id, f'Пост отсутствует!')

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'add_adposted', state = '*')
async def mailings_forw1(c: types.CallbackQuery, state: FSMContext):
    await add_adpost_st.mes.set()
    await bot.send_message(c.from_user.id, '<i>Перешли сообщение:</i>', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(IsAdmin(), state = add_adpost_st.mes, content_types=[ContentType.PHOTO, ContentType.TEXT, ContentType.VOICE, ContentType.VIDEO])
async def mailings_forw1(message: types.Message, state: FSMContext):
    rm = message.reply_markup
    uid = message.from_user.id
    mid = message.message_id
    await state.finish()
    await add_adpost(rm,uid,mid)
    await bot.send_message(message.from_user.id, '✔️ <b>Успешно</b>', reply_markup = await user_menu(message.from_user.id))


############# Линки #############


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'links')
async def call_links(c: types.CallbackQuery):
    await bot.edit_message_text(chat_id=c.from_user.id, text=f'➕ <b>Не забывайте добавлять ботов в каналы!</b> ➕\n<i>Выбери что сделать:</i>', message_id=c.message.message_id, reply_markup=await link_add_rem())

### Добавление линки ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'add_linked', state = '*')
async def links_add(c: types.CallbackQuery, state: FSMContext):
    await bot.send_message(c.from_user.id, '<i>Выбери тип:</i>', reply_markup=await type_link())

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'bot_add_linked', state = '*')
async def links_add(c: types.CallbackQuery, state: FSMContext): 
    await add_link_st.link.set()
    await state.update_data(type='bot')
    await bot.send_message(c.from_user.id, '<i>Линк на бота:</i>', reply_markup=ReplyKeyboardRemove())

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'channel_add_linked', state = '*')
async def links_add(c: types.CallbackQuery, state: FSMContext): 
    await add_link_st.link.set()
    await state.update_data(type='channel')
    await bot.send_message(c.from_user.id, '<i>Линк на канал | название</i>', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(IsAdmin(), state = add_link_st.link)
async def links_add_lnk1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        type = data['type']
        overall = message.text.split(' | ')
        data['link'] = overall[0]
        data['name'] = overall[1]

    if type == 'channel':
        await message.answer('<i>ID канала(@userinfobot), вместе с  "-":</i>')
        await add_link_st.next()
    else:
        channel_id = 'bot'
        link = overall[0]
        type = 'bot'
        name = overall[1]
        await state.finish()

        await add_link(link, channel_id, type, name)
        await message.answer(f'✔️ <b>Успешно!</b>\n<i>Ссылка:</i> <code>{link}</code>', reply_markup=await admin_menu())


@dp.message_handler(IsAdmin(), state = add_link_st.channel_id)
async def links_add_lnk2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        channel_id = message.text
        link = data['link']
        type = data['type']
        name = data['name']
    await state.finish()

    await add_link(link, channel_id, type, name)
    await message.answer(f'✔️ <b>Успешно!</b>\n<i>Имя канала</i>: <code>{name}</code>\n<i>Ссылка:</i> <code>{link}</code>\n<i>ID канала</i>: <code>{channel_id}</code>', reply_markup=await admin_menu())

### Удаление линки ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'rem_linked', state = '*')
async def links_rem(c: types.CallbackQuery, state: FSMContext):
    await rem_link_st.channel_id.set()
    await bot.send_message(c.from_user.id, '<i>Введи <b>ССЫЛКУ</b> канала/бота, которого хочешь удалить:</i>', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(IsAdmin(), state = rem_link_st.channel_id)
async def links_rem_lnk1(message: types.Message, state: FSMContext):
    await state.finish()
    link = message.text

    await remove_link(link)
    await message.answer(f'✔️ <b>Успешно!</b>\n<i>Ссылка</i>: <code>{link}</code>', reply_markup=await admin_menu())

### Просмотр линков ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'get_linked', state = '*')
async def links_add(c: types.CallbackQuery, state: FSMContext):
    channels = await get_links()
    await bot.send_message(c.from_user.id, '<i>Линки + ID каналов на данный момент:</i>')
    i = 0
    if channels != []:
        for data in channels:
            if data[2] == 'channel':
                if i == 0:
                    txt = '1'
                else:
                    txt = str(i + 1)
                await bot.send_message(c.from_user.id, f'🖥 <b>Линка №{txt}</b>\n<i>Имя канала:</i> <code>{data[3]}</code>\n<i>Линк:</i> <code>{data[0]}</code>\n<i>ID канала:</i> <code>{data[1]}</code>')
                i+=1
    await bot.send_message(c.from_user.id, '<i>Линки ботов на данный момент:</i>')
    i = 0
    if channels != []:
        for data in channels:
            if data[2] == 'bot':
                if i == 0:
                    txt = '1'
                else:
                    txt = str(i + 1)
                await bot.send_message(c.from_user.id, f'🤖 <b>Линка №{txt}</b>\n<i>Линк:</i> <code>{data[0]}</code>')
                i+=1
    else:
        await bot.send_message(c.from_user.id, f'✖️ <b>Линки отсутствуют</b> ✖️', reply_markup = await user_menu(c.from_user.id))


############# Рекламные линки #############


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'adlinks')
async def call_adlinks(c: types.CallbackQuery):
    await bot.edit_message_text(chat_id=c.from_user.id, text=f'➕ <b>Рекламные линки:</b>\n<i>Выбери что сделать:</i>', message_id=c.message.message_id, reply_markup=await adlink_add_rem())

### Добавление рекламной линки ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'add_adlinked', state = '*')
async def adlinks_add(c: types.CallbackQuery, state: FSMContext):
    await add_adlink_st.name.set()
    await bot.send_message(c.from_user.id, '➕ <b>Отправьте название канала</b>\n<i>Оно будет отображаться только в статистике</i>')

@dp.message_handler(IsAdmin(), state = add_adlink_st.name)
async def links_add_lnk2(message: types.Message, state: FSMContext):
    await state.finish()
    name = message.text
    code = 'ad-'+await random_word(10)
    link = f'https://t.me/{bot_user}?start='+code
    await add_adlink(name, code)
    await message.answer(f'✔️ <b>Ваша ссылка:</b> <code>{link}</code>', reply_markup = await user_menu(message.from_user.id))

### Очистка рекламных линок ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'clear_adlinked', state = '*')
async def adlinks_rem(c: types.CallbackQuery, state: FSMContext):
    await clear_adlinks()
    await bot.send_message(c.from_user.id, '✔️ <b>Успешно</b>', reply_markup = await user_menu(c.from_user.id))

### Просмотр рекламных линков ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'get_adlinked', state = '*')
async def adlinks_get(c: types.CallbackQuery, state: FSMContext):
    adlinks = await get_adlinks()
    await bot.send_message(c.from_user.id, '<b>Имя канала | линк | кол-во вступивших</b>')
        
    text = ''
    for link in adlinks:
        text += f'<code>{link[0]}</code> | <code>t.me/{bot_user}?start={link[1]}</code> | <code>{link[2]}</code>\n'

    if text == '':
        text = '✖️ <b>В боте отсутствуют рекламные линки</b> ✖️'

    await bot.send_message(c.from_user.id, text, reply_markup = await user_menu(c.from_user.id))



############# Рассылка #############


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'mailing')
async def callback_rassilka(c: types.CallbackQuery):
    await bot.edit_message_text(chat_id=c.from_user.id, text='<i>Выбери что сделать:</i>', message_id=c.message.message_id, reply_markup=await mailing_pic_not())

### Текстовая ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'mailing_text', state = '*')
async def mailings_text(c: types.CallbackQuery, state: FSMContext):
    await mailing_st.keyb.set()
    await bot.send_message(c.from_user.id, '<b>Напиши inline-клавиатуру в виде, можно много, каждую на новую строку:</b>\n\ntext | link\n\n<i><u>Если не надо пиши:</u></i> <code>0</code>', reply_markup=InlineKeyboardMarkup())

@dp.message_handler(IsAdmin(), state = mailing_st.keyb)
async def mailings_text1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keyb = message.text
        if keyb == '0':
            keyb = types.InlineKeyboardMarkup(1)
        else:
            a = keyb.split('\n')
            keyb = types.InlineKeyboardMarkup(1)
            for but in a:
                b = but.split(' | ')
                print(b)
                keyb.add(InlineKeyboardButton(str(b[0]).strip(), url=str(b[1]).strip()))
        data['keyb'] = str(keyb)

        await message.answer('<i>Напиши текст рассылки</i>', reply_markup=InlineKeyboardMarkup(row_width=1,
                                                                                               inline_keyboard=[
                                                                                                   [
                                                                                                       InlineKeyboardButton(text='Отменить', callback_data='quit')
                                                                                                   ]
                                                                                               ]))
        await mailing_st.next()

@dp.message_handler(IsAdmin(), state = mailing_st.text)
async def mailings_text1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keyb = data['keyb']
        await state.finish()
        text = message.text
        users = await get_users()
        nice = 0
        nothing = 0
        for user in users:
            try:
                await bot.send_message(user[0], text, reply_markup=keyb, disable_web_page_preview=True)
                nice += 1
            except:
                nothing += 1
                pass

        await message.answer(f'💲 <b>Рассылка окончена!</b> 💲\n<i>Дошло:</i> {str(nice)}\n<i>Не дошло:</i> {str(nothing)}', reply_markup = await user_menu(message.from_user.id))

### Текстовая + Пикча ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'mailing_pic', state = '*')
async def mailings_text(c: types.CallbackQuery, state: FSMContext):
    await mailing_st_pic.source_pic.set()
    await bot.send_message(c.from_user.id, '<i>Отправь фото:</i>', reply_markup=InlineKeyboardMarkup(row_width=1,
                                                                                               inline_keyboard=[
                                                                                                   [
                                                                                                       InlineKeyboardButton(text='Отменить', callback_data='quit')
                                                                                                   ]
                                                                                               ]))

@dp.message_handler(IsAdmin(), content_types=ContentType.PHOTO, state = mailing_st_pic.source_pic)
async def mailings_text1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        a = await message.answer('<i>Скачиваю...</i>')
        src_rand = 'ads_pic.jpg'
        await message.photo[-1].download(src_rand)
        data['source_pic'] = src_rand
        await bot.delete_message(message.from_user.id, message.message_id)
        await bot.delete_message(a.chat.id, a.message_id)
        await message.answer(f"<b>Напиши inline-клавиатуру в виде, можно много, каждую на новую строку:</b>\n\ntext | link\n\n<i><u>Если не надо пиши:</u></i> <code>0</code>")
    await mailing_st_pic.next()

@dp.message_handler(IsAdmin(), state = mailing_st_pic.keyb)
async def mailings_text2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keyb = message.text
        if keyb == '0':
            keyb = types.InlineKeyboardMarkup(1)
        else:
            a = keyb.split('\n')
            keyb = types.InlineKeyboardMarkup(1)
            for but in a:
                b = but.split(' | ')
                keyb.add(InlineKeyboardButton(str(b[0]).strip(), url=str(b[1]).strip()))
        data['keyb'] = str(keyb)

        await message.answer('<i>Напиши текст рассылки</i>', reply_markup=InlineKeyboardMarkup(row_width=1,
                                                                                               inline_keyboard=[
                                                                                                   [
                                                                                                       InlineKeyboardButton(text='Отменить', callback_data='quit')
                                                                                                   ]
                                                                                               ]))
        await mailing_st_pic.next()

@dp.message_handler(IsAdmin(), state = mailing_st_pic.text)
async def mailings_text1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        source_pic = data['source_pic']
        keyb = data['keyb']
        text = message.text
    await state.finish()
        
    users = await get_users()
    nice = 0
    nothing = 0
    for user in users:
        try:
            await bot.send_photo(user[0], photo=open(source_pic, 'rb'), caption=text, reply_markup=keyb)
            nice += 1
        except:
            nothing += 1
            pass
    os.remove(source_pic)
    await message.answer(f'💲 <b>Рассылка окончена!</b> 💲\n<i>Дошло:</i> {str(nice)}\n<i>Не дошло:</i> {str(nothing)}', reply_markup = await user_menu(message.from_user.id))



@dp.callback_query_handler(IsAdmin(), state=[mailing_st.text, mailing_st_pic.source_pic, mailing_st_pic.text, mailing_st_pic.keyb])
async def mailings_quit(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Рассылка отменена', reply_markup=await admin_menu())