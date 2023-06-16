import pygame as pg

from LoadingMenu import LoadingMenu
from MainMenu import MainMenu


class MenuManager:
    def __init__(self, core):

        self.currentGameState = 'MainMenu'

        self.gameMainMenu = MainMenu()
        self.gameLoadingMenu = LoadingMenu(core)

    def update(self, core):
        if self.currentGameState == 'MainMenu':
            pass

        elif self.currentGameState == 'Loading':
            self.gameLoadingMenu.update(core)

        elif self.currentGameState == 'Game':
            core.get_map().update(core)

    def render(self, core):
        if self.currentGameState == 'MainMenu':
            core.get_map().render_map(core)
            self.gameMainMenu.render(core)

        elif self.currentGameState == 'Loading':
            self.gameLoadingMenu.render(core)

        elif self.currentGameState == 'Game':
            core.get_map().render(core)
            core.get_map().get_ui().render(core)

        pg.display.update()

    def start_loading(self):
        self.currentGameState = 'Loading'
        self.gameLoadingMenu.update_time()
