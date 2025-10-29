# this file is for classes and definitions
# loader 3

# FOR YOUR OWN SAFETY ONLY KEEP 1 FUNCTION OPEN AT ONE TIME 👀👺

try:
    import math, random, pygame, pymunk, pathfinding, time
    from pygame import mixer as mx
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

def loader3(main_globals):

    dt = main_globals['dt'] # the god of them all

    """
    def get_random_walkable_position(main_globals): # DID NOT WORK 
        mask = main_globals['walkable_mask']
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        mask_width, mask_height = mask.get_size()

        while True:
            x = random.randrange(0, mask_width, ts)
            y = random.randrange(0, mask_height, ts)
            if mask.get_at((x, y))[:3] == (0, 255, 0):
                return x, y
    """

    class Shop:
        def __init__(self, main_globals, x = None, y = None):
            self.image = main_globals['shop_holder']
            self.x = x
            self. y = y

        def draw_shop(self, main_globals):
            screen = main_globals['screen']
            screen.fill((0, 0, 0))

    def spawn_blood_particles(space, player_x, player_y, player_size, amount=10):
        particles = []
        # bloods at player lower center
        spawn_x = player_x + player_size // 2
        spawn_y = player_y + player_size + 25

        # y where they stop
        landing_y = spawn_y + 30

        for _ in range(amount):
            # random size
            radius = random.randint(1, 2)
            body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
            body.position = spawn_x, spawn_y
            shape = pymunk.Circle(body, radius)
            shape.elasticity = 0.3
            shape.friction = 0.5

            impulse_x = random.uniform(-30, 30)
            impulse_y = -random.uniform(100, 200)
            body.apply_impulse_at_local_point((impulse_x, impulse_y))

            body.landing_y = landing_y
            space.add(body, shape)
            # random lifetime in s
            lifetime = random.uniform(1, 2)

            # random red
            color = (200 + random.randint(-30, 30), 0, 0)
            max_lifetime = lifetime
            particles.append((body, shape, color, lifetime, max_lifetime))

        return particles

    def save(main_globals, **new_data):
        pos = (main_globals['save_image'].get_width(), main_globals['screen'].get_height() - main_globals['save_image'].get_height())
        screen = main_globals['screen']
        connector = main_globals['connector_instance']

        data = connector.get_data()
        data.update(new_data)
        connector.set_data(data)
        connector.save_data()

        start = time.time()
        duration = 1.0
        while time.time() - start < duration:
            angle = ((time.time() - start) * 720) % 360
            rotated = pygame.transform.rotate(main_globals['save_image'], angle)
            rect = rotated.get_rect(center=pos)
            screen.blit(rotated, rect)
            pygame.display.flip()

        print(f"saved {new_data}")
        return True

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

            if function == "resolution":
                new_res = main_globals['resolutions'][main_globals['resolution_index']]
                main_globals['resolution'] = new_res
                save(main_globals, resolution=new_res)
                print(f"set resolution to {new_res}")

            elif function == "framerate":
                new_fps = main_globals['frame_caps'][main_globals['frame_cap_index']]
                main_globals['max_fps'] = new_fps
                save(main_globals, max_fps=new_fps)
                print(f"set fps to {new_fps}")

            elif function == "music":
                new_volume = main_globals.get('volume_preview', main_globals.get('music_volume', mx.music.get_volume()))
                main_globals['music_volume'] = new_volume
                main_globals.pop('volume_preview', None)
                mx.music.set_volume(new_volume)
                save(main_globals, music=new_volume)
                print(f"set music volume to {new_volume}")

    # im not sure if they work or not but they are kind of useless rn
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
            screen.blit(main_globals['key_w_hint'], (10 + block_size, main_globals['screen'].get_height() - block_size*2 - 10))
            screen.blit(main_globals['key_a_hint'], (10, main_globals['screen'].get_height() - block_size - 10))
            screen.blit(main_globals['key_s_hint'], (10 + block_size, main_globals['screen'].get_height() - block_size - 10))
            screen.blit(main_globals['key_d_hint'], (10 + block_size*2, main_globals['screen'].get_height() - block_size - 10))
            screen.blit(main_globals['key_e_hint'], (10 + block_size*2, main_globals['screen'].get_height() - block_size*2 - 10))
            # swap mouse image
            ticks = pygame.time.get_ticks() # ms
            if (ticks // 1000) % 2 == 0: # every s
                screen.blit(main_globals['mouse_blank_hint'], (main_globals['screen'].get_width() - main_globals['mouse_blank_hint'].get_width() - 10, main_globals['screen'].get_height() - main_globals['mouse_blank_hint'].get_height() - 10))
            else:
                screen.blit(main_globals['mouse_left_hint'], (main_globals['screen'].get_width() - main_globals['mouse_left_hint'].get_width() - 10, main_globals['screen'].get_height() - main_globals['mouse_left_hint'].get_height() - 10))
        else:
            main_globals['hint_alpha'] = 0

    def weapon_info(main_globals):
        screen = main_globals['screen']
        screen_w = main_globals['screen'].get_width()
        screen_h = main_globals['screen'].get_height()
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
        main_globals['player'].effect(effect, number)
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
        offset_x = tile_x * (tile_size + main_globals['tile_offset']) + tile_size // 2 - main_globals['screen'].get_width() // 2
        offset_y = tile_y * (tile_size + main_globals['tile_offset']) + tile_size // 2 - main_globals['screen'].get_height() // 2
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
        main_globals['spawn_weapons'](main_globals)
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
            main_globals['player'].respawn()

        main_globals['weapons_on_map'] = [
        w for w in main_globals['weapons_on_map']
            if not (math.isclose(w.x, center_x, abs_tol=1) and math.isclose(w.y, center_y, abs_tol=1))
        ]

        print(f"updating tilemap with {col_idx, row_idx, new_tile_type}")
        main_globals['tilemap'][row_idx][col_idx] = new_tile_type
        main_globals['rebuild_walkable_mask'](main_globals)
        print(f"new tilemap: {main_globals['tilemap']}")

    def draw_hud(main_globals, player):
        if player.alive:
            shake_x, shake_y = player.shake()
            screen = main_globals['screen']
            pygame.draw.circle(screen, (20, 20, 20), (100, 100), 80)
            screen.blit(main_globals['font'].render(str(player.health), True, (255, 255, 255)), (120, 200))
            screen.blit(main_globals['font'].render(str(player.wealth), True, (255, 215, 0)), (120, 250))
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
        pygame.draw.rect(screen, (20, 20, 20), (main_globals['screen'].get_width() // 2 - main_globals['screen'].get_width() // 4, main_globals['screen'].get_height() // 2 - main_globals['screen'].get_height() // 4, main_globals['screen'].get_width() // 2, main_globals['screen'].get_height() // 2), 0)
        screen.blit(main_globals['font'].render("paused", True, (255, 255, 255)), (main_globals['screen'].get_width() // 2 - 60, main_globals['screen'].get_height() // 2 - 22))
        mx.music.pause()

    def draw_menu(main_globals, mouse_pos):
        screen = main_globals['screen']
        screen.fill((0, 0, 0))
        if main_globals['menu_bg_can_animate']:
            target_x = main_globals['screen'].get_width() - main_globals['menu_background'].get_width()
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
            flash_surface = pygame.Surface((main_globals['screen'].get_width(), main_globals['screen'].get_height()))
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
        screen.blit(main_globals['thx'], (main_globals['screen'].get_width() // 2, 0))

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
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 100
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 100
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 100
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
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
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        # music slider
        pygame.draw.rect(screen, (120, 120, 120), music_slider)
        volume = main_globals.get('volume_preview', main_globals.get('music_volume', mx.music.get_volume()))
        filled_width = int(music_slider.width * volume)
        filled_rect = pygame.Rect(music_slider.x, music_slider.y, filled_width, music_slider.height)
        pygame.draw.rect(screen, (180, 180, 180), filled_rect)

        if main_globals['dragging_music_slider']:
            relative_x = mouse_pos[0] - music_slider.x
            volume = max(0.0, min(1.0, relative_x / music_slider.width))
            main_globals['volume_preview'] = volume

        if 'volume_preview' in main_globals and main_globals['volume_preview'] != main_globals.get('music_volume', mx.music.get_volume()):
            draw_apply_button(main_globals, main_globals['screen'].get_width() // 2 - 120, 90, "music")

        screen.blit(setting_font.render("music volume", True, (255, 255, 255)), (100, 100))
        screen.blit(setting_font.render(f"{int(volume * 100)}%", True, (255, 255, 255)), (main_globals['screen'].get_width() // 2 + 20, 100))

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
        resolution_index = main_globals['resolution_index']
        step = main_globals['resolution_slider_base'].width / (len(main_globals['resolutions']) - 1)

        if main_globals['dragging_resolution_slider']:
            relative_x = mouse_pos[0] - main_globals['resolution_slider_base'].x
            resolution_index = round(relative_x / step)
            resolution_index = max(0, min(resolution_index, len(main_globals['resolutions']) - 1))
            main_globals['resolution_index'] = resolution_index

        handle_width = 15
        handle_height = main_globals['resolution_slider_base'].height + 15
        handle_x = main_globals['resolution_slider_base'].x + resolution_index * step - handle_width // 2
        handle_y = main_globals['resolution_slider_base'].y - 7  # y offset
        handle_rect = pygame.Rect(handle_x, handle_y, handle_width, handle_height)

        screen.blit(setting_font.render("resolution", True, (255, 255, 255)), (100, 200))
        resolution_color = (120, 120, 120) if handle_rect.collidepoint(mouse_pos) else (70, 70, 70)
        pygame.draw.rect(screen, (40, 40, 40), main_globals['resolution_slider_base'])
        res = main_globals['resolutions'][resolution_index]
        res_text = f"{res[0]}x{res[1]}"
        screen.blit(setting_font.render(res_text, True, (255, 255, 255)), (main_globals['screen'].get_width() // 2 + 20, 200))
        pygame.draw.rect(screen, resolution_color, handle_rect)
        main_globals['resolution_slider'] = handle_rect
        if main_globals['resolution'] != res:
            draw_apply_button(main_globals, main_globals['screen'].get_width() // 2 - 120, 190, "resolution")

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
        screen.blit(setting_font.render(frame_text, True, (255, 255, 255)), (main_globals['screen'].get_width() // 2 + 20, 250))
        pygame.draw.rect(screen, framerate_color, handle_rect)
        main_globals['frame_slider'] = handle_rect
        if frame != main_globals['max_fps']:
            draw_apply_button(main_globals, main_globals['screen'].get_width() // 2 - 120, 242, "framerate")

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

    shop = Shop(main_globals)

    main_globals['player_gif'] = player_gif
    main_globals['draw_menu'] = draw_menu
    main_globals['draw_hud'] = draw_hud
    main_globals['draw_pause_menu'] = draw_pause_menu
    main_globals['draw_settings'] = draw_settings
    main_globals['draw_credits'] = draw_credits
    main_globals['draw_shop'] = Shop.draw_shop
    main_globals['draw_dead'] = draw_dead
    main_globals['musicswitcher'] = musicswitcher
    main_globals['get_camera_offset'] = get_camera_offset
    main_globals['draw_vignette'] = draw_vignette
    main_globals['make_initial_walkable_surface'] = make_initial_walkable_surface
    main_globals['update_tile'] = update_tile
    main_globals['rebuild_walkable_mask'] = rebuild_walkable_mask
    main_globals['interact'] = interact
    main_globals['new_mutation'] = new_mutation
    main_globals['weapon_info'] = weapon_info
    main_globals['draw_hints'] = draw_hints
    main_globals['draw_credits'] = draw_credits
    main_globals['draw_apply_button'] = draw_apply_button
    main_globals['save'] = save
    main_globals['spawn_blood_particles'] = spawn_blood_particles
    main_globals['distance_to'] = distance_to

    main_globals['shop'] = shop
    main_globals['Shop'] = Shop


    print("loader3 file loaded")