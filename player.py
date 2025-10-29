# this file is for loading player

import random
from pygame import mixer as mx

def player(main_globals):

    dt = main_globals['dt'] # the god of them all

    class Player:
        def __init__(self, main_globals, x, y):
            self.x = x
            self.y = y
            self.speed = 2
            self.health = 100
            self.alive = True
            self.shake_timer = 0
            self.main_globals = main_globals
            self.weapons = []
            self.wealth = 50000 # consider this debug money for now
            self.locked = False

        def move(self, dx, dy):
            new_x = self.x + dx * self.speed * dt * 60
            new_y = self.y + dy * self.speed * dt * 60
            if self.locked:
                mask = self.main_globals.get('locked_mask')
            else:
                mask = self.main_globals.get('walkable_mask')

            # horizontal
            new_x = self.x + dx * self.speed
            can_move_x = True
            for cy_offset in (25, self.main_globals['player_size'] + 25):
                cx = new_x + 6 if dx < 0 else new_x + self.main_globals['player_size'] - 6
                cy = self.y + cy_offset
                if cx < 0 or cy < 0 or cx >= mask.get_width() or cy >= mask.get_height() or mask.get_at((int(cx), int(cy)))[:3] != (0, 255, 0):
                    can_move_x = False
                    break
                
            # vertical
            new_y = self.y + dy * self.speed
            can_move_y = True
            for cx_offset in (6, self.main_globals['player_size'] - 6):
                cx = self.x + cx_offset
                cy = new_y + 25 if dy < 0 else new_y + self.main_globals['player_size'] + 25
                if cx < 0 or cy < 0 or cx >= mask.get_width() or cy >= mask.get_height() or mask.get_at((int(cx), int(cy)))[:3] != (0, 255, 0):
                    can_move_y = False
                    break
                
            if can_move_x:
                self.x = new_x
            if can_move_y:
                self.y = new_y

        def shake(self):
            dt = self.main_globals['dt']
            if self.shake_timer > 0:
                self.shake_timer -= 1 * dt * 60
                return random.randint(-5, 5), random.randint(-5, 5)
            return 0, 0

        def damaged(self, amount):
            self.health -= amount
            self.shake_timer = 10

            # spawn bloodes at players
            blood_x = self.x + self.main_globals['player_size'] / 2
            blood_y = self.y + self.main_globals['player_size'] / 2
            new_particles = self.main_globals['spawn_blood_particles'](
                self.main_globals['space'], blood_x, blood_y, amount // 2
            )
            self.main_globals['blood_particles'].extend(new_particles)

            if self.health <= 0:
                self.die()
            else:
                """self.main_globals['hurt_sound'].play()
                please fix this man"""

        def die(self):
            self.main_globals['game_stage'] = "dead"
            print("player died")

        def respawn(self):
            print("player respawning")
            main_globals['spawn_set'] = False
            self.alive = True
            self.x = self.main_globals['spawn_x']
            self.y = self.main_globals['spawn_y']
            self.weapons = []
            self.main_globals['blood_particles'] = []
            mx.music.rewind()

        def effect(self, effect_type, number):
            if effect_type == "heal":
                player.health += number
                if player.health > 100:
                    player.health = 100
            elif effect_type == "healfull":
                player.health = 100

        def attack(self, main_globals):
            if len(self.weapons) != 0:
                self.weapons[0].attack(self, main_globals)

    player = Player(main_globals, main_globals['spawn_x'], main_globals['spawn_y'])

    main_globals['player'] = player
    main_globals['Player'] = Player 

    print("player file loaded")