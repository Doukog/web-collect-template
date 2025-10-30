from asyncio import run as asyncio_run
from core import Task


async def main():
    task = Task()
    await task.start()


if __name__ == "__main__":
    asyncio_run(main())
