import pygame
import config as cfg
import os
import math

def rotate_shift(image, angle, pos, shift):
  #print(angle, pos, shift)
  ch_x, ch_y = shift
  image = pygame.transform.rotate(image, angle)
  rect = image.get_rect(center=pos)
  rect.centerx += math.sin(math.radians(angle)) * ch_y + math.cos(math.radians(angle)) * ch_x
  rect.centery += math.cos(math.radians(angle)) * ch_y - math.sin(math.radians(angle)) * ch_x
  #print(image, rect)
  return image, rect
  
class AnimatedSprite:
  def __init__(self, game, x, y, path='resources/sprites/player', ratio=cfg.PLAYER_SCALE, anim_speed = cfg.ANIM_SPEED):
    self.game = game
    self.image = pygame.image.load(path+'/0.png').convert_alpha()
    self.desired_size = (cfg.WIDTH*ratio, cfg.WIDTH*ratio/self.image.get_rect().width*self.image.get_rect().height)
    self.image = pygame.transform.scale(self.image, self.desired_size)
    self.rect = self.image.get_rect(topleft = (x, y))
    self.anims = self.get_anims(path) # получить все анимации из папки
    self.anim_name = list(self.anims.keys())[0]
    self.current_anim = self.anims[self.anim_name]
    self.animation_time_last = pygame.time.get_ticks()
    self.animation_trigger = False
    self.speedx = 0
    self.speedy = 0
    self.frame = 0
    self.orientation = True
    self.team = 0
    self.last_damage = 0
    self.anim_speed = anim_speed
    self.angle = 0
    
  def recieve_damage(self, amount):
    self.hp -= amount
    
  def kill(self):
    self.game.sprites.remove(self)
    self.game.entities.remove(self)
    self.game.bullets.remove(self)
    del self
    
  def get_anims(self, path):
    d = {}
    files = os.listdir(path)
    for file in files:
      if os.path.isdir(path+'/'+file):
        d[file] = self.get_anim_from_dir(path+'/'+file)
    return d

  def get_anim_from_dir(self, path):
    anim = []
    files = os.listdir(path)
    for file in files:
      if os.path.isfile(path+'/'+file):
        i = pygame.image.load(path+'/'+file).convert_alpha()
        i = pygame.transform.scale(i, self.desired_size)
        anim.append(i)
    return anim

  
  def update(self):
    self.check_anim_time()
    self.animate()
    self.move(self.speedx*self.game.delta_time/33, self.speedy*self.game.delta_time/33, self.game.blocks)

  def check_anim_time(self):
    self.animation_trigger = False
    time_now = pygame.time.get_ticks()
    if time_now - self.animation_time_last > self.anim_speed:
      self.animation_time_last = time_now
      self.animation_trigger = True
    
  def animate(self):
    if self.animation_trigger:
      #self.current_anim.rotate(-1) #deque
      #self.image = self.current_anim[0]
      if self.frame + 1 == len(self.current_anim):
        self.frame = 0
        self.current_anim = self.anims[self.anim_name]
      else:
        self.frame += 1
      self.image = self.current_anim[self.frame]
      #self.orientation = True
      

  def check_collision(self, dx, dy, group):
    self.rect.move_ip((dx, dy))
    hits = group.spritecollide(self) #pygame.sprite.spritecollide(self, group, False)
    self.rect.move_ip((-dx, -dy))
    return hits

  def move(self, sx, sy, group):
    while self.check_collision(0, sy, group):
        if sy >= 0:
            sy -= 1
        else:
            sy += 1

    while self.check_collision(sx, sy, group):
        if sx >= 0:
            sx -= 1
        else:
            sx += 1

    self.rect.move_ip(sx, sy)
    
  def get_angle(self, x2, y2):
    x1, y1 = self.rect.center
    angle = (math.atan2(y2-y1, x2-x1) - math.pi*2) * -1
    return (angle * 180 / math.pi) - 180

