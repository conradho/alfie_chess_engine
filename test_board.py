import pytest

from board import COLOR, Board, Piece


def test_pieces_displayed_as_unicode_symbol() -> None:
    king = Piece(name="King", color=COLOR.black, abbreviation="K", symbol=u"\u2654")
    assert str(king) == "♔"


@pytest.fixture
def new_board() -> Board:
    return Board()


def test_board_creation_defaults_to_empty_board(new_board: Board) -> None:
    for row in new_board.mailbox:
        for square in row:
            assert square.piece is None


def test_board_creation_defaults_to_white_to_move(new_board: Board) -> None:
    assert new_board.next_move == COLOR.white


def test_board_created_with_correct_algebraic_notation_coordinates(new_board: Board) -> None:
    assert new_board.mailbox[0][0].coordinate == "a1"


def test_board_created_with_colored_squares(new_board: Board) -> None:
    assert new_board.mailbox[0][0].color == COLOR.black


def test_can_print_board(new_board: Board) -> None:
    expected_empty_board = "\x1b[30m\x1b[47m\n╒══╤══╤══╤══╤══╤══╤══╤══╕\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n╘══╧══╧══╧══╧══╧══╧══╧══╛\x1b[0m"  # noqa
    assert str(new_board) == expected_empty_board
