import re
from typing import List
from datetime import datetime

import aiofiles

from packages.file_time.creation_time import creation_date
from model.csv import CSVFileTable,CSVFile

def csv_read(filepath:str,filename:str) -> List[CSVFile]:
    """
    csvファイルを読み込む

    filepath: str
        ファイルのパス
    filename: str
        ファイル名

    return
    ------
    csv_list: List[CSVFile]
        csvファイルのデータ
    """
    filename = filename.replace("data_", "")
    filename = filename.replace(".csv", "")
    # ファイル名から記録時間を取得
    record_time = re.match(r'\d{8}', filename)
    if record_time is None:
        create_time = datetime.fromtimestamp(creation_date(filepath))
    else:
        create_time = datetime.strptime(record_time.group(), '%Y%m%d')

    create_time_str = create_time.strftime('%Y%m%d')
    csv_list:List[CSVFile] = list()

    with open(filepath, 'r') as f:
        data = f.readlines()
    # データを読み込む
    for d in data:
        time_str = create_time_str + d.split(',')[0]
        time = datetime.strptime(time_str, '%Y%m%d%H:%M:%S.%f')
        csv_list.append(CSVFile(**{
            "time":time,
            "raw_data":int(d.split(',')[1]),
            "flag":int(d.split(',')[2])
        }))

    return csv_list

async def async_csv_read(filepath:str,filename:str) -> List[CSVFile]:
    """
    csvファイルを非同期処理で読み込む

    filepath: str
        ファイルのパス
    filename: str
        ファイル名

    return
    ------
    csv_list: List[CSVFile]
        csvファイルのデータ
    """
    filename = filename.replace("data_", "")
    filename = filename.replace("log_", "")
    filename = filename.replace(".csv", "")
    record_time = re.match(r'\d{8}', filename)
    if record_time is None:
        create_time = datetime.fromtimestamp(creation_date(filepath))
    else:
        create_time = datetime.strptime(record_time.group(), '%Y%m%d')

    create_time_str = create_time.strftime('%Y%m%d')
    csv_list:List[CSVFile] = list()

    async with aiofiles.open(filepath, 'r') as f:
        data = await f.readlines()
        for d in data:
            time_str = create_time_str + d.split(',')[0]
            time = datetime.strptime(time_str, '%Y%m%d%H:%M:%S.%f')
            csv_list.append(CSVFile(**{
                "time":time,
                "raw_data":int(d.split(',')[1]),
                "flag":int(d.split(',')[2])
            }))

    return csv_list

def csv_create(csv_list:List[CSVFileTable],filename:str) -> None:
    """
    csvファイルを作成する

    csv_list: List[CSVFileTable]
        csvファイルのデータ
    filename: str
        ファイル名
    """
    csv_data = ""
    for csv in csv_list:
        csv_data += f"{csv.time.strftime('%Y%m%d%H:%M:%S.%f')},{csv.raw_data},{csv.flag}\n"

    with open(file=filename, mode='w') as f:
        f.write(csv_data)

async def async_csv_create(csv_list:List[CSVFileTable],filename:str) -> None:
    """
    csvファイルを非同期処理で作成する

    csv_list: List[CSVFileTable]
        csvファイルのデータ
    filename: str
        ファイル名
    """
    csv_data = ""
    for csv in csv_list:
        csv_data += f"{csv.time.strftime('%Y%m%d%H:%M:%S.%f')},{csv.raw_data},{csv.flag}\n"

    async with aiofiles.open(filename, mode='w') as f:
        await f.write(csv_data)