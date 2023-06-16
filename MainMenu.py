import pygame as pg


class MainMenu:
    def __init__(self):
        self.mainImage = pg.image.load(r'images/Other/name.png').convert_alpha()

    def render(self, core):
        core.screen.blit(self.mainImage, (50, 50))
