from asyncio import Lock
from aiofiles import open as aiofiles_open
from typing import Any, TypedDict, Literal, Unpack

write_txt_lock = Lock()


class FileOpenOptions(TypedDict, total=False):
    newline: Any | None


async def read_txt(
    file_path: str,
    r_mode: Literal["r", "r+", "rb", "rb+"] = "r",
    w_mode: Literal["w", "w+", "wb", "wb+"] = "w",
    encoding: str | None = None,
    **kwargs: Unpack[FileOpenOptions],
):
    async with write_txt_lock:
        async with aiofiles_open(
            file_path, mode=r_mode, encoding=encoding, **kwargs
        ) as f:
            lines = await f.readlines()
        if not lines:
            return None
        first_line = lines[0].strip()
        async with aiofiles_open(
            file_path, mode=w_mode, encoding=encoding, **kwargs
        ) as f:
            remaining_lines = lines[1:]
            await f.writelines(remaining_lines)
        return first_line
