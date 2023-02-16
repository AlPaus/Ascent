import pygame
import config as cfg
import math
from animated_sprite import AnimatedSprite
from effect import Effect
from weapon import Weapon, LyingWeapon

class Shockwave:
    def __init__(self, game, team):
      self.game = game
      self.team = team
      self.size = 5
      self.image = self.make_image(self.size)
      self.rect = self.image.get_rect(center=self.game.p.rect.center)
      self.center = self.rect.center

    @staticmethod
    def make_image(size):
      img = pygame.Surface((size, size))
      pygame.draw.circle(img, 'magenta', (size//2, size//2), size//2, 5)
      img.set_colorkey('black')
      return img

    def collide(self, group):
      out = []
      for sp in group:
        d = ((self.rect.centerx - sp.rect.centerx) ** 2 + (self.rect.centery - sp.rect.centery)**2) ** 0.5
        if d <= self.size // 2 and sp.team != self.team:
          out.append(sp)
      return out
        
    def kill(self):
      self.game.sprites.remove(self)
      
    def update(self):
      if self.size < 550:
        self.size += 12
        self.image = self.make_image(self.size)
        self.rect = self.image.get_rect(center=self.center)
        [sp.kill() for sp in self.collide(self.game.bullets)]
        
      else:
        self.kill()
      

class Player(AnimatedSprite):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, path='resources/sprites/player3', ratio=cfg.PLAYER_SCALE)
        self.angle = 0
        self.weapon = None
        self.chosen_weapon = 1
        self.weapon_dict = {1:None, 2:None, 3:None}
        self.ammo_left = {1:-1, 2:-1, 3:-1}
        self.hp = cfg.PLAYER_HP
        self.last_jump = 0 #pygame.time.get_ticks()
        self.jump_dir = (0, 0)
        self.last_key = pygame.key.get_pressed()
        self.is_reloading = False
        self.reachable_weapon = None

    def recieve_damage(self, amount):
      if pygame.time.get_ticks() - self.last_damage > cfg.IMMORTALITY_TIME and not pygame.time.get_ticks() - self.last_jump < cfg.JUMP_TIME:
        if amount > 0:
          self.last_damage = pygame.time.get_ticks()
          self.hp -= amount

    def change_weapon(self, to, new=False):
      if self.weapon_dict[to] is not None and not self.is_reloading:
        self.chosen_weapon = to
        if self.weapon:
          self.weapon.kill()
        if new:
          w = Weapon(self.game, self, self.weapon_dict[to], current_ammo = -1)
        else:
          w = Weapon(self.game, self, self.weapon_dict[to], current_ammo = self.ammo_left[self.chosen_weapon])
        self.weapon = w
        self.game.sprites.add(w)
        self.ammo_left[to] = w.ammo

    def find_closest_weapon(self):
      s_lw = sorted(self.game.lying_weapons, key=lambda o: (o.rect.centerx - self.game.p.rect.centerx) ** 2 + (o.rect.centery - self.game.p.rect.centery) ** 2)
      lw = s_lw[0]
      if ((lw.rect.centerx-self.rect.centerx)*(lw.rect.centerx-self.rect.centerx) + (lw.rect.centery-self.rect.centery) * (lw.rect.centery-self.rect.centery)) ** 0.5 <= cfg.MEASURE:
        self.reachable_weapon = lw
      else:
        self.reachable_weapon = None

    def pick_up_weapon(self):
      if self.reachable_weapon:
        lw = self.reachable_weapon
        if self.weapon_dict[1] == None:
          self.weapon_dict[1] = lw.path
          self.change_weapon(1, new=True)
          self.ammo_left[1] = self.weapon.max_ammo
        elif self.weapon_dict[2] == None:
          self.weapon_dict[2] = lw.path
          self.change_weapon(2, new=True)
          self.ammo_left[2] = self.weapon.max_ammo
        elif self.weapon_dict[3] == None:
          self.weapon_dict[3] = lw.path
          self.change_weapon(3, new=True)
          self.ammo_left[3] = self.weapon.max_ammo
        else:
          path = self.weapon_dict[self.chosen_weapon]
          self.weapon_dict[self.chosen_weapon] = lw.path
          self.change_weapon(self.chosen_weapon, new=True)
          nw = LyingWeapon(self.game, self.rect.x, self.rect.y, path)
          self.game.sprites.add(nw)
          
          print(self.weapon, self.ammo_left)
        lw.kill()


    def ability(self):
      pass
      
    def update(self):
        self.find_closest_weapon()
        is_jumping = pygame.time.get_ticks() - self.last_jump < cfg.JUMP_TIME
        mkeys = self.game.mkeys # 0 - лкм, 1 - колесико, 2 - пкм
        mx, my = self.game.mouse_pos
        self.angle = self.get_angle(mx, my)
      
        self.speedx, self.speedy = 0, 0
        key = pygame.key.get_pressed()
        if self.weapon:
          self.is_reloading = self.weapon.reloading
        if False and key[pygame.K_f] and not self.last_key[pygame.K_f]:
          e = Effect(self.game, self.rect.x, self.rect.y, 'explode1', 0, self.team)
          e.anim_speed = 200
          self.game.bullets.add(e)
          self.game.sprites.add(e)

          
        if key[pygame.K_1] and not self.last_key[pygame.K_1]:
          self.change_weapon(1)
        elif key[pygame.K_2] and not self.last_key[pygame.K_2]:
          self.change_weapon(2)
        elif key[pygame.K_3] and not self.last_key[pygame.K_3]:
          self.change_weapon(3)

          
        if is_jumping:
          self.speedx, self.speedy = self.jump_dir
        else:
          if key[pygame.K_w] and key[pygame.K_d]:
            self.speedx = math.sqrt(2)/2*cfg.PLAYER_SPEED
            self.speedy = math.sqrt(2)/-2*cfg.PLAYER_SPEED 
          elif key[pygame.K_w] and key[pygame.K_a]:
            self.speedx = math.sqrt(2)/-2*cfg.PLAYER_SPEED
            self.speedy = math.sqrt(2)/-2*cfg.PLAYER_SPEED
            
          elif key[pygame.K_s] and key[pygame.K_a]:
            self.speedx = math.sqrt(2)/-2*cfg.PLAYER_SPEED
            self.speedy = math.sqrt(2)/2*cfg.PLAYER_SPEED
          elif key[pygame.K_s] and key[pygame.K_d]:
            self.speedx = math.sqrt(2)/2*cfg.PLAYER_SPEED
            self.speedy = math.sqrt(2)/2*cfg.PLAYER_SPEED
          else:
            if key[pygame.K_w]:
                self.speedy = -cfg.PLAYER_SPEED
            elif key[pygame.K_s]:
                self.speedy = cfg.PLAYER_SPEED
            if key[pygame.K_a]:
                self.speedx = -cfg.PLAYER_SPEED
            elif key[pygame.K_d]:
                self.speedx = cfg.PLAYER_SPEED
          if key[pygame.K_SPACE] and not is_jumping and pygame.time.get_ticks() - self.last_jump > cfg.JUMP_CD:
            self.last_jump = pygame.time.get_ticks()
            is_jumping = True
            self.jump_dir = (self.speedx*cfg.JUMP_SPEED, self.speedy*cfg.JUMP_SPEED)
          if key[pygame.K_e] and not self.last_key[pygame.K_e]:
            self.pick_up_weapon()
          if key[pygame.K_f]:
            s = Shockwave(self.game, self.team)
            self.game.sprites.add(s)
        if mkeys[0]:
          if self.weapon:
            self.weapon.shoot()
            self.ammo_left[self.chosen_weapon] = self.weapon.ammo

        if self.hp > 0:
          if is_jumping:
              if 'jump' in self.anims:
                if self.anim_name != 'jump':
                  self.animation_trigger = True
                self.anim_name = 'jump'
          elif self.speedx == 0 and self.speedy == 0:
              if self.anim_name != 'idle':
                self.animation_trigger = True
              self.anim_name = 'idle'
          else:
              if self.anim_name != 'walk':
                self.animation_trigger = True
              self.anim_name = 'walk'
        else:
          if self.anim_name != 'dead':
            self.animation_trigger = True
          self.anim_name = 'dead'
          
        super().update()
        self.last_key = key
        if self.angle <= 90 or self.angle >= 270:
          self.orientation = False
        else:
          self.orientation = True 

