import wave
import re
import struct

import numpy as np
from datetime import datetime

from model.wav import ReadWaveFile
from packages.file_time.creation_time import creation_date

def wav_read(filename:str) -> ReadWaveFile:
    """
    wavファイルを読み込む

    filename: str
        ファイル名

    return
    ------
    read_wave_file: ReadWaveFile
        wavファイルのデータ
    """
    # ファイルから記録時間を取得
    create_time = datetime.fromtimestamp(creation_date(filename))
    wf = wave.open(filename, 'r')
    channels = wf.getnchannels()
    width = wf.getsampwidth()
    sampling_rate = wf.getframerate()
    frames = wf.getnframes()
    # waveの実データを取得し、数値化
    data = wf.readframes(wf.getnframes())
    wav_buffer16:np.ndarray[np.int16] = np.frombuffer(data, dtype=np.int16)
    wf.close()

    read_wave_file = ReadWaveFile(**{
        "filename":filename,
        "sampling_freq":sampling_rate,
        "channel":channels,
        "sample_width":width,
        "frames":frames,
        "create_time":create_time,
        "wav_buffer16":wav_buffer16
    })
    return read_wave_file

async def async_wav_read(filepath:str,filename:str) -> ReadWaveFile:
    filename = filename.replace("log_", "")
    filename = filename.replace(".wav", "")
    record_time = re.match(r'\d{8}_\d{6}', filename)
    if record_time is None:
        create_time = datetime.fromtimestamp(creation_date(filepath))
    else:
        create_time = datetime.strptime(record_time.group(), '%Y%m%d_%H%M%S')

    print(create_time)
    wf = wave.open(filepath, 'r')
    channels = wf.getnchannels()
    width = wf.getsampwidth()
    sampling_rate = wf.getframerate()
    frames = wf.getnframes()
    # waveの実データを取得し、数値化
    data = wf.readframes(wf.getnframes())
    #wav_buffer16:np.ndarray[np.int16] = np.frombuffer(data, dtype=np.int16)
    wf.close()

    read_wave_file = ReadWaveFile(**{
        "filename":filepath,
        "sampling_freq":sampling_rate,
        "channel":channels,
        "sample_width":width,
        "frames":frames,
        "create_time":create_time,
        "wav_buffer16":data
    })
    return read_wave_file

def wave_create_bytes(
    data:bytes,
    channel:int,
    sampling_freq:int,
    sample_width:int,
    out_file:str
) -> None:
    """
    wavファイルを作成する

    data: bytes
        wavデータ
    channel: int
        チャンネル数
    sampling_freq: int
        サンプリング周波数
    sample_width: int
        サンプル幅
    out_file: str
        出力ファイル名
    """
    wav_buffer16:np.ndarray[np.int16] = np.frombuffer(data, dtype=np.int16)
    outd = struct.pack("h" * len(wav_buffer16), *wav_buffer16)

    # 書き出し
    ww = wave.open(out_file, 'w')
    ww.setnchannels(channel)
    ww.setsampwidth(sample_width)
    ww.setframerate(sampling_freq)
    ww.writeframes(outd)
    ww.close()

async def async_wave_create_bytes(
    data:bytes,
    channel:int,
    sampling_freq:int,
    sample_width:int,
    out_file:str
) -> None:
    wav_buffer16:np.ndarray[np.int16] = np.frombuffer(data, dtype=np.int16)
    outd = struct.pack("h" * len(wav_buffer16), *wav_buffer16)

    # 書き出し
    ww = wave.open(out_file, 'w')
    ww.setnchannels(channel)
    ww.setsampwidth(sample_width)
    ww.setframerate(sampling_freq)
    ww.writeframes(outd)
    ww.close()