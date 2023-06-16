import pygame as pg
from Values import *


class Entity:
    def __init__(self):
        self.state = 0
        self.x_v = 0
        self.y_v = 0
        self.move_direction = True
        self.on_ground = False
        self.collision = True
        self.image = None
        self.rect = None

    def die(self, core, instantly, crushed):
        pass

    def render(self, core):
        pass

    def updateX(self, blocks):
        self.rect.x += self.x_v

        for block in blocks:
            if block and block.type != 'BackgroundObject':
                if pg.Rect.colliderect(self.rect, block.rect):
                    if self.x_v > 0:
                        self.rect.right = block.rect.left
                        self.x_v = - self.x_v
                    elif self.x_v < 0:
                        self.rect.left = block.rect.right
                        self.x_v = - self.x_v

    def updateY(self, blocks):
        self.rect.y += self.y_v * FALL_MULTIPLIER

        self.on_ground = False
        for block in blocks:
            if block and block.type != 'BackgroundObject':
                if pg.Rect.colliderect(self.rect, block.rect):
                    if self.y_v > 0:
                        self.on_ground = True
                        self.rect.bottom = block.rect.top
                        self.y_v = 0

    def check_map_borders(self, core):
        if self.rect.y >= 448:
            self.die(core, True, False)
        if self.rect.x <= 1 and self.x_v < 0:
            self.x_v = - self.x_v


class Flower(Entity):
    ANIMATION_SPEED = 15
    MAX_IMAGES = 4

    def __init__(self, x, y, image_paths=('images/Flower/flower1.png', 'images/Flower/flower2.png',
                                          'images/Flower/flower3.png', 'images/Flower/flower4.png')):
        super().__init__()
        self.rect = pg.Rect(x, y, 32, 32)
        self.spawned = False
        self.spawn_y_offset = 0
        self.current_image = 0
        self.image_tick = 0
        self.images = [pg.image.load(path).convert_alpha() for path in image_paths]

    def check_collision_with_player(self, core):
        player = core.get_map().get_player()
        if self.rect.colliderect(player.rect):
            player.set_powerlvl(3, core)
            core.get_map().get_mobs().remove(self)

    def update_image(self):
        self.image_tick += 1

        if self.image_tick == self.ANIMATION_SPEED * self.MAX_IMAGES:
            self.image_tick = 0
            self.current_image = 0
        elif self.image_tick % self.ANIMATION_SPEED == 0:
            self.current_image += 1

    def spawn_animation(self):
        self.spawn_y_offset -= 1
        self.rect.y -= 1

        if self.spawn_y_offset == -32:
            self.spawned = True

    def update(self, core):
        self.check_collision_with_player(core)
        if self.spawned:
            self.update_image()
        else:
            self.spawn_animation()

    def render(self, core):
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))


def power_up_player(core):
    core.get_map().get_player().set_powerlvl(2, core)


class Mushroom(Entity):
    MUSHROOM_IMAGE = None
    MUSHROOM_SIZE = 32

    def __init__(self, x, y, move_direction):
        super().__init__()

        # Initialize the MUSHROOM_IMAGE if it hasn't been already
        if Mushroom.MUSHROOM_IMAGE is None:
            Mushroom.MUSHROOM_IMAGE = pg.image.load('images/Other/mushroom.png').convert_alpha()

        self.rect = pg.Rect(x, y, Mushroom.MUSHROOM_SIZE, Mushroom.MUSHROOM_SIZE)
        self.x_v = 1 if move_direction else -1
        self.spawned = False
        self.spawn_y_offset = 0
        self.image = Mushroom.MUSHROOM_IMAGE

    def check_collision_with_player(self, core):
        if self.rect.colliderect(core.get_map().get_player().rect):
            power_up_player(core)
            self.remove_self_from_game(core)

    def remove_self_from_game(self, core):
        core.get_map().get_mobs().remove(self)

    def die(self, core, instantly, crushed):
        self.remove_self_from_game(core)

    def spawn_animation(self):
        self.spawn_y_offset -= 1
        self.rect.y -= 1

        if self.spawn_y_offset == - Mushroom.MUSHROOM_SIZE:
            self.spawned = True

    def update(self, core):
        if self.spawned:
            self.apply_gravity()
            self.handle_movement(core)
        else:
            self.spawn_animation()

    def apply_gravity(self):
        if not self.on_ground:
            self.y_v += GRAVITY

    def handle_movement(self, core):
        blocks = core.get_map().get_blocks_for_collision(self.rect.x // Mushroom.MUSHROOM_SIZE,
                                                         self.rect.y // Mushroom.MUSHROOM_SIZE)
        self.updateX(blocks)
        self.updateY(blocks)
        self.check_map_borders(core)

    def render(self, core):
        core.screen.blit(self.image, core.get_map().get_camera().apply(self))


def play_sound(core, sound_name):
    core.get_sound().play(sound_name, 0)


class Goomba(Entity):
    def __init__(self, x, y, move_direction):
        super().__init__()
        self.rect = pg.Rect(x, y, 32, 32)
        self.x_v = 1 if move_direction else -1
        self.crushed = False
        self.current_image = 0
        self.image_tick = 0
        self.images = [
            pg.image.load(f'images/Goomba/goomba_{i}.png').convert_alpha() for i in range(3)
        ]
        self.images.append(pg.transform.flip(self.images[0], False, True))

    def remove_self(self, core):
        core.get_map().get_mobs().remove(self)

    def die(self, core, instantly, crushed):
        if instantly:
            self.remove_self(core)
        else:
            core.get_map().get_player().add_score(core.get_map().score_for_killing_mob)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)

            self.state = -1
            self.collision = False

            if crushed:
                self.crushed = True
                self.image_tick = 0
                self.current_image = 2
                play_sound(core, 'kill_mob')
            else:
                self.y_v = -4
                self.current_image = 3
                play_sound(core, 'shot')

    def check_collision_with_player(self, core):
        if self.collision and self.state != -1 and self.rect.colliderect(core.get_map().get_player().rect):
            if core.get_map().get_player().y_v > 0:
                self.die(core, instantly=False, crushed=True)
                core.get_map().get_player().reset_jump()
                core.get_map().get_player().jump_on_mob()
            elif not core.get_map().get_player().unkillable:
                core.get_map().get_player().set_powerlvl(0, core)

    def update_image(self):
        self.image_tick += 1
        if self.image_tick in [14, 28]:
            self.current_image = 1 if self.image_tick == 14 else 0
            if self.image_tick == 28:
                self.image_tick = 0

    def update(self, core):
        if self.state == 0:
            self.update_image()
            if not self.on_ground:
                self.y_v += GRAVITY

            blocks = core.get_map().get_blocks_for_collision(int(self.rect.x // 32), int(self.rect.y // 32))
            self.updateX(blocks)
            self.updateY(blocks)
            self.check_map_borders(core)

        elif self.state == -1:
            if self.crushed:
                self.image_tick += 1
                if self.image_tick == 50:
                    self.remove_self(core)
            else:
                self.y_v += GRAVITY
                self.rect.y += self.y_v
                self.check_map_borders(core)

    def render(self, core):
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))


