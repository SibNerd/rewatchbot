"""
Initiates Telegram Bot.
"""

import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ['TOKEN']
DATABASE_URL = os.environ['DATABASE_URL']

bot = Bot(token=TOKEN)
storage=MemoryStorage()
dp = Dispatcher(bot, storage=storage)
