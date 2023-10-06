
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

# Google App Engine設定
```
gcloud compute backend-services update <backend service name> --timeout=<expected duration>
```