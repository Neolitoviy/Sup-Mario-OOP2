import pygame as pg

from Text import Text

TIME_OUT_LONG = 5250
TIME_OUT_SHORT = 2500


class LoadingMenu:
    def __init__(self, core):
        self.iTime = pg.time.get_ticks()
        self.loadingType = True
        self.bg = pg.Rect(0, 0, 800, 448)
        self.text = Text('LEVEL ' + core.gameWorld.get_name(), 32, (800 / 2, 448 / 2))

    def update(self, core):
        timeout = TIME_OUT_LONG if not self.loadingType else TIME_OUT_SHORT
        if pg.time.get_ticks() >= self.iTime + timeout:
            if self.loadingType:
                core.gameMM.currentGameState = 'Game'
                core.get_sound().play('theme', 222222)
                core.get_map().in_event = False
            else:
                core.gameMM.currentGameState = 'MainMenu'
                self.set_text_and_type('LEVEL ' + core.gameWorld.get_name(), True)
                core.get_map().reset(True)

    def set_text_and_type(self, text, type):
        self.text = Text(text, 32, (800 / 2, 448 / 2))
        self.loadingType = type

    def render(self, core):
        pg.draw.rect(core.screen, (0, 0, 0), self.bg)
        self.text.render(core)

    def update_time(self):
        self.iTime = pg.time.get_ticks()
