import pygame as pg
from Values import *


class Fireball:
    def __init__(self, x, y, move_direction):
        super().__init__()

        self.rect = pg.Rect(x, y, 16, 16)
        self.x_fireball = 5 if move_direction else -5
        self.y_fireball = 0
        self.state = 0
        self.direction = move_direction

        self.current_image = 0
        self.image_tick = 0
        self.images = [pg.image.load('images/Fireball/fireball.png').convert_alpha()]
        self.images.append(pg.transform.flip(self.images[0], False, True))
        self.images.append(pg.transform.flip(self.images[0], True, True))
        self.images.append(pg.transform.flip(self.images[0], True, False))
        self.images.append(pg.image.load('images/Fireball/firework0.png').convert_alpha())
        self.images.append(pg.image.load('images/Fireball/firework1.png').convert_alpha())
        self.images.append(pg.image.load('images/Fireball/firework2.png').convert_alpha())

    def updateX(self, blocks):
        self.rect.x += self.x_fireball

        for block in blocks:
            if block != 0 and block.type != 'BackgroundObject':
                if pg.Rect.colliderect(self.rect, block.rect):
                    self.start_boom()

    def updateY(self, blocks):
        self.rect.y += self.y_fireball
        for block in blocks:
            if block != 0 and block.type != 'BackgroundObject':
                if pg.Rect.colliderect(self.rect, block.rect):
                    self.rect.bottom = block.rect.top
                    self.y_fireball = -3

    def start_boom(self):
        self.x_fireball = 0
        self.y_fireball = 0
        self.current_image = 4
        self.image_tick = 0
        self.state = -1

    def update_image(self, core):
        self.image_tick += 1

        if self.state == -1:
            if self.image_tick % 10 == 0:
                self.current_image += 1
            if self.current_image == 7:
                core.get_map().remove_bang(self)

        if self.state == 0:
            if self.image_tick % 15 == 0:
                self.current_image += 1
                if self.current_image > 3:
                    self.current_image = 0
                    self.image_tick = 0

    def check_map_borders(self, core):
        if self.rect.x <= 0 or self.rect.x >= 6768 or self.rect.y > 448:
            core.get_map().remove_bang(self)

    def move(self, core):
        self.y_fireball += GRAVITY

        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        self.updateY(blocks)
        self.updateX(blocks)

        self.check_map_borders(core)

    def check_collision_with_mobs(self, core):
        for mob in core.get_map().get_mobs():
            if self.rect.colliderect(mob.rect):
                if mob.collision:
                    mob.die(core, instantly=False, crushed=False)
                    self.start_boom()

    def update(self, core):
        if self.state == 0:
            self.update_image(core)
            self.move(core)
            self.check_collision_with_mobs(core)
        elif self.state == -1:
            self.update_image(core)

    def render(self, core):
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
