# API
FastAPIで構築したAPIサーバー
ファイルアップロードは以下のように実装すること
<details>
<summary>curlの場合</summary>

```
$ curl -X POST "http://localhost:5000/save-upload-file/wav/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "fileb=@fastsample/test/data/toujyo.wav;type=audio/wav"
```

</details>
<details>
<summary>pythonのrequestsによるwavファイルアップロードの実装</summary>

```python
# -*- coding: utf-8 -*-
import requests


BASE_URL = "http://localhost:5000"

def wav_upload():
    fileName = '{ファイルパス}'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'fileb': (fileName, fileDataBinary, 'audio/wav')}

    url = f'{BASE_URL}/save-upload-file/wav/'
    response = requests.post(url=url, files=files, timeout=100)

    print(response.status_code)
    print(response.content)

if __name__ == "__main__":
    wav_upload()
```
</details>

ダウンロードの場合は以下のようなurlにgetリクエストを送ることでダウンロードできる
```
http://localhost:5000/download-file/pic/?start_time=2023-10-25%205:59:00&end_time=2023-10-25%206:01:00
```
この場合、2023-10-25 5:59:00から2023-10-25 6:01:00までの間の画像がダウンロードされる

|パス|HTTPメゾット|概要|
|---|---|---|
|/|get|hello worldがjsonで返ってくる|
|/save-upload-file/csv/|post|csvのアップロード|
|/save-upload-file/wav/|post|wavのアップロード|
|/save-upload-file/pic/|post|picのアップロード|
|/save-upload-file/video/|post|h264のアップロード|
|/download-file/csv/?start_time={time}&end_time={time}|get|指定された時刻間のデータが記録されたcsvがダウンロードされる|
|/download-file/wav/?start_time={time}&end_time={time}|get|指定された時刻間の音声データがwavとしてダウンロードされる|
|/download-file/pic/?start_time={time}&end_time={time}|get|指定された時刻間の画像がダウンロードされる|
|/download-file/video/?start_time={time}&end_time={time}|get|指定された時刻間の動画がダウンロードされる|

# wifi確認
```
iwconfig

Oyama Lab
Oyama Lab Guest
Oyama Lab 2.4GHz
```
# wifi設定
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
priority=100
priorityの値が低いほど優先的に接続される
(だがラズパイで有効になってる気配がないので、使わないssidはコメントアウトが有効)
```
# 仮想環境の構築
```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
deactivate
```

# nginxの設定
```
sudo apt install nginx
sudo nano /etc/nginx/conf.d/default.conf

以下、設定
server {
    # ルータにのみ設定
    #listen 80 default_server;
    #listen [::]:80 default_server;

    location / {
        proxy_pass http://localhost:8000/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
    }
}

sudo service nginx restart
```

# FastAPIの起動
```
uvicorn main:app --reload --host=192.168.249.116 --port=8000
```


# 仮想環境の構築
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
``````

# FastAPIサーバー起動
```
cd app
source venv/bin/activate
uvicorn main:app --reload --host=192.168.249.1 --port=8000
or
python3 main.py
```

# ルータ起動方法
起動まで時間がかかります
```
sudo iw phy phy0 interface add ap0 type __ap
sudo ip link set ap0 address de:a6:32:a8:e0:24

sudo systemctl restart hostapd.service
sudo systemctl restart dhcpcd.service
sudo systemctl restart dnsmasq.service
```

# Nginx起動
```
sudo systemctl start nginx
```

# Google App Engineデプロイ
```
gcloud app deploy
```

# Google App Engine設定(WebSocket使用時に必要、一度フレキシブル環境に変更する必要があり。**スタンダードには戻せないので注意**)
```
gcloud compute backend-services update <backend service name> --timeout=<expected duration>
```