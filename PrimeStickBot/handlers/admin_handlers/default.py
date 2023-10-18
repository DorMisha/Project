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

panel_text = "🔧 <b>Панель:</b>\n\nВыберите нужную вам настройку"


@dp.message_handler(IsAdmin(), text = "🔧 Панель 🔧", state = "*")
async def helpomation(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(panel_text, reply_markup= await admin_menu())

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'close_panel', state = "*")
async def call_close_panel(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(c.from_user.id, c.message.message_id)
    await bot.send_message(chat_id=c.from_user.id, text=f'Вернулись в главное меню', reply_markup= await user_menu(c.from_user.id))

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'backtime', state = "*")
async def call_links(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(c.from_user.id, c.message.message_id)
    await c.message.answer(panel_text, reply_markup= await admin_menu())

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'adm_stick', state ='*')
async def list_stick(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(c.from_user.id, c.message.message_id)
    await c.message.answer('Меню:', reply_markup= await adm_list_stikers(c.from_user.id))

@dp.callback_query_handler(IsAdmin(), lambda c: 'set_' in c.data, state='*')
async def work_with_rand_pack(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await c.message.delete()
    data = c.data.replace('set_', '')
    await bot.send_message(c.from_user.id, f'Выберите, что делать с набором <i>{data}</>', reply_markup=await list_stikers_in_set(name=data))

@dp.callback_query_handler(IsAdmin(), lambda c: 'delete_rand_pack_' in c.data, state='*')
async def delete_rand_set(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await c.message.delete()
    data = c.data.replace('delete_rand_pack_', '')
    await delete_rand_stickerpack(data)
    await bot.send_message(c.from_user.id, 'Набор удален', reply_markup=await adm_list_stikers(c.from_user.id))


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'new_stikerpack', state='*')
async def add_rand_stickpack(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await c.message.answer('Введите название существующего стикерпака \nПример: \n<i>(https://t.me/addstickers/<b>Name</b></i>)', reply_markup=await cancel_kb())
    await add_list_stick.text.set()


@dp.message_handler(state=add_list_stick.text)
async def add_pack_in_list(message: types.Message, state: FSMContext):
    name = message.text
    try:
        test = await bot.get_sticker_set(name=name)

        await add_rand_pack(message.from_user.id, name)
        await message.answer('Название добавлено', reply_markup=await adm_list_stikers(message.from_user.id))
    except:
        await message.answer('Набора с таким именем не существует',
                             reply_markup=await adm_list_stikers(message.from_user.id))



    await state.finish()

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'stats')
async def call_close_panel(c: types.CallbackQuery):
    await bot.delete_message(c.from_user.id, c.message.message_id)
    data = await get_stats()
    text = f"""
🤖 <u><b>В боте</b></u> 🤖
👤 <b>Всего:</b> <code>{data[0]}</code>
🗣 <b>Живых:</b> <code>{data[1]}</code>
☠️ <b>Мертвых:</b> <code>{data[0] - data[1]}</code>

За сегодня: <code>{data[2]}</code>
Саморост: <code>{data[3]}</code>
За неделю:  <code>{data[4]}</code>
Саморост: <code>{data[5]}</code>

🍿 <u><b>С рекламных ссылок:</b></u>
👤 <b>Всего:</b> <code>{data[6]}</code>

За сегодня: <code>{data[7]}</code>
За неделю: <code>{data[8]}</code>
    """
    await bot.send_message(chat_id=c.from_user.id, text=text, reply_markup= await back_panel())

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'download_users')
async def panel_get_users(c: types.CallbackQuery):
    a = await c.message.answer(f"<i>Собираю ...</i>")
    
    users = await get_users()
    with open("data/users.txt", "w") as f:
        pass
    for us in users:
        with open("data/users.txt", "a+") as f:
            f.write(us[0]+'\n')

    await a.delete()
    await bot.send_document(c.from_user.id, open("data/users.txt", "rb"))
    os.remove('data/users.txt')

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'delete_disactive_users')
async def panel_get_users(c: types.CallbackQuery):
    await remove_disactive_users.check.set()
    await c.message.answer('<b>Нажми «✅ Подтвердить»</b>', reply_markup=await confirm_kb())

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'confirm', state = remove_disactive_users.check)
async def panel_get_users(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete()
    await state.finish()
    data = await get_disactive_users()
    await c.message.answer(f'<b>Удаляю <code>{str(len(data))}</code> юзеров</b>')
    await delete_users(data)
    await c.message.answer('<b>✅ Успешно удалено!</b>')


############# Линки #############


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'links')
async def call_links(c: types.CallbackQuery):
    await bot.edit_message_text(chat_id=c.from_user.id, text=f'➕ <b>Не забывайте добавлять ботов в каналы!</b> ➕\n<i>Выбери что сделать:</i>', message_id=c.message.message_id, reply_markup=await link_add_rem(await get_links()))

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
    await bot.send_message(c.from_user.id, '<i>Линк на канал:</i>', reply_markup=ReplyKeyboardRemove())

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'channel_fake_add_linked', state = '*')
async def links_add(c: types.CallbackQuery, state: FSMContext): 
    await add_link_st.link.set()
    await state.update_data(type='channel_fake')
    await bot.send_message(c.from_user.id, '<i>Линк на канал:</i>', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(IsAdmin(), state = add_link_st.link)
async def links_add_lnk1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        type = data['type']
        data['link'] = message.text

    if type == 'channel':
        await message.answer(f'\n<i>Перешли пост с этого канала:</i>')
        await add_link_st.next()
    elif type == 'channel_fake':
        channel_id = 'channel_fake'
        link = message.text
        type = 'channel_fake'
        await state.finish()

        await add_link(link, channel_id, type, 'fake-'+str(random.randint(100000,999999)))
        await message.answer(f'✔️ <b>Успешно!</b>\n<i>Ссылка:</i> <code>{link}</code>', reply_markup=await admin_menu())
    else:
        channel_id = 'bot'
        link = message.text
        type = 'bot'
        await state.finish()

        await add_link(link, channel_id, type, 'bot-'+str(random.randint(100000,999999)))
        await message.answer(f'✔️ <b>Успешно!</b>\n<i>Ссылка:</i> <code>{link}</code>', reply_markup=await admin_menu())


@dp.message_handler(IsAdmin(), state = add_link_st.channel_id, content_types=[ContentType.ANY])
async def links_add_lnk2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        channel_id = message.forward_from_chat.id
        name = message.forward_from_chat.title
        link = data['link']
        type = data['type']
    await state.finish()

    await add_link(link, channel_id, type, name)
    await message.answer(f'✔️ <b>Успешно!</b>\n<i>Ссылка:</i> <code>{link}</code>\n<i>ID канала</i>: <code>{channel_id}</code>', reply_markup=await admin_menu())


@dp.callback_query_handler(IsAdmin(), lambda c: 'l1nk_' in c.data, state = '*')
async def adlinks_get(c: types.CallbackQuery, state: FSMContext):
    name = c.data.replace('l1nk_', '')
    data = await get_link(name)
    text = f"""
🔗 <b>Ссылка «{data[3]}» (<a href='{data[0]}'>*ССЫЛКА*</a>)</b>

⛓ <b>Ссылка:</b> <code>{data[0]}</code>
🆔 <b>Айди:</b> <code>{data[1]}</code>
    """
    await bot.send_message(c.from_user.id, text, reply_markup=await remove_link_kb(), disable_web_page_preview=True)

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'remove_link')
async def call_adlinks(c: types.CallbackQuery):
    link = c.message.text.split('\n')[2].split(': ')[1].strip()
    print(link)
    await remove_link(link)
    links = await get_links()
    await c.message.answer('✅ <b>Успешно!</b>', reply_markup=await links_kb(links))