def load_images():
    image_files = ['images/Koopa/koopa_0.png', 'images/Koopa/koopa_1.png', 'images/Koopa/koopa_dead.png']
    images = [pg.image.load(img).convert_alpha() for img in image_files]
    flipped_images = [pg.transform.flip(img, True, False) for img in images]
    images.extend(flipped_images)
    return images


class Koopa(Entity):
    def __init__(self, x, y, move_direction):
        super().__init__()
        self.rect = pg.Rect(x, y, 32, 46)

        self.move_direction = move_direction
        self.x_v = 1 if move_direction else -1

        self.current_image = 0
        self.image_tick = 0
        self.images = load_images()

    def check_collision_with_player(self, core):
        if not self.collision:
            return
        if not self.rect.colliderect(core.get_map().get_player().rect):
            return
        if self.state == -1:
            return
        player = core.get_map().get_player()
        if player.y_v > 0:
            self.change_state(core)
            core.get_sound().play('kill_mob', 0)
            player.reset_jump()
            player.jump_on_mob()
        elif not player.unkillable:
            player.set_powerlvl(0, core)

    def check_collision_with_mobs(self, core):
        for mob in core.get_map().get_mobs():
            if mob is not self:
                if self.rect.colliderect(mob.rect):
                    if mob.collision:
                        mob.die(core, instantly=False, crushed=False)

    def die(self, core, instantly, crushed):
        if not instantly:
            core.get_map().get_player().add_score(core.get_map().score_for_killing_mob)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)
            self.state = -1
            self.y_v = -4
            self.current_image = 5
        else:
            core.get_map().get_mobs().remove(self)

    def change_state(self, core):
        self.state += 1
        self.current_image = 2

        # 0 1
        if self.rect.h == 46:
            self.x_v = 0
            self.rect.h = 32
            self.rect.y += 14
            core.get_map().get_player().add_score(100)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=100)
        elif self.state == 2:
            core.get_map().get_player().add_score(100)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=100)

            if core.get_map().get_player().rect.x - self.rect.x <= 0:
                self.x_v = 6
            else:
                self.x_v = -6
        elif self.state == 3:
            self.die(core, instantly=False, crushed=False)

    def update_image(self):
        self.image_tick += 1

        self.move_direction = self.x_v > 0

        if self.image_tick == 35:
            self.current_image = 4 if self.move_direction else 1
        elif self.image_tick == 70:
            self.current_image = 3 if self.move_direction else 0
            self.image_tick = 0

    def update_common(self, core):
        if not self.on_ground:
            self.y_v += GRAVITY

        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        self.updateX(blocks)
        self.updateY(blocks)

        self.check_map_borders(core)

    def update(self, core):
        if self.state == 0:
            self.update_image()
            self.update_common(core)

        elif self.state in [1, 2]:
            self.update_common(core)
            if self.state == 2:
                self.check_collision_with_mobs(core)

        elif self.state == -1:
            self.rect.y += self.y_v
            self.y_v += GRAVITY

            self.check_map_borders(core)

    def render(self, core):
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))

