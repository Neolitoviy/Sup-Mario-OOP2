from os import environ

import pygame as pg
from pygame.locals import *

from Values import *
from Map import Map
from MenuManager import MenuManager
from Sound import Sound


class Core:
    def __init__(self):
        pg.display.set_caption('Marrio')
        icon = pg.image.load('images/Other/icon.png')
        pg.display.set_icon(icon)
        pg.display.set_mode((WINDOW_W, WINDOW_H))
        environ['SDL_VIDEO_CENTERED'] = '1'
        pg.mixer.pre_init(44100, -16, 2, 1024)
        pg.init()

        self.run = True
        self.keyR = False
        self.keyL = False
        self.keyU = False
        self.keyD = False
        self.keyShift = False

        self.gameWorld = Map('1-1')
        self.gameSound = Sound()
        self.gameMM = MenuManager(self)

        self.screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pg.time.Clock()

    def get_map(self):
        return self.gameWorld

    def get_mm(self):
        return self.gameMM

    def get_sound(self):
        return self.gameSound

    def update(self):
        self.get_mm().update(self)

    def render(self):
        self.get_mm().render(self)

    def main_loop(self):
        while self.run:
            self.input()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def input(self):
        if self.get_mm().currentGameState == 'Game':
            self.input_player()
        else:
            self.input_menu()

    def input_player(self):
        for e in pg.event.get():

            if e.type == pg.QUIT:
                self.run = False

            elif e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    self.keyR = True
                elif e.key == K_LEFT:
                    self.keyL = True
                elif e.key == K_DOWN:
                    self.keyD = True
                elif e.key == K_UP:
                    self.keyU = True
                elif e.key == K_LSHIFT:
                    self.keyShift = True

            elif e.type == KEYUP:
                if e.key == K_RIGHT:
                    self.keyR = False
                elif e.key == K_LEFT:
                    self.keyL = False
                elif e.key == K_DOWN:
                    self.keyD = False
                elif e.key == K_UP:
                    self.keyU = False
                elif e.key == K_LSHIFT:
                    self.keyShift = False

    def input_menu(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.run = False

            elif e.type == KEYDOWN:
                if e.key == K_RETURN:
                    self.get_mm().start_loading()
