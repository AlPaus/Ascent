import pygame
import config as cfg
from raycasting import RayCasting
pygame.init()
pygame.mixer.init()
from animated_sprite import Group, MasterGroup
from player import Player
from weapon import LyingWeapon, ExplodeBullet
from interface import UI
from effect import Effect
import math
from graph import create_level
import pygame_menu
from room import create_room

menu_name = 'main' # main game settings
# SDICT = cfg.S_DICT

def reverse_visible(ar):
  visible = ar == 0
  ar[visible] = 155
  visible = ~visible
  ar[visible] = 0


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)
  
    
class Game:

  def remake_screen(self):
    self.size = [cfg.WIDTH, cfg.HEIGHT]
    if cfg.FULLSCREEN:
      self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
    else:
      self.screen = pygame.display.set_mode(self.size)
    
    self.shiftx = cfg.WIDTH * 0.9 #430
    self.shifty = cfg.HEIGHT * 0.9 #240      
    self.menu = pygame_menu.Menu('THE GAME', cfg.WIDTH, cfg.HEIGHT)
    self.menu.add.button('New game', self.to_game)
    self.menu.add.button('Settings',self.to_options)
    self.menu.add.button('Quit', pygame.quit)

    self.option_menu = pygame_menu.Menu('Settings', cfg.WIDTH, cfg.HEIGHT)
    self.option_menu.add.button('Back', self.to_menu_save_settings)
    resolutions = [('480x270', (480, 270)), ('1440x810', (1440, 810)), ('1600x900', (1600, 900)), ('1920x1080', (1920, 1080))]
    fps_list = [('30',30),('45',45),('60',60)]
    self.option_menu.add.selector('Res:', resolutions, onchange=self.change_res)
    self.option_menu.add.selector('FPS:', fps_list, onchange=self.change_fps)
    self.option_menu.add.button('Draw lights:' + '+'*int(self.new_lights) + '-'*(1-int(self.new_lights)), self.toggle_light)
    self.option_menu.add.button('Forward:' + str(cfg.BUTTONS['forward']), lambda: self.get_new_button('forward'))
      
  def __init__(self):
    self.clock = pygame.time.Clock()
    self.time = 0
    self.new_lights = True
    self.debug_mode = False
    self.remake_screen()
    self.tmp = []
    self.new_raycast = RayCasting(self)
    self.wallmap = []
    self.sprites = MasterGroup(self)
    self.entities = Group(self)
    self.bullets = Group(self)
    self.blocks = Group(self)
    self.weapons = Group(self)
    self.delta_time = 1
    self.obstacles = []
    self.lying_weapons = Group(self)
    self.door_group = []
    self.cx, self.cy = 0, 0
    self.p = Player(self, 1.3*cfg.MEASURE, 3.3*cfg.MEASURE)
    self.ui = UI(self)
    pygame.mixer.music.load('resources/music/bgm_defence.wav')
    #pygame.mixer.music.play()
    
    doors = create_level(3)
    self.door_group.extend(create_room(self, 0, 0, doors=doors[0]))
    self.door_group.extend(create_room(self, cfg.ROOM_SIZE+2, 0, doors = doors[1]))
    self.door_group.extend(create_room(self, 0, cfg.ROOM_SIZE+2, doors = doors[3]))
    self.door_group.extend(create_room(self, cfg.ROOM_SIZE+2, cfg.ROOM_SIZE+2, doors=doors[4]))
    
    lw = LyingWeapon(self, 2.75*cfg.MEASURE,2.75*cfg.MEASURE, path = 'resources/weapons/bean_shooter')
    lw2 = LyingWeapon(self, 2.95*cfg.MEASURE,2.95*cfg.MEASURE, path = 'resources/weapons/rocket_launcher')
    lw3 = LyingWeapon(self, 3.15*cfg.MEASURE,3.75*cfg.MEASURE, path = 'resources/weapons/bean_shooter')
    lw4 = LyingWeapon(self, 4*cfg.MEASURE,5*cfg.MEASURE, path = 'resources/weapons/rocket_launcher')
    #e1 = Enemy(self, 2.75*cfg.MEASURE,2.75*cfg.MEASURE,'enemy1')
    
    
    self.sprites.add(self.p,lw,lw2,lw3,lw4 ) 
    self.entities.add(self.p) #, e1)

  def close_doors(self):
    print('closed doors')
    for door in self.door_group:
      door.close()

  def open_doors(self):
    print('opened doors')
    for door in self.door_group:
      door.open()

  def get_new_button(self, action: str):
    print('Press new button...')
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < 10000:
      events = pygame.event.get()
      for event in events:
          if event.type == pygame.QUIT:
              print('aborted')
              return None
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_ESCAPE:
                print('aborted')
                return None
              else:
                cfg.BUTTONS[action] = event.key
                print('new key is set to', event.key)
                return None
    print('aborted (t)')
                

  def change_fps(self,_ ,val2):
    cfg.FPS = val2
    cfg.S_DICT['FPS'] = val2

  def toggle_light(self):
    self.new_lights = not self.new_lights
    self.remake_screen()
    
  def change_res(self, _, val2):
    cfg.WIDTH, cfg.HEIGHT = val2
    cfg.S_DICT['WIDTH'], cfg.S_DICT['HEIGHT'] = val2
    self.remake_screen()

  def to_game(self):
    global menu_name
    menu_name = 'game'

  def to_menu(self):
    global menu_name
    menu_name = 'main'

  def to_menu_save_settings(self):
    cfg.dump_settings(cfg.S_DICT)
    global menu_name
    menu_name = 'main'

  def to_options(self):
    global menu_name
    menu_name = 'settings'


  def draw(self):
    self.screen.fill((0, 100, 100))
    self.sprites.draw()
    #self.weapons.draw()
    
    if self.new_lights:
      self.new_raycast.draw()
      
    self.ui.draw()
    
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
    # collisions
    hits = self.entities.collide(self.bullets)
    for reciever, bullets in hits.items():
      for bullet in bullets:
        if bullet.team != reciever.team and reciever.hp > 0:
          if type(bullet) == ExplodeBullet:
            bullet.explode()
            reciever.recieve_damage(bullet.damage)
          elif type(bullet) != Effect:
            reciever.recieve_damage(bullet.damage)
            bullet.kill()
          elif type(bullet) == Effect:
            if not reciever in bullet.damaged:
              reciever.recieve_damage(bullet.damage)
              bullet.damaged[reciever] = self.time
    self.new_raycast.update()
    self.sprites.update()
    #self.weapons.update()
    self.ui.update()
    self.delta_time = self.clock.tick(cfg.FPS)
    self.time += self.delta_time
    #print(self.delta_time)

  def mainloop(self):
    global menu_name
    run = True
    while run:
        events = pygame.event.get()
        if menu_name == 'game':
          for event in events:
              if event.type == pygame.QUIT:
                  menu_name = 'main'
              if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_v:
                    self.debug_mode = not self.debug_mode
                  if event.key == pygame.K_ESCAPE:
                    menu_name = 'main'
          self.update()
          self.draw()
        elif menu_name == 'main':
          self.menu.update(events)
          self.menu.draw(self.screen)
        elif menu_name == 'settings':
          self.option_menu.update(events)
          self.option_menu.draw(self.screen)
        pygame.display.flip()

  
def game_run():
    G = Game()
    G.mainloop()
    
      
if __name__ == '__main__':
    game_run()
