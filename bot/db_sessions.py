# from shemas import User, Shows
from databases import Database
from configs import DATABASE_URL
from db import users, shows
import re



async def add_new_user(new_user_id, name):
    async with Database(DATABASE_URL) as db:
        query = "SELECT * FROM users WHERE user_id = :user_id"
        result = await db.fetch_one(query=query, values={'user_id': new_user_id})
        if not result:
            query = users.insert()
            values = {'user_id': new_user_id, 'name': name}
            add_user = await db.execute(query=query, values=values)
            return True
        else:
            return False
    


async def add_show(user_id, user_message):
    show_name, show_type = re.split(r', ', user_message)
    async with Database(DATABASE_URL) as db:
        query = "INSERT INTO shows(user_id, name, type) VALUES(:user_id, :name, :type)"
        values = {'user_id': user_id, 'name': show_name, 'type': show_type}
        result = await db.execute(query=query, values=values)
        


async def add_to_watched(id, message):
            pass



async def get_show_rate(id, name):
            pass



async def get_show_notes(id, name):
            pass