d = {
  'Block': 0,
  'Enemy': 10,
  'Player': 15,
  'Weapon': 20,
  'LyingWeapon': 25,
  'Bullet': 30,
  'ExplodeBullet':35,
  'Shockwave':50,
  'Effect': 40  
}
class Group:
  def __init__(self, game, *items):
    self.game = game
    self.content = [*items]

  def __iter__(self):
    #for el in self.content:
    #  yield el
    return self.content.__iter__()

  def add(self, *items):
    self.content += items

  def update(self):
    for sp in self.content:
      sp.update()
    #print([x.__class__.__name__ for x in self.content])

  def spritecollide(self, sprite):
    # должен вернуть все спрайты из группы, с которыми столкнулся sprite
    hits = []
    for sp in self.content:
      if sprite.rect.colliderect(sp.rect):
        hits.append(sp)

    return hits
  
  def remove(self, other):
    if other in self.content:
      self.content.remove(other)

  def collide(self, other):
    hits = {}
    for sprite in self.content:
      for sp2 in other.content:
        if sprite.rect.colliderect(sp2.rect):
          if sprite not in hits:
            hits[sprite] = []
          hits[sprite] += [sp2]
    return hits
      

class MasterGroup(Group):
  def __init__(self, game, *items):
    super().__init__(game, *items)

  def update(self):
    self.content = sorted(self.content, key=lambda s: d[type(s).__name__])
    super().update()

  def draw(self):
    screen = self.game.screen
    cx = self.game.cx
    cy = self.game.cy
    for sprite in self.content:
      if type(sprite).__name__ in ['Weapon', 'Bullet', 'ExplodeBullet']:
        shift = list(sprite.shift)
        image = sprite.image
        if not sprite.orientation:
          image = pygame.transform.flip(image, False, True)
          shift[1] *= -1
        rect = sprite.rect
        image, rect = rotate_shift(image, sprite.angle, sprite.rect.center, shift)
        screen.blit(image, rect.move(cx, cy))
        #screen.blit(pygame.transform.rotozoom(sprite.image, sprite.angle, 1), sprite.rect.move(cx, cy))
        if type(sprite).__name__ == 'Weapon':
          if sprite.reloading:
            time = (pygame.time.get_ticks() - sprite.reload_start) / sprite.reload
            tmp = sprite.rect.move(cx, cy+cfg.HEIGHT/35)
            tmp.width *= (1-time)
            tmp.height = cfg.HEIGHT/60
            pygame.draw.rect(screen, (0, 255, 0), tmp)
      elif type(sprite).__name__ == 'LyingWeapon':
        
        screen.blit(sprite.image, sprite.rect.move(cx, cy))
        if sprite == self.game.p.reachable_weapon:
          ol = sprite.outline.copy()
          n = 0
          for point in ol:
            ol[n] = (point[0] + sprite.rect.x + cx, point[1] + sprite.rect.y + cy)
            n += 1
          pygame.draw.polygon(screen, 'white', ol, 1)
          
      elif type(sprite).__name__ == "Player":
        im = sprite.image.copy()
        if pygame.time.get_ticks() - sprite.last_damage <= cfg.IMMORTALITY_TIME:
          im.set_alpha(150)
        if not sprite.orientation:
          im = pygame.transform.flip(im, True, False)
        screen.blit(im, sprite.rect.move(cx, cy))
      #   pygame.draw.rect(screen, (255, 0, 0, 155), sprite.rect.move(cx, cy))
      elif type(sprite).__name__ == "Enemy":
        hp = sprite.hp / sprite.max_hp 
        tmp = sprite.rect.move(cx, cy)
        tmp.width *= hp
        tmp.height = cfg.HEIGHT/60
        #print(tmp.width, tmp.height)
        screen.blit(sprite.image, sprite.rect.move(cx, cy))
        pygame.draw.rect(screen, 'red', tmp)
      else:
        screen.blit(sprite.image, sprite.rect.move(cx, cy))
  