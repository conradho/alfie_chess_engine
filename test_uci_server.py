import signal
import subprocess
import sys
from pathlib import Path

import pytest


def test_can_exit_server_with_ctrl_c() -> None:
    command = f'{sys.executable} {str(Path("./uci_server.py").resolve())}'
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE)
    # it is running indefinitely
    with pytest.raises(subprocess.TimeoutExpired):
        proc.wait(timeout=1)
    proc.send_signal(signal.SIGINT)

    try:
        proc.wait(timeout=0.5)
    except subprocess.TimeoutExpired:  # pragma: no cover
        proc.terminate()
        pytest.fail("server should have exited")
