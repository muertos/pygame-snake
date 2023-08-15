import pygame, random, sys, os
from pygame.locals import *

# Constants
SCREEN_WIDTH = 626
SCREEN_HEIGHT = 476
CELL_WIDTH = 8
LINE_COLOR = (0,0,0)
BG_COLOR = (0,0,0)
SNAKE_COLOR = (0,0,220)
SNAKE_LENGTH = 8
SNAKE_SPEED = 60
APPLE_COLOR = (220,0,0)

class Game():
  screen_width = SCREEN_WIDTH
  screen_height = SCREEN_HEIGHT
  cell_width = CELL_WIDTH
  bg_color = BG_COLOR

  def __init__(self) -> None:
    pygame.init()
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill(self.bg_color)
    self.screen.blit(self.background, (0,0))
    pygame.display.flip()
    self.screen.fill(self.bg_color)
    self.draw_snake = pygame.USEREVENT

  def run(self, snake, apple):
    pygame.time.set_timer(self.draw_snake, snake.speed)
    while True:
      self.clock.tick(120)
      self.screen.blit(self.background, (0,0))
      self.screen.blit(snake.score_text, (0,0))

      # event handler
      for e in pygame.event.get():
        if e.type == QUIT:
          return
        if e.type == self.draw_snake:
          snake.update_pos(self.background, apple)
          snake.draw_cell(self.background, snake.x, snake.y, snake.color)

      # get keypresses
      # TODO: (for fun) Remove one of the directions and replace it with a toggle, maybe try that for both
      keys = pygame.key.get_pressed()
      if keys[pygame.K_LEFT]:
        snake.dx = -1
        snake.dy = 0
      if keys[pygame.K_RIGHT]:
        snake.dx = 1
        snake.dy = 0
      if keys[pygame.K_UP]:
        snake.dy = -1
        snake.dx = 0
      if keys[pygame.K_DOWN]:
        snake.dy = 1
        snake.dx = 0
      if keys[pygame.K_END]:
        sys.exit(0)

      pygame.display.flip()

class Grid(Game):
  width = int(Game.screen_width / (Game.cell_width + 1))
  height = int((Game.screen_height) / (Game.cell_width + 1))

  def __init__(self, Game) -> None:
    self.matrix = [[0 for i in range(self.width)] for j in range(self.height)]

  def draw_grid(self, background, line_color):
    for x in range(0, self.screen_width, self.cell_width + 1):
      pygame.draw.line(background, line_color, (0 + x, 0), (0 + x, self.screen_height))
    for y in range(0, self.screen_height, self.cell_width + 1):
      pygame.draw.line(background, line_color, (0, 0 + y), (self.screen_width, 0 + y))

  def draw_cell(self, background, x, y, color):
    pygame.draw.rect(background, color, Rect(
      x * (self.cell_width + 1) - self.cell_width,
      y * (self.cell_width + 1) - self.cell_width,
      self.cell_width - 1,
      self.cell_width - 1
      )
    )

class Snake(Grid):
  def __init__(self, speed, color) -> None:
    pygame.mixer.init()
    self.s = "sound"
    self.eat_apple = pygame.mixer.Sound(os.path.join(self.s, "beep.wav"))
    self.length = SNAKE_LENGTH
    self.x = self.length
    self.y = 1
    self.speed = speed
    self.color = color
    self.pos = []
    self.dx = 1
    self.dy = 0
    self.score = 0
    self.font = pygame.font.SysFont(None, 24)
    self.score_text = self.font.render(f"score: {self.score}", True, (0,200,0))
    # initialize snake coordinates
    for i in range(self.length):
      if self.dx == 1:
        self.pos.insert(0, (i + 1, self.y))
      if self.dx == -1:
        self.pos.append((i + 1, self.y))
      if self.dy == 1:
        self.pos.insert(0, (self.x, i + 1))
      if self.dy == -1:
        self.pos.append((self.x, i + 1))

  def update_score(self):
    self.score += 1
    self.score_text = self.font.render(f"score: {self.score}", True, (0,200,0))

  def update_pos(self, background, apple):
    # extract snake head x,y from 0th pos
    hx = self.pos[0][0]
    hy = self.pos[0][1]
    # extract snake tail x,y
    tx = self.pos[self.length - 1][0]
    ty = self.pos[self.length - 1][1]
    # draw head
    self.draw_cell(background, hx, hy, self.color)
    # erase tail
    self.draw_cell(background, tx, ty, Game.bg_color)
    # update head x,y
    self.x += self.dx
    self.y += self.dy
    # wall collision detection
    if self.x > Grid.width:
        self.x = 1
    if self.x < 0:
        self.x = Grid.width
    if self.y > Grid.height:
        self.y = 1
    if self.y < 0:
        self.y = Grid.height
    # check if snake ate apple
    if (self.x, self.y) == (apple.x, apple.y):
      self.length += 1
      pygame.mixer.Sound.play(self.eat_apple)
      apple.generate(self)
      self.update_score()
      apple.draw_cell(background, apple.x, apple.y, apple.color)
      # this seems wrong, but it works
      self.pos.insert(0, (self.x, self.y))
    # check if snake collided with itself
    for i in range(self.length):
      # avoid index error
      if i == self.length - 1:
        break
      if self.pos[i + 1] == (self.x, self.y):
        print("you collided with yourself!")
        sys.exit()
    self.pos.insert(0, (self.x, self.y))
    self.pos.pop(self.length)

class Apple(Snake):
  def __init__(self, color) -> None:
    # don't spawn an x value within the snake's coords
    self.x = random.randrange(int(Game.screen_width / (Game.cell_width + 1) + SNAKE_LENGTH))
    self.y = random.randrange(int(Game.screen_height / (Game.cell_width + 1)))
    self.color = color

  def generate(self, snake):
    """ generate new Apple x,y """
    self.x = random.randrange(int(Game.screen_width / (Game.cell_width + 1)))
    self.y = random.randrange(int(Game.screen_height / (Game.cell_width + 1)))
    while (self.x, self.y) in snake.pos:
      self.x = random.randrange(int(Game.screen_width / (Game.cell_width + 1)))
      self.y = random.randrange(int(Game.screen_height / (Game.cell_width + 1)))