################# AD POST #################


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'adpost')
async def call_links(c: types.CallbackQuery):
    await bot.edit_message_text(chat_id=c.from_user.id, text=f'➕<i>Выбери что сделать:</i>', message_id=c.message.message_id, reply_markup=await adpost_add_rem(await get_adposts()))

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'get_adposted', state = '*')
async def adlinks_rem(c: types.CallbackQuery, state: FSMContext):
    all_data = await get_adposts()
    await bot.send_message(c.from_user.id, '<b>Рекламные посты на данный момент</b>', reply_markup=await adpost_add_rem(all_data))

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'remove_adpost', state = '*')
async def adlinks_rem(c: types.CallbackQuery, state: FSMContext):
    id = c.message.text.split('\n')[0].split('№')[1].strip()
    await rem_adpost(id)
    await bot.send_message(c.from_user.id, '✔️ <b>Успешно</b>', reply_markup = await user_menu(c.from_user.id))

@dp.callback_query_handler(IsAdmin(), lambda c: 'adpost_' in c.data, state = '*')
async def adlinks_get(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete()
    id = c.data.replace('adpost_', '')
    data = await get_adpost(id)
    if data != None:
        if data[1] != 'None':
            await bot.copy_message(c.from_user.id, data[2], data[3], parse_mode='Markdown', reply_markup=data[1], allow_sending_without_reply=True)
            await bot.send_message(c.from_user.id, f'<b>Пост №{str(data[0])}</b>\n📱 <b>Осталось показов: <code>{str(int(data[5]) - int(data[4]))}</code> (<code>{str(data[5])}</code>)</b>\n👁 <b>Пост просмотрен:</b> <code>{data[4]}</code> раз(а)', reply_markup=await rem_adpost_kb())
        else:
            await bot.copy_message(c.from_user.id, data[2], data[3], parse_mode='Markdown', allow_sending_without_reply=True)
            await bot.send_message(c.from_user.id, f'<b>Пост №{str(data[0])}</b>\n📱 <b>Осталось показов: <code>{str(int(data[5]) - int(data[4]))}</code> (<code>{str(data[5])}</code>)</b>\n👁 <b>Пост просмотрен:</b> <code>{data[4]}</code> раз(а)', reply_markup=await rem_adpost_kb())
    
    all_data = await get_adposts()
    await bot.send_message(c.from_user.id, '<b>Рекламные посты на данный момент</b>', reply_markup=await adpost_add_rem(all_data))

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'add_adposted', state = '*')
async def mailings_forw1(c: types.CallbackQuery, state: FSMContext):
    await add_adpost_st.mes.set()
    await bot.send_message(c.from_user.id, '<i>Перешли сообщение:</i>', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(IsAdmin(), state = add_adpost_st.mes, content_types=[ContentType.PHOTO, ContentType.TEXT, ContentType.VOICE, ContentType.VIDEO])
async def mailings_forw1(message: types.Message, state: FSMContext):
    rm = message.reply_markup
    uid = message.from_user.id
    mid = message.message_id
    async with state.proxy() as data:
        data['mes'] = [rm, uid, mid]

    await add_adpost_st.next()
    await bot.send_message(message.from_user.id, '<i>Отправь количество показов:</i>')

@dp.message_handler(IsAdmin(), state = add_adpost_st.count)
async def mailings_forw1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        mes = data['mes']
        count = message.text

    await state.finish()
    await add_adpost(mes[0],mes[1],mes[2],count)
    await bot.send_message(message.from_user.id, '✔️ <b>Успешно</b>', reply_markup = await user_menu(message.from_user.id))



############# Рекламные линки #############


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'adlinks')
async def call_adlinks(c: types.CallbackQuery):
    await bot.edit_message_text(chat_id=c.from_user.id, text=f'➕ <b>Рекламные линки:</b>\n<i>Выбери что сделать:</i>', message_id=c.message.message_id, reply_markup=await adlink_add_rem(await get_adlinks()))

