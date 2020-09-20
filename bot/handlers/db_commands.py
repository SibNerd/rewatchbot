from aiogram import types
from states import ToWatchlist, ToWatched
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import texts
import db_sessions
from create_bot import dp



@dp.message_handler(commands=['to_watchlist'])
async def add_to_watchlist(message: types.Message):
    await message.answer(texts.TO_WATCHLIST_INFO)
    async def to_watchlist(message: types.Message):
        await db_sessions.add_show(message.chat.id, message.text)
        await message.answer(f'Шоу было добавлено в ваш список.')


"""      
@dp.message_handler(commands=['watched'])
async def add_to_watched(message: types.Message):
    user = message.chat.id
    await message.answer(texts.TO_WATCHED_INFO)
    pass
"""
