import pandas as pd

from google.cloud import storage as gcs
from io import BytesIO

from model.envconfig import EnvConfig

env = EnvConfig()


class GCSWrapper:
    def __init__(self, bucket_id:str) -> None:
        """GCSのラッパークラス
        Arguments:
            bucket_id {str} -- GoogleCloudStorage Bucket ID
        """
        self._client = gcs.Client.from_service_account_json(json_credentials_path=env.GOOGLE_APPLICATION_CREDENTIALS)
        self._bucket = self._client.get_bucket(bucket_id)

    def show_bucket_names(self) -> None:
        """バケット名の一覧を表示
        """
        [print(bucket.name) for bucket in self._client.list_buckets()]

    def show_file_names(self) -> None:
        """バケット内のファイル一覧を表示
        """
        [print(file.name) for file in self._client.list_blobs(self._bucket)]

    def upload_file(self, local_path:str, gcs_path:str) -> None:
        """GCSにローカルファイルをアップロード

        Arguments:
            local_path {str} -- local file path
            gcs_path {str} -- gcs file path
        """
        blob = self._bucket.blob(gcs_path)
        blob.upload_from_filename(local_path)

    def upload_file_as_dataframe(
        self,
        df:pd.DataFrame,
        gcs_path:str,
        flg_index:bool=False,
        flg_header:bool=True
    ) -> None:
        """GCSにpd.DataFrameをCSVとしてアップロード

        Arguments:
            df {pd.DataFrame} -- DataFrame for upload
            gcs_path {str} -- gcs file path

        Keyword Arguments:
            flg_index {bool} -- DataFrame index flg (default: {False})
            flg_header {bool} -- DataFrame header flg (default: {True})
        """
        blob = self._bucket.blob(gcs_path)
        blob.upload_from_string(df.to_csv(
            index=flg_index, header=flg_header, sep=","))

    def download_file(
        self,
        local_path:str,
        gcs_path:str
    ) -> None:
        """GCSのファイルをファイルとしてダウンロード

        Arguments:
            local_path {str} -- local file path
            gcs_path {str} -- gcs file path
        """
        blob = self._bucket.blob(gcs_path)
        blob.download_to_filename(local_path)

    def download_file_as_dataframe(
        self,
        gcs_csv_path:str
    ) -> pd.DataFrame:
        """GCSのファイルをpd.DataFrameとしてダウンロード

        Arguments:
            gcs_csv_path {str} -- gcs file path (only csv file)

        Returns:
            [pd.DataFrame] -- csv data as pd.DataFrame
        """
        blob = self._bucket.blob(gcs_csv_path)
        content = blob.download_as_string()
        df = pd.read_csv(BytesIO(content))
        return df
