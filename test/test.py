import wave
import librosa
import numpy as np
from datetime import datetime, timedelta

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    TIMESTAMP,
    DECIMAL,
    BOOLEAN,
    Float,
    create_engine
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

FileName = './data/audio_2/log_20230321_124636.wav' # mono
SQLALCHEMY_DATABASE_URI = "sqlite:///./sqlite/test.db"

Base = declarative_base()

ENGINE = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)

class WaveTable(Base):
    __tablename__ = 'wavetable'
    time = Column('time', TIMESTAMP, primary_key=True)
    sampling_freq = Column('sampling_freq', DECIMAL)
    channel = Column('channel', Integer)
    sample_width = Column('sample_width', Integer)
    frame_rate = Column('frame_rate', Integer)
    frame_count = Column('frame_count', Float)

def wav_create_db(filename:str):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
    session = SessionLocal()
    time_pkey = datetime.now()

    wf = wave.open(filename, 'r')
    channels = wf.getnchannels()
    width = wf.getsampwidth()
    sampling_rate = wf.getframerate()
    frames = wf.getnframes()
    # wavファイルの音声データを読み込む
    y, sr = librosa.load(path=filename, sr=sampling_rate)
    time_rate = 1.0 / sr

    for i,rate in enumerate(y):
        if i % sr == 0:
            pass
            #print(rate)
        time_pkey += timedelta(microseconds=time_rate*1000000)
        session.add(WaveTable(
            time=time_pkey,
            sampling_freq=sr,
            channel=channels,
            sample_width=width,
            frame_rate=sampling_rate,
            frame_count=rate
        ))

    session.commit()
    print('チャンネル数 :', channels)
    print('サンプル幅 :', width)
    print('サンプリングレート :', sampling_rate)
    print('フレーム数 :', frames)
    print('パラメータ :', wf.getparams())
    print('長さ（秒） :', frames / sampling_rate)
    print('読み込み位置 :', wf.tell())
    print('フレームのバイト数 :', wf.getsampwidth())
    print('フレームレート :', wf.getframerate())
    print('フレーム数 :', wf.getnframes())
    print('チャンネル数 :', wf.getnchannels())
    wf.close()

def wav_read_db(before_time:datetime, after_time:datetime):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
    session = SessionLocal()
    wav_data = session.query(WaveTable).filter(
        WaveTable.time.between(
            before_time,
            after_time
        )
    ).all()
    for data in wav_data:
        print(data.time)
        print(data.sampling_freq)
        print(data.channel)
        print(data.sample_width)
        print(data.frame_rate)
        print(data.frame_count)

def table_in():
    # テーブル作成
    Base.metadata.create_all(bind=ENGINE)

if __name__ == '__main__':
    table_in()
    #wav_create_db(FileName)
    wav_read_db(datetime(2023, 11, 2, 10, 43, 52, 8), datetime(2023, 11, 2, 10, 43, 53, 8))