from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from loader import dp

from filters import IsPrivate, IsSubscriber
from utils.db_api import quick_commands as commands
from utils.misc import rate_limit
#IsSubscribe() надо менять

@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), IsSubscriber(), CommandStart())
async def command_start(message: types.Message):
    args = message.get_args()
    print(args)
    new_args = await commands.check_args(args, message.from_user.id)
    print(new_args)
    try:
        user = await commands.select_user(message.from_user.id)
        if user.status == 'active':
            await message.answer(f'Привет {user.first_name}\n'
                                 f'Ты уже зарегистрирован')
        elif user.status == 'baned':
            await message.answer('Ты забанен')
    except Exception:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                referral_id=int(new_args),
                                status='active',
                                balance=0)
        try:
            await dp.bot.send_message(chat_id=int(new_args), text=f'По твоей ссылке зарегистрировался {message.from_user.first_name}')
        except Exception:
            pass

        await message.answer('Ты успешно зарегистрирован')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/ban')
async def get_ban(message: types.Message):
    await commands.update_status(user_id=message.from_user.id, status='baned')
    await message.answer('Мы тебя забанили')

@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/unban')
async def get_unban(message: types.Message):
    await commands.update_status(user_id=message.from_user.id, status='active')
    await message.answer('Бана больше нет')

@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/profile')
async def profile(message: types.Message):
    user = await commands.select_user(user_id=message.from_user.id)
    await message.answer(f'ID - {user.user_id}\n'
                         f'First name - {user.first_name}\n'
                         f'Last name - {user.last_name}\n'
                         f'Username - {user.username}\n'
                         f'Status - {user.status}')