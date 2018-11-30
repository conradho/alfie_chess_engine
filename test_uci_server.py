import signal
import subprocess
import sys
import time
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest.mock import Mock, call, patch

import pytest
from uci_server import process_stdin

SERVER_FILE = str(Path("./uci_server.py").resolve())


def test_can_exit_server_with_ctrl_c() -> None:
    proc = subprocess.Popen([sys.executable, SERVER_FILE], stdin=subprocess.PIPE)
    # it is running indefinitely
    with pytest.raises(subprocess.TimeoutExpired):
        proc.wait(timeout=1)
    proc.send_signal(signal.SIGINT)

    try:
        proc.wait(timeout=0.5)
    except subprocess.TimeoutExpired:  # pragma: no cover
        proc.kill()
        with open(Path("./chess_engine.log")) as f:
            pytest.fail("server should have exited.\nserver log was:\n" + f.read())


def test_server_has_logging() -> None:
    with NamedTemporaryFile() as fp:
        proc = subprocess.Popen([sys.executable, SERVER_FILE, "--log", fp.name], stdin=subprocess.PIPE)
        time.sleep(1)
        with pytest.raises(subprocess.TimeoutExpired):
            proc.communicate(input=b"hilo there\n", timeout=0.01)
        proc.send_signal(signal.SIGINT)
        time.sleep(1)
        logfile = fp.read().decode("ascii")

        # logging should include startup message, stdin, heartbeat, and stopping message
        for logitem in ["starting", "hilo there", "heartbeat", "stopped"]:
            assert logitem in logfile


def test_delegates_to_uci_interface() -> None:
    with patch("uci_server.process_line") as mock_process_line:
        with patch("sys.stdin.readline", Mock(return_value="abc\n")):
            process_stdin()
            assert mock_process_line.call_args_list == [call("abc")]
