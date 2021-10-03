#!/usr/bin/env python3

from typing import Optional
import pygame
from constants import BLACK, RED, ROWS, COLS, SQUARE_SIZE, WHITE, BLUE, YELLOW
from piece import Piece

empty = None

class Board:
    def __init__(self):
        self.board = [[empty for _ in range(ROWS)] for _ in range(COLS)]
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()


    def draw_squares(self, win: pygame.Surface):
        win.fill(YELLOW)

        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, BLACK, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def create_board(self):
        board = self.board
        white_limit = (ROWS - 2)//2
        red_limit = white_limit + 1
        for row in range(ROWS):
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < white_limit:
                        board[row][col] = Piece(row, col, WHITE)
                    elif row > red_limit:
                        board[row][col] = Piece(row, col, RED)


    def move_piece(self, piece: Piece, row: int, col: int) -> None:
        board = self.board

        board[piece.row][piece.col], board[row][col] =\
        board[row][col], board[piece.row][piece.col]

        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1


    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        return self.board[row][col]


    def get_valid_moves(self, piece: Piece) -> dict[tuple[int, int], list[Piece]]:
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.is_king:
            moves.update(
                self._traverse_left(
                    start=row - 1,
                    stop=max(row - 3, -1),
                    step=-1,
                    color=piece.color,
                    left=left)
            )

            moves.update(
                self._traverse_right(
                    start=row - 1,
                    stop=max(row - 3, -1),
                    step=-1,
                    color=piece.color,
                    right=right)
            )

        if piece.color == WHITE or piece.is_king:
            moves.update(
                self._traverse_left(
                    start=row + 1,
                    stop=min(row + 3, ROWS),
                    step=1,
                    color=piece.color,
                    left=left)
            )

            moves.update(
                self._traverse_right(
                    start=row + 1,
                    stop=min(row + 3, ROWS),
                    step=1,
                    color=piece.color,
                    right=right)
            )

        return moves

    def remove_piece(self, pieces: list[Piece]):
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece is not empty:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def get_winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None


    def has_winner(self):
        return self.get_winner() != None


    def _traverse_left(self,
                       start: int,
                       stop: int,
                       step: int,
                       color: tuple,
                       left: int,
                       skipped: list=None):
        if skipped is None:
            skipped = []
        moves = {}
        last = []

        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.get_piece(r, left)
            if current is empty:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(
                        self._traverse_left(
                            start=r + step,
                            stop=row,
                            step=step,
                            color=color,
                            left=left - 1,
                            skipped=last)
                    )
                    moves.update(
                        self._traverse_right(
                            start=r + step,
                            stop=row,
                            step=step,
                            color=color,
                            right=left + 1,
                            skipped=last)
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves


    def _traverse_right(self,
                        start: int,
                        stop: int,
                        step: int,
                        color: tuple,
                        right: int,
                        skipped: list=None):
        if skipped is None:
            skipped = []
        moves = {}
        last = []

        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.get_piece(r, right)
            if current is empty:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(
                        self._traverse_left(
                            start=r + step,
                            stop=row,
                            step=step,
                            color=color,
                            left=right - 1,
                            skipped=last)
                    )
                    moves.update(
                        self._traverse_right(
                            start=r + step,
                            stop=row,
                            step=step,
                            color=color,
                            right=right + 1,
                            skipped=last)
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def draw_board(self, win: pygame.Surface) -> None:
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece is not empty:
                    piece.draw_piece(win)


    def eval(self) -> float:
        return self.white_left - self.red_left + self.white_kings*0.5 - self.red_kings*0.5

    def get_all_pieces(self, color: tuple) -> list:
        pieces = []
        for row in self.board:
            for piece in row:
                if piece is not empty and piece.color == color:
                    pieces.append(piece)

        return pieces
