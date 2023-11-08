from dotenv import load_dotenv
load_dotenv()

import os

class EnvConfig:
    """
    環境変数を取得するクラス

    Attributes
    ----------
    DB_DIALECT : str
        DBの種類(sqlite, mysql, postgresql, oracle, mssql)
    DB_DRIVER : str
        DBに接続するためのドライバー
        指定しなければ，"default" DBAPIになる
    DB_DATABASE : str
        DBの名前
    DB_HOST : str
        ホスト名を指定
        (localhost,IPアドレス)
    DB_PORT : str
        ポート番号
    DB_USER : str
        DBに接続することができるユーザ名
    DB_PASSWORD : str
        DBに接続するためのパスワードを
    DB_CHARSET : str
        文字コード
    """
    DB_DIALECT = os.environ.get("DB_DIALECT")
    DB_DRIVER = os.environ.get("DB_DRIVER")
    DB_DATABASE = os.environ.get("DB_DATABASE")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_CHARSET = os.environ.get("DB_CHARSET")
    DATABASE_URI = f"{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}{DB_CHARSET}"
    NODRIVER_DATABASE_URI = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"