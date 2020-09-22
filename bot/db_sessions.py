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
    show_name, show_type = user_message
    async with Database(DATABASE_URL) as db:
        query = "INSERT INTO shows(user_id, name, type) VALUES(:user_id, :name, :type)"
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type}
        result = await db.execute(query=query, values=values)
        


async def add_to_watched(user_id, user_message):
    show_name, show_type = user_message
    async with Database(DATABASE_URL) as db:
        query = "SELECT * FROM shows WHERE user_id = :user_id AND name = :name AND type = :type"
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type}
        result = await db.execute(query=query, values=values)
        if not result:
            query = "INSERT INTO shows(user_id, name, type, is_watched) VALUES(:user_id, :name, :type, is_watched = :is_watched)"
            values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type, 'is_watched': True}
        else:
            query = "UPDATE shows SET is_watched = :is_watched WHERE user_id = :user_id AND name = :name AND type = :type"
            values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type, 'is_watched': True}
        await db.execute(query=query, values=values)
        


async def add_show_rate(user_id, name_type, rate):
    show_name, show_type = name_type
    async with Database(DATABASE_URL) as db:
        query = 'UPDATE shows SET rate = :rate WHERE user_id = :user_id AND name = :name AND type = :type'
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type, 'rate': rate}
        result = await db.execute(query=query, values=values)
    


async def add_show_note(user_id, name_type, note):
    show_name, show_type = name_type
    async with Database(DATABASE_URL) as db:
        query = 'UPDATE shows SET note = :note WHERE user_id = :user_id AND name = :name AND type = :type'
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type, 'note': note}
        result = await db.execute(query=query, values=values)



async def get_show_rate(user_id, user_message):
    show_name, show_type = user_message
    async with Database(DATABASE_URL) as db:
        query = 'SELECT rate FROM shows WHERE user_id = :user_id AND name = :name AND type = :type'
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type}
        result = await db.fetch_one(query=query, values=values)
        if not result:
            result = 'У данного шоу нет оценки.'
        return result[0]



async def get_show_note(user_id, user_message):
    show_name, show_type = user_message
    async with Database(DATABASE_URL) as db:
        query = 'SELECT note FROM shows WHERE user_id = :user_id AND name = :name AND type = :type'
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type}
        result = await db.fetch_one(query=query, values=values)
        if not result:
            result = 'У данного шоу нет заметки.'
        return result[0]

