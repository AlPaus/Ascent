import pygame
import config as cfg
from animated_sprite import AnimatedSprite, Group
from player import Player
from weapon import Weapon, LyingWeapon, ExplodeBullet
from enemy import Enemy
from interface import UI
from effect import Effect
pygame.init()

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

      
class Game:
  def __init__(self):
    self.size = [cfg.WIDTH, cfg.HEIGHT]
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode(self.size)
    self.sprites = Group(self)
    self.entities = Group(self)
    self.bullets = Group(self)
    self.blocks = Group(self)
    self.weapons = Group(self)
    self.ui = UI(self)
    self.delta_time = 1
  
    self.cx, self.cy = 0, 0
    self.p = Player(self, 200, 200)
    
    b1 = Block(self, 0, 0, cfg.MEASURE, cfg.ROOM_SIZE, path='resources/textures/walls/0.png')
    b2 = Block(self, 0, 0, cfg.ROOM_SIZE, cfg.MEASURE, path='resources/textures/walls/0.png')
    
    b3 = Block(self, 0, cfg.ROOM_SIZE-cfg.MEASURE, cfg.ROOM_SIZE, cfg.MEASURE, path='resources/textures/walls/0.png')
    b4 = Block(self, cfg.ROOM_SIZE-cfg.MEASURE, 0, cfg.MEASURE, cfg.ROOM_SIZE,path='resources/textures/walls/0.png')
    
    # b2 = Block(self, 300, 300, 200,50)
    # b3 = Block(self,150,110,100,40)
    lw = LyingWeapon(self, 100,100, path = 'resources/weapons/bean_shooter')
    lw2 = LyingWeapon(self, 120,120, path = 'resources/weapons/rocket_launcher')
    # e1 = Enemy(self, 300,300,'enemy1')

    
    self.sprites.add(b1, b2, b3, b4, self.p,lw,lw2) #e1
    self.entities.add(self.p) #e1
    self.blocks.add(b1,b2,b3,b4)

  def draw(self):
    self.screen.fill((0, 100, 100))
    self.sprites.draw()
    self.weapons.draw()
    self.ui.draw()
    pygame.display.flip()  # позволяет увидеть изменения на экране

  def update(self):
    self.mkeys = pygame.mouse.get_pressed(3)
    mx, my = pygame.mouse.get_pos()
    
    px = self.p.rect.centerx
    py = self.p.rect.centery
    # set camera at center
    self.cx = self.size[0]//2 - px
    self.cy = self.size[1]//2 - py
    # adjust by mouse position
    self.cx -= 0.8 * (mx - self.size[0]//2)
    self.cy -= 0.8 * (my - self.size[1]//2)
    self.mouse_pos = (mx-self.cx, my-self.cy)

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
        G.update()
        G.draw()
      
if __name__ == '__main__':
    game_run()
