# this file is for classes and definitions
# loader 3

# FOR YOUR OWN SAFETY ONLY KEEP 1 FUNCTION OPEN AT ONE TIME 👀👺

import math, random, pygame, pydub, pytweening, scipy, pymunk, pathfinding
from PIL import Image
from pygame import mixer as mx
from pymunk import shapes
import time

def loader3(main_globals):

    dt = main_globals['dt'] # the god of them all

    def draw_apply_button(main_globals, x, y, function):
        font = pygame.font.SysFont(None, 24)
        screen = main_globals['screen']
        if main_globals['apply_button'] is not pygame.rect.Rect(x, y, 100, 40):
            main_globals['apply_button'] = pygame.rect.Rect(x, y, 100, 40)
        pygame.draw.rect(screen, (70, 70, 70), main_globals['apply_button'])
        text_surf = font.render("Apply", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['apply_button'].center)
        screen.blit(text_surf, text_rect)

        if main_globals['apply_button'].collidepoint(main_globals['mouse_pos']) and pygame.mouse.get_pressed()[0]:
            # if function == "resolution":
            #     new_res = main_globals['resolutions'][main_globals['resolution_index']]
            #     main_globals['screen_w'], main_globals['screen_h'] = new_res
            #     print(f"set resolution to {new_res}")

            if function == "framerate":
                new_fps = main_globals['frame_caps'][main_globals['frame_cap_index']]
                main_globals['max_fps'] = new_fps
                print(f"set fps to {new_fps}")

    def draw_hints(main_globals):
        screen = main_globals['screen']
        alpha = main_globals['hint_alpha']
        main_globals['hint_alpha'] = alpha
        block_size = main_globals['key_w_hint'].get_width()

        if main_globals['idle_time'] >= main_globals['idle_threshold']:
            alpha = main_globals.get('hint_alpha', 0)
            alpha += dt * 255 / main_globals['hint_fade_duration']
            if alpha > 255:
                alpha = 255
            main_globals['hint_alpha'] = alpha
            main_globals['key_w_hint'].set_alpha(alpha)
            main_globals['key_a_hint'].set_alpha(alpha)
            main_globals['key_s_hint'].set_alpha(alpha)
            main_globals['key_d_hint'].set_alpha(alpha)
            main_globals['key_e_hint'].set_alpha(alpha)
            main_globals['mouse_left_hint'].set_alpha(alpha)
            main_globals['mouse_blank_hint'].set_alpha(alpha)
            screen.blit(main_globals['key_w_hint'], (10 + block_size, main_globals['screen_h'] - block_size*2 - 10))
            screen.blit(main_globals['key_a_hint'], (10, main_globals['screen_h'] - block_size - 10))
            screen.blit(main_globals['key_s_hint'], (10 + block_size, main_globals['screen_h'] - block_size - 10))
            screen.blit(main_globals['key_d_hint'], (10 + block_size*2, main_globals['screen_h'] - block_size - 10))
            screen.blit(main_globals['key_e_hint'], (10 + block_size*2, main_globals['screen_h'] - block_size*2 - 10))
            # swap mouse image
            ticks = pygame.time.get_ticks() # ms
            if (ticks // 1000) % 2 == 0: # every s
                screen.blit(main_globals['mouse_blank_hint'], (main_globals['screen_w'] - main_globals['mouse_blank_hint'].get_width() - 10, main_globals['screen_h'] - main_globals['mouse_blank_hint'].get_height() - 10))
            else:
                screen.blit(main_globals['mouse_left_hint'], (main_globals['screen_w'] - main_globals['mouse_left_hint'].get_width() - 10, main_globals['screen_h'] - main_globals['mouse_left_hint'].get_height() - 10))
        else:
            main_globals['hint_alpha'] = 0

    def weapon_info(main_globals):
        screen = main_globals['screen']
        screen_w = main_globals['screen_w']
        screen_h = main_globals['screen_h']
        info_bg_x = screen_w - main_globals['weapon_info_bg'].get_width()
        info_bg_y = screen_h - main_globals['weapon_info_bg'].get_height()
        screen.blit(main_globals['weapon_info_bg'], (info_bg_x, info_bg_y))
        weapon = main_globals['player'].weapons[0]
        weapon_image = main_globals['weapon_images'][weapon.name]
        screen.blit(weapon_image, (info_bg_x + 20, info_bg_y + 20))

    def new_mutation(main_globals, effect, number):
        screen = main_globals['screen']
        mutation_alpha = 0
        while mutation_alpha < 255:
            mutation_alpha += 20
            if mutation_alpha > 255:
                mutation_alpha = 255
            screen.fill((0, 0, 0))
            main_globals['mutation_image'].set_alpha(mutation_alpha)
            screen.blit(main_globals['mutation_image'], (0, 0))
            time.sleep(0.01)
            pygame.display.flip()
        player.effect(effect, number)
        time.sleep(1)
        while mutation_alpha > 0:
            mutation_alpha -= 25
            if mutation_alpha < 0:
                mutation_alpha = 0
            screen.fill((0, 0, 0))
            main_globals['mutation_image'].set_alpha(mutation_alpha)
            screen.blit(main_globals['mutation_image'], (0, 0))
            time.sleep(0.01)
            pygame.display.flip()
        main_globals['mutation_image'].set_alpha(255)

    def interact(main_globals, player, x, y, function):
        if distance_to(player, (x, y)) < main_globals['interact_distance']:
            if main_globals['pressed_e'] and not main_globals['is_paused'] and function is not None:
                function()
                print(f"player interacted with something at ({x}, {y})")
                main_globals['pressed_e'] = False

    def spawn_weapons(main_globals):
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        weapon_types = list(main_globals['weapon_images'].keys())

        for row_idx, row in enumerate(main_globals['tilemap']):
            for col_idx, tile_type in enumerate(row):
                if tile_type == 2:
                    center_x = col_idx * ts + main_globals['tile_size'] // 2
                    center_y = row_idx * ts + main_globals['tile_size'] // 2

                    if any(math.isclose(w.x, center_x, abs_tol=1) and math.isclose(w.y, center_y, abs_tol=1) for w in main_globals['weapons_on_map']):
                        continue
                    # pick random
                    weapon_name = random.choice(weapon_types)
                    new_weapon = main_globals['Weapon'](weapon_name)
                    new_weapon.x = center_x
                    new_weapon.y = center_y
                    main_globals['weapons_on_map'].append(new_weapon)
                    print(f"spawned weapon '{weapon_name}' on tile ({row_idx}, {col_idx})")
                    print(f"weapons on map: {main_globals['weapons_on_map']}")

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
        def __repr__(self):
            return f"Weapon('{self.name}')"
        def can_attack(self):
            current_time = time.time()
            return (current_time - self.last_attack_time) >= self.cooldown
        def attack(self, player, main_globals):
            slash_img = main_globals['slash_image']
            if self.can_attack():
                self.last_attack_time = time.time()
                mouse_pos = pygame.mouse.get_pos()
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

                # if main_globals['attack_counter'] == 1:
                #     rotated_slash = pygame.transform.flip(rotated_slash, False, True)
                # elif main_globals['attack_counter'] == 2:
                #     pass # for now otherwise like a jab thing
                # if main_globals['attack_counter'] >= 2:
                #     main_globals['attack_counter'] = 0

                mouse_x_world = mouse_pos[0] + main_globals['camera_x']
                if mouse_x_world < player_cx:
                    main_globals['facing_left'] = True
                else:
                    main_globals['facing_left'] = False

                if 'active_slashes' not in main_globals:
                    main_globals['active_slashes'] = []
                main_globals['active_slashes'].append((rotated_slash, slash_rect, pygame.time.get_ticks() + 150))
            else:
                remaining = round(self.cooldown - (time.time() - self.last_attack_time), 2)
                print(f"{self.name} is on cooldown for {remaining} more seconds")
        def pickup(self, player):
            if len(player.weapons) > 0:
                old_weapon = player.weapons.pop(0)
                old_weapon.x = self.x
                old_weapon.y = self.y
                main_globals['weapons_on_map'].append(old_weapon)
                print(f"player dropped {old_weapon.name}")
            player.weapons.append(self)

            if self in main_globals['weapons_on_map']:
                main_globals['weapons_on_map'].remove(self)

            print(f"player picked up {self.name}")
        def draw(self, screen, x, y):
            screen.blit(main_globals['weapon_images'][self.name], (x, y))

    def distance_to(thing1, thing2):
        def get_xy(thing):
            if hasattr(thing, "x") and hasattr(thing, "y"):
                # if thing is player use center
                if isinstance(thing, main_globals['Player']):
                    return thing.x + main_globals['player_size'] // 2, thing.y + main_globals['player_size'] // 2
                return thing.x, thing.y
            elif isinstance(thing, (tuple, list)) and len(thing) >= 2:
                return thing[0], thing[1]
            else:
                raise TypeError(f"bad type: {thing}")

        x1, y1 = get_xy(thing1)
        x2, y2 = get_xy(thing2)
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    class Enemy():
        def __init__(self, main_globals, x, y, type):
            self.main_globals = main_globals
            self.x = x
            self.y = y
            self.size = main_globals['enemy_size']
            self.health = 50
            self.alive = True
            self.speed = 0.8
            self.type = type
            self.test_image = main_globals['enemy_test_0']
        
        def damaged(self, damage):
            self.health -= damage
            if self.health <= 0:
                self.die()

        def move(self):
            if self.alive:
                pass

        def draw(self):
            if self.alive and self.type == 0:
                pass
        
        def die(self):
            pass # heh
        
    def match_state(main_globals, state): # useless indian naganou function for stages # >:(
        match state:
            case "in menu":
                main_globals['draw_menu'](main_globals, main_globals['mouse_pos'])
            case "in dungeon":
                main_globals['draw_dungeon'](main_globals, main_globals['player'], main_globals['is_paused'], main_globals['facing_left'])
                main_globals['draw_hints'](main_globals)
            case "in settings":
                main_globals['draw_settings'](main_globals, main_globals['mouse_pos'])
            case "dead":
                main_globals['draw_dead'](main_globals, main_globals['mouse_pos'])
            case "in credits":
                main_globals['draw_credits'](main_globals, main_globals['mouse_pos'])

    def player_gif(main_globals):
        frames = []
        player_gif = main_globals['playergif']
        try:
            while True:
                frame = player_gif.convert("RGBA")
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                py_image = pygame.image.fromstring(data, size, mode).convert_alpha()
                frames.append(py_image)
                player_gif.seek(player_gif.tell() + 1)
        except EOFError:
            pass
        main_globals['frames'] = frames

    def musicswitcher(main_globals, indexhere):
        if main_globals['currently_playing_index'] != indexhere:
            mx.music.load(main_globals['musics'][indexhere])
            mx.music.play(-1)
            main_globals['currently_playing_index'] = indexhere

    def get_camera_offset(main_globals, player, tile_size):
        player_center_x = player.x + main_globals['player_size'] // 2
        player_center_y = player.y + main_globals['player_size'] // 2

        tile_x = player_center_x // (tile_size + main_globals['tile_offset'])
        tile_y = player_center_y // (tile_size + main_globals['tile_offset'])
        # camera snaps to the center
        offset_x = tile_x * (tile_size + main_globals['tile_offset']) + tile_size // 2 - main_globals['screen_w'] // 2
        offset_y = tile_y * (tile_size + main_globals['tile_offset']) + tile_size // 2 - main_globals['screen_h'] // 2
        return offset_x, offset_y

    def make_initial_walkable_surface(tilemap, main_globals):
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        tile_size = main_globals['tile_size']
        mask = pygame.Surface((len(tilemap[0]) * ts, len(tilemap) * ts))
        mask.fill((0, 0, 0))  # black is not walkable

        bridge_fraction = 0.25
        bridge_size = int(tile_size * bridge_fraction)

        for row_idx, row in enumerate(tilemap):
            for col_idx, tile_type in enumerate(row):
                if tile_type in main_globals['walkable_tiles']:
                    tx = col_idx * ts
                    ty = row_idx * ts
                    # draw main tile
                    pygame.draw.rect(mask, (0, 255, 0), (tx, ty, tile_size, tile_size))

                    # horizontal bridge
                    if col_idx + 1 < len(row) and tilemap[row_idx][col_idx + 1] in main_globals['walkable_tiles']:
                        if main_globals['bridging'] == True:
                            pygame.draw.rect(mask, (0, 255, 0), (tx + tile_size, ty + tile_size//2 - bridge_size//2,bridge_size, bridge_size))

                    # vertical bridge
                    if row_idx + 1 < len(tilemap) and tilemap[row_idx + 1][col_idx] in main_globals['walkable_tiles']:
                        if main_globals['bridging'] == True:
                            pygame.draw.rect(mask, (0, 255, 0), (tx + tile_size//2 - bridge_size//2, ty + tile_size, bridge_size, bridge_size))
        spawn_weapons(main_globals)
        return mask

    def rebuild_walkable_mask(main_globals):
        print("rebuilding walkable mask")
        tilemap = main_globals['tilemap']
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        mask_width = len(tilemap[0]) * ts
        mask_height = len(tilemap) * ts

        new_mask = pygame.Surface((mask_width, mask_height))
        new_mask.fill((0, 0, 0))

        main_globals['walkable_mask'] = new_mask

        main_globals['walkable_mask'] = main_globals['make_initial_walkable_surface'](tilemap, main_globals)

    def update_tile(main_globals, col_idx, row_idx, new_tile_type):
        # ex. update_tilemap(main_globals, 0, 0, 99)
        # clear old tiles if new tile is a spawn tile

        ts = main_globals['tile_size'] + main_globals['tile_offset']
        center_x = col_idx * ts + main_globals['tile_size'] // 2
        center_y = row_idx * ts + main_globals['tile_size'] // 2

        if new_tile_type == 99:
            print("clearing tiles")
            for i in range(len(main_globals['tilemap'])):
                for j in range(len(main_globals['tilemap'][0])):
                    main_globals['tilemap'][i][j] = 0
            player.respawn()

        main_globals['weapons_on_map'] = [
        w for w in main_globals['weapons_on_map']
            if not (math.isclose(w.x, center_x, abs_tol=1) and math.isclose(w.y, center_y, abs_tol=1))
        ]

        print(f"updating tilemap with {col_idx, row_idx, new_tile_type}")
        main_globals['tilemap'][row_idx][col_idx] = new_tile_type
        main_globals['rebuild_walkable_mask'](main_globals)
        print(f"new tilemap: {main_globals['tilemap']}")

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
            self.score = 0 # hehe

        def move(self, dx, dy):
            new_x = self.x + dx * self.speed * dt * 60
            new_y = self.y + dy * self.speed * dt * 60
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
            if self.shake_timer > 0:
                self.shake_timer -= 1 * dt * 60
                return random.randint(-5, 5), random.randint(-5, 5)
            return 0, 0

        def damaged(self, amount):
            self.health -= amount
            self.shake_timer = 10
            if self.health <= 0:
                self.die()
            else:
                self.main_globals['hurt_sound'].play()

        def die(self):
            self.main_globals['game_stage'] = "dead"
            print("player died")

        def respawn(self):
            print("player respawning")
            main_globals['spawn_set'] = False
            self.alive = True
            self.x = self.main_globals['spawn_x']
            self.y = self.main_globals['spawn_y']
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

    def draw_hud(main_globals, player):
        if player.alive:
            shake_x, shake_y = player.shake()
            screen = main_globals['screen']
            pygame.draw.circle(screen, (20, 20, 20), (100, 100), 80)
            screen.blit(main_globals['font'].render(str(player.health), True, (255, 255, 255)), (120, 200))
            if player.health > 66:
                screen.blit(main_globals['player_health_images'][0], (-50 + shake_x, -50 + shake_y))
            elif player.health > 33:
                screen.blit(main_globals['player_health_images'][1], (-50 + shake_x, -50 + shake_y))
            else:
                screen.blit(main_globals['player_health_images'][2], (-50 + shake_x, -50 + shake_y))

    def draw_vignette(main_globals, player):
        if player.alive:
            max_alpha = 180
            vignette_alpha = max_alpha * (1 - player.health / 100)
            main_globals['vignette'].set_alpha(vignette_alpha)
            main_globals['screen'].blit(main_globals['vignette'], (0, 0))

    def draw_pause_menu(main_globals):
        screen = main_globals['screen']
        pygame.draw.rect(screen, (20, 20, 20), (main_globals['screen_w'] // 2 - main_globals['screen_w'] // 4, main_globals['screen_h'] // 2 - main_globals['screen_h'] // 4, main_globals['screen_w'] // 2, main_globals['screen_h'] // 2), 0)
        screen.blit(main_globals['font'].render("paused", True, (255, 255, 255)), (main_globals['screen_w'] // 2 - 60, main_globals['screen_h'] // 2 - 22))
        mx.music.pause()

    def draw_menu(main_globals, mouse_pos):
        screen = main_globals['screen']
        screen.fill((0, 0, 0))
        if main_globals['menu_bg_can_animate']:
            target_x = main_globals['screen_w'] - main_globals['menu_background'].get_width()
            if main_globals['menu_bg_x'] > target_x:
                main_globals['menu_bg_x'] -= 10
            else:
                main_globals['menu_bg_x'] = target_x
                main_globals['menu_bg_can_animate'] = False
                main_globals['flash_active'] = True

        screen.blit(main_globals['menu_background'], (main_globals['menu_bg_x'], 0))

        if main_globals['flash_active'] and main_globals['flash_alpha'] < 255:
            main_globals['flash_alpha'] += main_globals['flash_speed']
            if main_globals['flash_alpha'] > 255:
                main_globals['flash_alpha'] = 255
            flash_surface = pygame.Surface((main_globals['screen_w'], main_globals['screen_h']))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(255 - main_globals['flash_alpha'])
            screen.blit(flash_surface, (0, 0))
        else:
            main_globals['flash_active'] = False

        if main_globals['menu_bg_can_animate']== False and main_globals['flash_active'] == False:
            # play button
            play_color = (70, 70, 70) if main_globals['play_button'].collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(screen, play_color, main_globals['play_button'])
            text_surf = main_globals['font'].render("Play", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=main_globals['play_button'].center)
            screen.blit(text_surf, text_rect.topleft)
            # settings button
            settings_color = (70, 70, 70) if main_globals['settings_button'].collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(screen, settings_color, main_globals['settings_button'])
            text_surf = main_globals['font'].render("Settings", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=main_globals['settings_button'].center)
            screen.blit(text_surf, text_rect.topleft)
            # kredits batten :robot:
            credits_color = (70, 70, 70) if main_globals['credits_button'].collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(screen, credits_color, main_globals['credits_button'])
            text_surf = main_globals['font'].render("Credits", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=main_globals['credits_button'].center)
            screen.blit(text_surf, text_rect.topleft)

    def draw_credits(main_globals, mouse_pos):
        screen = main_globals['screen']
        to_menu = main_globals['to_menu']
        font = main_globals['font']
        credits_font = pygame.font.SysFont(None, 34)
        screen.fill((0, 0, 0))

        screen.blit(font.render("credits", True, (255, 255, 255)), (20, 20))
        # screen.blit(main_globals['thx'], (540, 0)) # i got the coordinates right first try btw

        # no problem man
        screen.blit(main_globals['thx'], (main_globals['screen_w'] // 2, 0))

        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        text_surf = font.render("To menu", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['to_menu'].center)
        screen.blit(text_surf, text_rect.topleft)

        # credits text
        screen.blit(credits_font.render("shmuby ones", True, (255, 255, 255)), (50, 100))
        screen.blit(credits_font.render("made some code and pixel art", True, (255, 255, 255)), (50, 150))

        screen.blit(credits_font.render("deal bedal maks", True, (255, 255, 255)), (50, 250))
        screen.blit(credits_font.render("some more code and the sfx", True, (255, 255, 255)), (50, 300))

        screen.blit(credits_font.render("SPECIAL THANKS!!!:", True, (255, 255, 255)), (50, 400))

        screen.blit(credits_font.render("you", True, (255, 255, 255)), (50, 500))
        screen.blit(credits_font.render("for playing, my boy", True, (255, 255, 255)), (50, 550))

        # liners (credits edition)
        liner_y = 85
        liner = pygame.Rect(50, liner_y, main_globals['screen_w'] / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 100
        liner = pygame.Rect(50, liner_y, main_globals['screen_w'] / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen_w'] / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 100
        liner = pygame.Rect(50, liner_y, main_globals['screen_w'] / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen_w'] / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen_w'] / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen_w'] / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 100
        liner = pygame.Rect(50, liner_y, main_globals['screen_w'] / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

    def draw_settings(main_globals, mouse_pos):
        screen = main_globals['screen']
        music_slider = main_globals['music_slider']
        to_menu = main_globals['to_menu']
        font = main_globals['font']
        setting_font = pygame.font.SysFont(None, 34)
        screen.fill((0, 0, 0))

        screen.blit(font.render("settings", True, (255, 255, 255)), (20, 20))
        # liners
        liner_y = 85
        liner = pygame.Rect(100, liner_y, main_globals['screen_w'] - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen_w'] - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen_w'] - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen_w'] - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen_w'] - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        # music slider
        pygame.draw.rect(screen, (120, 120, 120), music_slider)
        volume = mx.music.get_volume()
        filled_width = int(music_slider.width * volume)
        filled_rect = pygame.Rect(music_slider.x, music_slider.y, filled_width, music_slider.height)
        pygame.draw.rect(screen, (180, 180, 180), filled_rect)

        mouse_pressed = pygame.mouse.get_pressed()
        if main_globals['dragging_music_slider']:
            relative_x = mouse_pos[0] - music_slider.x
            volume = max(0.0, min(1.0, relative_x / music_slider.width))
            mx.music.set_volume(volume)

        screen.blit(setting_font.render("music volume", True, (255, 255, 255)), (100, 100))
        screen.blit(setting_font.render(f"{int(volume * 100)}%", True, (255, 255, 255)), (main_globals['screen_w'] // 2 + 20, 100))

        # return
        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        text_surf = font.render("To menu", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['to_menu'].center)
        screen.blit(text_surf, text_rect.topleft)

        # hints
        screen.blit(setting_font.render("hints", True, (255, 255, 255)), (100, 150))
        hints_color = (70, 70, 70) if main_globals['hints_button'].collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, hints_color, main_globals['hints_button'])
        text_surf = setting_font.render(main_globals['hints_text'], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['hints_button'].center)
        screen.blit(text_surf, text_rect.topleft)

        # resolution
        # resolution_index = main_globals['resolution_index']
        # step = main_globals['frame_slider_base'].width / (len(main_globals['resolutions'])-1)

        # if main_globals['dragging_resolution_slider']:
        #     relative_x = mouse_pos[0] - main_globals['resolution_slider_base'].x
        #     resolution_index = round(relative_x / step)
        #     resolution_index = max(0, min(resolution_index, len(main_globals['resolutions'])-1))
        #     main_globals['resolution_index'] = resolution_index

        # handle_width = 15
        # handle_height = main_globals['resolution_slider_base'].height + 15
        # handle_x = main_globals['resolution_slider_base'].x + resolution_index * step - handle_width // 2
        # handle_y = main_globals['resolution_slider_base'].y - 7 # y offset
        # handle_rect = pygame.Rect(handle_x, handle_y, handle_width, handle_height)

        # screen.blit(setting_font.render("resolution", True, (255, 255, 255)), (100, 200))
        # resolution_color = (120, 120, 120) if handle_rect.collidepoint(mouse_pos) else (70, 70, 70)
        # pygame.draw.rect(screen, (40, 40, 40), main_globals['resolution_slider_base'])
        # res = main_globals['resolutions'][resolution_index]
        # res_text = f"{res[0]}x{res[1]}"
        # screen.blit(setting_font.render(res_text, True, (255, 255, 255)), (main_globals['screen_w'] // 2 + 20, 200))
        # pygame.draw.rect(screen, resolution_color, handle_rect)
        # main_globals['resolution_slider'] = handle_rect
        # if res != main_globals['resolution']:
        #     draw_apply_button(main_globals, main_globals['screen_w'] // 2 - 120, 200, "resolution")

        # framerate cap
        frame_cap_index = main_globals['frame_cap_index']
        step = main_globals['frame_slider_base'].width / (len(main_globals['frame_caps'])-1)

        if main_globals['dragging_frame_slider']:
            relative_x = mouse_pos[0] - main_globals['frame_slider_base'].x
            frame_cap_index = round(relative_x / step)
            frame_cap_index = max(0, min(frame_cap_index, len(main_globals['frame_caps'])-1))
            main_globals['frame_cap_index'] = frame_cap_index

        handle_width = 15
        handle_height = main_globals['frame_slider_base'].height + 15
        handle_x = main_globals['frame_slider_base'].x + frame_cap_index * step - handle_width // 2
        handle_y = main_globals['frame_slider_base'].y - 7 # y offset
        handle_rect = pygame.Rect(handle_x, handle_y, handle_width, handle_height)

        screen.blit(setting_font.render("framerate cap", True, (255, 255, 255)), (100, 250))
        framerate_color = (120, 120, 120) if handle_rect.collidepoint(mouse_pos) else (70, 70, 70)
        pygame.draw.rect(screen, (40, 40, 40), main_globals['frame_slider_base'])
        frame = main_globals['frame_caps'][frame_cap_index]
        frame_text = f"{frame} fps"
        screen.blit(setting_font.render(frame_text, True, (255, 255, 255)), (main_globals['screen_w'] // 2 + 20, 250))
        pygame.draw.rect(screen, framerate_color, handle_rect)
        main_globals['frame_slider'] = handle_rect
        if frame != main_globals['max_fps']:
            draw_apply_button(main_globals, main_globals['screen_w'] // 2 - 120, 242, "framerate")

    def draw_dead(main_globals, mouse_pos):
        screen = main_globals['screen']
        font = main_globals['font']
        to_menu = main_globals['to_menu']

        screen.blit(font.render("ded", True, (255, 255, 255)), (20, 20))
        main_globals['musicswitcher'](main_globals, 1)

        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        text_surf = font.render("To menu", True, (255, 255, 255))
        screen.blit(text_surf, to_menu.topleft)

    def draw_dungeon(main_globals, player, is_paused, facing_left):
        screen = main_globals['screen']
        camera_x = main_globals['camera_x']
        camera_y = main_globals['camera_y']
        camera_speed = main_globals['camera_speed']
        current_frame = main_globals['current_frame']
        frame_timer = main_globals['frame_timer']
        frame_delay = main_globals['frame_delay']
        frames = main_globals['frames']
        player_size = main_globals['player_size']
        enemy_size = main_globals['enemy_size']
        screen.fill((0, 0, 0))

        target_x, target_y = get_camera_offset(main_globals, player, main_globals['tile_size'])
        camera_x += (target_x - camera_x) * camera_speed
        camera_y += (target_y - camera_y) * camera_speed
        main_globals['camera_x'] = camera_x
        main_globals['camera_y'] = camera_y
        ts = main_globals['tile_size'] + main_globals['tile_offset']

        mask_width, mask_height = main_globals['walkable_mask'].get_size()
        tile_surface = main_globals['tile_images']
        for y in range(0, mask_height, ts):
            for x in range(0, mask_width, ts):
                if main_globals['walkable_mask'].get_at((x, y))[:3] == (0, 255, 0):
                    screen.blit(tile_surface, (x - camera_x, y - camera_y))

        for row_idx, row in enumerate(main_globals['tilemap']):
            for col_idx, tile_type in enumerate(row):
                if tile_type == 99: # makes player spawn here 
                    if main_globals['spawn_set'] == False:
                        ts = main_globals['tile_size'] + main_globals['tile_offset']
                        main_globals['spawn_x'] = col_idx * ts + (main_globals['tile_size'] - player_size) // 2
                        main_globals['spawn_y'] = row_idx * ts + (main_globals['tile_size'] - player_size) // 2
                        if main_globals.get('player') is None:
                            main_globals['player'] = main_globals['Player'](main_globals, main_globals['spawn_x'], main_globals['spawn_y'])
                        else:
                            main_globals['player'].x = main_globals['spawn_x']
                            main_globals['player'].y = main_globals['spawn_y']
                        main_globals['spawn_set'] = True

                elif tile_type == 2:
                    screen.blit(main_globals['pedistal_image'], (col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_width() // 2, row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_height() // 2 + 50))

                elif tile_type == 3: # okay...
                    main_globals["enemy_spawn_x"] = col_idx * ts + (main_globals['tile_size'] - enemy_size) // 2
                    main_globals["enemy_spawn_y"] = row_idx * ts + (main_globals['tile_size'] - enemy_size) // 2

                    enemy.x = main_globals['enemy_spawn_x']     
                    enemy.y = main_globals['enemy_spawn_y']

                    
        # draw weapons
        for weapon in main_globals['weapons_on_map'][:]:
            weapon_image = main_globals['weapon_images'][weapon.name]
            draw_x = weapon.x - weapon_image.get_width() // 2 - camera_x + 15
            draw_y = weapon.y - weapon_image.get_height() // 2 - camera_y
            weapon.draw(screen, draw_x, draw_y)

            # interact image
            if distance_to(player, weapon) < main_globals['interact_distance']:
                screen.blit(main_globals['interact_image'], (draw_x, draw_y + weapon_image.get_height()))

                # pick up weapon
                main_globals['interact'](main_globals, player, weapon.x, weapon.y, lambda w=weapon: w.pickup(player))

        # draw slash
        if 'active_slashes' in main_globals:
            now = pygame.time.get_ticks()  # current time in ms
            still_active = []
            for slash_img, slash_rect, expiry in main_globals['active_slashes']:
                if now < expiry:
                    screen.blit(slash_img, slash_rect)
                    still_active.append((slash_img, slash_rect, expiry))
            main_globals['active_slashes'] = still_active

        # animate player
        frame_timer += 1
        if frame_timer >= frame_delay:
            frame_timer = 0
            if main_globals['moving_up'] or main_globals['moving_down'] or main_globals['moving_left'] or main_globals['moving_right']:
                current_frame = (current_frame + 1) % len(frames)
            else:
                current_frame = 1
        main_globals['frame_timer'] = frame_timer
        main_globals['current_frame'] = current_frame

        player_frame = pygame.transform.scale(frames[current_frame], (player_size * 3, player_size * 3))
        if main_globals['facing_left']:
            player_frame = pygame.transform.flip(player_frame, True, False)

        offset_x = (player_size * 3 - player_size) // 2
        offset_y = (player_size * 3 - player_size) // 2
        shake_x, shake_y = player.shake()
        draw_x = player.x - camera_x - offset_x + shake_x
        draw_y = player.y - camera_y - offset_y + shake_y
        if facing_left:
            draw_x += 30
        else:
            draw_x -= 30

        screen.blit(player_frame, (draw_x, draw_y))
        if len(player.weapons) > 0:
            weapon = player.weapons[0]
            weapon_image = main_globals['weapon_images'][weapon.name]
            scale_fraction = 1.8
            weapon_image = pygame.transform.scale(weapon_image, ((main_globals['player_size'] // 2) * scale_fraction, (main_globals['player_size'] // 2) * scale_fraction))
            weapon_image = pygame.transform.rotate(weapon_image, 65)
            weapon_image = pygame.transform.flip(weapon_image, True, False)

            weapon_x = draw_x + player_size + 40 # x offset
            weapon_y = draw_y + player_size // 2 + 36  # y offset

            if facing_left:
                weapon_image = pygame.transform.flip(weapon_image, True, False)
                weapon_x -= 90

            screen.blit(weapon_image, (weapon_x, weapon_y))

        if is_paused == False:
            draw_vignette(main_globals, player)
            mx.music.unpause()
            dx = dy = 0
            if main_globals['moving_up']: dy -= 1
            if main_globals['moving_down']: dy += 1
            if main_globals['moving_left']:
                dx -= 1
                main_globals['facing_left'] = True
            if main_globals['moving_right']:
                dx += 1
                main_globals['facing_left'] = False
            player.move(dx, dy)
            draw_hud(main_globals, player)
        else:
            draw_pause_menu(main_globals)

    player = Player(main_globals, main_globals['spawn_x'], main_globals['spawn_y'])
    enemy = Enemy(main_globals, main_globals['enemy_spawn_x'], main_globals['enemy_spawn_y'], 0)

    main_globals['player_gif'] = player_gif
    main_globals['draw_menu'] = draw_menu
    main_globals['draw_dungeon'] = draw_dungeon
    main_globals['draw_hud'] = draw_hud
    main_globals['draw_pause_menu'] = draw_pause_menu
    main_globals['draw_settings'] = draw_settings
    main_globals['draw_credits'] = draw_credits
    main_globals['draw_dead'] = draw_dead
    main_globals['musicswitcher'] = musicswitcher
    main_globals['get_camera_offset'] = get_camera_offset
    main_globals['draw_vignette'] = draw_vignette
    main_globals['make_initial_walkable_surface'] = make_initial_walkable_surface
    main_globals['update_tile'] = update_tile
    main_globals['rebuild_walkable_mask'] = rebuild_walkable_mask
    main_globals['match_state'] = match_state
    main_globals['spawn_weapons'] = spawn_weapons
    main_globals['interact'] = interact
    main_globals['new_mutation'] = new_mutation
    main_globals['weapon_info'] = weapon_info
    main_globals['draw_hints'] = draw_hints
    main_globals['draw_credits'] = draw_credits
    main_globals['draw_apply_button'] = draw_apply_button

    main_globals['player'] = player
    main_globals['enemy'] = enemy
    main_globals['Player'] = Player 
    main_globals['Weapon'] = Weapon


    print("loader3 file loaded")