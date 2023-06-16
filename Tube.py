import pygame as pg

class Tube:
    def __init__(self, x, y):
        super().__init__()
        image = pg.image.load('images/Other/tube.png').convert_alpha()
        length = (12 - y) * 32
        self.image = image.subsurface(pg.Rect(0, 0, 64, length))
        self.rect = pg.Rect(x * 32, y * 32, 64, length)

    def render(self, core):
        core.screen.blit(self.image, core.get_map().get_camera().apply(self))