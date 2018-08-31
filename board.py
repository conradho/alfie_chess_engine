from dataclasses import dataclass


@dataclass(frozen=True)
class Piece:
    name: str
    color: str
    abbreviation: str
    symbol: str

    def __repr__(self):
        return self.symbol
