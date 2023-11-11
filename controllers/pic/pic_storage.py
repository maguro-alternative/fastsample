# 環境変数を使用しアクセスする場合
from model.envconfig import EnvConfig
from google.cloud import storage

env = EnvConfig()

# google cloud storageのクライアントインスタンスを作成
CLIENT = storage.Client.from_service_account_json(json_credentials_path=env.GOOGLE_APPLICATION_CREDENTIALS)
#バケットのインスタンスを取得
BUCKET = CLIENT.bucket(bucket_name=env.BUCKET_NAME)