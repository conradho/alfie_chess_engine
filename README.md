[![Build Status](https://travis-ci.org/conradho/alfie_chess_engine.svg?branch=master)](https://travis-ci.org/conradho/alfie_chess_engine)
[![Coverage Status](https://coveralls.io/repos/github/conradho/alfie_chess_engine/badge.svg?branch=master)](https://coveralls.io/github/conradho/alfie_chess_engine?branch=master)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This project runs on python3.7

### Testing and pre-commit hooks:
- from rootdir
    - pytest
    - mypy --python-version 3.7 --config-file mypy.ini .
    - pytest --cov=. --cov-config=.coveragerc --cov-fail-under=100
- currently also running pytest with `-W ignore::DeprecationWarning` because the tabulate has a deprecation warning


### Upgrading to newer libraries
- `sed 's/==.*//' requirements.txt > requirements-unpinned.txt`
- `pip install --upgrade -r requirements-unpinned.txt`
- `pip freeze > requirements.txt`

### Todo
- consider having merging pieces/squres, and adding empty/no piece as a type of square/piece
- other board features needed:
    - repetitions of the position
    - whether last move was a pawn move (en passant)
    - can white/black still castle/which way
    - `no_progress_count` (number of moves since captures/pawn moves)
- setup pyup.io
- engine dies quietly if log path is not writeable


### References
- [python code](https://github.com/thomasahle/sunfish/) interfacing with UCI
- [UCI protocol](http://wbec-ridderkerk.nl/html/UCIProtocol.html)
- [FEN notation](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
