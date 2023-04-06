import pygame
from animated_sprite import AnimatedSprite
import config as cfg

class ChestLid(pygame.sprite.Sprite):
  def __init__(self,game,x,y,type,position, scale):
    super().__init__()
    if(type == 0):
      if(position == 'left'):
        self.image = pygame.image.load('resources/chests/blue_chest/open/left.png')
      else:
        self.image = pygame.image.load('resources/chests/blue_chest/open/right.png')
    elif(type == 1):
      if(position == 'left'):
        self.image = pygame.image.load('resources/chests/blue_chest/open/left.png')
      else:
        self.image = pygame.image.load('resources/chests/blue_chest/open/right.png')
    else:
      if(position == 'left'):
        self.image = pygame.image.load('resources/chests/blue_chest/open/left.png')
      else:
        self.image = pygame.image.load('resources/chests/blue_chest/open/right.png')
    self.image = pygame.transform.rotozoom(self.image, 0, scale)
    self.rect = self.image.get_rect()
    if position == 'left':
      self.rect.right = x
    else:
      self.rect.left = x
    self.rect.centery = y
    self.speedx = 0

  def update(self):
    self.rect.move_ip(self.speedx * self.game.delta_time / 33, 0)
    
class Chest(pygame.sprite.Sprite):
  def __init__(self, game, x, y, type):
    self.game = game
    super().__init__()
    if(type == 0):
      self.image = pygame.image.load('resources/chests/blue_chest/0.png')
      self.image = pygame.transform.rotozoom(self.image, 0, cfg.MEASURE / self.image.get_size()[0])
      self.body = pygame.image.load('resources/chests/blue_chest/open/body.png')
      self.body = pygame.transform.rotozoom(self.body, 0, cfg.MEASURE / self.image.get_size()[0])
    elif(type == 1):
      self.image = pygame.image.load('resources/chests/blue_chest/0.png')
      self.image = pygame.transform.rotozoom(self.image, 0, cfg.MEASURE / self.image.get_size()[0])
      self.body = pygame.image.load('resources/chests/blue_chest/open/body.png')
      self.body = pygame.transform.rotozoom(self.body, 0, cfg.MEASURE / self.image.get_size()[0])
    else:
      self.image = pygame.image.load('resources/chests/blue_chest/0.png')
      self.image = pygame.transform.rotozoom(self.image, 0, cfg.MEASURE / self.image.get_size()[0])
      self.body = pygame.image.load('resources/chests/blue_chest/open/body.png')
      self.body = pygame.transform.rotozoom(self.body, 0, cfg.MEASURE / self.image.get_size()[0])

    self.rect = self.image.get_rect(topleft = (x, y))
    self.type = type
    self.open_time = -1
    self.frame = 0
    scale = cfg.MEASURE / self.image.get_size()[0]
    self.l_lid = ChestLid(game, self.rect.centerx,self.rect.centery, type, 'left', scale)
    self.r_lid = ChestLid(game, self.rect.centerx, self.rect.centery, 
type, 'right', scale)

  def open(self):
    self.open_time = self.game.time
    self.image = self.body
    self.l_lid.speedx = -5
    self.r_lid.speedx = 5
    self.game.sprites.add(self.l_lid)
    self.game.sprites.add(self.r_lid)
    print('opened chest')

  def update(self):
    if self.game.time - self.open_time <= 1000:
      self.r_lid.speedx = 0
      self.l_lid.speedx = 0
    

class Portal(AnimatedSprite):
  def __init__(self, game, x, y):
    super().__init__(game, x, y, path='')