#!/usr/bin/env python3

import pygame
from constants import RED, WHITE, SQUARE_SIZE, GRAY, CROWN

class Piece:
    PADDING = SQUARE_SIZE//2*0.3
    OUTLINE = 2

    def __init__(self, row: int, col: int, color: tuple):
        self.row = row
        self.col = col
        self.color = color
        self.is_king = False
        self.x, self.y = self.calc_pos()


    def calc_pos(self) -> tuple:
        x = SQUARE_SIZE*self.col + SQUARE_SIZE//2
        y = SQUARE_SIZE*self.row + SQUARE_SIZE//2
        return x, y


    def make_king(self) -> None:
        self.is_king = True


    def draw_piece(self, win: pygame.Surface) -> None:
        radius = SQUARE_SIZE//2 - Piece.PADDING

        # self.x, self.y = self.calc_pos()
        # Draw the outline (border) of the piece
        pygame.draw.circle(win, GRAY, (self.x, self.y), radius + Piece.OUTLINE)
        # Draw the piece
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.is_king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))


    def move(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.x, self.y = self.calc_pos()

    def __repr__(self):
        return str(self.color)
