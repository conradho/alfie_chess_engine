"""
Usage: uci_server.py [--log <logfile>]

--log    specify the logfile path. Otherwise it defaults to chess_engine.log in the current working directory.
"""
import asyncio
import datetime
import logging
import signal
import sys
from pathlib import Path

from docopt import docopt
from uci_interface import process_line

HEARTBEAT_FREQUENCY = 5


async def heartbeat() -> None:
    while True:
        logging.debug(f"heartbeat: {datetime.datetime.now()}")
        await asyncio.sleep(HEARTBEAT_FREQUENCY)


def ask_exit() -> None:
    # this is just a synchronous function that puts something onto the loop. we
    # need to cancel the tasks from within the loop because after we cancel, we
    # want to await for the tasks to complete before stopping the loop
    logging.debug("stopping")

    async def stop_all_tasks() -> None:
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]  # type: ignore
        for task in tasks:
            task.cancel()
        await asyncio.wait(tasks, timeout=0.5)
        asyncio.get_event_loop().stop()
        logging.debug("stopped")

    asyncio.get_event_loop().create_task(stop_all_tasks())


def process_stdin() -> None:
    command = sys.stdin.readline().rstrip("\n")
    if command:
        logging.debug(f"received from stdin: {repr(command)}")
    process_line(command)


async def setup_server(loop: asyncio.AbstractEventLoop) -> None:
    loop.create_task(heartbeat())
    loop.add_reader(sys.stdin.fileno(), process_stdin)
    loop.add_signal_handler(signal.SIGINT, ask_exit)


if __name__ == "__main__":  # pragma: no cover
    arguments = docopt(__doc__)
    log_path = str(arguments["<logfile>"]) if arguments["--log"] else "./chess_engine.log"
    # must not log before setting up the config
    logging.basicConfig(filename=str(Path(log_path).resolve()), level=logging.DEBUG)
    logging.debug("starting")
    loop = asyncio.get_event_loop()
    # calling an `async function` returns a coroutine and create_task takes
    # that coro and turns it into a task to be executed on the loop
    loop.create_task(setup_server(loop))
    loop.run_forever()
    loop.close()
