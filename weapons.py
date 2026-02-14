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

                    # pick weapon to spawn
                    weights = [main_globals['weapon_stats'][w]['chance'] for w in weapon_types]
                    weapon_name = random.choices(weapon_types, weights=weights, k=1)[0]
                    new_weapon = main_globals['Weapon'](weapon_name)
                    new_weapon.x = center_x
                    new_weapon.y = center_y
                    main_globals['weapons_on_map'].append(new_weapon)
                    chance = main_globals['weapon_stats'][weapon_name]['chance']
                    print(f"spawned {weapon_name} on ({row_idx} {col_idx}), with chance {chance*100}%, ", end="")

    class Weapon():
        def __init__(self, name):
            self.name = name
            stats = main_globals['weapon_stats'][name]
            self.damage = stats['damage']
            self.range = stats['range']
            self.cooldown = stats['cooldown']
            self.type = stats['type']

            self.proj_speed = stats.get('proj_speed', 300)
            self.gravity = stats.get('gravity', 0)

            self.x = main_globals['tile_size'] // 2
            self.y = main_globals['tile_size'] // 2
            self.last_attack_time = 0

        def __repr__(self): # makes it printable without memory locations
            return f"Weapon('{self.name}', type='{self.type}')"

        def can_attack(self):
            current_time = time.time()
            return (current_time - self.last_attack_time) >= self.cooldown * main_globals['cooldown_mult']

        def attack(self, player, main_globals):
            if not self.can_attack():
                remaining = round(self.cooldown - (time.time() - self.last_attack_time), 2)
                # print(f"{self.name} is on cooldown for {remaining} more seconds, ", end="")
                return

            # print(f"player attacked with {self.name}, ", end="")
            self.last_attack_time = time.time()

            player_cx = player.x + main_globals['player_size'] // 2
            player_cy = player.y + main_globals['player_size'] // 2 + 20

            mouse_pos = main_globals['mouse_pos']

            # angle to mouse
            dx = mouse_pos[0] - (player_cx - main_globals['camera_x'])
            dy = mouse_pos[1] - (player_cy - main_globals['camera_y'])
            angle_deg = math.degrees(math.atan2(-dy, dx))
            angle_rad = math.atan2(dy, dx)

            # attack
            if self.type == "melee":
                self.melee_attack(player, main_globals, player_cx, player_cy, angle_deg)
            elif self.type == "ranged":
                self.ranged_attack(player, main_globals, player_cx, player_cy, angle_rad, proj_radius=main_globals['weapon_stats'][self.name].get('proj_radius', 8))
            elif self.type == "special":
                self.special_attack(player, main_globals, self.name)

            # face player
            mouse_x_world = mouse_pos[0] + main_globals['camera_x']
            if mouse_x_world < player_cx:
                main_globals['facing_left'] = True
            else:
                main_globals['facing_left'] = False

        def melee_attack(self, player, main_globals, player_cx, player_cy, angle_deg):
            slash_img = main_globals['slash_image']

            # scale slash based on range
            scaled_height = int(slash_img.get_height() * (self.range / 50))
            scaled_slash = pygame.transform.scale(slash_img, (slash_img.get_width(), scaled_height))

            # rotate slash to angle
            rotated_slash = pygame.transform.rotate(scaled_slash, angle_deg)

            # offset from player center by range
            offset_x = math.cos(math.radians(-angle_deg)) * self.range
            offset_y = math.sin(math.radians(-angle_deg)) * self.range

            slash_rect = rotated_slash.get_rect(center=(
                player_cx - main_globals['camera_x'] + offset_x,
                player_cy - main_globals['camera_y'] + offset_y
            ))

            # store active slashes
            if 'active_slashes' not in main_globals:
                main_globals['active_slashes'] = []

            main_globals['active_slashes'].append({
                'image': rotated_slash,
                'rect': slash_rect,
                'expiry': pygame.time.get_ticks() + 150,
                'hit_enemies': set()
            })

        def ranged_attack(self, player, main_globals, player_cx, player_cy, angle_rad, proj_radius=8):
            proj_img = main_globals['projectile_images'].get(self.name, None)

            # create projectile with stats
            projectile = main_globals['Projectile'](
                x=player_cx,
                y=player_cy,
                angle=angle_rad,
                speed=self.proj_speed,
                damage=self.damage,
                owner=self,
                image=proj_img,
                gravity=self.gravity,
                radius=proj_radius,
                pierce=main_globals['weapon_stats'][self.name].get('pierce', 0),
                pierced=0,
            )

            # store active projectiles
            if 'active_projectiles' not in main_globals:
                main_globals['active_projectiles'] = []

            main_globals['active_projectiles'].append(projectile)

            # print(f"shot {self.name} projectile: speed={self.proj_speed}, range={self.range}")

        def special_attack(self, player, main_globals, type): # each weapon gets their own type

            player_cx = player.x + main_globals['player_size'] // 2
            player_cy = player.y + main_globals['player_size'] // 2 + 20
            mouse_pos = main_globals['mouse_pos']

            if type == "katana":

                # stats
                expiry = 110 # ms each attack is visible
                hits = 2 # how many attacks after the first
                delay = 180 # ms between attacks
                effect = None # special effect

                attack_image = main_globals['special_attack_images'][type]
                images = [
                    attack_image,
                    pygame.transform.flip(attack_image, False, True)
                ]

                # angle to mouse
                dx = mouse_pos[0] - (player_cx - main_globals['camera_x'])
                dy = mouse_pos[1] - (player_cy - main_globals['camera_y'])
                angle = math.degrees(math.atan2(-dy, dx))

                # offset from player center
                distance = self.range
                offset_x = math.cos(math.radians(-angle)) * distance
                offset_y = math.sin(math.radians(-angle)) * distance

                # rotate and scale both images
                rotated_images = []
                rects = []
                for img in images:
                    scaled_height = int(img.get_height() * (distance / 50))
                    scaled_img = pygame.transform.scale(img, (img.get_width(), scaled_height))
                    rotated_img = pygame.transform.rotate(scaled_img, angle)
                    rotated_images.append(rotated_img)
                    rects.append(rotated_img.get_rect(center=(player_cx - main_globals['camera_x'] + offset_x, player_cy - main_globals['camera_y'] + offset_y)))

                # create parent
                parent_attack = {
                    'image': rotated_images[0],
                    'flipimage': rotated_images[1],
                    'rect': rects[0],
                    'fliprect': rects[1],
                    # 'expiry': ((delay*hits + expiry*hits)*hits**2)**2, # i dont know man just some high number # actually i calculated this and its 1.5 hours
                    'expiry': pygame.time.get_ticks() + (delay + expiry) * hits + 100,
                    'hits': hits,
                    'hit_enemies': set(),
                    'delay': delay,
                    'next_spawn': pygame.time.get_ticks(),
                    'effect': effect,
                    'draw': False,
                    'flip_next': True,
                    'child_lifetime': expiry
                }
                main_globals['active_special_attacks'].append(parent_attack)

            if type == "knife":
                slash_img = main_globals['special_attack_images']['knife']

                dx = mouse_pos[0] - (player_cx - main_globals['camera_x'])
                dy = mouse_pos[1] - (player_cy - main_globals['camera_y'])
                angle = math.degrees(math.atan2(-dy, dx))
                angle_deg = angle + random.uniform(-15, 15) # slight spread

                # rotate slash to angle
                rotated_slash = pygame.transform.rotate(slash_img, angle_deg)

                # offset from player center by range
                offset_x = math.cos(math.radians(-angle_deg)) * self.range
                offset_y = math.sin(math.radians(-angle_deg)) * self.range

                slash_rect = rotated_slash.get_rect(center=(
                    player_cx - main_globals['camera_x'] + offset_x,
                    player_cy - main_globals['camera_y'] + offset_y
                ))

                # store active slashes
                if 'active_slashes' not in main_globals:
                    main_globals['active_slashes'] = []

                main_globals['active_slashes'].append({
                    'image': rotated_slash,
                    'rect': slash_rect,
                    'expiry': pygame.time.get_ticks() + 150,
                    'hit_enemies': set()
                })

        def pickup(self, player):
            if len(player.weapons) > 0:
                old_weapon = player.weapons.pop(0)
                old_weapon.x = self.x
                old_weapon.y = self.y
                main_globals['weapons_on_map'].append(old_weapon) # swap weapons
                print(f"player dropped {old_weapon.name}, ", end="")
            player.weapons.append(self)

            if self in main_globals['weapons_on_map']:
                main_globals['weapons_on_map'].remove(self)

            print(f"player picked up {self.name}, ", end="")

        def draw(self, screen, x, y):
            screen.blit(main_globals['weapon_images'][self.name], (x, y))

    class Projectile:
        def __init__(self, x, y, angle, speed, damage, owner, image=None, gravity=0, radius=8, pierce=0, pierced=0):
            self.x = x
            self.y = y
            self.angle = angle # in radians
            self.speed = speed
            self.damage = damage
            self.owner = owner
            self.gravity = gravity
            self.alive = True
            self.distance_travelled = 0
            self.hit_enemies = set()
            self.lifetime = 5.0 # max lifetime
            self.radius = radius
            self.pierce = pierce
            self.pierced = pierced
            self.trail_positions = []

            if image:
                self.image = pygame.transform.scale(image, (30, 30))
                self.trail_color = main_globals['get_dominant_color'](image)
            else:
                self.image = None
                self.trail_color = main_globals['get_dominant_color'](None) # defaults to something

        def update(self, main_globals):
            dt = main_globals['dt']

            # movement
            dx = math.cos(self.angle) * self.speed * dt * 60
            dy = math.sin(self.angle) * self.speed * dt * 60

            # apply gravity
            if self.gravity != 0:
                dy += self.gravity * dt * 60

            self.x += dx
            self.y += dy

            self.distance_travelled += math.hypot(dx, dy)
            self.lifetime -= dt

            # check if out of range or lifetime expired
            if self.distance_travelled >= self.owner.range or self.lifetime <= 0:
                self.alive = False

            # update trail
            self.trail_positions.append((self.x, self.y))
            if len(self.trail_positions) > 8: # last 8 positions
                self.trail_positions.pop(0)

        def draw(self, screen, main_globals):
            if len(self.trail_positions) > 1:
                for i in range(len(self.trail_positions) - 1):
                    pos1 = self.trail_positions[i]
                    pos2 = self.trail_positions[i + 1]

                    # convert space
                    x1 = int(pos1[0] - main_globals['camera_x'])
                    y1 = int(pos1[1] - main_globals['camera_y'])
                    x2 = int(pos2[0] - main_globals['camera_x'])
                    y2 = int(pos2[1] - main_globals['camera_y'])

                    # fade based on position in trail
                    alpha_factor = i / len(self.trail_positions)

                    # draw line segment
                    width = max(1, int(5 * alpha_factor))
                    pygame.draw.line(screen, self.trail_color, (x1, y1), (x2, y2), width)

            draw_x = int(self.x - main_globals['camera_x'])
            draw_y = int(self.y - main_globals['camera_y'])

            if self.image:
                rect = self.image.get_rect(center=(draw_x, draw_y))
                screen.blit(self.image, rect)
            else:
                # draw a circle if no image
                pygame.draw.circle(screen, (255, 220, 120), (draw_x, draw_y), self.radius)
                pygame.draw.circle(screen, (255, 200, 80), (draw_x, draw_y), self.radius // 2) # trail

    main_globals['spawn_weapons'] = spawn_weapons
    main_globals['Weapon'] = Weapon
    main_globals['Projectile'] = Projectile

    print("weapons, ", end = "")