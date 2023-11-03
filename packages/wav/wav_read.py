import wave
import librosa

import numpy as np
from datetime import datetime

from fastsample.model.wav import ReadWaveFile
from fastsample.packages.file_time.creation_time import creation_date

def wav_read(filename:str) -> ReadWaveFile:
    create_time = datetime.fromtimestamp(creation_date(filename))
    wf = wave.open(filename, 'r')
    channels = wf.getnchannels()
    width = wf.getsampwidth()
    sampling_rate = wf.getframerate()
    # waveの実データを取得し、数値化
    data = wf.readframes(wf.getnframes())
    wav_buffer16:np.ndarray[np.int16] = np.frombuffer(data, dtype=np.int16)
    # wavファイルの音声データを読み込む
    _, sr = librosa.load(path=filename, sr=sampling_rate)
    wf.close()

    read_wave_file = ReadWaveFile(
        filename=filename,
        sampling_freq=sr,
        channel=channels,
        sample_width=width,
        create_time=create_time,
        wav_buffer16=wav_buffer16
    )
    return read_wave_file