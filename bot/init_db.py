import os
from sqlalchemy import create_engine, MetaData
from db import users, shows

database = os.environ['DATABASE_URL']

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[users, shows])



if __name__ == "__main__":
    engine = create_engine(database)
    create_tables(engine)