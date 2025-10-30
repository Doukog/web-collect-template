from asyncio import Lock
from openpyxl import Workbook
from io import BytesIO
from aiofiles import open as aiofiles_open
from os import path as os_path, makedirs as os_makedirs
from typing import Any, TypedDict, Literal, Unpack

write_txt_lock = Lock()
write_excel_lock = Lock()

class FileOpenOptions(TypedDict, total=False):
    newline: Any | None


async def write_txt(
    file_path: str,
    content: str,
    mode: Literal["w", "a", "w+", "a+", "wb", "wb+"] = "w",
    encoding: str | None = None,
    **kwargs: Unpack[FileOpenOptions],
):
    async with write_txt_lock:
        dir_path = os_path.dirname(file_path)

        if dir_path and not os_path.exists(dir_path):
            os_makedirs(dir_path)

        async with aiofiles_open(
            file_path, mode=mode, encoding=encoding, **kwargs
        ) as f:
            await f.write(content)


async def write_excel(file_path: str, data: list):
    async with write_excel_lock:
        dir_path = os_path.dirname(file_path)

        if dir_path and not os_path.exists(dir_path):
            os_makedirs(dir_path)
        
        wb = Workbook()
        ws = wb.active
        
        for row in data:
            ws.append(row)
        
        excel_buffer = BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)

        async with aiofiles_open(file_path, 'wb') as f:
            await f.write(excel_buffer.getvalue())