import pygame as pg


class GameUI:
    def __init__(self):
        self.font = pg.font.Font('fonts/font.ttf', 20)
        self.text = ['POINTS', 'COINS', 'MAP', 'TIME', 'LIVES']
        self.positions = [(60, 35), (230, 35), (375, 35), (557, 35), (730, 35)]

    def _render_text(self, core, index, text):
        text_surface = self.font.render(str(text), False, (255, 255, 255))
        rect = text_surface.get_rect(center=self.positions[index])
        core.screen.blit(text_surface, rect)

    def render(self, core):
        x = 10
        for word in self.text:
            rect = self.font.render(word, False, (255, 255, 255))
            core.screen.blit(rect, (x, 0))
            x += 168

        player = core.get_map().get_player()
        self._render_text(core, 0, player.score)
        self._render_text(core, 1, player.coins)
        self._render_text(core, 2, core.get_map().get_name())
        self._render_text(core, 3, core.get_map().time)
        self._render_text(core, 4, player.numOfLives)