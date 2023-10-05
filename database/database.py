from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

import os

# sqlの種類(sqlite,mysql)
DIALECT = os.environ.get('')
# DBに接続するためのドライバー
DRIVER = os.environ.get('',default='')
# DBのユーザ名
USERNAME = os.environ.get('')
# DBのパスワード
PASSWORD = os.environ.get('')
# ホスト名を指定(localhost,IPアドレス)
HOST = os.environ.get('')
# ポート番号
PORT = os.environ.get('')
# データベース名
DATABASE = os.environ.get('')
# 文字コード
CHARSET_TYPE = f"?charset={os.environ.get('',default='utf8')}"

SQLALCHEMY_DATABASE_URI = f"{DIALECT}://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}{CHARSET_TYPE}"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    connect_args={
        "check_same_thread": False
    },
    echo=True
)

Base = declarative_base()

# Todoテーブルの定義
class Todo(Base):
    __tablename__ = 'todos'
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String(200))
    done = Column('done', Boolean, default=False)

# テーブル作成
Base.metadata.create_all(bind=engine)

class DataBaseConnect:
    """
    dialect     :str
        DBの種類(sqlite, mysql, postgresql, oracle, mssql)
    driver      :str
        DBに接続するためのドライバー
        指定しなければ，"default" DBAPIになる
    username    :str
        DBに接続することができるユーザ名
    password    :str
        DBに接続するためのパスワードを
    host        :str
        ホスト名を指定
        (localhost,IPアドレス)
    port        :str
        ポート番号
    database    :str
        接続するデータベース名
    charset_type:str
        文字コード(utf8)
    """
    def __init__(
        self,
        dialect     :str,
        username    :str,
        password    :str,
        host        :str,
        port        :int,
        database    :str,
        charset_type:str
    ) -> None:
        self.dialect = dialect
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.charset_type = charset_type