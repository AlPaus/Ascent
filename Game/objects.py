import pygame
from animated_sprite import AnimatedSprite
import config as cfg


class ChestLid(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type, position, scale):
        super().__init__()

        if (type == 0):
            if (position == 'left'):
                self.image = pygame.image.load('resources/chests/blue_chest/open/left.png')
            else:
                self.image = pygame.image.load('resources/chests/blue_chest/open/right.png')
        elif (type == 1):
            if (position == 'left'):
                self.image = pygame.image.load('resources/chests/blue_chest/open/left.png')
            else:
                self.image = pygame.image.load('resources/chests/blue_chest/open/right.png')
        else:
            if (position == 'left'):
                self.image = pygame.image.load('resources/chests/blue_chest/open/left.png')
            else:
                self.image = pygame.image.load('resources/chests/blue_chest/open/right.png')
        w, h = int(self.image.get_size()[0] * scale), int(self.image.get_size()[1] * scale)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        if position == 'left':
            self.rect.right = x
        else:
            self.rect.left = x
        self.rect.top = y
        self.speedx = 0
        self.game = game

    def update(self):
        print(self.speedx)
        self.rect.move_ip(self.speedx * self.game.delta_time / 33, 0)


class Chest(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        super().__init__()
        if (type == 0):
            self.image = pygame.image.load('resources/chests/blue_chest/0.png')
            scale = cfg.MEASURE / self.image.get_size()[0]
            w, h = int(self.image.get_size()[0] * scale), int(self.image.get_size()[1] * scale)
            self.image = pygame.transform.scale(self.image, (w, h))
            self.body = pygame.image.load('resources/chests/blue_chest/open/body.png')
            self.body = pygame.transform.scale(self.body, (w, h))
        elif (type == 1):
            self.image = pygame.image.load('resources/chests/blue_chest/0.png')
            scale = cfg.MEASURE / self.image.get_size()[0]
            w, h = int(self.image.get_size()[0] * scale), int(self.image.get_size()[1] * scale)
            self.image = pygame.transform.scale(self.image, (w, h))
            self.body = pygame.image.load('resources/chests/blue_chest/open/body.png')
            self.body = pygame.transform.scale(self.body, (w, h))
        else:
            self.image = pygame.image.load('resources/chests/blue_chest/0.png')
            scale = cfg.MEASURE / self.image.get_size()[0]
            w, h = int(self.image.get_size()[0] * scale), int(self.image.get_size()[1] * scale)
            self.image = pygame.transform.scale(self.image, (w, h))
            self.body = pygame.image.load('resources/chests/blue_chest/open/body.png')
            self.body = pygame.transform.scale(self.body, (w, h))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = type
        self.startx = -1
        self.frame = 0
        self.l_lid = ChestLid(game, self.rect.centerx, self.rect.top, type, 'left', scale)
        self.r_lid = ChestLid(game, self.rect.centerx, self.rect.top,
                              type, 'right', scale)

        self.outline = pygame.mask.from_surface(self.image).outline()
    def open(self):
        self.game.lying_weapons.remove(self)
        self.startx = self.r_lid.rect.centerx
        self.image = self.body
        self.l_lid.speedx = -2
        self.r_lid.speedx = 2
        self.game.sprites.add(self.l_lid)
        self.game.sprites.add(self.r_lid)

    def update(self):
        if self.startx != -1 and abs(self.startx - self.r_lid.rect.centerx) >= self.r_lid.rect.width:
            self.r_lid.rect.left = self.rect.right
            self.l_lid.rect.right = self.rect.left
            self.r_lid.speedx = 0
            self.l_lid.speedx = 0


class Portal(AnimatedSprite):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, path='')
