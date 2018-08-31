from dataclasses import dataclass
from typing import List, NamedTuple, Union

# We make the type of Colour just a boolean for now so that we can flexibly change this later
Colour = bool


class Colours(NamedTuple):
    white: Colour = False
    black: Colour = True


COLOUR = Colours()


@dataclass(frozen=True)
class Piece:
    name: str
    color: Colour
    abbreviation: str
    symbol: str

    def __repr__(self) -> str:
        return self.symbol


class Board:
    mailbox: List[List[Union[Piece, None]]] = [[None] * 8] * 8
    next_move: Colour = COLOUR.white
