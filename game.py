#!/usr/bin/env python3

import pygame
from board import Board
from constants import RED, WHITE, BLUE, SQUARE_SIZE

empty = None

class Game:
    def __init__(self, win: pygame.Surface):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.win = win


    def update(self) -> None:
        self.board.draw_board(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()


    def reset(self) -> None:
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}


    def select(self, row: int, col: int) -> bool:
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)

        if piece is not empty and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False


    def _move(self, row: int, col: int) -> bool:
        piece = self.board.get_piece(row, col)
        if self.selected and piece is empty and (row, col) in self.valid_moves:
            self.board.move_piece(self.selected, row, col)

            skipped = self.valid_moves.get((row, col))

            if skipped:
                self.board.remove_piece(skipped)

            self.change_turn()
        else:
            return False

        return True

    def get_winner(self):
        return self.board.get_winner()


    def change_turn(self) -> None:
        self.valid_moves = {}
        self.turn = RED if self.turn == WHITE else WHITE

    def draw_valid_moves(self, moves: dict) -> None:
        radius = SQUARE_SIZE//2 - SQUARE_SIZE//2*0.7
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win,
                BLUE,
                (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2),
                radius
            )


    def get_board(self):
        return self.board


    def ai_move(self, board: Board):
        self.board = board
        self.change_turn()