### Добавление рекламной линки ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'add_adlinked', state = '*')
async def adlinks_add(c: types.CallbackQuery, state: FSMContext):
    await add_adlink_st.name.set()
    await bot.send_message(c.from_user.id, '➕ <b>Отправьте название канала</b>\n<i>Оно будет отображаться только в статистике</i>')

@dp.message_handler(IsAdmin(), state = add_adlink_st.name)
async def links_add_lnk2(message: types.Message, state: FSMContext):
    await state.finish()
    name = message.text
    code = name
    link = f'https://t.me/{bot_user}?start='+name
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
    await c.message.delete()
    adlinks = await get_adlinks()
    await bot.send_message(c.from_user.id, '<b>Рекламные ссылки на данный момент</b>', reply_markup=await adlink_add_rem(adlinks))

### Suck ###

@dp.callback_query_handler(IsAdmin(), lambda c: 'adlink_' in c.data, state = '*')
async def adlinks_get(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete()
    name = c.data.replace('adlink_', '')
    data = await get_adlinks_stat(name)
    text = f"""
📊 <b>Статистика ссылки «{name}» (<a href='https://t.me/{bot_user}?start={name}'>*ССЫЛКА*</a>)</b>

🔗 <b>Всего юзеров:</b> <code>{data[0]}</code>
🥏 <b>Подписавшихся на ОП</b>: <code>{data[3]}</code>
<b>За сегодня:</b> <code>{data[1]}</code>
<b>За неделю:</b> <code>{data[2]}</code>
    """
    await bot.send_message(c.from_user.id, text, reply_markup=await back_adlinks_kb(), disable_web_page_preview=True)

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'backadlinks', state = '*')
async def adlinks_get(c: types.CallbackQuery, state: FSMContext):
    adlinks = await get_adlinks()
    await c.message.delete()
    await c.message.answer('<b>Рекламные ссылки на данный момент</b>', reply_markup=await adlink_add_rem(adlinks))

