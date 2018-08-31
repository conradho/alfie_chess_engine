from board import COLOUR, Board, Piece


def test_pieces_displayed_as_unicode_symbol() -> None:
    king = Piece(name="King", color=COLOUR.black, abbreviation="K", symbol=u"\u2654")
    assert str(king) == "\u2654"


def test_board_creation_defaults_to_empty_board() -> None:
    new_board = Board()
    for row in new_board.mailbox:
        for square in row:
            assert square is None
