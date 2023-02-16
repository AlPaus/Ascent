import pygame
import config as cfg
from animated_sprite import Group
font = pygame.font.Font('resources/Minecraft.ttf', 15)

class UI(Group):
  def __init__(self, game):
    super().__init__(game)
    self.hp_bar = HealthBar(game)
    self.weapon_bars = [WeaponBar(game, i) for i in range(1, 4)]
    # self.ability_bar = AbilityBar(game)
    self.content += [self.hp_bar]
    self.content += self.weapon_bars
    
  def draw(self):
    screen = self.game.screen
    for sprite in self.content:
      screen.blit(sprite.image, sprite.rect)
      

class HealthBar:
  def __init__(self, game):
    self.game = game
    self.back = pygame.transform.scale(pygame.image.load('resources/hp_bar_back.png'), (cfg.MEASURE*3, cfg.MEASURE*0.4))
    self.front = pygame.Surface((cfg.MEASURE*2.8, cfg.MEASURE*0.35))
    self.front.fill((255, 0, 0))
    self.image = self.back.copy()
    self.image.blit(self.front, (0, 0))
    self.rect = self.image.get_rect(topleft = (10, 10))

  def update(self):
    hp = self.game.p.hp
    scale = hp/cfg.PLAYER_HP
    l = max(0, cfg.MEASURE*2.64*scale)
    self.front = pygame.Surface((l, cfg.MEASURE*0.14))
    self.front.fill((255, 0, 0))
    self.image = self.back.copy()
    self.image.blit(self.front, (10, 5.5))

class WeaponBar:
  def __init__(self, game, num):
    self.game = game
    self.player = game.p
    self.num = num
    self.image = pygame.Surface((cfg.MEASURE*2, cfg.MEASURE))
    self.rect = self.image.get_rect(topleft=(0,cfg.HEIGHT - 3.15 * cfg.MEASURE +(num-1)*(cfg.MEASURE*1.05)))
    self.image.fill((189,154,122))
    n_im = font.render(str(self.num), True, 'white')
    self.image.blit(n_im, (5, 5))
    self.reserved = self.image.copy()
    self.image.set_alpha(100)

  def update(self):
    if self.player.weapon_dict[self.num] != None:
      self.weapon_image = pygame.transform.scale(pygame.image.load(self.player.weapon_dict[self.num] + '/0.png'), (cfg.MEASURE* 1,cfg.MEASURE * 0.5))
      tmp = self.weapon_image.get_rect(center=(self.rect.width//2, self.rect.height//2))
      self.image = self.reserved.copy()
      self.image.blit(self.weapon_image, tmp)
      name = self.player.weapon_dict[self.num].split('/')[-1]
      maxammo = cfg.WEAPONS_CONF[name]['max_ammo']
      a_text = f'{self.player.ammo_left[self.num]}/{maxammo}'
      a_im = font.render(a_text, True, 'white')
      place = a_im.get_rect(bottomright = (cfg.MEASURE*2 - 5, cfg.MEASURE - 5))
      self.image.blit(a_im, place)
      
      
    if self.player.chosen_weapon == self.num:
      self.image.set_alpha(255)
    elif self.player.weapon_dict[self.num] != None:
      self.image.set_alpha(155)
    else:
      self.image.set_alpha(100)
    
      
    

class AbilityBar:
  pass