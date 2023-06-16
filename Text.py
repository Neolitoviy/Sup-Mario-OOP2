import pygame as pg


class Text:
    def __init__(self, text, fontsize, rect_center, textcolor=(255, 255, 255)):
        self.font = pg.font.Font('fonts/font.ttf', fontsize)
        self.text_surface = self.font.render(text, False, textcolor)
        self.rect = self.text_surface.get_rect(center=rect_center)
        self.y_offset = 0

    def update(self, core):
        self.rect.y -= 1
        self.y_offset -= 1

        if self.y_offset == -100:
            core.get_map().remove_text(self)

    def render(self, core):
        core.screen.blit(self.text_surface, self.rect)

    def render_in_game(self, core):
        core.screen.blit(self.text_surface, core.get_map().get_camera().apply(self))
