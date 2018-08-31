from dataclasses import dataclass
from typing import NamedTuple


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
