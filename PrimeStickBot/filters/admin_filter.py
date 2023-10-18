from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from config.config_file import global_admins

class IsAdmin(BoundFilter):
	async def check(self, message: types.Message):
		return message.from_user.id in global_admins
