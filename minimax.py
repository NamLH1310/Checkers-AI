#!/usr/bin/env python3

from copy import deepcopy
from typing import Optional
from constants import RED, WHITE, INF
from board import Board
from piece import Piece

def simulate_move(piece: Optional[Piece],
                  move: tuple[int, int],
                  board: Board,
                  skipped: list[Piece]
                  ):
    row, col = move
    board.move_piece(piece, row, col)
    if skipped:
        board.remove_piece(skipped)

    return board

def get_all_moves(game_state: Board, color: tuple) -> list[Board]:
    moves = []

    for piece in game_state.get_all_pieces(color):
        valid_moves = game_state.get_valid_moves(piece)
        for move, skipped in valid_moves.items():
            temp_board = deepcopy(game_state)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_state = simulate_move(temp_piece, move, temp_board, skipped)
            moves.append(new_state)

    return moves

def minimax(
        game_state: Board,
        depth: int,
        max_player: bool,
            ) -> tuple[float, Board]:

    if depth == 0 or game_state.has_winner():
        return game_state.eval(), game_state

    best_move: Board

    if max_player:
        max_eval = -INF
        for move in get_all_moves(game_state, WHITE):
            evaluation, _ = minimax(move, depth - 1, False)
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move

        return max_eval, best_move
    else:
        min_eval = INF
        for move in get_all_moves(game_state, RED):
            evaluation, _ = minimax(move, depth - 1, True)
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move

        return min_eval, best_move
