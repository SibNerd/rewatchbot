import logging
from configs import TOKEN
from aiogram import Bot, Dispatcher, executor, types
import texts

API_TOKEN = TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(texts.HELP_INFO)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    
