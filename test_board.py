from board import COLOUR, Piece


def test_pieces_displayed_as_unicode_symbol() -> None:
    king = Piece(name="King", color=COLOUR.black, abbreviation="K", symbol=u"\u2654")
    assert str(king) == "\u2654"
