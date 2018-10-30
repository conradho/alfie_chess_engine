import string
from itertools import cycle
from typing import List, NamedTuple, Optional

from colorama import Back, Fore, Style
from tabulate import tabulate

from dataclasses import dataclass

# We make the type of Colour just a boolean for now so that we can flexibly change this later
Color = bool


class Colors(NamedTuple):
    white: Color = False
    black: Color = True


COLOR = Colors()


# dataclass has auto init/repr etc, and also frozen option raises exception if fields are assigned to
@dataclass(frozen=True)
class Piece:
    name: str
    color: Color
    abbreviation: str
    symbol: str

    def __repr__(self) -> str:
        return self.symbol


@dataclass(frozen=True)
class Square:
    coordinate: str
    color: Color
    symbol: str
    piece: Optional[Piece]

    def __repr__(self) -> str:
        return self.symbol


class Board:
    # internal representation of the board is "mailbox" format
    # ie. a square-centric board representation where the encoding of every
    # square resides in a separately addressable memory element The square
    # number, or its file and rank, acts like an address to a post box, which
    # might be empty or may contain one chess piece.
    mailbox: List[List[Square]]
    next_move: Color = COLOR.white

    def __init__(self) -> None:
        self.mailbox = []
        color_iterator = cycle([COLOR.black, COLOR.white])
        # symbol_iterator = cycle("\u25A0\u25A1")
        for row_number in range(1, 9):
            row = []
            for col_alpha in string.ascii_lowercase[:8]:
                row.append(
                    Square(coordinate=f"{col_alpha}{row_number}", color=next(color_iterator), symbol=" ", piece=None)
                )
            self.mailbox.append(row)

    def __repr__(self) -> str:
        # clear screen
        # board_string = "\x1b[2J"
        board_string = Fore.BLACK + Back.WHITE + "\n"
        board_string += tabulate(reversed(self.mailbox), tablefmt="fancy_grid")
        return board_string + Style.RESET_ALL
