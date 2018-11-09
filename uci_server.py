import asyncio
import datetime
import logging
import signal
import sys
from pathlib import Path

logging.basicConfig(filename=str(Path("./chess_engine.log").resolve()), level=logging.DEBUG)


async def heartbeat() -> None:
    while True:
        logging.debug(datetime.datetime.now())
        await asyncio.sleep(600)


async def stop_all_tasks() -> None:
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]  # type: ignore
    for task in tasks:
        task.cancel()
    await asyncio.wait(tasks, timeout=0.5)
    asyncio.get_event_loop().stop()
    logging.debug("stopped")


def ask_exit() -> None:
    # this is just a synchronous function that puts something onto the loop. we
    # need to cancel the tasks from within the loop because after we cancel, we
    # want to wait for the tasks to complete before stopping the loop
    logging.debug("stopping")
    asyncio.get_event_loop().create_task(stop_all_tasks())


def process_stdin() -> None:
    stdin = sys.stdin.readline()
    logging.debug(f"received from stdin: {repr(stdin)}")


def run_server() -> None:
    loop = asyncio.get_event_loop()
    # calling the hearbeat function returns a coroutine and create_task takes a
    # coro and turns it into a task to be executed in the loop
    loop.create_task(heartbeat())
    loop.add_reader(sys.stdin.fileno(), process_stdin)
    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    run_server()
