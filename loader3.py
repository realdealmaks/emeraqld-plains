# this file is for random parts of the game

# loader 3

try:
    import math, random, pygame, pymunk, pathfinding, time
    from pygame import mixer as mx
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

def loader3(main_globals):

    font = pygame.font.Font("assets/font/editundo.ttf", 24)
    bigfont = pygame.font.Font("assets/font/editundo.ttf", 48)
    setting_font = credits_font = pygame.font.Font("assets/font/editundo.ttf", 28)
    smallfont = pygame.font.Font("assets/font/editundo.ttf", 22)

    def draw_minimap(main_globals, tilemap, player):
        screen = main_globals['screen']

        background_rect_surf = pygame.Surface((75, 75), pygame.SRCALPHA)
        background_rect_surf.fill((50, 50, 50, 128)) # color and alpha

        tl_size = 10
        tl_spacing = 2 # spacing between tiles
        padding = 18 # offset from top right corner

        rows = len(tilemap)
        cols = len(tilemap[0])

        # player tile
        player_tile_x = (player.x + main_globals['player_size'] // 2) // (main_globals['tile_size'] + main_globals['tile_offset'])
        player_tile_y = (player.y + main_globals['player_size'] // 2) // (main_globals['tile_size'] + main_globals['tile_offset'])

        # view around player
        view_radius = 2
        start_x = max(player_tile_x - view_radius, 0)
        start_y = max(player_tile_y - view_radius, 0)
        end_x = min(player_tile_x + view_radius, cols - 1)
        end_y = min(player_tile_y + view_radius, rows - 1)

        offset_x = screen.get_width() - background_rect_surf.get_width() - padding
        offset_y = padding

        center_x = offset_x + background_rect_surf.get_width() // 2
        center_y = offset_y + background_rect_surf.get_height() // 2

        screen.blit(background_rect_surf, (offset_x, offset_y))

        # draw tiles
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if tilemap[y][x] in main_globals['walkable_tiles']:
                    tile_color = (90, 90, 90) # default
                    if (x, y) == (player_tile_x, player_tile_y): # for tile with player
                        tile_color = (140, 140, 240)
                    elif (x, y) in main_globals['active_tiles']: # for explored tiles
                        tile_color = (170, 170, 170)

                    rel_x = (x - player_tile_x) * (tl_size + tl_spacing)
                    rel_y = (y - player_tile_y) * (tl_size + tl_spacing)

                    rect = pygame.Rect(
                        center_x + rel_x - tl_size // 2,
                        center_y + rel_y - tl_size // 2,
                        tl_size,
                        tl_size
                    )
                    pygame.draw.rect(screen, tile_color, rect)

    def is_on_active_tile(main_globals, x, y):
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        tile_x = (x + main_globals['player_size'] // 2) // ts
        tile_y = (y + main_globals['player_size'] // 2) // ts
        tile = (tile_x, tile_y)

        return tile in main_globals['active_tiles']

    def reset(main_globals):
        main_globals['player'].health = 100
        main_globals['player'].weapons = []
        main_globals['tilemap'] = main_globals['start_tilemap']
        main_globals['spawn_set'] = False
        main_globals['player'].wealth = 0
        main_globals['groups_spawned'] = 0
        main_globals['enemy_list'] = []
        main_globals['in_shop'] = False
        main_globals['blood_particles'] = []
        main_globals['money_texts'] = []
        main_globals['Weapon'] = None
        main_globals['facing_left'] = False
        main_globals['make_initial_walkable_surface'](main_globals['tilemap'], main_globals)
        main_globals['is_paused'] = False

    def execute():
        try:
            main_globals['is_paused'] = True

            cmd = input("> ")

            while cmd not in ["q", "quit", "exit", "x"]:
                if cmd == "help":
                    print("\nbranching commands:\n"
                            "weapon -> weapon name\n"
                            "money -> amount\n"
                            "health -> amount\n"
                            "stage -> stage name\n"

                            "\nregular commands:\n"
                            "rebuild - rebuild floor\n"
                            "reset - reset dungeon\n"
                            "respawn - respawn player\n"
                            "ccache - clear data\n"

                            "\nexit commands:\n"
                            "quit, q, exit, x\n"
                        )

                elif cmd == "weapon":
                    weapon_name = input(">> name: ")
                    new_weapon = main_globals['Weapon'](weapon_name)
                    main_globals['player'].weapon = new_weapon
                    main_globals['player'].weapons = [new_weapon]
                    print("set")

                elif cmd == "money":
                    main_globals['give_money'](int(input(">> amount: "))), print("set")

                elif cmd == "health":
                    main_globals['player'].health = int(input(">> amount: ")), print("set")

                elif cmd == "rebuild":
                    main_globals['remake_floor'](), print("done")

                elif cmd == "reset":
                    main_globals['reset'](main_globals), print("done")

                elif cmd == "stage":
                    main_globals['game_stage'] = input(">> stage: "), print("done")

                elif cmd == "respawn":
                    main_globals['player'].respawn(), print("done")

                elif cmd == "ccache":
                    for i in main_globals['connector_instance'].data:
                        main_globals['save'](main_globals, **{i: main_globals['connector_instance'].default_data[i]})

                else:
                    print("invalid")

                cmd = input("> ")

            main_globals['is_paused'] = False

        except Exception as e:
            main_globals['is_paused'] = False
            print(e)

    def give_money(amount):  # some indicator for getting rich 🤑
        if main_globals['money_texts']:
            existing = main_globals['money_texts'][0]
            existing['amount'] += amount
            existing['text'] = font.render("+" + str(existing['amount']), True, (255, 255, 0))
            existing['timer'] = 3.0 # reset timer
        else:
            main_globals['money_texts'] = [{
                'amount': amount,
                'text': font.render("+" + str(amount), True, (255, 255, 0)),
                'timer': 3.0
            }]

    def remake_floor():
        tilemap = main_globals['tilemap']
        rows = len(tilemap)
        cols = len(tilemap[0])
        min_distance = 4  # minimum distance between start and end
        min_straight = 1  # minimum distance before turning again
        tile_choices = [1, 2, 3] # tiles the path can be filled with
        tile_probs = [0.5, 0.1, 0.4] # in order * 100 in %

        # pick start and end far enough apart
        while True:
            start_r = random.randint(0, rows - 1)
            start_c = random.randint(0, cols - 1)
            end_r = random.randint(0, rows - 1)
            end_c = random.randint(0, cols - 1)
            distance = abs(start_r - end_r) + abs(start_c - end_c)
            if distance >= min_distance:
                break

        # mark start and end
        update_tile(main_globals, start_c, start_r, 99)
        update_tile(main_globals, end_c, end_r, 98)

        # r = hoRizontal c = vertiCal
        current_r, current_c = start_r, start_c
        current_dir = 'r' if random.random() < 0.5 else 'c'
        straight_count = 0

        path_tiles = []

        while (current_r, current_c) != (end_r, end_c):
            dr = end_r - current_r
            dc = end_c - current_c

            can_turn = straight_count >= min_straight
            if current_dir == 'r' and dc != 0:
                step = 1 if dc > 0 else -1
                current_c += step
                straight_count += 1
            elif current_dir == 'c' and dr != 0:
                step = 1 if dr > 0 else -1
                current_r += step
                straight_count += 1
            elif can_turn:
                if current_dir == 'r' and dr != 0:
                    step = 1 if dr > 0 else -1
                    current_r += step
                    current_dir = 'c'
                    straight_count = 1
                elif current_dir == 'c' and dc != 0:
                    step = 1 if dc > 0 else -1
                    current_c += step
                    current_dir = 'r'
                    straight_count = 1
            else:
                if current_dir == 'r' and dc == 0 and dr != 0:
                    step = 1 if dr > 0 else -1
                    current_r += step
                    current_dir = 'c'
                    straight_count = 1
                elif current_dir == 'c' and dr == 0 and dc != 0:
                    step = 1 if dc > 0 else -1
                    current_c += step
                    current_dir = 'r'
                    straight_count = 1

            # make tile in the path a random one
            if tilemap[current_r][current_c] not in (99, 98):
                tile_value = random.choices(tile_choices, weights=tile_probs)[0]
                path_tiles.append((current_r, current_c, tile_value))

        # force at least 1 tile 2 or 3
        if not any(tile[2] in (2, 3) for tile in path_tiles):
            idx = random.randint(0, len(path_tiles) - 1)
            r, c, _ = path_tiles[idx]
            path_tiles[idx] = (r, c, random.choice([2, 3]))

        # update tilemap
        for r, c, val in path_tiles:
            update_tile(main_globals, c, r, val)

        print("new tilemap is:")
        main_globals['current_floor'] += 1 # save floors
        if main_globals['current_floor'] > main_globals['best_floor']:
            main_globals['best_floor'] = main_globals['current_floor']
            save(main_globals, best_floor=main_globals['best_floor'])
        for i in range(len(main_globals['tilemap'])):
            print(main_globals['tilemap'][i])
        main_globals['rebuild_walkable_mask'](main_globals)

    def draw_mode_selection(main_globals, mouse_pos):
        screen = main_globals['screen']
        screen.fill((0, 0, 0))
        dt = main_globals['dt']

        base_size = (200, 50)
        hover_size = (220, 60)
        anim_speed = 5.5
        hover_scale = 1.1
        shrink_scale = 0.9

        main_globals.setdefault('mode1_scaled', main_globals['mode1img'])
        main_globals.setdefault('mode2_scaled', main_globals['mode2img'])

        main_globals.setdefault('mode1_last_size', main_globals['mode1img'].get_size())
        main_globals.setdefault('mode2_last_size', main_globals['mode2img'].get_size())

        button1 = main_globals['mode1button']
        button2 = main_globals['mode2button']
        hover1 = button1.collidepoint(mouse_pos)
        hover2 = button2.collidepoint(mouse_pos)

        for key, value in [
            ('mode1_scale', 1.0),
            ('mode2_scale', 1.0),
            ('mode1_dim', 150),
            ('mode2_dim', 150),
            ('mode1_btn_size', list(base_size)),
            ('mode2_btn_size', list(base_size))
        ]:
            if key not in main_globals:
                main_globals[key] = value

        if hover1:
            target_scale1, target_scale2 = hover_scale, shrink_scale
            target_dim1, target_dim2 = 0, 150
        elif hover2:
            target_scale1, target_scale2 = shrink_scale, hover_scale
            target_dim1, target_dim2 = 150, 0
        else:
            target_scale1 = target_scale2 = 1.0
            target_dim1 = target_dim2 = 150

        main_globals['mode1_scale'] += (target_scale1 - main_globals['mode1_scale']) * anim_speed * dt
        main_globals['mode2_scale'] += (target_scale2 - main_globals['mode2_scale']) * anim_speed * dt
        main_globals['mode1_dim'] += (target_dim1 - main_globals['mode1_dim']) * anim_speed * dt
        main_globals['mode2_dim'] += (target_dim2 - main_globals['mode2_dim']) * anim_speed * dt

        new_size1 = (
            int(main_globals['mode1img'].get_width() * main_globals['mode1_scale']),
            int(main_globals['mode1img'].get_height() * main_globals['mode1_scale'])
        )
        new_size2 = (
            int(main_globals['mode2img'].get_width() * main_globals['mode2_scale']),
            int(main_globals['mode2img'].get_height() * main_globals['mode2_scale'])
        )

        new_size1 = (max(1, new_size1[0]), max(1, new_size1[1]))
        new_size2 = (max(1, new_size2[0]), max(1, new_size2[1]))

        if new_size1 != main_globals['mode1_last_size']:
            main_globals['mode1_scaled'] = pygame.transform.smoothscale(
                main_globals['mode1img'], new_size1
            )
            main_globals['mode1_last_size'] = new_size1

        if new_size2 != main_globals['mode2_last_size']:
            main_globals['mode2_scaled'] = pygame.transform.smoothscale(
                main_globals['mode2img'], new_size2
            )
            main_globals['mode2_last_size'] = new_size2

        bg1 = main_globals['mode1_scaled']
        bg2 = main_globals['mode2_scaled']

        bg1_pos = (0, 0)
        bg2_pos = (screen.get_width() - bg2.get_width(), 0)

        screen.blit(bg1, bg1_pos)
        if main_globals['mode1_dim'] > 0:
            dim1 = pygame.Surface(bg1.get_size(), pygame.SRCALPHA)
            dim1.fill((0, 0, 0, int(main_globals['mode1_dim'])))
            screen.blit(dim1, bg1_pos)

        screen.blit(bg2, bg2_pos)
        if main_globals['mode2_dim'] > 0:
            dim2 = pygame.Surface(bg2.get_size(), pygame.SRCALPHA)
            dim2.fill((0, 0, 0, int(main_globals['mode2_dim'])))
            screen.blit(dim2, bg2_pos)

        for key, target in [('mode1_btn_size', hover_size if hover1 else base_size), ('mode2_btn_size', hover_size if hover2 else base_size)]:
            curr = main_globals[key]
            curr[0] += (target[0] - curr[0]) * anim_speed * dt
            curr[1] += (target[1] - curr[1]) * anim_speed * dt

        button1.width, button1.height = map(int, main_globals['mode1_btn_size'])
        button1.topleft = (screen.get_width() // 4 - base_size[0] // 2, screen.get_height() // 2)
        color1 = (70, 70, 70) if hover1 else (40, 40, 40)
        pygame.draw.rect(screen, color1, button1, border_radius=8)
        text_surf1 = main_globals['font'].render("1", True, (255, 255, 255))
        screen.blit(text_surf1, text_surf1.get_rect(center=button1.center))

        button2.width, button2.height = map(int, main_globals['mode2_btn_size'])
        button2.left = screen.get_width() * 3 // 4 - base_size[0] // 2
        if hover2:
            button2.left -= button2.width - base_size[0]
        button2.top = screen.get_height() // 2
        color2 = (70, 70, 70) if hover2 else (40, 40, 40)
        pygame.draw.rect(screen, color2, button2, border_radius=8)
        text_surf2 = main_globals['font'].render("2", True, (255, 255, 255))
        screen.blit(text_surf2, text_surf2.get_rect(center=button2.center))

    def transition_to_dungeon(main_globals, screen):

        if not main_globals.get('transition_active', False):
            return

        dt = main_globals['dt']

        for key, default in [
            ('transition_phase', 'in'),
            ('transition_progress', 0.0),
            ('transition_hold_timer', 0.0)
        ]:
            if key not in main_globals:
                main_globals[key] = default

        phase = main_globals['transition_phase']
        speed = main_globals.get('transition_speed', 2.2)

        if phase == "in":
            main_globals['transition_progress'] += speed * dt
            if main_globals['transition_progress'] >= 1.0:
                main_globals['transition_progress'] = 1.0
                main_globals['transition_phase'] = "hold"
                main_globals['transition_hold_timer'] = 0.0

        elif phase == "hold":
            main_globals['transition_hold_timer'] += dt
            if main_globals['transition_hold_timer'] >= main_globals.get('transition_hold_duration', 0.5):
                main_globals['transition_phase'] = "out"
                main_globals['transition_progress'] = 1.0

                selected_mode = main_globals.get('selected_mode')
                if selected_mode == 1: # send to dungeon
                    player = main_globals['player']
                    player.weapons = []
                    player.respawn()
                    player.effect("healfull", 0)
                    main_globals['musicswitcher'](main_globals, 0)
                    main_globals['game_stage'] = "in dungeon"
                    main_globals['tilemap'] = main_globals['start_tilemap']
                    mx.music.unpause()
                elif selected_mode == 2: # send to yo mama hous
                    pass

        elif phase == "out":
            main_globals['transition_progress'] -= speed * dt
            if main_globals['transition_progress'] <= 0.0:
                main_globals['transition_progress'] = 0.0
                main_globals['transition_active'] = False
                main_globals['player'].alive = True
                main_globals['player'].locked = False
                main_globals['transition_phase'] = "in" # reset ...for next time

        screen_width, screen_height = screen.get_size()
        progress = main_globals['transition_progress']
        side = main_globals.get('transition_side', 'left')

        if side == 'left':
            rect = pygame.Rect(0, 0, int(screen_width * progress), screen_height)
        else:
            rect = pygame.Rect(screen_width - int(screen_width * progress), 0, int(screen_width * progress), screen_height)

        pygame.draw.rect(screen, (0, 0, 0), rect)

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

        for i in range(amount):
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

    def save(main_globals, **new_data): # save data to json
        connector = main_globals['connector_instance']

        data = connector.get_data()
        data.update(new_data)
        connector.set_data(data)
        connector.save_data()

        print(f"saved {new_data}, ", end="")
        return True

    def draw_apply_button(main_globals, x, y, function): # apply the changes to save data
        screen = main_globals['screen']
        if main_globals['apply_button'] is not pygame.rect.Rect(x, y, 100, 40): # make it with x and y
            main_globals['apply_button'] = pygame.rect.Rect(x, y, 100, 40)

        pygame.draw.rect(screen, (70, 70, 70), main_globals['apply_button'])
        text_surf = font.render("Apply", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['apply_button'].center)
        screen.blit(text_surf, text_rect)

        if main_globals['apply_button'].collidepoint(main_globals['mouse_pos']) and pygame.mouse.get_pressed()[0]:
            # apply the change if clicked
            if function == "resolution": # changes resolution
                new_res = main_globals['resolutions'][main_globals['resolution_index']]
                main_globals['resolution'] = new_res
                save(main_globals, resolution=new_res)
                print(f"set resolution to {new_res}")

            elif function == "framerate": # changes max fps of real screen
                new_fps = main_globals['frame_caps'][main_globals['frame_cap_index']]
                main_globals['max_fps'] = new_fps
                save(main_globals, max_fps=new_fps)
                print(f"set fps to {new_fps}")

            elif function == "music": # changes music volume
                new_volume = main_globals.get('volume_preview', main_globals.get('music_volume', mx.music.get_volume()))
                main_globals['music_volume'] = new_volume
                main_globals.pop('volume_preview', None) # reset bar preview
                mx.music.set_volume(new_volume)
                save(main_globals, music=new_volume)
                print(f"set music volume to {new_volume}")

    def draw_hints(main_globals): # not really hints, just like keybinds but with a timer
        dt = main_globals['dt']
        screen = main_globals['screen']
        alpha = main_globals['hint_alpha']
        main_globals['hint_alpha'] = alpha
        block_size = main_globals['key_w_hint'].get_width()

        if main_globals['idle_time'] >= main_globals['idle_threshold'] or main_globals['is_paused']: # if player is idle for long enough
            alpha = main_globals.get('hint_alpha', 0)
            alpha += dt * 255 / main_globals['hint_fade_duration']
            if alpha > 255:
                alpha = 255

            # really shoulda made a for loop for ts
            # i did
            main_globals['hint_alpha'] = alpha
            hints = {
                'key_w_hint': (10 + block_size, main_globals['screen'].get_height() - block_size*2 - 10),
                'key_a_hint': (10, main_globals['screen'].get_height() - block_size - 10),
                'key_s_hint': (10 + block_size, main_globals['screen'].get_height() - block_size - 10),
                'key_d_hint': (10 + block_size*2, main_globals['screen'].get_height() - block_size - 10),
                'key_e_hint': (10 + block_size*2, main_globals['screen'].get_height() - block_size*2 - 10),
            }

            for key, pos in hints.items():
                main_globals[key].set_alpha(alpha)
                screen.blit(main_globals[key], pos)

            # swap mouse image
            ticks = pygame.time.get_ticks() # ms
            if (ticks // 1000) % 2 == 0: # s
                main_globals['mouse_blank_hint'].set_alpha(alpha)
                screen.blit(main_globals['mouse_blank_hint'], (main_globals['screen'].get_width() - main_globals['mouse_blank_hint'].get_width() - 10, main_globals['screen'].get_height() - main_globals['mouse_blank_hint'].get_height() - 10))
            else:
                main_globals['mouse_left_hint'].set_alpha(alpha)
                screen.blit(main_globals['mouse_left_hint'], (main_globals['screen'].get_width() - main_globals['mouse_left_hint'].get_width() - 10, main_globals['screen'].get_height() - main_globals['mouse_left_hint'].get_height() - 10))
        else:
            main_globals['hint_alpha'] = 0

    def weapon_info(main_globals):
        screen = main_globals['screen']
        weapons = main_globals['player'].weapons
        screen_w = main_globals['screen'].get_width()
        screen_h = main_globals['screen'].get_height()
        screen.blit(main_globals['weapon_frame'], (screen_w // 2 - main_globals['weapon_frame'].get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2))

        if not weapons or weapons[0] is None:
            # draw some hands or something
            return

        weapon = main_globals['player'].weapons[0]
        weapon_image = main_globals['weapon_images'][weapon.name]
        screen.blit(weapon_image, (screen_w // 2 - main_globals['weapon_frame'].get_width() // 2 + 35, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 30))

        # stats
        text = smallfont.render(weapon.name, True, (255, 255, 255))
        screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 20))

        text = smallfont.render(str(weapon.damage), True, (255, 255, 255))
        screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 50))

        text = smallfont.render(str(weapon.range), True, (255, 255, 255))
        screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 80))

        text = smallfont.render(str(weapon.cooldown), True, (255, 255, 255))
        screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 110))

    def new_mutation(main_globals, effect, number): # not used at all yet
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

    def interact(main_globals, player, x, y, function): # interaction prompt
        if distance_to(player, (x, y)) < main_globals['interact_distance']: # if player is within reach
            if main_globals['pressed_e'] and not main_globals['is_paused'] and function is not None:
                function()
                print(f"player interacted at ({x}, {y}), ", end="")
                main_globals['pressed_e'] = False # prevent spam

    def distance_to(thing1, thing2): # basically just math.isclose without math.isclose
        def get_xy(thing): # kind of totally useless but i wont bother
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

    def player_gif(main_globals): # makes the player gif to frames
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

    def get_camera_offset(main_globals, player, tile_size): # offset of the camera depending on tile with player
        player_center_x = player.x + main_globals['player_size'] // 2
        player_center_y = player.y + main_globals['player_size'] // 2

        tile_x = player_center_x // (tile_size + main_globals['tile_offset'])
        tile_y = player_center_y // (tile_size + main_globals['tile_offset'])
        # camera moves to the center of the tile
        offset_x = tile_x * (tile_size + main_globals['tile_offset']) + tile_size // 2 - main_globals['screen'].get_width() // 2
        offset_y = tile_y * (tile_size + main_globals['tile_offset']) + tile_size // 2 - main_globals['screen'].get_height() // 2
        return offset_x, offset_y

    def make_initial_walkable_surface(tilemap, main_globals, bridging=True, counter=0): # make the initial walkable mask as its own surface
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
                    # draw main tile in mask
                    pygame.draw.rect(mask, (0, 255, 0), (tx, ty, tile_size, tile_size))

                    if bridging == True: # for enabling bridges/pathing between tiles
                        # horizontal bridge
                        if col_idx + 1 < len(row) and tilemap[row_idx][col_idx + 1] in main_globals['walkable_tiles']:
                            pygame.draw.rect(mask, (0, 255, 0), (tx + tile_size, ty + tile_size//2 - bridge_size//2,bridge_size, bridge_size))

                        # vertical bridge
                        if row_idx + 1 < len(tilemap) and tilemap[row_idx + 1][col_idx] in main_globals['walkable_tiles']:
                            pygame.draw.rect(mask, (0, 255, 0), (tx + tile_size//2 - bridge_size//2, ty + tile_size, bridge_size, bridge_size))

        main_globals['spawn_weapons'](main_globals)
        if counter == 0:
            # cba to make a seperate mask so calls itself with a counter for looping
            main_globals['locked_mask'] = make_initial_walkable_surface(tilemap, main_globals, False, counter + 1)
            print(f"previous active tiles: {main_globals['active_tiles']}")
            main_globals['active_tiles'] = []
        return mask

    def rebuild_walkable_mask(main_globals): # rebuilds the mask if something changed
        print("rebuilding walkable mask")
        tilemap = main_globals['tilemap']
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        mask_width = len(tilemap[0]) * ts
        mask_height = len(tilemap) * ts

        new_mask = pygame.Surface((mask_width, mask_height))
        new_mask.fill((0, 0, 0)) # clear mask

        main_globals['walkable_mask'] = new_mask

        # remake the mask
        main_globals['walkable_mask'] = main_globals['make_initial_walkable_surface'](tilemap, main_globals)

    def update_tile(main_globals, col_idx, row_idx, new_tile_type): # updates a specific tile
        # ex. update_tilemap(main_globals, 0, 0, 99)
        # update tilemap ( glogales, column index, row index, tile type )

        ts = main_globals['tile_size'] + main_globals['tile_offset']
        center_x = col_idx * ts + main_globals['tile_size'] // 2
        center_y = row_idx * ts + main_globals['tile_size'] // 2

        if new_tile_type == 99: # clears other tiles if new tile is a spawn tile
            print("clearing tiles")
            for i in range(len(main_globals['tilemap'])):
                for j in range(len(main_globals['tilemap'][0])):
                    main_globals['tilemap'][i][j] = 0
            main_globals['player'].respawn()

        main_globals['weapons_on_map'] = [ # remove all weapons that are not on the new tiles
        w for w in main_globals['weapons_on_map']
            if not (math.isclose(w.x, center_x, abs_tol=1) and math.isclose(w.y, center_y, abs_tol=1))
        ]

        print(f"updating tilemap with {col_idx, row_idx} as type {new_tile_type}, ", end="")
        main_globals['tilemap'][row_idx][col_idx] = new_tile_type # actually updates the tile
        if 'groups_spawned' in main_globals:
            main_globals['groups_spawned'] = 0

    def draw_hud(main_globals, player): # top left images for symboling his health
        if player.alive: # IS HE????????
            shake_x, shake_y = player.shake() # reuse player shake for the hud
            screen = main_globals['screen']
            pygame.draw.circle(screen, (20, 20, 20), (100, 100), 80) # i think we should remove the text
            screen.blit(bigfont.render(str(player.health), True, (255, 255, 255)), (120, 200))
            screen.blit(bigfont.render(str(player.wealth), True, (255, 215, 0)), (120, 250)) # just realised man good job!!!!! wealth health
            if player.health > 66: # jebo vam siks seven 🤖
                screen.blit(main_globals['player_health_images'][0], (-50 + shake_x, -50 + shake_y))
            elif player.health > 33:
                screen.blit(main_globals['player_health_images'][1], (-50 + shake_x, -50 + shake_y))
            else:
                screen.blit(main_globals['player_health_images'][2], (-50 + shake_x, -50 + shake_y))

    def draw_vignette(main_globals, player): # if you dont know what 'vignette' means go away!
        if player.alive: # you filthy hog
            max_alpha = 180
            try:
                if main_globals['vignette'].get_alpha() != max_alpha * (1 - player.health / 100):
                    vignette_alpha = max_alpha * (1 - player.health / 100)
                    main_globals['vignette'].set_alpha(vignette_alpha)
            except UnboundLocalError: # if it dont exists yet
                vignette_alpha = max_alpha
            main_globals['screen'].blit(main_globals['vignette'], (0, 0))

    def draw_pause_menu(main_globals): # the thing you see when paused
        screen = main_globals['screen']
        screen.blit(main_globals['font'].render("paused", True, (255, 255, 255)), (main_globals['screen'].get_width() // 2 - 60, main_globals['screen'].get_height() // 4 - 22))
        mx.music.pause()
        weapon_info(main_globals)

    def draw_menu(main_globals, mouse_pos): # main menu
        screen = main_globals['screen']
        screen.fill((0, 0, 0))

        if main_globals['menu_bg_can_animate']: # roll in on first launch
            target_x = main_globals['screen'].get_width() - main_globals['menu_background'].get_width()
            if main_globals['menu_bg_x'] > target_x:
                main_globals['menu_bg_x'] -= 10
            else:
                main_globals['menu_bg_x'] = target_x
                main_globals['menu_bg_can_animate'] = False
                main_globals['flash_active'] = True

        screen.blit(main_globals['menu_background'], (main_globals['menu_bg_x'], 0))

        # flash at the first launch
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

        # if i finished showing off my skills ( animation )
        if main_globals['menu_bg_can_animate']== False and main_globals['flash_active'] == False:

            # title
            title_text = main_globals['font'].render("Title", True, (255, 255, 255))
            title_rect = title_text.get_rect(topleft=(10, 5)) # for some reason top looks way bigger even if its same number
            screen.blit(title_text, title_rect)

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

            # battle pass button :kekw:
            bp_color = (70, 70, 70) if main_globals['bp_button'].collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(screen, bp_color, main_globals['bp_button'])
            text_surf = font.render("Battle Pass", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=main_globals['bp_button'].center)
            screen.blit(text_surf, text_rect.topleft)
            # uncomment if you dare
            # i dared and its staying this way ;)

    def draw_credits(main_globals, mouse_pos): # cursed with 1% total fps
        screen = main_globals['screen']
        to_menu = main_globals['to_menu']
        font = main_globals['font']
        screen.fill((0, 0, 0))

        screen.blit(font.render("credits", True, (255, 255, 255)), (20, 20))
        # screen.blit(main_globals['thx'], (540, 0)) # i got the coordinates right first try btw
        # show off

        # no problem man
        screen.blit(main_globals['thx'], (main_globals['screen'].get_width() // 2, 0))

        # return
        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        text_surf = font.render("return", True, (255, 255, 255))
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

        # framerate cap slider
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
        screen.fill((0, 0, 0))

        screen.blit(font.render("ded", True, (255, 255, 255)), (20, 20))
        main_globals['musicswitcher'](main_globals, 1)

        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        text_surf = font.render("To menu", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['to_menu'].center)
        screen.blit(text_surf, text_rect.center)

    def draw_battle_pass(main_globals, mouse_pos):
        screen = main_globals['screen']
        font = main_globals['font']
        buy_button = main_globals['buy_button']
        buy_button_color = (70, 70, 70) if buy_button.collidepoint(mouse_pos) else (40, 40, 40)
        text_surf = font.render("14.99€", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['buy_button'].center)

        screen.fill((0, 0, 0))
        screen.blit(main_globals['battlepass_image'], (0, 0))
        pygame.draw.rect(screen, buy_button_color, buy_button)
        screen.blit(text_surf, text_rect.topleft)

    shop = Shop(main_globals)

    # add functions to main globallers
    main_globals['player_gif'] = player_gif
    main_globals['draw_menu'] = draw_menu
    main_globals['draw_hud'] = draw_hud
    main_globals['draw_pause_menu'] = draw_pause_menu
    main_globals['draw_settings'] = draw_settings
    main_globals['draw_credits'] = draw_credits
    main_globals['draw_shop'] = Shop.draw_shop
    main_globals['draw_dead'] = draw_dead
    main_globals['draw_battle_pass'] = draw_battle_pass
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
    main_globals['draw_mode_selection'] = draw_mode_selection
    main_globals['draw_transition'] = transition_to_dungeon
    main_globals['remake_floor'] = remake_floor
    main_globals['give_money'] = give_money
    main_globals['execute'] = execute
    main_globals['reset'] = reset
    main_globals['draw_minimap'] = draw_minimap
    main_globals['is_on_active_tile'] = is_on_active_tile

    # add classes to main globall
    main_globals['shop'] = shop
    main_globals['Shop'] = Shop

    print("loader3, ", end = "")