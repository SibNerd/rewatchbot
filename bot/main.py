from create_bot import dp, DATABASE_URL
from aiogram import executor
from databases import Database
import handlers

database = Database(DATABASE_URL)

async def on_startup(db):
    await database.connect()

async def on_shutdown(dp):
    await database.disconnect()

#main function
if __name__ == "__main__":
    executor.start_polling(
        dp, 
        skip_updates=True, 
        on_startup=on_startup, 
        on_shutdown=on_shutdown)
