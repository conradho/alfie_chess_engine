import string
from dataclasses import dataclass
from itertools import cycle
from typing import Iterator, List, NamedTuple, Optional

from colorama import Back, Fore, Style

from tabulate import tabulate

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
    notation: str
    symbol: str

    def __repr__(self) -> str:
        return self.symbol


class Pieces(NamedTuple):
    K: Piece = Piece(name="King", color=COLOR.white, notation="K", symbol="\u2654")
    Q: Piece = Piece(name="Queen", color=COLOR.white, notation="Q", symbol="\u2655")
    R: Piece = Piece(name="Rook", color=COLOR.white, notation="R", symbol="\u2655")
    B: Piece = Piece(name="Bishop", color=COLOR.white, notation="B", symbol="\u2657")
    N: Piece = Piece(name="Knight", color=COLOR.white, notation="N", symbol="\u2658")
    P: Piece = Piece(name="Pawn", color=COLOR.white, notation="", symbol="\u2659")
    k: Piece = Piece(name="King", color=COLOR.black, notation="K", symbol="\u265a")
    q: Piece = Piece(name="Queen", color=COLOR.black, notation="Q", symbol="\u265b")
    r: Piece = Piece(name="Rook", color=COLOR.black, notation="R", symbol="\u265c")
    b: Piece = Piece(name="Bishop", color=COLOR.black, notation="B", symbol="\u265d")
    n: Piece = Piece(name="Knight", color=COLOR.black, notation="N", symbol="\u265e")
    p: Piece = Piece(name="Pawn", color=COLOR.black, notation="", symbol="\u265f")


PIECES = Pieces()


@dataclass
class Square:
    coordinate: str
    color: Color
    piece: Optional[Piece]

    def __repr__(self) -> str:
        return self.piece.symbol if self.piece else " "


class Board:
    # internal representation of the board is "mailbox" format
    # ie. a square-centric board representation where the encoding of every
    # square resides in a separately addressable memory element The square
    # number, or its file and rank, acts like an address to a post box, which
    # might be empty or may contain one chess piece.
    # the first "row" is the 8th row, as we'd want to print the 8th row first,
    # and also because FEN notation has the 8th row first
    mailbox: List[List[Square]]
    next_move: Color
    en_passant: Optional[Square]
    castling: str
    half_move_clock: int
    full_move: int

    def __init__(self) -> None:
        self.mailbox = []
        color_iterator = cycle([COLOR.black, COLOR.white])
        for row_number in range(8, 0, -1):
            row = []
            for col_alpha in string.ascii_lowercase[:8]:
                row.append(Square(coordinate=f"{col_alpha}{row_number}", color=next(color_iterator), piece=None))
            self.mailbox.append(row)

    def __repr__(self) -> str:
        # clear screen
        # board_string = "\x1b[2J"
        board_string = "\n" + Fore.BLACK + Back.WHITE + "\n"
        board_string += tabulate(self.mailbox, tablefmt="fancy_grid")
        return board_string + "\n" + Style.RESET_ALL + "\n"

    def get_square_from_coordinate(self, coordinate: str) -> Square:
        row = int(coordinate[1])
        col = ord(coordinate[0].lower()) - 97
        return self.mailbox[-row][col]

    def setup_FEN_position(self, fen: str) -> None:
        fen_mailbox, active, self.castling, en_passant, halfmove_clock, fullmove = fen.split(" ")
        self.halfmove_clock = int(halfmove_clock)
        self.fullmove = int(fullmove)
        self.next_move = COLOR.white if active == "w" else COLOR.black
        if en_passant != "-":
            self.en_passant = self.get_square_from_coordinate(en_passant)
        else:
            self.en_passant = None

        def generate_mailbox_squares() -> Iterator[Square]:
            for row in self.mailbox:
                for square in row:
                    yield square

        mailbox_squares = generate_mailbox_squares()

        for row in fen_mailbox.split("/"):
            for char in row:
                if char.isnumeric():
                    for ii in range(int(char)):
                        next(mailbox_squares).piece = None
                else:
                    next(mailbox_squares).piece = getattr(PIECES, char)
