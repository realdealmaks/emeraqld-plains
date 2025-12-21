# this file is for random parts of the game

# loader 3

try:
    import random, pygame, pymunk, types
    from pygame import mixer as mx
    import numpy as np
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

def loader3(main_globals):

    font = pygame.font.Font("assets/font/editundo.ttf", 24)
    bigfont = pygame.font.Font("assets/font/editundo.ttf", 48)
    setting_font = credits_font = pygame.font.Font("assets/font/editundo.ttf", 28)
    smallfont = pygame.font.Font("assets/font/editundo.ttf", 22)
    smallerfont = pygame.font.Font("assets/font/editundo.ttf", 16)

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
        for row_idx, row in enumerate(tilemap):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    if (row_idx, col_idx) == player_tile:
                        text_surface = font.render("move along", True, (255, 255, 255))
                        draw_x = col_idx * ts - camera_x
                        draw_y = row_idx * ts - camera_y
                        screen.blit(text_surface, (draw_x, draw_y))
                if tile == 2:
                    if (row_idx, col_idx) == player_tile:
                        text_surface = font.render("take it", True, (255, 255, 255))
                        draw_x = col_idx * ts - camera_x
                        draw_y = row_idx * ts - camera_y
                        screen.blit(text_surface, (draw_x, draw_y))
                if tile == 99:
                    if (row_idx, col_idx) == player_tile:
                        text_surface = font.render("press esc", True, (255, 255, 255))
                        draw_x = col_idx * ts - camera_x
                        draw_y = row_idx * ts - camera_y
                        screen.blit(text_surface, (draw_x, draw_y))
                if tile == 88:
                    if (row_idx, col_idx) == player_tile:
                        text_surface = font.render("shop for items", True, (255, 255, 255))
                        draw_x = col_idx * ts - camera_x
                        draw_y = row_idx * ts - camera_y
                        screen.blit(text_surface, (draw_x, draw_y))
                if tile == 3:
                    if (row_idx, col_idx) == player_tile:
                        text_surface = font.render("beat bobbers", True, (255, 255, 255))
                        draw_x = col_idx * ts - camera_x
                        draw_y = row_idx * ts - camera_y
                        screen.blit(text_surface, (draw_x, draw_y))
                if tile == 98:
                    if (row_idx, col_idx) == player_tile:
                        text_surface = font.render("enter a new floor", True, (255, 255, 255))
                        draw_x = col_idx * ts - camera_x
                        draw_y = row_idx * ts - camera_y
                        screen.blit(text_surface, (draw_x, draw_y))

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