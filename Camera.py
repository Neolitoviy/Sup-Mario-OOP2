import pygame as pg
from Values import *


class Camera:
    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)
        self.calculate_camera_rect(self.rect)

    def apply(self, target):
        return target.rect.x + self.rect.x, target.rect.y

    def update(self, target):
        self.rect = self.calculate_camera_rect(target)

    def reset(self):
        self.rect = pg.Rect(0, 0, *self.rect.size)

    def calculate_camera_rect(self, target_rect):
        target_x, target_y, target_width, target_height = target_rect
        half_window_w, half_window_h = WINDOW_W / 2, WINDOW_H / 2

        x = -target_x + half_window_w - target_width / 2

        x = min(0, x)
        x = max(-(self.rect.width - WINDOW_W), x)
        y = WINDOW_H - self.rect.height

        return pg.Rect(x, y, self.rect.width, self.rect.height)