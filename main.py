#!/usr/bin/env python3

import pygame
from constants import WIDTH, HEIGHT, FPS, WHITE, SQUARE_SIZE, RED
from game import Game
# from board import Board
# from piece import Piece
from minimax import minimax

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos: tuple) -> tuple:
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main() -> None:
    game_over = False

    clock = pygame.time.Clock()

    game = Game(WIN)

    # Event loop
    while not game_over:
        clock.tick(FPS)

        if game.turn == WHITE:
            _, new_board = minimax(game.get_board(), 4, True)
            game.ai_move(new_board)

        if game.get_winner() is not None:
            print('RED win' if game.get_winner() == RED else 'WHITE win')
            game_over = True

        # Handling event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)


        game.update()

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
