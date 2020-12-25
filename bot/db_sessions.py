"""
Module with bot functions.
"""

from databases import Database
from db import users, shows
import re
import os

DATABASE_URL = os.environ['DATABASE_URL']



async def add_new_user(new_user_id, name):
    """ Checks, if given user exists in Database, and if not, add new one.

    Args:
        new_user_id (int): user Telegram ID
        name (str): user Telegram Name

    Returns:
        bool: True if user was added to DB, False otherwise
    """
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
    """Adds new show to DB for chosen User with 'Seen' set to 'False'.

    Args:
        user_id (int): User Telegram ID
        user_message (str): Name and Type of the show
    """
    show_name, show_type = user_message
    async with Database(DATABASE_URL) as db:
        query = "INSERT INTO shows(user_id, name, type) VALUES(:user_id, :name, :type)"
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type}
        result = await db.execute(query=query, values=values)
        


async def add_to_watched(user_id, user_message):
    """Adds show to DB for chosen User with 'Seen' set to 'True'

    Args:
        user_id (int): User Telegram ID
        user_message (str): Name and Type of the show
    """
    show_name, show_type = user_message
    async with Database(DATABASE_URL) as db:
        query = "SELECT * FROM shows WHERE user_id = :user_id AND name = :name AND type = :type"
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type}
        result = await db.execute(query=query, values=values)
        if not result:
            query = "INSERT INTO shows(user_id, name, type, is_watched) VALUES(:user_id, :name, :type, :is_watched)"
            values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type, 'is_watched': True}
        else:
            query = "UPDATE shows SET is_watched = :is_watched WHERE user_id = :user_id AND name = :name AND type = :type"
            values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type, 'is_watched': True}
        await db.execute(query=query, values=values)
        


async def get_watchlist(user_id):
    """Gets User's watchlist

    Args:
        user_id (int): User's Telegram ID

    Returns:
        list[str]: list of all shows in User's watchlist
    """
    async with Database(DATABASE_URL) as db:
        query = 'SELECT name, type FROM shows WHERE user_id = :user_id AND is_watched = :is_watched'
        values = {'user_id': user_id, 'is_watched': False}
        result = await db.execute(query=query, values=values)
        if not result:
            result = 'Ваш список желаемого к просмотру пуст.'
        return result



async def add_show_rate(user_id, name_type, rate):
    """Adds User's rate for chosen Show

    Args:
        user_id (int): User Telegram ID
        name_type (str): Name and Type of the show
        rate (int): Rate of the show
    """
    show_name, show_type = name_type
    async with Database(DATABASE_URL) as db:
        query = 'UPDATE shows SET rate = :rate WHERE user_id = :user_id AND name = :name AND type = :type'
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type, 'rate': rate}
        result = await db.execute(query=query, values=values)
    


async def add_show_note(user_id, name_type, note):
    """Adds User's note for chosen show

    Args:
        user_id (int): User Telegram ID
        name_type (str): Name and Type of the show
        note (str): Note for the show
    """
    show_name, show_type = name_type
    async with Database(DATABASE_URL) as db:
        query = 'UPDATE shows SET note = :note WHERE user_id = :user_id AND name = :name AND type = :type'
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type, 'note': note}
        result = await db.execute(query=query, values=values)



async def get_show_rate(user_id, user_message):
    """Gets User's rate of the chosen show

    Args:
        user_id (int): User Telegram ID
        user_message (str): Name and Type of the show

    Returns:
        result: rate of the chosen show of chosen User or text, that chosen show doesn't have a rate
    """
    show_name, show_type = user_message
    async with Database(DATABASE_URL) as db:
        query = 'SELECT rate FROM shows WHERE user_id = :user_id AND name = :name AND type = :type'
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type}
        result = await db.fetch_one(query=query, values=values)
        if not result:
            result = 'У данного шоу нет оценки.'
        return result[0]



async def get_show_average_rate(user_message):
    """Gets average rate of the chosen show

    Args:
        user_message (str): Name and Type of the show

    Returns:
        arate: average rate of the show or text, that chosen show doesn't have any rates.
    """
    show_name, show_type = user_message
    async with Database(DATABASE_URL) as db:
        query = 'SELECT rate FROM shows WHERE name = :name AND type = :type'
        values = {'name': show_name, 'type': show_type}
        result = db.fetch_all(query=query, values=values)
        if not result:
            arate = 'У данного шоу нет оценок.'
        elif len(result)>1:
            arate = 0
            for i in result:
                arate += i
            arate = int(arate/len(result))
        else:
            arate = result[0]
        return arate



async def get_show_note(user_id, user_message):
    """ Gets User's Note of the chosen show

    Args:
        user_id (int): User Telegram ID
        user_message (str): Name and Type of the Show

    Returns:
        result: User's note
    """
    show_name, show_type = user_message
    async with Database(DATABASE_URL) as db:
        query = 'SELECT note FROM shows WHERE user_id = :user_id AND name = :name AND type = :type'
        values = {'user_id': user_id, 'name': show_name.lower(), 'type': show_type}
        result = await db.fetch_one(query=query, values=values)
        if not result:
            result = 'У данного шоу нет заметки.'
        return result[0]

