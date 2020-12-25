"""
Module for complex commands, uses finite states for user's input handling.
"""

from aiogram import types
from states import ToWatchlist, ToWatched, GetRate, GetNote
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import texts
import db_sessions
from create_bot import dp
import re



# Добавить шоу в список "Хочу посмотреть"

@dp.message_handler(commands=['to_watchlist'], state='*')
async def add_to_watchlist_setup(message: types.Message):
    await message.answer(texts.INFO_SETUP)
    await ToWatchlist.add_name_and_type.set()

@dp.message_handler(state=ToWatchlist.add_name_and_type, content_types=types.ContentTypes.TEXT)
async def add_to_watchlist_main(message: types.Message, state: FSMContext):
    user_data = re.split(r'\n', message.text)
    if len(user_data) == 2:
        await db_sessions.add_show(message.chat.id, user_data)
        await message.answer('Шоу было добавлено в ваш список.')
        await state.finish()
    else:
        await message.answer(texts.INFO_SETUP)
        return



# Добавить шоу в список просмотренного

@dp.message_handler(commands=['watched'], state='*')
async def add_to_watched_setup(message: types.Message):
    await message.answer(texts.INFO_SETUP)
    await ToWatched.add_name_and_type.set()

@dp.message_handler(state=ToWatched.add_name_and_type, content_types=types.ContentTypes.TEXT)
async def add_to_watched_nametype(message: types.Message, state: FSMContext):
    user_data = re.split('\n', message.text)
    if len(user_data) == 2:
        await db_sessions.add_to_watched(message.chat.id, user_data)
        await state.update_data(show_name_type=message.text)
        await ToWatched.next()
        await message.answer(texts.TO_WATCHED_INFO_RATE_NOTE)
    else:
        await message.answer('Пожалуйста, напишите тип шоу следующей строкой.')
        return

@dp.message_handler(state=ToWatched.ask_rate_and_note, content_types=types.ContentTypes.TEXT)
async def add_to_watched_ratenote(message: types.Message, state: FSMContext):
    user_answer = message.text.lower()
    if user_answer == "да":
        await ToWatched.next()
        await message.answer(texts.TO_WATCHED_INFO_RATE)
    elif user_answer == "нет":
        await state.finish()
        await message.answer('Вы решили не добавлять оценку и заметку к просмотренному шоу. Шоу было добавлено в просмотренные.')
    else:
        await message.answer('Пожалуйста, введите Да/Нет или Yes/No.')
        return

@dp.message_handler(state=ToWatched.add_rate, content_types=types.ContentTypes.TEXT)
async def add_to_watched_rate(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        rate = int(message.text)
        if rate in range(1, 6):
            await db_sessions.add_rate(message.chat.id, user_data['show_name_type'], rate)
            await ToWatched.next()
            await message.answer(texts.TO_WATCHED_INFO_NOTE)
        else:
            await message.answer('Пожалуйста, введите число от 1 до 5.')   
            return         
    except ValueError:
        user_answer = message.text.lower()
        if user_answer == 'далее':
            await ToWatched.next()
            await message.answer(texts.TO_WATCHED_INFO_NOTE)
        else:
            await message.answer('Пожалуйста, введите число от 1 до 5.')
            return
            
@dp.message_handler(state=ToWatched.add_note, content_types=types.ContentTypes.TEXT)
async def add_to_watched_note(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text.lower() == 'конец':
        await state.finish()
    else:
        await db_sessions.add_note(message.chat.id, user_data['show_name_type'], message.text)
        await state.finish()
    await message.answer('Шоу было добавлено в просмотренные.')



# Получить заметку о шоу

@dp.message_handler(commands=['get_note'], state='*')
async def get_show_note_setup(message: types.Message):
    await message.answer(texts.INFO_SETUP)
    await GetNote.get_note.set()

@dp.message_handler(state=GetNote.get_note, content_types=types.ContentTypes.TEXT)
async def get_show_note(message: types.Message, state: FSMContext):
    user_data = re.split(r'\n', message.text)
    if len(user_data) == 2:
        note = await db_sessions.get_show_note(message.chat.id, user_data)
        await message.answer(note)
        await state.finish()
    else:
        await message.answer(texts.INFO_SETUP)



# получить рейтинг шоу

@dp.message_handler(commands=['get_rate'], state="*")
async def get_show_rate_setup(message: types.Message):
    await message.answer(texts.INFO_SETUP)
    await GetRate.get_rate.set()

@dp.message_handler(state=GetRate.get_rate, content_types=types.ContentTypes.TEXT)
async def get_show_average_rate(message: types.Message, state: FSMContext):
    user_data = re.split(r'\n', message.text)
    if len(user_data) == 2:
        rate = await db_sessions.get_show_rate(message.chat.id, user_data)
        await message.answer('Средний рейтинг: ', rate)
        await state.finish()
    else:
        await message.answer(texts.INFO_SETUP)
