from aiogram import Dispatcher

from .admin_filter import IsAdmin

def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)