import pygame
import config as cfg
from animated_sprite import Group

class UI(Group):
  def __init__(self, game):
    super().__init__(game)
    self.hp_bar = HealthBar(game)
    # self.weapon_bar = WeaponBar(game)
    # self.ability_bar = AbilityBar(game)
    self.content += [self.hp_bar]
    
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
  pass

class AbilityBar:
  pass