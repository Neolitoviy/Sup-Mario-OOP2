import pygame as pg

from Values import *

QUESTION_BLOCK = 22
BRICK_BLOCK = 23


class Player:
    def __init__(self, x, y):
        self.numOfLives = 3
        self.score = 0
        self.coins = 0

        self.visible = True
        self.spriteTick = 0
        self.powerLVL = 0

        self.unkillable = False
        self.unkillableTime = 0

        self.inLevelUpAnimation = False
        self.inLevelUpAnimationTime = 0
        self.inLevelDownAnimation = False
        self.inLevelDownAnimationTime = 0

        self.already_jumped = False
        self.next_jump_time = 0
        self.next_fireball_time = 0
        self.x_v = 0
        self.y_v = 0
        self.direction = True
        self.on_ground = False
        self.fast_moving = False

        self.pos_x = x

        self.image = pg.image.load('images/Mario/mario.png').convert_alpha()
        self.sprites = []
        self.load_sprites()

        self.rect = pg.Rect(x, y, 32, 32)

    def load_sprites(self):
        self.sprites = [
            pg.image.load('images/Mario/mario.png'),
            pg.image.load('images/Mario/mario_move0.png'),
            pg.image.load('images/Mario/mario_move1.png'),
            pg.image.load('images/Mario/mario_move2.png'),
            pg.image.load('images/Mario/mario_jump.png'),
            pg.image.load('images/Mario/mario_end.png'),
            pg.image.load('images/Mario/mario_end1.png'),
            pg.image.load('images/Mario/mario_st.png'),
            pg.image.load('images/Mario/mario1.png'),
            pg.image.load('images/Mario/mario1_move0.png'),
            pg.image.load('images/Mario/mario1_move1.png'),
            pg.image.load('images/Mario/mario1_move2.png'),
            pg.image.load('images/Mario/mario1_jump.png'),
            pg.image.load('images/Mario/mario1_end.png'),
            pg.image.load('images/Mario/mario1_end1.png'),
            pg.image.load('images/Mario/mario1_st.png'),
            pg.image.load('images/Mario/mario2.png'),
            pg.image.load('images/Mario/mario2_move0.png'),
            pg.image.load('images/Mario/mario2_move1.png'),
            pg.image.load('images/Mario/mario2_move2.png'),
            pg.image.load('images/Mario/mario2_jump.png'),
            pg.image.load('images/Mario/mario2_end.png'),
            pg.image.load('images/Mario/mario2_end1.png'),
            pg.image.load('images/Mario/mario2_st.png'),
        ]

        for i in range(len(self.sprites)):
            self.sprites.append(pg.transform.flip(self.sprites[i], True, False))

        self.sprites.append(pg.image.load('images/Mario/mario_lvlup.png').convert_alpha())
        self.sprites.append(pg.transform.flip(self.sprites[-1], True, False))
        self.sprites.append(pg.image.load('images/Mario/mario_death.png').convert_alpha())

    def set_image(self, image_id):
        if image_id == len(self.sprites):
            # Якщо image_id дорівнює останньому індексу, встановлюємо останнє зображення
            self.image = self.sprites[-1]
        else:
            offset = self.powerLVL * 8

            if self.direction:
                # Встановлюємо зображення залежно від напрямку гравця та рівня потужності
                self.image = self.sprites[image_id + offset]
            else:
                # Встановлюємо зображення для зворотного напрямку гравця
                self.image = self.sprites[image_id + offset + 24]

    def update_image(self, core):
        # Інкрементування лічильника для анімації спрайта
        self.spriteTick += 1
        if core.keyShift:
            self.spriteTick += 1

        if self.powerLVL in (0, 1, 2):
            # Обробка стоячого стану гравця
            if self.x_v == 0:
                self.set_image(0)
                self.spriteTick = 0
            # Обробка руху гравця
            elif (
                    ((self.x_v > 0 and core.keyR and not core.keyL) or
                     (self.x_v < 0 and core.keyL and not core.keyR)) or
                    (self.x_v > 0 and not (core.keyL or core.keyR)) or
                    (self.x_v < 0 and not (core.keyL or core.keyR))
            ):
                # Анімація ходьби гравця
                if self.spriteTick > 30:
                    self.spriteTick = 0

                if self.spriteTick <= 10:
                    self.set_image(1)
                elif 11 <= self.spriteTick <= 20:
                    self.set_image(2)
                elif 21 <= self.spriteTick <= 30:
                    self.set_image(3)
                elif self.spriteTick == 31:
                    self.spriteTick = 0
                    self.set_image(1)
            # Обробка зупинення гравця при руху в протилежних напрямках
            elif (self.x_v > 0 and core.keyL and not core.keyR) or (self.x_v < 0 and core.keyR and not core.keyL):
                self.set_image(7)
                self.spriteTick = 0

            # Обробка анімації в повітрі
            if not self.on_ground:
                self.spriteTick = 0
                self.set_image(4)

    def update(self, core):
        self.player_physics(core)
        self.update_image(core)
        self.update_unkillable_time()

    def updateX(self, blocks):
        for block in blocks:
            if block != 0 and block.type != 'BackgroundObject':
                if self.rect.colliderect(block.rect):
                    if self.x_v > 0:
                        self.rect.right = block.rect.left
                        self.pos_x = self.rect.left
                        self.x_v = 0
                    elif self.x_v < 0:
                        self.rect.left = block.rect.right
                        self.pos_x = self.rect.left
                        self.x_v = 0

    def updateY(self, blocks, core):
        self.on_ground = False
        for block in blocks:
            if block != 0 and block.type != 'BackgroundObject':
                if self.rect.colliderect(block.rect):
                    if self.y_v > 0:
                        self.on_ground = True
                        self.rect.bottom = block.rect.top
                        self.y_v = 0
                    elif self.y_v < 0:
                        self.rect.top = block.rect.bottom
                        self.y_v = -self.y_v / 3
                        self.activate_block_action(core, block)

    def player_physics(self, core):
        # Обробка руху гравця вправо
        if core.keyR:
            self.x_v += SPEED_INCREASE_RATE
            self.direction = True
        # Обробка руху гравця вліво
        if core.keyL:
            self.x_v -= SPEED_INCREASE_RATE
            self.direction = False

        # Обробка стрибка гравця
        if not core.keyU:
            self.already_jumped = False
        elif core.keyU:
            if self.on_ground and not self.already_jumped:
                self.y_v = -JUMP_POWER
                self.already_jumped = True
                self.next_jump_time = pg.time.get_ticks() + 750
                if self.powerLVL >= 1:
                    core.get_sound().play('big_mario_jump', 0)
                else:
                    core.get_sound().play('small_mario_jump', 0)

        # Обробка швидкого руху гравця
        fast_moving = False
        if core.keyShift:
            fast_moving = True
            if self.powerLVL == 2:
                if pg.time.get_ticks() > self.next_fireball_time:
                    if not (self.inLevelUpAnimation or self.inLevelDownAnimation):
                        if len(core.get_map().projectiles) < 2:
                            self.shoot_fireball(core, self.rect.x, self.rect.y, self.direction)

        # Зменшення швидкості гравця при неактивних клавішах руху
        if not (core.keyR or core.keyL):
            if self.x_v > 0:
                self.x_v -= SPEED_DECREASE_RATE
            elif self.x_v < 0:
                self.x_v += SPEED_DECREASE_RATE
        else:
            # Обмеження максимальної швидкості гравця при русі
            if self.x_v > 0:
                if fast_moving:
                    if self.x_v > MAX_FASTMOVE_SPEED:
                        self.x_v = MAX_FASTMOVE_SPEED
                else:
                    if self.x_v > MAX_MOVE_SPEED:
                        self.x_v = MAX_MOVE_SPEED
            if self.x_v < 0:
                if fast_moving:
                    if (-self.x_v) > MAX_FASTMOVE_SPEED:
                        self.x_v = -MAX_FASTMOVE_SPEED
                else:
                    if (-self.x_v) > MAX_MOVE_SPEED:
                        self.x_v = -MAX_MOVE_SPEED

        # Зупинка гравця при дуже низькій швидкості руху
        if 0 < self.x_v < SPEED_DECREASE_RATE:
            self.x_v = 0
        if 0 > self.x_v > -SPEED_DECREASE_RATE:
            self.x_v = 0

        # Обробка падіння гравця
        if not self.on_ground:
            if self.y_v < 0 and core.keyU:
                self.y_v += GRAVITY
            elif self.y_v < 0 and not core.keyU:
                self.y_v += GRAVITY * LOW_JUMP_MULTIPLIER
            else:
                self.y_v += GRAVITY * FALL_MULTIPLIER
            if self.y_v > MAX_FALL_SPEED:
                self.y_v = MAX_FALL_SPEED

        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)

        self.pos_x += self.x_v
        self.rect.x = self.pos_x

        self.updateX(blocks)

        self.rect.y += self.y_v
        self.updateY(blocks, core)
        coord_y = self.rect.y // 32
        if self.powerLVL > 0:
            coord_y += 1
        for block in core.get_map().get_blocks_below(self.rect.x // 32, coord_y):
            if block != 0 and block.type != 'BackgroundObject':
                if pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect):
                    self.on_ground = True

        # Обробка смерті гравця при падінні з екрану
        if self.rect.y > 448:
            core.get_map().player_death(core)

        # Обробка перемоги гравця при досягненні прапорця
        if self.rect.colliderect(core.get_map().flag.pole_rect):
            core.get_map().player_win(core)

    def update_unkillable_time(self):
        if self.unkillable:
            self.unkillableTime -= 1
            if self.unkillableTime == 0:
                self.unkillable = False

    def activate_block_action(self, core, block):
        if block.typeID == QUESTION_BLOCK:
            core.get_sound().play('block_hit', 0)
            if not block.isActivated:
                block.spawn_bonus(core)
        elif block.typeID == BRICK_BLOCK:
            if self.powerLVL == 0:
                block.shaking = True
                core.get_sound().play('block_hit', 0)
            else:
                block.destroy(core)
                core.get_sound().play('brick_break', 0)
                self.add_score(50)

    def reset(self, reset_all):
        # Встановлення початкових значень для гравця
        self.rect.x = 96
        self.rect.y = 351
        self.pos_x = 96
        self.direction = True

        if self.powerLVL != 0:
            # Скидання рівня потужності гравця та зміна його положення
            self.rect.y += 32
            self.rect.h = 32
            self.powerLVL = 0

        if reset_all:
            # Скидання всіх значень, якщо reset_all=True
            self.numOfLives = 3
            self.score = 0
            self.coins = 0
            self.inLevelUpAnimation = False
            self.inLevelUpAnimationTime = 0
            self.visible = True
            self.spriteTick = 0
            self.powerLVL = 0
            self.unkillable = False
            self.unkillableTime = 0
            self.on_ground = False
            self.already_jumped = False
            self.x_v = 0
            self.y_v = 0
            self.inLevelDownAnimation = False
            self.inLevelDownAnimationTime = 0

    def reset_jump(self):
        self.already_jumped = False
        self.y_v = 0

    def reset_move(self):
        self.x_v = 0
        self.y_v = 0

    def jump_on_mob(self):
        self.already_jumped = True
        self.y_v = -4
        self.rect.y -= 6

    def set_powerlvl(self, power_lvl, core):
        # Перевірка, чи гравець має нульовий рівень потужності і не є неуразливим
        if self.powerLVL == 0 == power_lvl and not self.unkillable:
            # Гравець помирає
            core.get_map().player_death(core)
            self.inLevelUpAnimation = False
            self.inLevelDownAnimation = False

        # Перевірка, чи гравець має нульовий рівень потужності та потребує підвищення рівня
        elif self.powerLVL == 0 and self.powerLVL < power_lvl:
            # Гравець отримує перший рівень потужності
            self.powerLVL = 1
            core.get_sound().play('mushroom_eat', 0)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000)
            self.inLevelUpAnimation = True
            self.inLevelUpAnimationTime = 61

        # Перевірка, чи гравець має перший рівень потужності та потребує підвищення рівня
        elif self.powerLVL == 1 and self.powerLVL < power_lvl:
            # Гравець отримує другий рівень потужності
            core.get_sound().play('mushroom_eat', 0)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000)
            self.powerLVL = 2

        # Перевірка, чи гравець має вищий рівень потужності і потребує зниження рівня
        elif self.powerLVL > power_lvl:
            # Гравець втрачає потужність
            core.get_sound().play('pipe', 0)
            self.inLevelDownAnimation = True
            self.inLevelDownAnimationTime = 200
            self.unkillable = True
            self.unkillableTime = 200

        # Інший випадок, коли гравець отримує потужність (power_lvl залишається незмінним)
        else:
            core.get_sound().play('mushroom_eat', 0)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000)

    def pwrlvl_change(self):
        if self.inLevelDownAnimation:
            self.inLevelDownAnimationTime -= 1

            if self.inLevelDownAnimationTime == 0:
                self.inLevelDownAnimation = False
                self.visible = True
            elif self.inLevelDownAnimationTime % 20 == 0:
                self.visible = not self.visible

            if self.inLevelDownAnimationTime == 100:
                self.powerLVL = 0
                self.rect.y += 32
                self.rect.h = 32

        elif self.inLevelUpAnimation:
            self.inLevelUpAnimationTime -= 1

            if self.inLevelUpAnimationTime == 0:
                self.inLevelUpAnimation = False
                self.rect.y -= 32
                self.rect.h = 64

            elif self.inLevelUpAnimationTime in (60, 30):
                sprite_index = -3 if self.direction else -2
                self.image = self.sprites[sprite_index]
                self.rect.y -= 16
                self.rect.h = 48

            elif self.inLevelUpAnimationTime in (45, 15):
                sprite_index = 0 if self.direction else 24
                self.image = self.sprites[sprite_index]
                self.rect.y += 16
                self.rect.h = 32

    def anim_flag(self, core, walk_to_castle):
        if walk_to_castle:
            self.direction = True

            if not self.on_ground:
                self.y_v += GRAVITY if self.y_v <= MAX_FALL_SPEED else 0

            x = self.rect.x // 32
            y = self.rect.y // 32
            blocks = core.get_map().get_blocks_for_collision(x, y)

            self.rect.x += self.x_v
            if self.rect.colliderect(core.get_map().map[205][11]):
                self.visible = False
                core.get_map().get_event().player_in_castle = True
            self.updateX(blocks)

            self.rect.top += self.y_v
            self.updateY(blocks, core)

            x = self.rect.x // 32
            y = self.rect.y // 32
            if self.powerLVL > 0:
                y += 1
            for block in core.get_map().get_blocks_below(x, y):
                if block != 0 and block.type != 'BackgroundObject':
                    if pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect):
                        self.on_ground = True

        else:
            if core.get_map().flag.flag_rect.y + 20 > self.rect.y + self.rect.h:
                self.rect.y += 3

    def shoot_fireball(self, core, x, y, move_direction):
        core.get_map().spawn_fireball(x, y, move_direction)
        core.get_sound().play('fireball', 0)
        self.next_fireball_time = pg.time.get_ticks() + 400

    def add_coins(self, count):
        self.coins += count

    def add_score(self, count):
        self.score += count

    def render(self, core):
        if self.visible:
            core.screen.blit(self.image, core.get_map().get_camera().apply(self))
