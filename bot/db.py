"""
Creates Database with two tables: Users and Shows.
"""

import sqlalchemy as sa
from sqlalchemy import (
    Table, MetaData, ForeignKey, Column, Integer, Boolean, String, Text, DateTime
    )
metadata = MetaData()

users = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String, nullable=False)
    )

shows = Table(
    'shows', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id', ondelete="CASCADE")),
    Column('name', String, nullable=False),
    Column('type', String, nullable=False),
    Column('is_watched', Boolean, default=False),
    Column('rate', Integer, default=None),
    Column('note', Text, default=None)
    )