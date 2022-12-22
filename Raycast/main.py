import pygame, sys
from pygame.locals import QUIT
import math
from geometry import Light, move_along_vector

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('raycasting test!')
clock = pygame.time.Clock()
font = pygame.font.SysFont('None', 14)

lights_count = 1
obstacle_edges = 4
obstacle_edge_size = 75
draw = pygame.draw
draw_line = draw.line
draw_circle = draw.circle
draw_polygon = draw.polygon
BLACK = (0, 0, 0)
DARK = (155, 155, 155)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def new_obstacle(i, j: float):
    """Produce obstacle (polygon) of any size and number of vertices."""
    obstacle = []
    size = obstacle_edge_size
    edges = obstacle_edges
    for k in range(edges):
        angle = (k - 1) * (360 // edges)
        offset = 180 // edges
        point = move_along_vector((i, j), size, angle=angle - offset)
        obstacle.append(point)
    return obstacle

def create_obstacles():
  obstacles
  size = obstacle_edge_size
  for i in range(size * 2, 400, size * 3):
      for j in range(size * 2, 300, size * 3):
          obstacle = new_obstacle(i, j)
          obstacles.append(obstacle)
  return obstacles

def get_light_position(i, x, y):
  if not i:
      point = (x, y)
  else:
      angle = i * (360 // lights_count)
      point = move_along_vector((x, y), 10, angle=angle)
  return point
  
def update_lights(lights):
  for light in lights:
      light.update_visible_polygon()
          
def create_lights(obstacle):
  lights = []
  x, y = 400 // 2, 300 // 2
  for i in range(lights_count):
      color = (192, 192, 192)
      point = get_light_position(i, x, y)
      # noinspection PyTypeChecker
      light = Light(*point, color, obstacles)
      lights.append(light)
  return lights
  


def draw_obstacles(obstacles):
  for obstacle in obstacles:
    pygame.draw.polygon(screen, BLACK, obstacle)
    #print('drawing', obstacle)

def draw_light(lights):
    for light in lights:
        polygon = light.light_polygon
        if len(polygon) > 2:
            draw_polygon(screen, light.color, polygon)
        x, y = light.origin
        draw_circle(screen, RED, (int(x), int(y)), 5)


def redraw_screen(lights, obstacles):
  screen.fill(DARK)
  draw_obstacles(obstacles)
  draw_light(lights)
  pygame.display.update()

def on_motion(x, y, lights):
    lights[0].move_to(x, y)

      
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
      super().__init__()
      self.image = pygame.Surface((w, h))
      self.image.fill((255, 255, 0))
      self.rect = self.image.get_rect(topleft=(x, y))
      self.obstacle = []
      size = (self.rect.width**2+self.rect.height**2)**0.5/2
      alpha = math.degrees(math.atan(self.rect.width/self.rect.height))
      beta = 90 - alpha
      angles = [-1* (alpha + beta*2), -alpha, alpha, alpha + beta*2]
      for angle in angles:
        point = move_along_vector((x+w//2, y+h//2), size, angle=angle)
        self.obstacle.append(point)
     
sprites = pygame.sprite.Group()

b1 = Block(200,100,100,50)
b2 = Block(50,100,50,50)
# b3 = Block(100,50,30,80)
sprites.add(b1,b2)
obstacles = []
px, py = 50, 50
for b in (b1, b2):
  obstacles.append(b.obstacle)
lights = create_lights(obstacles)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
      py -= 5
    elif key[pygame.K_s]:
      py += 5
    if key[pygame.K_a]:
      px -= 5
    elif key[pygame.K_d]:
      px +=  5
    on_motion(px, py, lights)
    print(px,py)
  
    update_lights(lights)
    redraw_screen(lights,obstacles)
    sprites.draw(screen)
    for sprite in sprites:
      pygame.draw.rect(screen, (255, 0, 0), sprite.rect, 2)
    #pygame.display.flip()
    
    clock.tick(15)

