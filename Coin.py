import pygame as pg


class Coin:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 16, 28)

        self.y = -2
        self.y_offset = 0
        self.moving_up = True

        self.current_image = 0
        self.image_tick = 0
        self.images = [pg.image.load(f'images/Coin/coin{i + 1}.png').convert_alpha() for i in range(4)]

    def update(self, core):
        self.image_tick = (self.image_tick + 1) % 60
        self.current_image = self.image_tick // 15

        self.y_offset += self.y
        self.rect.y += self.y

        if abs(self.y_offset) >= 50:
            self.y = -self.y
            self.moving_up = not self.moving_up
        elif not self.moving_up and self.y_offset == 0:
            core.get_map().participles.remove(self)

    def render(self, core):
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
