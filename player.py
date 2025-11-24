# this file is for loading player logic

import random
from pygame import mixer as mx
import pygame

def player(main_globals):

    class Player:
        def __init__(self, main_globals, x, y):
            self.x = x
            self.y = y
            self.speed = 2 * main_globals['plr_spd_mult']
            self.health = 100
            self.max_hp = main_globals['player_max_health']
            self.alive = True
            self.shake_timer = 0
            self.main_globals = main_globals
            self.weapons = []
            self.wealth = 0 # broke ass bitch
            self.locked = False # if locked to current tile
            self.inventory = {}

            size = self.main_globals['player_size']
            self.rect = pygame.Rect(self.x, self.y, size, size)

        def move(self, dx, dy):
            dt = self.main_globals['dt']
            new_x = self.x + dx * self.speed * dt * 60
            new_y = self.y + dy * self.speed * dt * 60

            # change mask depending on lock
            if self.locked:
                mask = self.main_globals.get('locked_mask') # no bridge
            else:
                mask = self.main_globals.get('walkable_mask') # bridge

            # horizontal movement
            new_x = self.x + dx * self.speed
            can_move_x = True
            for cy_offset in (25, self.main_globals['player_size'] + 25):
                cx = new_x + 6 if dx < 0 else new_x + self.main_globals['player_size'] - 6
                cy = self.y + cy_offset
                if cx < 0 or cy < 0 or cx >= mask.get_width() or cy >= mask.get_height() or mask.get_at((int(cx), int(cy)))[:3] != (0, 255, 0):
                    can_move_x = False
                    break

            # vertical movement
            new_y = self.y + dy * self.speed
            can_move_y = True
            for cx_offset in (6, self.main_globals['player_size'] - 6):
                cx = self.x + cx_offset
                cy = new_y + 25 if dy < 0 else new_y + self.main_globals['player_size'] + 25
                if cx < 0 or cy < 0 or cx >= mask.get_width() or cy >= mask.get_height() or mask.get_at((int(cx), int(cy)))[:3] != (0, 255, 0):
                    can_move_y = False
                    break

            # actually move
            if can_move_x:
                self.x = new_x
            if can_move_y:
                self.y = new_y
            if can_move_x or can_move_y:
                self.rect.topleft = (self.x, self.y)

        def shake(self): # shakes the player around like a little baby in my arms
            dt = self.main_globals['dt']
            if self.shake_timer > 0:
                self.shake_timer -= 1 * dt * 60
                return random.randint(-5, 5), random.randint(-5, 5)
            return 0, 0

        def damaged(self, amount):
            self.health -= amount
            self.shake_timer = 10

            # spawn blood particles at player
            blood_x = self.x + self.main_globals['player_size'] / 2
            blood_y = self.y + self.main_globals['player_size'] / 2
            new_particles = self.main_globals['spawn_blood_particles'](
                self.main_globals['space'], blood_x, blood_y, amount // 2
            )
            if new_particles is not None:
                self.main_globals['blood_particles'].extend(new_particles)

            if self.health <= 0:
                self.die()
            else:
                # note: this will never be fixes
                """self.main_globals['hurt_sound'].play()
                please fix this man"""
                # this has and will be broken since day 1

        def die(self):
            self.main_globals['game_stage'] = "dead"
            main_globals['deaths'] += 1
            if main_globals['deaths'] > main_globals['total_deaths']:
                main_globals['save'](main_globals, total_deaths=main_globals['total_deaths'])
            main_globals['reset'](main_globals)
            print("player died")

        def respawn(self):
            print("player respawning")
            main_globals['spawn_set'] = False
            self.x = self.main_globals['spawn_x']
            self.y = self.main_globals['spawn_y']
            self.main_globals['blood_particles'] = []

        def effect(self, effect_type, number):
            if effect_type == "heal":
                player.health += number
                if player.health > self.max_hp:
                    player.health = self.max_hp

                # remove item from inventory
                for potion, heal in [('small_potion', 20), ('medium_potion', 40), ('large_potion', 60)]:
                    if potion in main_globals['player'].inventory and heal == number:
                        main_globals['player'].inventory[potion] -= 1
                        if main_globals['player'].inventory[potion] <= 0:
                            del main_globals['player'].inventory[potion]
                        break

            elif effect_type == "healfull":
                player.health = 100
            elif effect_type == "money":
                player.wealth += number
            elif effect_type == "max_hp":
                main_globals['player_max_health'] += number
                self.hp += main_globals['player_max_health'] - self.max_hp # heal for change
                self.max_hp = main_globals['player_max_health']
            elif effect_type == "ovr_damage":
                main_globals['damage_mult'] += number
            elif effect_type == "ovr_speed":
                main_globals['plr_spd_mult'] += number
                main_globals['proj_spd_mult'] += number
                main_globals['cooldown_mult'] -= number

        def attack(self, main_globals):
            if len(self.weapons) != 0:
                self.weapons[0].attack(self, main_globals)

    player = Player(main_globals, main_globals['spawn_x'], main_globals['spawn_y'])

    main_globals['player'] = player
    main_globals['Player'] = Player

    print("player, " , end = "")