import asyncio
import datetime
import logging
import sys
from pathlib import Path

logging.basicConfig(filename=str(Path("./chess_engine.log").resolve()), level=logging.DEBUG)


async def heartbeat() -> None:
    while True:
        logging.debug(datetime.datetime.now())
        await asyncio.sleep(5)


def process_stdin() -> None:
    stdin = sys.stdin.readline()
    logging.debug(f"received from stdin: {repr(stdin)}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # calling the hearbeat function returns a coroutine and create_task takes a
    # coro and turns it into a task to be executed in the loop
    loop.create_task(heartbeat())
    loop.add_reader(sys.stdin.fileno(), process_stdin)
    loop.run_forever()
