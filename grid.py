import pygame, random
from pygame.locals import *
from typing import Tuple

class Grid:
  """Defines a grid with cells and related functions"""
  def __init__(self, x: int, y: int, cell_width: int) -> None:
    self.MAX_X = x
    self.MAX_Y = y
    self.CELL_WIDTH = cell_width
    matrix_width = int(x / (cell_width + 1))
    matrix_height = int(y / (cell_width + 1))
    # referenced using [y][x]
    self.matrix = [[0 for i in range(matrix_width)] for j in range(matrix_height)]

  def draw_grid(self, background, color: Tuple[int,int,int]):
      for x in range(0, self.MAX_X, self.CELL_WIDTH + 1):
        pygame.draw.line(background, color, (0 + x, 0), (0 + x, self.MAX_Y))
        print(f"Line X: {x}")
      for y in range(0, self.MAX_Y, self.CELL_WIDTH + 1):
        pygame.draw.line(background, color, (0, 0 + y), (self.MAX_X, 0 + y))
        print(f"Line Y: {y}")

  def draw_cell(self, background, x: int, y: int, color: Tuple[int,int,int]):
    pygame.draw.rect(background, color, Rect(
      x * (self.CELL_WIDTH + 1) - self.CELL_WIDTH,
      y * (self.CELL_WIDTH + 1) - self.CELL_WIDTH,
      self.CELL_WIDTH - 1,
      self.CELL_WIDTH - 1
      )
    )

  def draw_rgb_cell(self, background, x: int, y: int):
    rand_color = (0,random.randrange(255),0)
    pygame.draw.rect(background, rand_color, Rect(
      x * self.CELL_WIDTH - self.CELL_WIDTH + 1,
      y * self.CELL_WIDTH - self.CELL_WIDTH + 1,
      self.CELL_WIDTH - 1,
      self.CELL_WIDTH - 1
      )
    )

  def update_grid():
    ...

  def check_pos(x: int, y: int):
    for y in MAX_Y:
      for x in MAX_X:
        if pos[x,y]:
          if pos[x+1,y]:
            # define rule here
            ...

  def rgb():
    ...

class Snake:
  """Defines a snake that can be drawn with cells in a Grid object"""
  ...

class Apple:
  """Defines an apple drawn on a Grid object that a snake eats"""
  ...