############# Рассылка #############


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'mailing')
async def callback_rassilka(c: types.CallbackQuery):
    await bot.edit_message_text(chat_id=c.from_user.id, text='<i>Выбери что сделать:</i>', message_id=c.message.message_id, reply_markup=await mailing_pic_not())

### Текстовая ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'mailing_text', state = '*')
async def mailings_text(c: types.CallbackQuery, state: FSMContext):
    await mailing_st.keyb.set()
    await bot.send_message(c.from_user.id, '<b>Напиши inline-клавиатуру в виде, можно много, каждую на новую строку:</b>\n\ntext | link\n\n<i><u>Если не надо пиши:</u></i> <code>0</code>', reply_markup=ReplyKeyboardRemove())

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
                keyb.add(InlineKeyboardButton(str(b[0]).strip(), url=str(b[1]).strip()))
        data['keyb'] = str(keyb)

        await message.answer('<i>Напиши текст рассылки</i>')
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
                await deactivate_user(user[0])
                nothing += 1
                pass

        await message.answer(f'💲 <b>Рассылка окончена!</b> 💲\n<i>Дошло:</i> {str(nice)}\n<i>Не дошло:</i> {str(nothing)}', reply_markup = await user_menu(message.from_user.id))

### Текстовая + Пикча ###

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'mailing_pic', state = '*')
async def mailings_text(c: types.CallbackQuery, state: FSMContext):
    await mailing_st_pic.source_pic.set()
    await bot.send_message(c.from_user.id, '<i>Отправь фото:</i>', reply_markup=ReplyKeyboardRemove())

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

        await message.answer('<i>Напиши текст рассылки</i>')
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
            await deactivate_user(user[0])
            nothing += 1
            pass
    os.remove(source_pic)
    await message.answer(f'💲 <b>Рассылка окончена!</b> 💲\n<i>Дошло:</i> {str(nice)}\n<i>Не дошло:</i> {str(nothing)}', reply_markup = await user_menu(message.from_user.id))


################# FORWARD #################


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'mailing_forw', state = '*')
async def mailings_forw1(c: types.CallbackQuery, state: FSMContext):
    await mailing_forward.mes.set()
    await bot.send_message(c.from_user.id, '<i>Перешли сообщение:</i>', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(IsAdmin(), state = mailing_forward.mes, content_types=[ContentType.PHOTO, ContentType.TEXT, ContentType.VOICE, ContentType.VIDEO])
async def mailings_forw1(message: types.Message, state: FSMContext):
    rm = message.reply_markup
    uid = message.from_user.id
    mid = message.message_id
    await state.finish()

    users = await get_users()
    nice = 0
    nothing = 0
    await message.answer('<b>Рассылка началась!</b>')
    for user in users:
        try:
            await bot.copy_message(user[0], uid, mid, parse_mode='Markdown', reply_markup=rm, allow_sending_without_reply=True)
            nice += 1
        except Exception as e:
            await deactivate_user(user[0])
            nothing += 1
            pass
    await message.answer(f'💲 <b>Рассылка окончена!</b> 💲\n<i>Дошло:</i> {str(nice)}\n<i>Не дошло:</i> {str(nothing)}', reply_markup = await user_menu(message.from_user.id))

@dp.message_handler(IsAdmin(), lambda message: message.forward_from_chat != None, state = "*", content_types=[ContentType.PHOTO, ContentType.TEXT, ContentType.VOICE, ContentType.VIDEO])
async def other_messages(message: types.Message, state: FSMContext):
    if message.forward_from_chat != None:
        await message.answer(f'🆔: <code>{message.forward_from_chat.id}</code>')