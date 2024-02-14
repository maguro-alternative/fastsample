# -*- coding: utf-8 -*-
import requests
import sys

# ★ポイント1
XLSX_MIMETYPE = 'audio/wav'

# <form action="/data/upload" method="post" enctype="multipart/form-data">
#   <input type="file" name="uploadFile"/>
#   <input type="submit" value="submit"/>
# </form>

# main

BASE_URL = "http://localhost:5000"
#BASE_URL = "https://glowing-vehicle-316505.an.r.appspot.com/"

"""
INSERT INTO picfile (
    filename,
    create_time,
    bucket_name,
    kamera_id
) VALUES (
    'log_20231025_060000.jpg',
    '2023-10-25 06:00:00',
    'glowing-vehicle-316505.appspot.com',
    1
);

INSERT INTO videofile (
    filename,
    create_time,
    bucket_name,
    kamera_id
) VALUES (
    'log_20231023_110012.h264',
    '2023-10-23 11:00:12',
    'glowing-vehicle-316505.appspot.com',
    1
);

INSERT INTO wavefile (
    filename,
    create_time,
    bucket_name,
    kamera_id
) VALUES (
    'log_20231111_161411.wav',
    '2023-11-11 16:14:11',
    'glowing-vehicle-316505.appspot.com',
    1
);

INSERT INTO csvfile (
    filename,
    create_time,
    bucket_name,
    kamera_id
) VALUES (
    'data_20231018_12.csv',
    '2023-10-18 12:00:00',
    'glowing-vehicle-316505.appspot.com',
    1
);

INSERT INTO csvtable (
    time,
    raw_data,
    flag,
    kamera_id
) VALUES (
    '2023-10-18 12:00:00',
    131,
    0,
    1
);

"""

def wav_upload():
    # ★ポイント2
    #fileName = './fastsample/test/data/toujyo.wav'
    #fileName = './fastsample/test/data/audio_2/log_20230321_124636.wav'
    fileName = './fastsample/test/data/audio_2/log_20231111_161411.wav'
    fileDataBinary = open(fileName, 'rb').read()
    files = {
        'fileb': (
            fileName, fileDataBinary, 'audio/wav'
        )
    }
    data = {
        'address': '192.168.1.248'
    }

    # ★ポイント3
    url = f'{BASE_URL}/save-upload-file/wav/'
    response = requests.post(url=url, files=files, data=data, timeout=100)

    print(response.status_code)
    print(response.content)

def wav_upload_timestamp():
    # ★ポイント2
    #fileName = './fastsample/test/data/toujyo.wav'
    #fileName = './fastsample/test/data/audio_2/log_20230321_124636.wav'
    fileName = './fastsample/test/data/audio_2/log_20231111_161411.wav'
    fileDataBinary = open(fileName, 'rb').read()
    files = {
        'fileb': (
            fileName, fileDataBinary, 'audio/wav'
        )
    }
    data = {
        'address': '192.168.1.248'
    }

    # ★ポイント3
    url = f'{BASE_URL}/save-upload-file/wav-timestamp/'
    response = requests.post(url=url, files=files, data=data, timeout=100)

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

def csv_upload_timestamp():
    # ★ポイント2
    fileName = './fastsample/test/data/data_20231018_12.csv'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'fileb': (fileName, fileDataBinary, 'text/csv')}

    # ★ポイント3
    url = f'{BASE_URL}/save-upload-file/csv-timestamp/'
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

def same_upload(filepath:str,url:str,minetype:str):
    files = {'fileb': (filepath, open(filepath, 'rb').read(), minetype)}
    response = requests.post(url=url, files=files, timeout=100)

    print(response.status_code)
    print(response.content)
    response.content


if __name__ == "__main__":
    args = sys.argv
    print(200)
    # python fileuptest.py [filepath] [minetype] [url]
    # python fileuptest.py log_20231025_060000.jpg image/jpeg http://localhost:8000/save-upload-file/pic/
    # python fileuptest.py log_20231023_110012.h264 video/h264 http://localhost:8000/save-upload-file/video/
    # python fileuptest.py log_20231111_161411.wav audio/wav http://localhost:8000/save-upload-file/wav/
    # python fileuptest.py data_20231018_12.csv text/csv http://localhost:8000/save-upload-file/csv/
    print({
        "filename":args[1],
        "temporary_filepath":f"/tmp/{args[1]}",
        "fileb_content_type":args[2]
    })
    #wav_upload()
    #csv_upload()
    #pic_upload()
    #video_upload()
