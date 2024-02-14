
import soundfile as sf
def wavload(path):
    data, samplerate = sf.read(path)
    return data, samplerate

import numpy as np
from matplotlib import pyplot as plt
path = "C:/Users/bi_wa/OneDrive - 日本大学/ドキュメント/ゼミナール/samplecode/fastsample/test/data/test.wav"

data, samplerate = wavload(path)

t = np.arange(0, len(data))/samplerate
plt.plot(t, data)
plt.show()
plt.close()