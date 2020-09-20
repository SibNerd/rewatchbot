from aiogram import types
from states import ToWatchlist, ToWatched, ChangeRateNote
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import texts
import db_sessions
from create_bot import dp




@dp.message_handler(commands=['to_watchlist'], state='*')
async def add_to_watchlist_setup(message: types.Message):
    await message.answer(texts.TO_WATCHLIST_INFO)
    await ToWatchlist.add_name_and_type.set()


@dp.message_handler(state=ToWatchlist.add_name_and_type, content_types=types.ContentTypes.TEXT)
async def add_to_watchlist_main(message: types.Message, state: FSMContext):
    await db_sessions.add_show(message.chat.id, message.text)
    await message.answer(f'Шоу было добавлено в ваш список.')
    await state.finish()


"""      
@dp.message_handler(commands=['watched'])
async def add_to_watched(message: types.Message):
    user = message.chat.id
    await message.answer(texts.TO_WATCHED_INFO)
    pass
"""
