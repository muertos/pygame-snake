#!/usr/bin/env python

import pygame
import random
import sys
import random

from pygame.locals import *
from grid import Grid

# events
draw_snake = pygame.USEREVENT
shoot = pygame.USEREVENT + 1

def main():
  #
  # VARIABLES
  #

  SCREEN_WIDTH: int = 1280 
  SCREEN_HEIGHT: int = 960 
  CELL_WIDTH: int = 4 

  grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_WIDTH)
  snake_length: int = 8
  
  # head position of snake
  x: int = snake_length
  y: int = 1
  
  # move to the right by default
  delta_x: int = 1
  delta_y: int = 0

  # array of snake coordinates
  pos = []
  # initialize snake coordinates
  for i in range(snake_length):
    if delta_x == 1:
      pos.insert(0, (i + 1, y))
    if delta_x == -1:
      pos.append((i + 1, y))
    if delta_y == 1:
      pos.insert(0, (x, i + 1))
    if delta_y == -1:
      pos.append((x, i + 1))

  # snakes eat apples
  apple_x = random.randrange(int(SCREEN_WIDTH / (CELL_WIDTH + 1)))
  apple_y = random.randrange(int(SCREEN_HEIGHT / (CELL_WIDTH + 1)))

  # pygame necessities
  pygame.init()
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((grid.MAX_X, grid.MAX_Y))
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0,0,0))
  screen.blit(background, (0,0))
  pygame.display.flip()
  screen.fill((255,255,255))

  # draw game grid
  grid.draw_grid(background, (100,100,100))

  # draw first apple
  grid.draw_cell(background, apple_x, apple_y, (220,0,0))

  # update snake position every 50ms
  pygame.time.set_timer(draw_snake, 50)
  # update snake bullet every 3ms
  #pygame.time.set_timer(shoot, 3)

  while True:
    clock.tick(120)
    screen.blit(background, (0,0))

    for e in pygame.event.get():
      if e.type == QUIT:
          return
      if e.type == draw_snake:
        # head x,y
        hx = pos[0][0]
        hy = pos[0][1]
        # tail x,y
        tx = pos[snake_length - 1][0]
        ty = pos[snake_length - 1][1]
        # draw head
        grid.draw_cell(background, hx, hy, (0,200,20))
        # erase tail
        grid.draw_cell(background, tx, ty, (0,0,0))
        # update snake head x,y
        x += delta_x
        y += delta_y

        for i in range(snake_length):
          _x = pos[i][0]
          _y = pos[i][1]
          # snake ate apple
          if x == apple_x and y == apple_y:
            snake_length += 1
            apple_x = random.randrange(int(SCREEN_WIDTH / (CELL_WIDTH + 1)))
            apple_y = random.randrange(int(SCREEN_HEIGHT / (CELL_WIDTH + 1)))
            # check to see if apple was drawn on the snake
            # TODO: does this actually work?
            keep_going = True
            while keep_going:
              for i in range(snake_length):
                _x = pos[i][0]
                _y = pos[i][1]
                if apple_x == _x and apple_y == _y:
                  print("apple spawn on snake")
                  # generate a new apple_x and apple_y and compare again
                  keep_going = True
                  apple_x = random.randrange(int(SCREEN_WIDTH / (CELL_WIDTH + 1)))
                  apple_y = random.randrange(int(SCREEN_HEIGHT / (CELL_WIDTH + 1)))
                  break
              keep_going = False
              grid.draw_cell(background, apple_x, apple_y, (220,0,0))
          # collision detection
          if x == _x and y == _y:
            print("You touched yourself! Bye")
            sys.exit()
        # update our tracking array's first element with the head of the snake
        pos.insert(0, (x, y))
      #if e.type == shoot:
      #  # draw snake bullet
      #  ... 

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      delta_x = -1
      delta_y = 0
    if keys[pygame.K_RIGHT]:
      delta_x = 1
      delta_y = 0
    if keys[pygame.K_UP]:
      delta_y = -1
      delta_x = 0
    if keys[pygame.K_DOWN]:
      delta_y = 1
      delta_x = 0
    if keys[pygame.K_SPACE]:
      shoot_event = True
    if keys[pygame.K_END]:
      return

    pygame.display.flip()

if __name__ == "__main__": main()