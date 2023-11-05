# -*- coding: utf-8 -*-
import requests

# ★ポイント1
XLSX_MIMETYPE = 'audio/wav'

# <form action="/data/upload" method="post" enctype="multipart/form-data">
#   <input type="file" name="uploadFile"/>
#   <input type="submit" value="submit"/>
# </form>

# main
if __name__ == "__main__":

    # ★ポイント2
    fileName = './fastsample/test/data/toujyo.wav'
    fileName = './fastsample/test/data/audio_2/log_20230321_124636.wav'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'fileb': (fileName, fileDataBinary, XLSX_MIMETYPE)}

    # ★ポイント3
    url = 'http://localhost:5000/save-upload-file/wav/'
    response = requests.post(url=url, files=files, timeout=100)

    print(response.status_code)
    print(response.content)
