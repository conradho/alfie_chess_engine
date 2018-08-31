from dataclasses import dataclass
from typing import List, NamedTuple, Union


class Colours(NamedTuple):
    white: bool = False
    black: bool = True


COLOUR = Colours()


@dataclass(frozen=True)
class Piece:
    name: str
    color: bool
    abbreviation: str
    symbol: str

    def __repr__(self) -> str:
        return self.symbol


class Board:
    mailbox: List[List[Union[Piece, None]]] = [[None] * 8] * 8
