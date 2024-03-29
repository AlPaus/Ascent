import pygame
import config as cfg
from animated_sprite import AnimatedSprite

class Effect(AnimatedSprite):
  def __init__(self,game,x,y,name, damage, team):
    self.x = x
    self.y = y
    
    attr = cfg.EFFECTS_CONF[name]
    ratio = attr['ratio']
    path = attr['path']
    anim_speed = attr['anim_speed']
    super().__init__(game, x, y, path, ratio, anim_speed)
    self.anim_name = 'effect'
    self.speedx = 0
    self.speedy = 0
    self.damage = damage
    self.team = team
    self.damaged = {}
    self.damage_wearoff = attr['damage_wearoff']
    self.sound = attr['sound']
    

  def animate(self):
    if self.animation_trigger:
      if self.frame + 1 == len(self.current_anim):
        self.kill()
      else:
        self.frame += 1
      self.image = self.current_anim[self.frame]
      self.orientation = True
    
  def update(self):
    #print(self, self.frame)
    super().update()
    #input(f'{self.frame}')
    todel = []
    for en, time in self.damaged.items():
      if self.game.time - time > self.damage_wearoff:
        todel.append(en)
    for it in todel:
      del self.damaged[it]

  def move(self, dx, dy, gr):
    self.rect.move_ip(dx, dy)

class SpawnEffect(Effect):
  def __init__(self, game, xpos, ypos):
    super().__init__(game,xpos,ypos,'enemy_spawn',0,0)
    
  
    