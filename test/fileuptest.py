# -*- coding: utf-8 -*-
import requests

# ★ポイント1
XLSX_MIMETYPE = 'audio/wav'

# <form action="/data/upload" method="post" enctype="multipart/form-data">
#   <input type="file" name="uploadFile"/>
#   <input type="submit" value="submit"/>
# </form>

# main

BASE_URL = "http://localhost:5000"
#BASE_URL = "https://glowing-vehicle-316505.an.r.appspot.com/"

def wav_upload():
    # ★ポイント2
    #fileName = './fastsample/test/data/toujyo.wav'
    #fileName = './fastsample/test/data/audio_2/log_20230321_124636.wav'
    fileName = './fastsample/test/data/audio_2/log_20231111_161411.wav'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'fileb': (fileName, fileDataBinary, 'audio/wav')}

    # ★ポイント3
    url = f'{BASE_URL}/save-upload-file/wav/'
    response = requests.post(url=url, files=files, timeout=100)

    print(response.status_code)
    print(response.content)

def csv_upload():
    # ★ポイント2
    fileName = './fastsample/test/data/data_20231018_12.csv'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'fileb': (fileName, fileDataBinary, 'text/csv')}

    # ★ポイント3
    url = f'{BASE_URL}/save-upload-file/csv/'
    response = requests.post(url=url, files=files, timeout=100)

    print(response.status_code)
    print(response.content)

def pic_upload():
    # ★ポイント2
    fileName = './fastsample/test/data/log_20231025_060000.jpg'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'fileb': (fileName, fileDataBinary, 'image/jpeg')}

    # ★ポイント3
    url = f'{BASE_URL}/save-upload-file/pic/'
    response = requests.post(url=url, files=files, timeout=100)

    print(response.status_code)
    print(response.content)

def video_upload():
    # ★ポイント2
    fileName = './fastsample/test/data/log_20231023_110012.h264'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'fileb': (fileName, fileDataBinary, 'video/h264')}

    # ★ポイント3
    url = f'{BASE_URL}/save-upload-file/video/'
    response = requests.post(url=url, files=files, timeout=100)

    print(response.status_code)
    print(response.content)


if __name__ == "__main__":
    wav_upload()
    #csv_upload()
    #pic_upload()
    #video_upload()
