import re
from typing import List
from datetime import datetime

from packages.file_time.creation_time import creation_date
from model.csv import CSVFile

def csv_read(filepath:str,filename:str) -> List[CSVFile]:
    filename = filename.replace("data_", "")
    filename = filename.replace(".csv", "")
    record_time = re.match(r'\d{8}', filename)
    if record_time is None:
        create_time = datetime.fromtimestamp(creation_date(filepath))
    else:
        create_time = datetime.strptime(record_time.group(), '%Y%m%d')

    create_time_str = create_time.strftime('%Y%m%d')
    csv_list:List[CSVFile] = list()

    with open(filepath, 'r') as f:
        data = f.readlines()
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
    filename = filename.replace("data_", "")
    filename = filename.replace(".csv", "")
    record_time = re.match(r'\d{8}', filename)
    if record_time is None:
        create_time = datetime.fromtimestamp(creation_date(filepath))
    else:
        create_time = datetime.strptime(record_time.group(), '%Y%m%d')

    create_time_str = create_time.strftime('%Y%m%d')
    csv_list:List[CSVFile] = list()

    with open(filepath, 'r') as f:
        data = f.readlines()
    for d in data:
        time_str = create_time_str + d.split(',')[0]
        time = datetime.strptime(time_str, '%Y%m%d%H:%M:%S.%f')
        csv_list.append(CSVFile(**{
            "time":time,
            "raw_data":int(d.split(',')[1]),
            "flag":int(d.split(',')[2])
        }))

    return csv_list