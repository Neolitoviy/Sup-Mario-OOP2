import pygame as pg


class BackgroundObject:
    def __init__(self, x, y, image):
        self.type = 'BackgroundObject'
        self.rect = pg.Rect(x, y, 32, 32)
        self.image = image

    def render(self, core):
        core.screen.blit(self.image, core.get_map().get_camera().apply(self))
