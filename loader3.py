# this file is for random parts of the game

# loader 3

try:
    import random, pygame, pymunk, types
    from pygame import mixer as mx
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

def loader3(main_globals):

    font = pygame.font.Font("assets/font/editundo.ttf", 24)
    bigfont = pygame.font.Font("assets/font/editundo.ttf", 48)
    setting_font = credits_font = pygame.font.Font("assets/font/editundo.ttf", 28)
    smallfont = pygame.font.Font("assets/font/editundo.ttf", 22)
    smallerfont = pygame.font.Font("assets/font/editundo.ttf", 16)

    def is_on_active_tile(main_globals, x, y):
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        tile_x = (x + main_globals['player_size'] // 2) // ts
        tile_y = (y + main_globals['player_size'] // 2) // ts
        tile = (tile_x, tile_y)

        return tile in main_globals['active_tiles']

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
        button2.left = screen.get_width() * 3 // 4 - button2.width // 2
        button2.top = screen.get_height() // 2
        color2 = (70, 70, 70) if hover2 else (40, 40, 40)
        pygame.draw.rect(screen, color2, button2, border_radius=8)
        text_surf2 = main_globals['font'].render("2", True, (255, 255, 255))
        screen.blit(text_surf2, text_surf2.get_rect(center=button2.center))

        # return
        to_menu = main_globals['to_menu']
        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        img_rect = main_globals['return_image'].get_rect(center=main_globals['to_menu'].center)
        screen.blit(main_globals['return_image'], img_rect.topleft)

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
        if main_globals['blood_text'] == "False":
            return
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

            elif function == "framerate": # changes max fps of real screen
                new_fps = main_globals['frame_caps'][main_globals['frame_cap_index']]
                main_globals['max_fps'] = new_fps
                save(main_globals, max_fps=new_fps)

            elif function == "music": # changes music volume
                new_volume = main_globals.get('volume_preview', main_globals.get('music_volume', mx.music.get_volume()))
                main_globals['music_volume'] = new_volume
                main_globals.pop('volume_preview', None) # reset bar preview
                mx.music.set_volume(new_volume)
                save(main_globals, music=new_volume)

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

    def musicswitcher(main_globals, indexhere, start=-1):
        if main_globals['currently_playing_index'] != indexhere:
            mx.music.load(main_globals['musics'][indexhere])
            mx.music.play(start)
            main_globals['currently_playing_index'] = indexhere

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

    shop = Shop(main_globals)

    # define functions and classes into main globals
    for name, obj in locals().items():
        if isinstance(obj, (types.FunctionType, type)):
            main_globals[name] = obj

    # add instances
    main_globals['shop'] = shop

    print("loader3, ", end = "")