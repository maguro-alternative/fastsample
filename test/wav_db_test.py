import wave
import librosa
import numpy as np
from datetime import datetime, timedelta
import struct

from sqlalchemy import (
    Boolean,
    BigInteger,
    Column,
    Integer,
    String,
    TIMESTAMP,
    DECIMAL,
    BOOLEAN,
    BINARY,
    Float,
    create_engine
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

FileName = './data/audio_2/log_20230321_124636.wav' # mono
FileName = './data/toujyo.wav' # stereo
SQLALCHEMY_DATABASE_URI = "sqlite:///./sqlite/test.db"

Base = declarative_base()

ENGINE = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)

class WaveTable(Base):
    __tablename__ = 'wavetable2'
    time = Column('time', TIMESTAMP, primary_key=True)
    sampling_freq = Column('sampling_freq', DECIMAL)
    channel = Column('channel', Integer)
    sample_width = Column('sample_width', Integer)
    frame_rate = Column('frame_rate', Integer)
    frame_count_float = Column('frame_count_float', Float)
    frame_count = Column('frame_count', BINARY)

def wav_create_db(filename:str):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
    session = SessionLocal()
    time_pkey = datetime.now()

    wf = wave.open(filename, 'r')
    channels = wf.getnchannels()
    width = wf.getsampwidth()
    sampling_rate = wf.getframerate()
    frames = wf.getnframes()
    # waveの実データを取得し、数値化
    data = wf.readframes(wf.getnframes())
    X:np.ndarray[np.int16] = np.frombuffer(data, dtype=np.int16)
    # wavファイルの音声データを読み込む
    y, sr = librosa.load(path=filename, sr=sampling_rate)
    time_rate = 1.0 / sr

    for rate,float_rate in zip(X,y):
        time_pkey += timedelta(microseconds=time_rate*1000000)
        session.add(WaveTable(
            time=time_pkey,
            sampling_freq=sr,
            channel=channels,
            sample_width=width,
            frame_rate=sampling_rate,
            frame_count_float=float_rate,
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

    byte = b''
    for data in wav_data:
        byte += data.frame_count

    # 90秒分に相当するフレーム数を算出
    time = 1
    frames = int(wav_data[0].channel * wav_data[0].sampling_freq * time)
    X = np.frombuffer(byte, dtype=np.int16)

    # 出力データを生成
    outf = './data/test.wav'
    Y = X[:frames]
    print(type(Y), len(Y))
    outd = struct.pack("h" * len(Y), *Y)

    # 書き出し
    ww = wave.open(outf, 'w')
    ww.setnchannels(wav_data[0].channel)
    ww.setsampwidth(wav_data[0].sample_width)
    ww.setframerate(wav_data[0].sampling_freq)
    ww.writeframes(outd)
    ww.close()

def table_in():
    # テーブル作成
    Base.metadata.create_all(bind=ENGINE)

def float2binary(data:np.float32, sampwidth:int) -> bytes:
    data = (data*(2**(8*sampwidth-1)-1)).reshape(data.size, 1) # Normalize (float to int)
    frames:bytes = b''
    if sampwidth == 1:
        data = data + 128
        frames = data.astype(np.uint8).tobytes()
    elif sampwidth == 2:
        frames = data.astype(np.int16).tobytes()
    elif sampwidth == 3:
        a32 = np.asarray(data, dtype = np.int32)
        a8 = (a32.reshape(a32.shape + (1,)) >> np.array([0, 8, 16])) & 255
        frames = a8.astype(np.uint8).tobytes()
    elif sampwidth == 4:
        frames = data.astype(np.int32).tobytes()
    return frames


if __name__ == '__main__':
    #table_in()
    #wav_create_db(FileName)
    #wav_read_db(datetime(2023, 11, 2, 17, 59, 32, 154365), datetime(2023, 11, 2, 17, 59, 34, 154366))
    wav_read_db(datetime(2023, 11, 2, 18, 14, 25, 989078), datetime(2023, 11, 2, 18, 14, 28, 989079))
    #wavreadtest()