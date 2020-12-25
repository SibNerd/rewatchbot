"""
Module for functions, working with general comands.
"""

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types
from create_bot import dp
import texts
import db_sessions



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Creates new User in DB (or says, that this user already exist in BD) and send info message.
    """
    is_new_user = await db_sessions.add_new_user(message.chat.id, message.chat.username)
    if is_new_user:
        await message.answer(texts.HELP_INFO)
    else:
        await message.answer('Вы уже включили бота. Выберите /help для получения информации.')



@dp.message_handler(commands=['help'])
async def send_help_message(message: types.Message):
    """
    Send info message.
    """
    await message.answer(texts.HELP_INFO)



@dp.message_handler(Text(equals=['cansel', 'отмена'], ignore_case=True), state='*')
async def cansel_operation(message: types.Message, state: FSMContext):
    """ Cansels current command.
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Отмена команды.')

