import pygame as pg


class Sound:
    def __init__(self):
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        sound_files = {
            'theme': 'sounds/theme.wav',
            'theme_fast': 'sounds/theme-fast.wav',
            'level_end': 'sounds/levelend.wav',
            'coin': 'sounds/coin.wav',
            'small_mario_jump': 'sounds/jump.wav',
            'big_mario_jump': 'sounds/jumpbig.wav',
            'brick_break': 'sounds/blockbreak.wav',
            'block_hit': 'sounds/blockhit.wav',
            'mushroom_appear': 'sounds/mushroomappear.wav',
            'mushroom_eat': 'sounds/mushroomeat.wav',
            'death': 'sounds/death.wav',
            'pipe': 'sounds/pipe.wav',
            'kill_mob': 'sounds/kill_mob.wav',
            'game_over': 'sounds/gameover.wav',
            'scorering': 'sounds/scorering.wav',
            'fireball': 'sounds/fireball.wav',
            'shot': 'sounds/shot.wav'
        }

        for name, file_path in sound_files.items():
            self.sounds[name] = pg.mixer.Sound(file_path)

    def play(self, name, loops):
        sound = self.sounds.get(name)
        if sound:
            sound.play(loops=loops)

    def stop(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.stop()

    def start_fast_music(self, core):
        if core.get_map().get_name() == '1-1':
            self.stop('theme')
            self.play('theme_fast', 222222)
