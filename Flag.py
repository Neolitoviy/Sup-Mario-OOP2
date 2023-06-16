import pygame as pg


class Flag:
    FLAG_SPEED = 3
    FLAG_LIMIT = 255

    def __init__(self, x, y, pole_image_path='images/flag/flagpole.png', flag_image_path='images/flag/flag.png'):
        self.rect = None
        self.flag_omitted = False
        self.flag_offset = 0

        self.pole_image = pg.image.load(pole_image_path).convert_alpha()
        self.pole_rect = pg.Rect(x + 8, y, 16, 304)
        self.flag_image = pg.image.load(flag_image_path).convert_alpha()
        self.flag_rect = pg.Rect(x - 18, y + 16, 32, 32)

    def move_flag_down(self):
        self.flag_offset += self.FLAG_SPEED
        self.flag_rect.y += self.FLAG_SPEED

        if self.flag_offset >= self.FLAG_LIMIT:
            self.flag_omitted = True

    def render(self, core):
        self.rect = self.pole_rect
        core.screen.blit(self.pole_image, core.get_map().get_camera().apply(self))

        self.rect = self.flag_rect
        core.screen.blit(self.flag_image, core.get_map().get_camera().apply(self))
