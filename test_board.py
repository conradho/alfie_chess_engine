import string
from textwrap import dedent

import pytest
from board import COLOR, PIECES, Board


@pytest.fixture
def board() -> Board:
    return Board()


def test_pieces_displayed_as_unicode_symbol() -> None:
    assert str(PIECES.K) == "♔"


def test_board_creation_defaults_to_empty_board(board: Board) -> None:
    for row in board.mailbox:
        for square in row:
            assert square.piece is None


def test_board_created_with_correct_algebraic_notation_coordinates(board: Board) -> None:
    assert board.mailbox[7][0].coordinate == "a1"


def test_board_created_with_colored_squares(board: Board) -> None:
    assert board.mailbox[7][0].color == COLOR.black


def test_can_print_empty_board(board: Board) -> None:
    expected_empty_board = "\n\x1b[30m\x1b[47m\n╒══╤══╤══╤══╤══╤══╤══╤══╕\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n├──┼──┼──┼──┼──┼──┼──┼──┤\n│  │  │  │  │  │  │  │  │\n╘══╧══╧══╧══╧══╧══╧══╧══╛\n\x1b[0m\n"  # noqa
    assert str(board) == expected_empty_board


def test_pieces_are_printed_if_they_are_on_square(board: Board) -> None:
    board.mailbox[7][0].piece = PIECES.K
    board.mailbox[7][1].piece = PIECES.r

    expected_board = dedent(
        """
        \x1b[30m\x1b[47m
        ╒═══╤═══╤══╤══╤══╤══╤══╤══╕
        │   │   │  │  │  │  │  │  │
        ├───┼───┼──┼──┼──┼──┼──┼──┤
        │   │   │  │  │  │  │  │  │
        ├───┼───┼──┼──┼──┼──┼──┼──┤
        │   │   │  │  │  │  │  │  │
        ├───┼───┼──┼──┼──┼──┼──┼──┤
        │   │   │  │  │  │  │  │  │
        ├───┼───┼──┼──┼──┼──┼──┼──┤
        │   │   │  │  │  │  │  │  │
        ├───┼───┼──┼──┼──┼──┼──┼──┤
        │   │   │  │  │  │  │  │  │
        ├───┼───┼──┼──┼──┼──┼──┼──┤
        │   │   │  │  │  │  │  │  │
        ├───┼───┼──┼──┼──┼──┼──┼──┤
        │ ♔ │ ♜ │  │  │  │  │  │  │
        ╘═══╧═══╧══╧══╧══╧══╧══╧══╛
        \x1b[0m
        """
    )
    assert str(board) == expected_board


def test_get_square_from_coordinate(board: Board) -> None:
    for row_number in range(1, 9):
        for col_alpha in string.ascii_lowercase[:8]:
            coordinate = f"{col_alpha}{row_number}"
            square = board.get_square_from_coordinate(coordinate)
            assert square.coordinate == coordinate


def test_setup_FEN_position(board: Board) -> None:
    board.setup_FEN_position("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
    assert board.next_move == COLOR.black
    assert board.castling == "KQkq"
    assert board.en_passant is None
    assert board.halfmove_clock == 1
    assert board.fullmove == 2

    assert board.get_square_from_coordinate("e4").piece == PIECES.P
    assert board.get_square_from_coordinate("c5").piece == PIECES.p
    assert board.get_square_from_coordinate("f3").piece == PIECES.N

    board.setup_FEN_position("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
    assert board.en_passant == board.get_square_from_coordinate("e3")
