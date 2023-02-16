import pygame
import config as cfg

pygame.init()
from animated_sprite import Group, MasterGroup
from player import Player
from weapon import Weapon, LyingWeapon, ExplodeBullet
from enemy import Enemy
from interface import UI
from effect import Effect
import math
from geometry import Light, move_along_vector
import numpy as np
from graph import create_level


def reverse_visible(ar):
  visible = ar == 0
  ar[visible] = 155
  visible = ~visible
  ar[visible] = 0

def get_light_position(i, x, y):
  if not i:
      point = (x, y)
  else:
      angle = i * (360 // 1)
      point = move_along_vector((x, y), 10, angle=angle)
  return point
          
def create_lights(x, y, color):
  point = get_light_position(0, x, y)
  # noinspection PyTypeChecker
  light = Light(*point, color, ())
  return light

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)
  
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, a, b, path=None, color=(0, 120, 60)):
        self.game = game
        super().__init__()
        self.image = pygame.Surface((a, b))
        if not path:
          self.image.fill(color)
        else:
          image = pygame.image.load(path)
          image = pygame.transform.scale(image, (cfg.MEASURE, cfg.MEASURE))
          for i in range(0, a, cfg.MEASURE):
            for j in range(0, b, cfg.MEASURE):
              self.image.blit(image, (i, j))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.obstacle = []
        size = (self.rect.width**2+self.rect.height**2)**0.5/2
        alpha = math.degrees(math.atan(self.rect.width/self.rect.height))
        beta = 90 - alpha
        angles = [-1* (alpha + beta*2), -alpha, alpha, alpha + beta*2]
        for angle in angles:
          point = move_along_vector((x+a//2, y+b//2), size, angle=angle)
          self.obstacle.append(point)

      
class Game:
  def __init__(self):
    self.size = [cfg.WIDTH, cfg.HEIGHT]
    self.clock = pygame.time.Clock()
    
    self.screen = pygame.display.set_mode(self.size)
    self.draw_lights = True
    self.debug_mode = False
    #if self.debug_mode:
    self.shiftx = 430
    self.shifty = 240
    self.tmp = []
      #self.screen = pygame.display.set_mode((self.size[0]*1.8, self.size[1]*2.8))
      
    
    self.sprites = MasterGroup(self)
    self.entities = Group(self)
    self.bullets = Group(self)
    self.blocks = Group(self)
    self.weapons = Group(self)
    self.delta_time = 1
    self.obstacles = []
    self.lying_weapons = Group(self)
  
    self.cx, self.cy = 0, 0
    self.p = Player(self, 200, 200)
    self.ui = UI(self)
    self.light = create_lights(1, 1, 'red')
    if self.draw_lights:
      self.light = create_lights(cfg.WIDTH*1.8//2, cfg.HEIGHT*1.8//2, (50, 50, 50, 200))
    doors = create_level(3)
    self.create_room(0, 0, doors=doors[0])
    self.create_room(14, 0, doors = doors[1])
    self.create_room(0, 14, doors = doors[3])
    self.create_room(14, 14, doors=doors[4])

    
    # b2 = Block(self, 300, 300, 200,50)
    # b3 = Block(self,150,110,100,40)
    lw = LyingWeapon(self, 100,100, path = 'resources/weapons/bean_shooter')
    lw2 = LyingWeapon(self, 120,120, path = 'resources/weapons/rocket_launcher')
    lw3 = LyingWeapon(self, 130,100, path = 'resources/weapons/bean_shooter')
    lw4 = LyingWeapon(self, 140,120, path = 'resources/weapons/rocket_launcher')
    e1 = Enemy(self, 100,100,'enemy1')

    
    self.sprites.add(self.p,lw,lw2,lw3,lw4, e1) 
    self.entities.add(self.p, e1) #, e1)

  def create_room(self, posx, posy, doors):
    #doors = ['up','left','down','right']
    #obstacles = []
    l = ((cfg.ROOM_SIZE // cfg.MEASURE) // 2 - 1) * cfg.MEASURE

    if 'up' in doors:
      b1 = Block(self, posx*cfg.MEASURE, posy*cfg.MEASURE, l, cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)

      d = Block(self, (posx + 4) * cfg.MEASURE, (posy-2) * cfg.MEASURE, cfg.MEASURE, 2*cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(d)
      self.blocks.add(d)
      self.obstacles.append(d.obstacle)

      b1 = Block(self, (posx + 2) * cfg.MEASURE + l, posy*cfg.MEASURE, l, cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)
    else:
      b1 = Block(self, posx*cfg.MEASURE, posy*cfg.MEASURE, cfg.ROOM_SIZE, cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)
      
    if 'left' in doors:
      b1 = Block(self, posx*cfg.MEASURE, posy*cfg.MEASURE, cfg.MEASURE, l, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)

      d = Block(self, (posx - 2) * cfg.MEASURE, (posy + 7) * cfg.MEASURE, 2*cfg.MEASURE, cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(d)
      self.blocks.add(d)
      self.obstacles.append(d.obstacle)

      b1 = Block(self, posx*cfg.MEASURE, (posy + 2) * cfg.MEASURE + l, cfg.MEASURE, l-cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)
    else:
      b1 = Block(self, posx*cfg.MEASURE, cfg.MEASURE + posy*cfg.MEASURE, cfg.MEASURE, cfg.ROOM_SIZE - 2 * cfg.MEASURE, path='resources/textures/walls/0.png')
    self.sprites.add(b1)
    self.blocks.add(b1)
    self.obstacles.append(b1.obstacle)

    if 'down' in doors:
      b1 = Block(self, posx*cfg.MEASURE, (posy-1)*cfg.MEASURE+cfg.ROOM_SIZE, l, cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)
      

      b1 = Block(self, (posx + 2) * cfg.MEASURE + l, (posy-1)*cfg.MEASURE+cfg.ROOM_SIZE, l, cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)

      d = Block(self, (posx + 7) * cfg.MEASURE, posy*cfg.MEASURE+cfg.ROOM_SIZE, cfg.MEASURE, 2*cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(d)
      self.blocks.add(d)
      self.obstacles.append(d.obstacle)
    else:
      b1 = Block(self, posx*cfg.MEASURE , (posy-1)*cfg.MEASURE + cfg.ROOM_SIZE, cfg.ROOM_SIZE, cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)
    
    if 'right' in doors:
      b1 = Block(self, (posx-1)*cfg.MEASURE+cfg.ROOM_SIZE, (posy+1)*cfg.MEASURE, cfg.MEASURE, l-cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)

      d = Block(self, (posx) * cfg.MEASURE+cfg.ROOM_SIZE, (posy + 4) * cfg.MEASURE, 2*cfg.MEASURE, cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(d)
      self.blocks.add(d)
      self.obstacles.append(d.obstacle)

      b1 = Block(self, (posx-1)*cfg.MEASURE + cfg.ROOM_SIZE, (posy + 2) * cfg.MEASURE + l, cfg.MEASURE, l-cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)

      
      
    else:  
      b1 = Block(self, cfg.ROOM_SIZE + (posx-1)*cfg.MEASURE,  cfg.MEASURE + posy*cfg.MEASURE, cfg.MEASURE,cfg.ROOM_SIZE - 1 *cfg.MEASURE, path='resources/textures/walls/0.png')
      self.sprites.add(b1)
      self.blocks.add(b1)
      self.obstacles.append(b1.obstacle)
    self.light.add_obstacles(self.obstacles)

    

  def draw(self):
    self.screen.fill((0, 100, 100))
    self.sprites.draw()
    #self.weapons.draw()
    if self.draw_lights:
      shadow = pygame.Surface((cfg.WIDTH*3, cfg.HEIGHT*5), pygame.SRCALPHA, 32).convert_alpha()
      polygon = self.light.light_polygon
      pygame.draw.polygon(shadow, (0, 0, 0), polygon)
      ar = pygame.surfarray.pixels_alpha(shadow)
  
      reverse_visible(ar)
      del ar
      shadow.unlock()
      mx, my = self.mouse
      self.screen.blit(shadow, (-0.8*mx,-0.8*my))
    self.ui.draw()
    
    if self.debug_mode:
      self.screen.fill('gray')
      pygame.draw.circle(self.screen, 'red', self.light.origin, 5)
      for obstacle in self.tmp:
        pygame.draw.polygon(self.screen, 'black', obstacle, 2)
    
    if False:
      for sprite in self.sprites.content:
        pygame.draw.rect(self.screen, 'red', sprite.rect.move(self.cx, self.cy), 2)
    
    pygame.display.flip()  # позволяет увидеть изменения на экране

  def update(self):
    self.mkeys = pygame.mouse.get_pressed(3)
    mx, my = pygame.mouse.get_pos()
    self.mouse = (mx, my)
    
    px = self.p.rect.centerx
    py = self.p.rect.centery
    # set camera at center
    self.cx = self.size[0]//2 - px
    self.cy = self.size[1]//2 - py
    # adjust by mouse position
    self.cx -= 0.8 * (mx - self.size[0]//2)
    self.cy -= 0.8 * (my - self.size[1]//2)

    self.mouse_pos = (mx-self.cx, my-self.cy)
    if self.draw_lights:
      tmp = []
      for obstacle in self.obstacles:
        tmp.append([])
        for i in obstacle:
          a = i[0] - px + self.shiftx
          b = i[1] - py + self.shifty
          tmp[-1].append((a, b))
      #print(self.shiftx, self.shifty)
      self.tmp = tmp
      #self.light.move_to(px, py)
      self.light.new_obstacles(tmp)
      self.light.update_visible_polygon()
    # collisions
    hits = self.entities.collide(self.bullets)
    for reciever, bullets in hits.items():
      for bullet in bullets:
        if bullet.team != reciever.team:
          reciever.recieve_damage(bullet.damage)
          if type(bullet) == ExplodeBullet:
            bullet.explode()
          if type(bullet) != Effect:
            bullet.kill()
          
    
    self.sprites.update()
    #self.weapons.update()
    self.ui.update()
    self.delta_time = self.clock.tick(cfg.FPS)
    #print(self.delta_time)

  
    
def game_run():
    G = Game()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                  G.debug_mode = not G.debug_mode
                '''
                if event.key == pygame.K_UP:
                  G.shifty -= 10
                if event.key == pygame.K_DOWN:
                  G.shifty += 10
                if event.key == pygame.K_LEFT:
                  G.shiftx -= 10
                if event.key == pygame.K_RIGHT:
                  G.shiftx += 10'''
        G.update()
        G.draw()
      
if __name__ == '__main__':
    game_run()
