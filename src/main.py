#!/usr/bin/env python

from objects import *

def main():
  # create all required objects
  game = Game()
  grid = Grid(game)
  apple = Apple(APPLE_COLOR)
  snake = Snake(SNAKE_SPEED, SNAKE_COLOR)

  # draw game header, includes the score
  # draw game grid
  grid.draw_grid(game.background, LINE_COLOR)

  # draw first apple
  apple.draw_cell(game.background, apple.x, apple.y, apple.color)

  # main game loop
  game.run(snake, apple)

if __name__ == "__main__": main()
