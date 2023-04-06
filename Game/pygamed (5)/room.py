import config as cfg
import pygame
from enemy import Spawner
from objects import Chest, Portal
import math

class RoomController:
    def __init__(self, game, pos, spawners):
      self.visible = True
      self.game = game
      self.posx,self.posy = pos
      self.image = pygame.Surface(((cfg.ROOM_SIZE - 4 )* cfg.MEASURE, (cfg.ROOM_SIZE - 4) * cfg.MEASURE))
      self.image.fill('red')
      self.image.set_alpha(100)
      
      self.spawners = spawners
      for spawner in self.spawners:
        spawner.set_controller(self)
      self.enemies = []
      self.active = False
      self.room_passed = False
      
  # loc -> pos
    @property
    def rect(self):
      top = (self.posx+2) * cfg.MEASURE
      left = (self.posy+2) *cfg.MEASURE
      width = (cfg.ROOM_SIZE - 4) * cfg.MEASURE
      height = (cfg.ROOM_SIZE - 4) * cfg.MEASURE
      return pygame.Rect(top, left, width, height)

    def deactivate(self):
      self.active = False
      print(self.game.wallmap.__len__())
      print(self.game.blocks.content.__len__())
      self.game.open_doors()
      print('after')
      print(self.game.wallmap.__len__())
      print(self.game.blocks.content.__len__())

    def activate(self):
        self.active = True
        self.game.close_doors()
        for spawner in self.spawners:
          spawner.active = True

    def update(self):
      if not self.room_passed:
        if not self.active:
          if self.rect.colliderect(self.game.p.rect):
            self.activate()
        else:
          if all([not spawner.active for spawner in self.spawners]) == True and not self.enemies:
            self.room_passed = True
            self.deactivate()

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, a, b, path=None, color=(0, 120, 60)):
        self.game = game
        self.visible=True
        super().__init__()
        self.image = pygame.Surface((a, b))
        if not path:
          self.image.fill(color)
        else:
          image = pygame.image.load(path)
          image = pygame.transform.scale(image, (cfg.MEASURE, cfg.MEASURE))
          for im, i in enumerate(range(0, a, cfg.MEASURE)):
            for jm, j in enumerate(range(0, b, cfg.MEASURE)):
              self.image.blit(image, (i, j))
              self.game.wallmap.append((x // cfg.MEASURE + im, y // cfg.MEASURE + jm))
        self.rect = self.image.get_rect(topleft=(x, y))

class Door(Block):
  
  opened_im = pygame.image.load('resources/doors/0.png')
  opened_im = pygame.transform.scale(opened_im, (cfg.MEASURE, cfg.MEASURE*24/16))
  closed_im = pygame.image.load('resources/doors/1.png')
  closed_im = pygame.transform.scale(closed_im, (cfg.MEASURE, cfg.MEASURE/14*17))
  
  def __init__(self,game,x,y):
    super(Door, self).__init__(game, x, y, cfg.MEASURE, cfg.MEASURE)
    self.close()

  def open(self):
    self.closed = False
    self.image = self.opened_im
    self.game.blocks.remove(self)
    self.game.wallmap.remove((self.rect.left // cfg.MEASURE, self.rect.top // cfg.MEASURE))

  def close(self):
    self.closed = True
    self.image = self.closed_im
    if self not in self.game.blocks:
      self.game.blocks.add(self)
    pos = (self.rect.left // cfg.MEASURE, self.rect.top // cfg.MEASURE)
    if pos not in self.game.wallmap:
      self.game.wallmap.append(pos)

      

def create_room(game, posx, posy, doors):
    l = ((cfg.ROOM_SIZE) // 2 - 1) * cfg.MEASURE
    doors_insts = []

    if 'up' in doors:
      b1 = Block(game, posx*cfg.MEASURE, posy*cfg.MEASURE, l, cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      

      d = Block(game, (posx + 5) * cfg.MEASURE, (posy-2) * cfg.MEASURE, cfg.MEASURE, 2*cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(d)
      game.blocks.add(d)
      
      b1 = Block(game, (posx + 2) * cfg.MEASURE + l, posy*cfg.MEASURE, l, cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      
      dr1 = Door(game,l+posx*cfg.MEASURE,posy*cfg.MEASURE)
      game.sprites.add(dr1)
      dr2 = Door(game,l+(posx+1)*cfg.MEASURE,posy*cfg.MEASURE)
      game.sprites.add(dr2)
      doors_insts += [dr1, dr2]
      
    else:
      b1 = Block(game, posx*cfg.MEASURE, posy*cfg.MEASURE, cfg.ROOM_SIZE*cfg.MEASURE, cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      
      
    if 'left' in doors:
      b1 = Block(game, posx*cfg.MEASURE, posy*cfg.MEASURE, cfg.MEASURE, l, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      

      d = Block(game, (posx - 2) * cfg.MEASURE, (posy + 8) * cfg.MEASURE, 2*cfg.MEASURE, cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(d)
      game.blocks.add(d)
      
      b1 = Block(game, posx*cfg.MEASURE, (posy + 2) * cfg.MEASURE + l, cfg.MEASURE, l-cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)

      dr1 = Door(game,posx*cfg.MEASURE,posy*cfg.MEASURE+l)
      game.sprites.add(dr1)
      dr2 = Door(game,posx*cfg.MEASURE,(posy+1)*cfg.MEASURE+l)
      game.sprites.add(dr2)      
      doors_insts += [dr1, dr2]
      
    else:
      b1 = Block(game, posx*cfg.MEASURE, cfg.MEASURE + posy*cfg.MEASURE, cfg.MEASURE, cfg.ROOM_SIZE * cfg.MEASURE - 2 * cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      

    if 'down' in doors:
      b1 = Block(game, posx*cfg.MEASURE, (posy-1)*cfg.MEASURE+cfg.ROOM_SIZE*cfg.MEASURE, l, cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      
      

      b1 = Block(game, (posx + 2) * cfg.MEASURE + l, (posy-1)*cfg.MEASURE+cfg.ROOM_SIZE*cfg.MEASURE, l, cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      

      d = Block(game, (posx + 8) * cfg.MEASURE, posy*cfg.MEASURE+cfg.ROOM_SIZE * cfg.MEASURE, cfg.MEASURE, 2*cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(d)
      game.blocks.add(d)

      dr1 = Door(game,l+posx*cfg.MEASURE,(posy-1)*cfg.MEASURE+cfg.MEASURE * cfg.ROOM_SIZE)
      game.sprites.add(dr1)
      dr2 = Door(game,l+(posx+1)*cfg.MEASURE,(posy-1)*cfg.MEASURE + cfg.MEASURE * cfg.ROOM_SIZE)
      game.sprites.add(dr2)
      doors_insts += [dr1, dr2]
      
    else:
      b1 = Block(game, posx*cfg.MEASURE , (posy-1)*cfg.MEASURE + cfg.ROOM_SIZE * cfg.MEASURE, cfg.ROOM_SIZE * cfg.MEASURE, cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      
    
    if 'right' in doors:
      b1 = Block(game, (posx-1)*cfg.MEASURE+cfg.ROOM_SIZE* cfg.MEASURE, (posy+1)*cfg.MEASURE, cfg.MEASURE, l-cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      

      d = Block(game, (posx) * cfg.MEASURE+cfg.ROOM_SIZE * cfg.MEASURE, (posy + 5) * cfg.MEASURE, 2*cfg.MEASURE, cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(d)
      game.blocks.add(d)
      
      b1 = Block(game, (posx-1)*cfg.MEASURE + cfg.ROOM_SIZE * cfg.MEASURE, (posy + 2) * cfg.MEASURE + l, cfg.MEASURE, l-cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)

      dr1 = Door(game,(posx-1)*cfg.MEASURE+cfg.ROOM_SIZE*cfg.MEASURE,posy*cfg.MEASURE+l)
      game.sprites.add(dr1)
      dr2 = Door(game,(posx-1)*cfg.MEASURE +cfg.ROOM_SIZE*cfg.MEASURE,(posy+1)*cfg.MEASURE+l)
      game.sprites.add(dr2)      
      doors_insts += [dr1, dr2]

    else:  
      b1 = Block(game, cfg.ROOM_SIZE * cfg.MEASURE + (posx-1)*cfg.MEASURE,  cfg.MEASURE + posy*cfg.MEASURE, cfg.MEASURE,cfg.ROOM_SIZE * cfg.MEASURE - 1 *cfg.MEASURE, path='resources/textures/walls/0.png')
      game.sprites.add(b1)
      game.blocks.add(b1)
      

    if posx == 0 and posy == 0:
        rc = RoomController(game, (posx, posy), [])
        game.sprites.add(rc)
    elif posx == cfg.ROOM_SIZE + 2 and posy == 0:
      spawners = pattern3(game, (cfg.ROOM_SIZE + 2, 0))
      rc = RoomController(game, (posx,posy), spawners)
      game.sprites.add(rc)
    elif posx == 0 and posy == cfg.ROOM_SIZE + 2:
      spawners = pattern3(game, (0, cfg.ROOM_SIZE + 2))
      rc = RoomController(game, (posx, posy), spawners)
      game.sprites.add(rc)
    elif posx == cfg.ROOM_SIZE + 2 and posy == cfg.ROOM_SIZE + 2:
      spawners = pattern3(game, (cfg.ROOM_SIZE + 2, cfg.ROOM_SIZE + 2))
      rc = RoomController(game, (posx, posy), spawners)
      game.sprites.add(rc)

    return doors_insts

def pattern1(game, pos):
  posx, posy = pos
  spawners = []
  s1 = Spawner(game, (posx + 4) * cfg.MEASURE, (posy + 6) * cfg.MEASURE, cfg.MEASURE*4, cfg.MEASURE*4, [['enemy2','enemy1','enemy1'],['enemy1','enemy2']])
  game.sprites.add(s1)
  spawners.append(s1)

  b1 = Block(game, (posx + 10) * cfg.MEASURE,
            (posy + 1) * cfg.MEASURE, 1*cfg.MEASURE,
            2*cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b1)
  game.blocks.add(b1)
  
  
  b2 = Block(game, (posx + 3) * cfg.MEASURE,
            (posy + 3) * cfg.MEASURE, 2*cfg.MEASURE,
            2*cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b2)
  game.blocks.add(b2)
  
  
  b3 = Block(game, (posx + 9) * cfg.MEASURE,
            (posy + 5) * cfg.MEASURE, cfg.MEASURE,
            1*cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b3)
  game.blocks.add(b3)
  
  
  b4 = Block(game, (posx + 9) * cfg.MEASURE,
            (posy + 6) * cfg.MEASURE, 2*cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b4)
  game.blocks.add(b4)
  
  
  b5 = Block(game, (posx + 5) * cfg.MEASURE,
            (posy + 10) * cfg.MEASURE, cfg.MEASURE*5,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b5)
  game.blocks.add(b5)

  return spawners
  
  

def pattern2(game, pos):
  spawners = []
  posx, posy = pos
  s1 = Spawner(game, (posx + 7) * cfg.MEASURE, (posy + 2) * cfg.MEASURE, cfg.MEASURE*2, cfg.MEASURE*2, [['enemy2',],['enemy1'],['enemy2']])
  game.sprites.add(s1)
  spawners.append(s1)

  s2 = Spawner(game, (posx+ 9) * cfg.MEASURE, (posy + 7) * cfg.MEASURE, cfg.MEASURE*2, cfg.MEASURE*2, [['enemy1'],['enemy2','enemy1']])
  game.sprites.add(s2)
  spawners.append(s2)
  b1 = Block(game, (posx + 7) * cfg.MEASURE,
            (posy + 6) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b1)
  game.blocks.add(b1)
  
  
  b2 = Block(game, (posx + 4) * cfg.MEASURE,
            (posy + 3) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b2)
  game.blocks.add(b2)
  
  
  b3 = Block(game, (posx + 5) * cfg.MEASURE,
            (posy + 4) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b3)
  game.blocks.add(b3)
  
  
  b4 = Block(game, (posx + 6) * cfg.MEASURE,
            (posy + 5) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b4)
  game.blocks.add(b4)
  

  
  b6 = Block(game, (posx + 6) * cfg.MEASURE,
            (posy + 10) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b6)
  game.blocks.add(b6)
  
  
  b7 = Block(game, (posx + 5) * cfg.MEASURE,
            (posy + 9) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b7)
  game.blocks.add(b7)
  
  
  b8 = Block(game, (posx + 4) * cfg.MEASURE,
            (posy + 8) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b8)
  game.blocks.add(b8)
  

  b9= Block(game, (posx + 7) * cfg.MEASURE,
            (posy + 6) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b9)
  game.blocks.add(b9)
  
  
  b10 = Block(game, (posx + 3) * cfg.MEASURE,
            (posy + 7) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b10)
  game.blocks.add(b10)
  

  b11 = Block(game, (posx + 10) * cfg.MEASURE,
            (posy + 3) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE*2, path='resources/textures/walls/0.png')
  game.sprites.add(b11)
  game.blocks.add(b11)
  
  
  b12 = Block(game, (posx + 9) * cfg.MEASURE,
            (posy + 10) * cfg.MEASURE, cfg.MEASURE*2,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b12)
  game.blocks.add(b12)

  return spawners
  
def pattern3(game, pos):
  posx, posy = pos
  spawners = []
  s1 = Spawner(game, (posx + 6) * cfg.MEASURE, (posy + 2) * cfg.MEASURE, cfg.MEASURE*2, cfg.MEASURE*2, [['enemy2'],['enemy1']])
  game.sprites.add(s1)
  spawners.append(s1)

  s2 = Spawner(game, (posx + 6) * cfg.MEASURE, (posy + 10) * cfg.MEASURE, cfg.MEASURE*2, cfg.MEASURE*2, [['enemy1'],['enemy2','enemy1']])
  game.sprites.add(s2)
  spawners.append(s2)
  
  
  b1 = Block(game, (posx + 1) * cfg.MEASURE,
            (posy + 1) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b1)
  game.blocks.add(b1)
  
  
  b2 = Block(game, (posx + 2) * cfg.MEASURE,
            (posy + 2) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b2)
  game.blocks.add(b2)
  
  
  b3 = Block(game, (posx + 3) * cfg.MEASURE,
            (posy + 3) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b3)
  game.blocks.add(b3)
  
  
  b4 = Block(game, (posx + 4) * cfg.MEASURE,
            (posy + 4) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b4)
  game.blocks.add(b4)
  

  b5 = Block(game, (posx + 12) * cfg.MEASURE,
            (posy + 1) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b5)
  game.blocks.add(b5)
  

  b6 = Block(game, (posx + 11) * cfg.MEASURE,
            (posy + 2) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b6)
  game.blocks.add(b6)
  
  
  b7 = Block(game, (posx + 10) * cfg.MEASURE,
            (posy + 3) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b7)
  game.blocks.add(b7)
  
  
  b8 = Block(game, (posx + 9) * cfg.MEASURE,
            (posy + 4) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b8)
  game.blocks.add(b8)
  


  b9 = Block(game, (posx + 1) * cfg.MEASURE,
            (posy + 12) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b9)
  game.blocks.add(b9)
  
  
  b10 = Block(game, (posx + 2) * cfg.MEASURE,
            (posy + 11) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b10)
  game.blocks.add(b10)
  
  
  b11 = Block(game, (posx + 3) * cfg.MEASURE,
            (posy + 10) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b11)
  game.blocks.add(b11)
  
  
  b12 = Block(game, (posx + 4) * cfg.MEASURE,
            (posy + 9) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b12)
  game.blocks.add(b12)
  

  b13 = Block(game, (posx + 12) * cfg.MEASURE,
            (posy + 12) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b13)
  game.blocks.add(b13)
  

  b14 = Block(game, (posx + 11) * cfg.MEASURE,
            (posy + 11) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b14)
  game.blocks.add(b14)
  
  
  b15 = Block(game, (posx + 10) * cfg.MEASURE,
            (posy + 10) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b15)
  game.blocks.add(b15)
  
  
  b16 = Block(game, (posx + 9) * cfg.MEASURE,
            (posy + 9) * cfg.MEASURE, cfg.MEASURE,
            cfg.MEASURE, path='resources/textures/walls/0.png')
  game.sprites.add(b16)
  game.blocks.add(b16)
  

  b17 = Block(game, (posx + 6) * cfg.MEASURE,
            (posy + 6) * cfg.MEASURE, cfg.MEASURE*2,
            cfg.MEASURE*2, path='resources/textures/walls/0.png')
  game.sprites.add(b17)
  game.blocks.add(b17)
  

  return spawners
  

  
