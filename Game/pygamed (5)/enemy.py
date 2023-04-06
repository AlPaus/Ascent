import pygame
import config as cfg
from animated_sprite import AnimatedSprite
from weapon import Weapon, Bullet
import math
from typing import List
from random import randint
from effect import SpawnEffect
import random

class Money(AnimatedSprite):
  sound = pygame.mixer.Sound('resources/sounds/fx_coin.wav')
  
  def __init__(self,game,x,y, value):
    
    path = 'resources/coins'
    self.value = value
    if value < 5:
      path +='/small'
    elif value < 20:
      path += '/medium'
    else:
      path += '/big'
    super().__init__(game,x,y,path,0.03, 45)
    self.anim_name = 'spin'
  def update(self):
    self.get_money(*self.game.p.rect.center)
    self.rect.move_ip(self.speedx * self.game.delta_time / 33, self.speedy * self.game.delta_time / 33)
    super().update()
    
  def get_money(self, px, py):
    if((px-self.rect.centerx)**2+(py-self.rect.centery)**2)**0.5 < cfg.MEASURE*1.5:
      angle = math.atan2(py-self.rect.centery, px-self.rect.centerx)
      speed = 10
      self.speedx = math.cos(angle) * speed
      self.speedy = math.sin(angle) * speed
      #self.speedx = (self.rect.centerx- px)/1000*33
      #self.speedy = (self.rect.centery- py)/1000*33
    if(self.rect.colliderect(self.game.p.rect)):
      self.kill()
      self.sound.play()
      self.game.p.money += self.value
    
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
    self.max_hp = attr['hp']
    self.speed = attr['speed']
    self.reaction_time = attr['reaction_time']
    self.dist = attr['enemy_dist']
    self.angle = 0
    self.orientation = True
    self.time_of_death = 0
    self.looted = False
    self.value = attr['value']
    self.sound = attr['sound']
    if self.sound:
      self.sound = pygame.mixer.Sound(self.sound)
    self.battle_cry_rate = 200
    

  def update(self):
    if self.hp > 0:
      if self.sound and random.randint(1, self.battle_cry_rate) == 1:
        self.sound.play()
      
      self.time_of_death = self.game.time
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
      self.speedx, self.speedy = (0,0)
      if(not self.looted):
        
        m = Money(self.game,self.rect.centerx,self.rect.centery,self.value)
        self.game.sprites.add(m)
        self.looted = True
        self.weapon.kill()
      if(self.game.time - self.time_of_death >= cfg.DEAD_BODY_TIME):
        self.kill()

    # basic moving
    super().update()

    # orientation
    if self.angle <= 90 or self.angle >= 270:
        self.orientation = False 
    else:
        self.orientation = True

class Spawner:
  def __init__(self, game, x, y, w, h, enemy_list:List[List]):
    self.game = game
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.rect = pygame.Rect(x, y, w, h)
    self.active = False
    self.enemy_list = enemy_list
    self.living_enems = []
    self.spawn_kd = 1500
    self.countdown = self.game.time
    self.is_spawning = False
    self.image = pygame.Surface((w, h))
    self.image.fill('red')
    self.image.set_alpha(50)
    self.controller = None
    self.visible = True

  def set_controller(self, c):
    self.controller = c

  def update(self):
    if self.active:
      if not self.living_enems:
        if self.enemy_list:
          if not self.is_spawning:
            self.countdown = self.game.time
            self.is_spawning = True
          else:
            if self.game.time - self.countdown >= self.spawn_kd:
              
              batch = self.enemy_list.pop(0)
              
              for name in batch:
                e = Enemy(self.game, -400, -400, name)
                w, h = e.image.get_size()
                xpos = randint(self.x,self.x+self.w-w)
                ypos = randint(self.y,self.y+self.h-h)
                e.rect.topleft = (xpos, ypos)
                ef = SpawnEffect(self.game, xpos,ypos)
                self.game.sprites.add(ef)
                self.game.sprites.add(e)
                self.game.entities.add(e)
                self.living_enems.append(e)
                self.controller.enemies.append(e)
              self.is_spawning = False
        else:
          self.active = False
      else:
        for enemy in self.living_enems:
          if enemy.hp <= 0:
            self.living_enems.remove(enemy)
            self.controller.enemies.remove(enemy)
  