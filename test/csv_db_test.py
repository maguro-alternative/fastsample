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