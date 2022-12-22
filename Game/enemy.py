import pygame
import config as cfg
from animated_sprite import AnimatedSprite
from weapon import Weapon, Bullet
import math

class Enemy(AnimatedSprite):
  def __init__(self, game, x, y, name, team=1):
    attr = cfg.ENEMIES_CONF[name]
    ratio = attr['ratio']
    path = attr['path']
    super().__init__(game, x, y, path, ratio)
    self.team = team
    self.weapon = Weapon(self.game, self, cfg.WEAPONS_CONF[attr['weapon']]['path'], team=self.team)
    self.game.weapons.add(self.weapon)
    self.game.sprites.add(self.weapon)
    self.hp = attr['hp']
    self.speed = attr['speed']
    self.reaction_time = attr['reaction_time']
    self.dist = attr['enemy_dist']
    self.angle = 0
    self.orientation = True

  def update(self):
    if self.hp > 0:
      p_x, p_y = self.game.p.rect.center
      self.angle = self.weapon.get_angle(p_x, p_y)
      # pygame.draw.line(self.game.screen, (255, 0, 0), self.weapon.rect.move(self.game.cx, self.game.cy).center, self.game.p.rect.move(self.game.cx, self.game.cy).center)
      # pygame.display.flip()
      range = math.sqrt((p_x-self.rect.centerx)**2+(p_y-self.rect.centery)**2)
      if range > self.dist:
        self.speedx = self.speed * math.cos(math.radians(self.angle)) * -1
        self.speedy = self.speed * math.sin(math.radians(self.angle))
      else:
        self.speedx = 0
        self.speedy = 0
      self.weapon.shoot()
    
    # choosing animation
    if self.hp > 0:
      if self.speedx == 0 and self.speedy == 0:
        self.anim_name = 'idle'
      else:
        self.anim_name = 'walk'
    else:
      self.anim_name = 'dead'

    # basic moving
    super().update()

    # orientation
    if self.orientation and (self.angle <= 90 or self.angle >= 270):
      self.image = pygame.transform.flip(self.image, True, False)
      self.orientation = False
    elif not self.orientation and (90 > self.angle > 270):
      self.image = pygame.transform.flip(self.image, True, False)
      self.orientation = True
    