#!/usr/bin/env python3

import pygame

WIDTH = HEIGHT = 800

ROWS = COLS = 8

SQUARE_SIZE = WIDTH//COLS

WHITE_HALVES = (ROWS - 2)//2

RED_HALVES = WHITE_HALVES + 1

NUM_PIECES = ROWS*WHITE_HALVES//2

FPS = 60

rgb = lambda r, g, b: (r, g, b)

RED    = rgb(255, 0, 0)
WHITE  = rgb(255, 255, 255)
YELLOW = rgb(252, 211, 140)
BLACK  = rgb(0, 0, 0)
BLUE   = rgb(0, 0, 255)
GRAY   = rgb(128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

INF = float('inf')
