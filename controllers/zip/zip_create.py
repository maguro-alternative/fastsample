import zipfile
from io import BytesIO
from typing import List
from fastapi.responses import StreamingResponse


def zipfiles(file_list:List[str]) -> StreamingResponse:
    """
    ファイルをzipに圧縮する

    file_list: List[str]
        ファイルのリスト
    """
    io = BytesIO()
    zip_sub_dir = "final_archive"
    zip_filename = "%s.zip" % zip_sub_dir
    with zipfile.ZipFile(io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            zip.write(fpath)
        zip.close()
    return StreamingResponse(
        iter([io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers = { "Content-Disposition":f"attachment;filename=%s" % zip_filename}
    )