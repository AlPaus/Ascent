import pygame
import math
import config as cfg


def reverse_visible(ar):
  visible = ar == 0
  ar[visible] = 155
  visible = ~visible
  ar[visible] = 0
  
class RayCasting:
  def __init__(self, game):
    self.game = game
    self.polygon = []
    self.delta_angle = 2*math.pi / cfg.S_DICT['NUM_RAYS']
    self.poly = []
    
  def update(self):
    self.polygon = []
    
    px, py = self.game.p.rect.center
    ox, oy = px/cfg.MEASURE, py/cfg.MEASURE
    x_map, y_map = px//cfg.MEASURE, py//cfg.MEASURE

    ray_angle = 0 - math.pi + 0.0001
    for ray in range(cfg.S_DICT['NUM_RAYS']):
      sin_a = math.sin(ray_angle)
      cos_a = math.cos(ray_angle)

      # hor
      y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
      depth_hor = (y_hor - oy) / sin_a
      x_hor = ox + depth_hor * cos_a

      delta_depth = dy / sin_a
      dx = delta_depth * cos_a

      for i in range(cfg.S_DICT['MAX_DEPTH']):
          tile_hor = int(x_hor), int(y_hor)
          if tile_hor in self.game.wallmap:
              break
          x_hor += dx
          y_hor += dy
          depth_hor += delta_depth

      # vert
      x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
      depth_vert = (x_vert - ox) / cos_a
      y_vert = oy + depth_vert * sin_a

      delta_depth = dx / cos_a
      dy = delta_depth * sin_a

      for i in range(cfg.S_DICT['MAX_DEPTH']):
          tile_vert = int(x_vert), int(y_vert)
          if tile_vert in self.game.wallmap:
              break
          x_vert += dx
          y_vert += dy
          depth_vert += delta_depth

      # depth
      if depth_vert < depth_hor:
          depth = depth_vert
      else:
          depth = depth_hor

      self.polygon.append([cfg.MEASURE * ox + cfg.MEASURE * depth * cos_a,
                          cfg.MEASURE * oy + cfg.MEASURE * depth * sin_a])

      ray_angle += self.delta_angle
    self.check_enemies()

  @staticmethod
  def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

  def check_enemies(self):
    for enemy in self.game.entities + self.game.bullets:
      if enemy == self.game.p:
        continue
      points = [enemy.rect.topleft, enemy.rect.topright, enemy.rect.bottomleft, enemy.rect.bottomright]
      if sum([self.point_in_polygon(p, self.polygon) for p in points]) >= 2:
        enemy.visible = True
        if hasattr(enemy, 'weapon'):
          enemy.weapon.visible = True
      else:
        enemy.visible = False
        if hasattr(enemy, 'weapon'):
          enemy.weapon.visible = False
    
  def draw(self):
    cx = self.game.cx
    cy = self.game.cy

    poly = []
    for point in self.polygon:
        poly.append((point[0] + cx, point[1] + cy))

    shadow = pygame.Surface((cfg.WIDTH, cfg.HEIGHT), pygame.SRCALPHA, 32).convert_alpha()

    pygame.draw.polygon(shadow, (0, 0, 0), poly)
    ar = pygame.surfarray.pixels_alpha(shadow)

    reverse_visible(ar)
    del ar
    shadow.unlock()
    self.game.screen.blit(shadow, (0, 0))
