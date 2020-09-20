from create_bot import dp
from aiogram import types
import texts
import db_sessions
from aiogram.dispatcher.filters import Text


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    is_new_user = await db_sessions.add_new_user(message.chat.id, message.chat.username)
    if is_new_user:
        await message.answer(texts.HELP_INFO)
    else:
        await message.answer('Вы уже включили бота. Выберите /help для получения информации.')



@dp.message_handler(commands=['help'])
async def send_help_message(message: types.Message):
    await message.answer(texts.HELP_INFO)



@dp.message_handler(Text(equals=['cansel', 'отмена'], ignore_case=True), state='*')
async def cansel_operation(message: types.Message):
    pass
