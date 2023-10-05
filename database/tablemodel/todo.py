from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Todoテーブルの定義
class Todo(Base):
    __tablename__ = 'todos'
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String(200))
    done = Column('done', Boolean, default=False)

import aiopg.sa
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

async def connect_to_postgresql():
    conn = await aiopg.connect(
        host='localhost',
        port=5432,
        user='your_username',
        password='your_password',
        database='your_database'
    )
    return conn

async def create_table(engine):
    metadata = MetaData()
    your_table = Table(
        'your_table', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        ...
    )
    await metadata.create_all(engine)

async def setup():
    connection = await connect_to_postgresql()
    engine = create_engine(connection)
    await create_table(engine)
    return connection, engine

from sqlalchemy.sql import select

async def execute_query(engine):
    async with engine.begin() as conn:
        result = await conn.execute(select([your_table]))
        rows = await result.fetchall()
        return rows
