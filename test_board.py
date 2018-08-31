from board import Piece


def test_pieces_displayed_as_unicode_symbol():
    king = Piece(name="King", color="W", abbreviation="K", symbol=u"\u2654")
    assert str(king) == "\u2654"
