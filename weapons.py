# weapon logic file

import pygame, random, math, time

def weapons(main_globals):

    def spawn_weapons(main_globals):
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        weapon_types = list(main_globals['weapon_images'].keys())

        for row_idx, row in enumerate(main_globals['tilemap']):
            for col_idx, tile_type in enumerate(row):
                if tile_type == 2:
                    center_x = col_idx * ts + main_globals['tile_size'] // 2
                    center_y = row_idx * ts + main_globals['tile_size'] // 2

                    # dont spawn if a weapon is already there
                    if any(math.isclose(w.x, center_x, abs_tol=1) and math.isclose(w.y, center_y, abs_tol=1) for w in main_globals['weapons_on_map']):
                        continue

                    # pick random weapon
                    weapon_name = random.randint(0, len(weapon_types) - 1)
                    weapon_name = weapon_types[weapon_name]
                    new_weapon = main_globals['Weapon'](weapon_name)
                    new_weapon.x = center_x
                    new_weapon.y = center_y
                    main_globals['weapons_on_map'].append(new_weapon)
                    print(f"spawned {weapon_name} on ({row_idx}, {col_idx})")
                    # print(f"weapons on map: {main_globals['weapons_on_map']}") too many prints

    class Weapon():
        def __init__(self, name):
            self.name = name
            stats = main_globals['weapon_stats'][name]
            self.damage = stats['damage']
            self.range = stats['range']
            self.cooldown = stats['cooldown']
            self.x = main_globals['tile_size'] // 2
            self.y = main_globals['tile_size'] // 2
            self.last_attack_time = 0

        def __repr__(self): # makes it printable without memory locations
            return f"Weapon('{self.name}')"

        def can_attack(self):
            current_time = time.time()
            return (current_time - self.last_attack_time) >= self.cooldown

        def attack(self, player, main_globals):
            slash_img = main_globals['slash_image']
            if self.can_attack():
                print(f"player attacked with {self.name}")
                self.last_attack_time = time.time()
                mouse_pos = pygame.mouse.get_pos()

                # default slash
                if self.name == "sword" or self.name == "axe" or self.name == "book": # remove book later
                    scaled_height = int(slash_img.get_height() * (self.range / 50))
                    scaled_slash = pygame.transform.scale(slash_img, (slash_img.get_width(), scaled_height))

                    player_cx = player.x + main_globals['player_size'] // 2
                    player_cy = player.y + main_globals['player_size'] // 2 + 20

                    # angle to mouse
                    dx = mouse_pos[0] - (player_cx - main_globals['camera_x'])
                    dy = mouse_pos[1] - (player_cy - main_globals['camera_y'])
                    angle = math.degrees(math.atan2(-dy, dx))

                    # offset from player center
                    distance = self.range
                    offset_x = math.cos(math.radians(-angle)) * distance
                    offset_y = math.sin(math.radians(-angle)) * distance

                    rotated_slash = pygame.transform.rotate(scaled_slash, angle)
                    slash_rect = rotated_slash.get_rect(center=(
                        player_cx - main_globals['camera_x'] + offset_x,
                        player_cy - main_globals['camera_y'] + offset_y
                    ))

                    """
                    pretty much scrapped but it was meant to be a jab
                    if main_globals['attack_counter'] == 1:
                        rotated_slash = pygame.transform.flip(rotated_slash, False, True)
                    elif main_globals['attack_counter'] == 2:
                        pass # for now otherwise like a jab thing
                    if main_globals['attack_counter'] >= 2:
                        main_globals['attack_counter'] = 0
                    """

                    mouse_x_world = mouse_pos[0] + main_globals['camera_x']
                    if mouse_x_world < player_cx:
                        main_globals['facing_left'] = True
                    else:
                        main_globals['facing_left'] = False

                    if 'active_slashes' not in main_globals:
                        main_globals['active_slashes'] = []
                    main_globals['active_slashes'].append({
                        'image': rotated_slash,
                        'rect': slash_rect,
                        'expiry': pygame.time.get_ticks() + 150, # time for it to disappear
                        'hit_enemies': set() # enemies hit by this
                    })

                # special attacks

                # book
                """
                elif self.name == "book":
                    pass
                """

            else: # if still on cooldown
                remaining = round(self.cooldown - (time.time() - self.last_attack_time), 2)
                print(f"{self.name} is on cooldown for {remaining} more seconds")

        def pickup(self, player):
            if len(player.weapons) > 0:
                old_weapon = player.weapons.pop(0)
                old_weapon.x = self.x
                old_weapon.y = self.y
                main_globals['weapons_on_map'].append(old_weapon) # swap weapons
                print(f"player dropped {old_weapon.name}")
            player.weapons.append(self)

            if self in main_globals['weapons_on_map']:
                main_globals['weapons_on_map'].remove(self)

            print(f"player picked up {self.name}")

        def draw(self, screen, x, y):
            screen.blit(main_globals['weapon_images'][self.name], (x, y))

    main_globals['spawn_weapons'] = spawn_weapons
    main_globals['Weapon'] = Weapon

    print("weapons file loaded")