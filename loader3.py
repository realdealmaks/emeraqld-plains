# this file is for random parts of the game

# loader 3

try:
    import random, pygame, pymunk, types, threading
    from pygame import mixer as mx
    import numpy as np
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

try:
    from connector_db import save_db
except ImportError as e:
    print("couldnt import save_db")

def loader3(main_globals):

    font = pygame.font.Font("assets/font/editundo.ttf", 24)
    bigfont = pygame.font.Font("assets/font/editundo.ttf", 48)
    setting_font = credits_font = pygame.font.Font("assets/font/editundo.ttf", 28)
    smallfont = pygame.font.Font("assets/font/editundo.ttf", 22)
    smallerfont = pygame.font.Font("assets/font/editundo.ttf", 16)

    tutorial_texts = {
        1: font.render("move along", True, (255, 255, 255)),
        2: font.render("take it", True, (255, 255, 255)),
        99: font.render("press esc", True, (255, 255, 255)),
        88: font.render("shop for items", True, (255, 255, 255)),
        3: font.render("beat bobbers", True, (255, 255, 255)),
        98: font.render("enter a new floor", True, (255, 255, 255)),
    }

    def tutorial_text(main_globals):
        screen = main_globals['screen']
        tilemap = main_globals['tilemap']
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        player = main_globals['player']
        font = main_globals['font']

        # player tile
        player_tile = (
            (player.y + main_globals['player_size'] // 2) // ts,
            (player.x + main_globals['player_size'] // 2) // ts
        )

        camera_x = int(main_globals['camera_x'])
        camera_y = int(main_globals['camera_y'])

        # what happens when player on tile
        row_idx, col_idx = player_tile
        if 0 <= row_idx < len(tilemap) and 0 <= col_idx < len(tilemap[0]):
            tile = tilemap[row_idx][col_idx]

            # if tile has tutorial text display it
            if tile in tutorial_texts:
                text_surface = tutorial_texts[tile]
                draw_x = col_idx * ts - camera_x
                draw_y = row_idx * ts - camera_y
                screen.blit(text_surface, (draw_x, draw_y))

    def get_dominant_color(image): # get the dominant color from an image
        if image is None:
            return (255, 200, 100) # default

        # scale down
        small = pygame.transform.scale(image, (20, 20))

        arr = pygame.surfarray.array3d(small)
        # list of pixels
        pixels = arr.reshape(-1, 3)

        # count color occurrences
        from collections import Counter
        color_counts = Counter(map(tuple, pixels))

        # ignore black, white, trans
        for color, count in color_counts.most_common():
            if sum(color) > 50 and sum(color) < 700:
                return color

    def auto_save(main_globals):
        if main_globals.get('autosaving'):
            return

        def save_task():
            main_globals['autosaving'] = True
            main_globals['spinner_active'] = True
            main_globals['autosave_start_time'] = pygame.time.get_ticks()

            save_db("data.json", "game_data.db")

            main_globals['autosave_finished'] = True
            print("auto saved, ", end="")

        main_globals['autosave_finished'] = False
        threading.Thread(target=save_task, daemon=True).start()

    def draw_autosave_spinner(main_globals):
        if 'loading_icon' not in main_globals:
            icon = pygame.image.load("assets/useful images/save.png").convert_alpha()
            main_globals['loading_icon'] = pygame.transform.scale2x(icon)

        if main_globals.get('spinner_active', False):
            now = pygame.time.get_ticks()
            start = main_globals.get('autosave_start_time', now)
            min_show_ms = 1200 # minimum display time in ms

            if 'autosave_angle' not in main_globals:
                main_globals['autosave_angle'] = 0
            main_globals['autosave_angle'] = (main_globals['autosave_angle'] + 6) % 360

            icon = main_globals['loading_icon']

            fixed_x = main_globals['screen_w'] - 20 - icon.get_width() // 2
            fixed_y = 20 + icon.get_height() // 2

            rotated_icon = pygame.transform.rotate(icon, main_globals['autosave_angle'])
            rotated_icon.set_alpha(180)
            rect = rotated_icon.get_rect(center=(fixed_x, fixed_y))
            main_globals['screen'].blit(rotated_icon, rect.topleft)

            smallfont = pygame.font.Font(None, 24)
            text = smallfont.render("autosaving", True, (255, 255, 255))
            text_rect = text.get_rect(midright=(fixed_x - icon.get_width() // 2 - 10, fixed_y))
            main_globals['screen'].blit(text, text_rect)

            if main_globals.get('autosave_finished', False) and (now - start >= min_show_ms) or main_globals['textures_ready'] and main_globals.get('autosave_finished', False):
                main_globals['spinner_active'] = False
                main_globals['autosaving'] = False
                main_globals.pop('autosave_start_time', None)
                main_globals.pop('autosave_finished', None)
                main_globals.pop('autosave_angle', None)

    def use_crystal(main_globals):
        player = main_globals['player']
        if player.inventory.get('crystal', 0) >= 1:
            player.inventory['crystal'] -= 1
            if player.inventory['crystal'] == 0:
                del player.inventory['crystal']
            main_globals['choosing'] = True
            main_globals['choosing_crystal'] = True

    def use_fragments(main_globals):
        player = main_globals['player']
        screen = main_globals['screen']
        if player.inventory['crystal_fragments'] >= 6:
            player.inventory['crystal_fragments'] -= 6
            if player.inventory['crystal_fragments'] == 0:
                del player.inventory['crystal_fragments']
            main_globals['add_to_inventory'](main_globals, 'crystal', 1)

    def spawn_blood_particles(space, player_x, player_y, player_size, amount=10):
        if main_globals['blood_text'] == "False": # if option disabled
            return
        particles = []
        # bloods at player lower center
        spawn_x = player_x + player_size // 2
        spawn_y = player_y + player_size + 25

        # y where they stop
        landing_y = spawn_y + 30 # kind of pointless because they dont live enough

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
        x2, y2 = get_xy(thing2) # this entire thing is only because i wanted the player center btw
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def musicswitcher(main_globals, indexhere, start=-1):
        if main_globals['currently_playing_index'] != indexhere:
            mx.music.load(main_globals['musics'][indexhere])
            mx.music.play(start)
            main_globals['currently_playing_index'] = indexhere

    # define functions and classes into main globals
    for name, obj in locals().items():
        if isinstance(obj, (types.FunctionType, type)):
            main_globals[name] = obj

    print("loader3, ", end = "")