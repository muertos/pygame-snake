#!/usr/bin/env python

from objects import *

# Constants
SCREEN_WIDTH = 626
SCREEN_HEIGHT = 476
CELL_WIDTH = 8
LINE_COLOR = (0,0,0)
BG_COLOR = (0,0,0)
SNAKE_COLOR = (0,0,220)
SNAKE_SPEED = 60
APPLE_COLOR = (220,0,0)

def main():
  # create all required objects
  game = Game()
  grid = Grid(game)
  apple = Apple(APPLE_COLOR)
  snake = Snake(SNAKE_SPEED, SNAKE_COLOR)

  # draw game grid
  grid.draw_grid(game.background, LINE_COLOR)

  # draw first apple
  apple.draw_cell(game.background, apple.x, apple.y, apple.color)

  # main game loop
  game.run(snake, apple)

if __name__ == "__main__": main()
