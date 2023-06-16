import pygame as pg
from Values import *


class Event:
    def __init__(self):
        self.type = 0
        self.delay = 0
        self.time = 0
        self.x_vel = 0
        self.y_vel = 0
        self.game_over = False
        self.player_in_castle = False
        self.tick = 0
        self.score_tick = 0

    def start_kill(self, core, game_over):
        self.type = 0
        self.delay = 4000
        self.y_vel = -4
        self.time = pg.time.get_ticks()
        self.game_over = game_over
        core.get_sound().stop('theme')
        core.get_sound().stop('theme_fast')
        core.get_sound().play('death', 0)
        core.get_map().get_player().set_image(len(core.get_map().get_player().sprites))

    def start_win(self, core):
        self.type = 1
        self.time = 0
        self.delay = 1500
        core.get_sound().stop('theme')
        core.get_sound().stop('theme_fast')
        core.get_sound().play('level_end', 0)
        player = core.get_map().get_player()
        player.set_image(5)
        player.x_v = 1
        player.rect.x += 10

        if core.get_map().time >= 300:
            score = 5000
        elif 200 <= core.get_map().time < 300:
            score = 2000
        else:
            score = 1000

        player.add_score(score)
        core.get_map().spawn_score_text(player.rect.x + 16, player.rect.y, score=score)

    def reset(self):
        self.type = 0
        self.delay = 0
        self.time = 0
        self.x_vel = 0
        self.y_vel = 0
        self.game_over = False
        self.player_in_castle = False
        self.tick = 0
        self.score_tick = 0

    def update(self, core):
        if self.type == 1:
            if self.player_in_castle:
                if core.get_map().time > 0:
                    self.score_tick += 1
                    if self.score_tick % 10 == 0:
                        core.get_sound().play('scorering', 0)
                    core.get_map().time -= 1
                    player = core.get_map().get_player()
                    player.add_score(50)
                else:
                    if self.time == 0:
                        self.time = pg.time.get_ticks()
                    elif pg.time.get_ticks() >= self.time + self.delay:
                        mm = core.get_mm()
                        mm.currentGameState = 'Loading'
                        gameLoadingMenu = mm.gameLoadingMenu
                        gameLoadingMenu.set_text_and_type('HAPPY END', False)
                        gameLoadingMenu.update_time()
                        core.get_sound().play('game_over', 0)
            else:
                flag = core.get_map().flag
                player = core.get_map().get_player()
                if not flag.flag_omitted:
                    player.set_image(5)
                    flag.move_flag_down()
                    player.anim_flag(core, False)
                else:
                    self.tick += 1
                    if self.tick == 1:
                        player.direction = False
                        player.set_image(6)
                        player.rect.x += 20
                    elif self.tick >= 30:
                        player.anim_flag(core, True)
                        player.update_image(core)
        if self.type == 0:
            self.y_vel += GRAVITY * FALL_MULTIPLIER if self.y_vel < 6 else 0
            player = core.get_map().get_player()
            player.rect.y += self.y_vel
            if pg.time.get_ticks() > self.time + self.delay:
                if self.game_over:
                    mm = core.get_mm()
                    mm.currentGameState = 'Loading'
                    gameLoadingMenu = mm.gameLoadingMenu
                    gameLoadingMenu.set_text_and_type('BETTER LUCK NEXT TIME', False)
                    gameLoadingMenu.update_time()
                    core.get_sound().play('game_over', 0)
                else:
                    player.reset_move()
                    player.reset_jump()
                    core.get_map().reset(False)
                    core.get_sound().play('theme', 222222)