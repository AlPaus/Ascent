import pygame
import config as cfg
import math
from animated_sprite import AnimatedSprite
from effect import Effect

class Player(AnimatedSprite):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, path='resources/sprites/player3', ratio=cfg.PLAYER_SCALE)
        self.angle = 0
        self.weapon = None
        self.weapon_list = []
        self.hp = cfg.PLAYER_HP
        self.last_jump = 0 #pygame.time.get_ticks()
        self.jump_dir = (0, 0)
        self.last_key = pygame.key.get_pressed()

    def recieve_damage(self, amount):
      if pygame.time.get_ticks() - self.last_damage > cfg.IMMORTALITY_TIME and not pygame.time.get_ticks() - self.last_jump < cfg.JUMP_TIME:
        if amount > 0:
          self.last_damage = pygame.time.get_ticks()
          self.hp -= amount
        
    def update(self):
        is_jumping = pygame.time.get_ticks() - self.last_jump < cfg.JUMP_TIME
        mkeys = self.game.mkeys # 0 - лкм, 1 - колесико, 2 - пкм
        mx, my = self.game.mouse_pos
        self.angle = self.get_angle(mx, my)
        
        self.speedx, self.speedy = 0, 0
        key = pygame.key.get_pressed()
        if key[pygame.K_f] and not self.last_key[pygame.K_f]:
          e = Effect(self.game, self.rect.x, self.rect.y, 'explode1', 0, self.team)
          e.anim_speed = 200
          self.game.bullets.add(e)
          self.game.sprites.add(e)
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
          if key[pygame.K_SPACE] and not is_jumping:
            self.last_jump = pygame.time.get_ticks()
            is_jumping = True
            self.jump_dir = (self.speedx*cfg.JUMP_SPEED, self.speedy*cfg.JUMP_SPEED)
          
        if mkeys[0]:
          if self.weapon:
            self.weapon.shoot()

        if self.hp > 0:
          if is_jumping:
              if 'jump' in self.anims:
                if self.anim_name != 'jump':
                  self.animation_trigger = True
                self.anim_name = 'jump'
              else:
                print("i don't have jumping animation")
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
        
        if self.orientation and (self.angle <= 90 or self.angle >= 270):
          self.image = pygame.transform.flip(self.image, True, False)
          self.orientation = False
        elif not self.orientation and (90 > self.angle > 270):
          self.image = pygame.transform.flip(self.image, True, False)
          self.orientation = True 
        