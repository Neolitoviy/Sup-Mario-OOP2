import pygame as pg
from Values import *

PARTICLE_IMAGE_PATH = 'images/Other/participle.png'
PARTICLE_RECT_SIZE = 16
INITIAL_SPEED = -4
X_OFFSETS = [-20, -20, 20, 20]
Y_OFFSETS = [16, -16, 16, -16]


class Participles:
    PARTICLE_IMAGE = None

    def __init__(self, x, y):
        if Participles.PARTICLE_IMAGE is None:
            Participles.PARTICLE_IMAGE = pg.image.load(PARTICLE_IMAGE_PATH).convert_alpha()

        self.image = Participles.PARTICLE_IMAGE
        self.rectangles = [pg.Rect(x + x_offset, y + y_offset, PARTICLE_RECT_SIZE, PARTICLE_RECT_SIZE)
                           for x_offset, y_offset in zip(X_OFFSETS, Y_OFFSETS)]
        self.dy = INITIAL_SPEED
        self.rect = None

    def update(self, core):
        self.dy += GRAVITY * FALL_MULTIPLIER
        self.move_rectangles()
        self.check_out_of_bounds(core)

    def move_rectangles(self):
        for i in range(len(self.rectangles)):
            self.rectangles[i].y += self.dy
            if i < 2:
                self.rectangles[i].x -= 1
            else:
                self.rectangles[i].x += 1

    def check_out_of_bounds(self, core):
        if self.rectangles[1].y > core.get_map().mapSize[1] * 32:
            core.get_map().participles.remove(self)

    def render(self, core):
        for rect in self.rectangles:
            self.rect = rect
            core.screen.blit(self.image, core.get_map().get_camera().apply(self))
