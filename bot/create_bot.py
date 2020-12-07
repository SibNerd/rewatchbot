    """
    Initiates Telegram Bot.
    """

import logging
from configs import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage=MemoryStorage()
dp = Dispatcher(bot, storage=storage)
