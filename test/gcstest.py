# 環境変数を使用しアクセスする場合
import os
from google.cloud import storage
from PIL import Image
import io

# google cloud storageのクライアントインスタンスを作成
client= storage.Client()

# 直にjsonファイルへアクセスする場合。
client = storage.Client.from_service_account_json(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
#バケットのインスタンスを取得
bucket = client.bucket('uploadfasttest')

#ファイルのblobインスタンスを取得
blob = bucket.blob('image.png')
def img_download():
    img = Image.open(io.BytesIO(blob.download_as_string()))
    img.save('sample.png')

def xlsx_download():
    ##ファイルのblobインスタンスを取得
    blob = bucket.blob('test.xlsx')
    buffer = io.BytesIO()
    blob.download_to_file(buffer)


def upload():
    blob.upload_from_filename(filename='sample.png')