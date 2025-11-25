# this file is for variables

try:
    import pygame
except ImportError as e:
    print(f"missing module{e}")

def loader1(main_globals):
    screen_w, screen_h = main_globals['screen_w'], main_globals['screen_h']
    # player variables
    main_globals['spawn_set'] = False
    main_globals['can_move_x'] = True
    main_globals['can_move_y'] = True
    main_globals['moving_up'] = False
    main_globals['moving_down'] = False
    main_globals['moving_left'] = False
    main_globals['moving_right'] = False
    main_globals['player_size'] = 50
    main_globals['current_frame'] = 0 # gif frame
    main_globals['frame_timer'] = 0 # time since last gif frame change
    main_globals['frame_delay'] = 50 # ms between gif frames
    main_globals['facing_left'] = False
    main_globals['frames'] = [] # player gif frames
    main_globals['pressed_e'] = False
    main_globals['pressed_f'] = False
    main_globals['spawn_x'] = 0
    main_globals['spawn_y'] = 0
    main_globals['player_max_health'] = 100

    # weapon variables
    main_globals['Weapon'] = None
    main_globals['attack_counter'] = 0 # what variation no. of attack the next one is # doesnt do shit rn
    main_globals['weapons_on_map'] = [] # weapons in the current tilemap
    main_globals['dual_wields'] = [ # weapons you can dual wield
            "katana"
        ]

    # dungeon variables
    main_globals['tilemap'] = [
        [0, 0, 0, 0, 88, 0, 0, 0], # 0 = void
        [0, 99, 1, 2, 98, 0, 0, 0], # 1 = empty
        [0, 0, 0, 0, 0, 0, 0, 0], # 99 = spawn tile
        [0, 0, 0, 0, 0, 0, 0, 0], # 88 = shop tile
        [0, 0, 0, 0, 0, 0, 0, 0], # 2 = weapon tile
        [0, 0, 0, 0, 0, 0, 0, 0], # 3 = enemy tile
        [0, 0, 0, 0, 0, 0, 0, 0], # 98 = end tile
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    main_globals['textures_ready'] = False
    main_globals['walkable_tiles'] = [1, 2, 3, 4, 99, 88, 98]
    main_globals['in_shop'] = False
    main_globals['tile_size'] = 600
    main_globals['tile_offset'] = 50
    main_globals['is_paused'] = False
    main_globals['money_texts'] = [] # + amount text
    main_globals['current_floor'] = 0
    main_globals['best_floor'] = None # record
    main_globals['groups_cleared'] = 0 # enemy groups
    main_globals['deaths'] = 0
    main_globals['enemies_killed'] = 0
    main_globals['total_enemies_killed'] = 0
    main_globals['most_groups_cleared'] = None # record
    main_globals['most_enemies_killed'] = None # record
    main_globals['richest_player'] = None # record
    main_globals['total_deaths'] = None # record
    main_globals['active_tiles'] = [] # tiles the player has walked on
    main_globals['tabs'] = { # pause menu tabs
        'player_stats': 'draw_pause_stats',
        'buttons': 'draw_pause_buttons',
        'weapon': 'weapon_info',
        'inventory': 'draw_inventory',
        'settings': 'draw_settings',
    }
    main_globals['proj_spd_mult'] = 1.1 # mult by range
    main_globals['damage_mult'] = 1.0
    main_globals['cooldown_mult'] = 1.0
    main_globals['plr_spd_mult'] = 1.0

    main_globals['selected_crystal_effect'] = None
    main_globals['crystals'] = [ # list of descriptions of crystals
        "increases max hp", # green
        "increases overall damage", # red
        "increases overall speed", # blue
    ]
    main_globals['inventory_texts'] = [] # + amount text image for inventory

    main_globals['crystal_effects'] = [ # list of functions for crystal effects lambla blablabla
            lambda main_globals: main_globals['player'].effect("max_hp", 20), # green
            lambda main_globals: main_globals['player'].effect("ovr_damage", 5), # red
            lambda main_globals: main_globals['player'].effect("ovr_speed", 0.4), # blue
        ]
    main_globals['choosing'] = False # if choosing something
    main_globals['choosing_crystal'] = False # if choosing crystal effect

    # generator :robot:
    def generate_update_tile_calls(tilemap): # makes calls of update tile to make the default tilemap
        calls = []
        for r, row in enumerate(tilemap):
            for c, val in enumerate(row):
                if val == 99:
                    calls.append(f"main_globals['update_tile'](main_globals, {c}, {r}, {val})")
        for r, row in enumerate(tilemap):
            for c, val in enumerate(row):
                if val != 0 and val != 99:
                    calls.append(f"main_globals['update_tile'](main_globals, {c}, {r}, {val})")
        return calls

    main_globals['default_tilemap_calls'] = generate_update_tile_calls(main_globals['tilemap'])

    # camera variables
    main_globals['camera_x'] = 0
    main_globals['camera_y'] = 0
    main_globals['camera_speed'] = 0.1

    # enemy variables
    main_globals['enemy_size'] = 50
    main_globals['enemy_type'] = None
    main_globals['groups_spawned'] = 0
    main_globals['enemy_list'] = [] # enemies in the current map
    main_globals['enemy_spawn_x'] = 0
    main_globals['enemy_spawn_y'] = 0

    # menu variables
    main_globals['menu_bg_x'] = main_globals['screen_w']
    main_globals['dragging_music_slider'] = False
    main_globals['dragging_resolution_slider'] = False
    main_globals['dragging_frame_slider'] = False
    main_globals['menu_bg_can_animate'] = True # the start anim
    main_globals['flash_alpha'] = 0 # flash in ^ anim
    main_globals['flash_active'] = False
    main_globals['flash_speed'] = 1

    # mode buttons
    # each one needs its own variable
    main_globals['mode1_scale'] = 1.0 # mode button1 scale
    main_globals['mode2_scale'] = 1.0 # mode button2 scale
    main_globals['mode1_dim'] = 150 # mode button1 dim
    main_globals['mode2_dim'] = 150 # mode button2 dim
    main_globals['mode1_btn_size'] = [200, 50] # mode button1 size
    main_globals['mode2_btn_size'] = [200, 50] # mode button2 size

    # game variables
    main_globals['game_stage'] = ""
    main_globals['font'] = pygame.font.Font("assets/font/editundo.ttf", 48)
    main_globals['developer_tools'] = True # changed in main
    main_globals['mouse_pressed'] = pygame.mouse.get_pressed()[0]
    main_globals['match'] = None # current match for switch case
    main_globals['interact_distance'] = 75 # distance to interact with things
    main_globals['currently_playing_index'] = 0 # music index
    main_globals['blood_text'] = "True" # blood toggle
    main_globals['blood'] = main_globals['blood_text'].split(", ")
    main_globals['dttv'] = 0 # i forgot what dttv stands for but its no. of letters until cmd
    main_globals['cmd_active'] = False
    main_globals['cmd_buffer'] = "" # collects inputs

    # hint variables
    main_globals['hint_alpha'] = 0
    main_globals['idle_time'] = 0 # time since last input
    main_globals['idle_threshold'] = 5 # time until hint shows
    main_globals['last_input_time'] = 0
    main_globals['hint_fade_duration'] = 0.5
    main_globals['hints_text'] = "True"
    main_globals['hints'] = main_globals['hints_text'].split(", ")

    # button variables
    main_globals['mouse_clicked'] = False # if previous frame mouse was clicked # prevents spam

    main_globals['music_slider'] = pygame.Rect(screen_w - 400, 100, 300, 20)
    main_globals['play_button'] = pygame.Rect(50, screen_h - 150, 200, 100) # to show modes
    main_globals['settings_button'] = pygame.Rect(50, screen_h - 300, 200, 100)
    main_globals['credits_button'] = pygame.Rect(50, screen_h - 450, 200, 100)
    main_globals['bp_button'] = pygame.Rect(50, screen_h - 600, 200, 100) # battlepass
    main_globals['to_menu'] = pygame.Rect(screen_w - 120, screen_h - 120, 65, 65) # return to menu
    main_globals['buy_button'] = pygame.Rect(20, screen_h - 150, 200, 100) # battlepass buy
    main_globals['hints_button'] = pygame.Rect(screen_w - 400, 143, 75, 35) # hints toggle
    main_globals['blood_button'] = pygame.Rect(screen_w - 400, 293, 75, 35) # blood toggle
    main_globals['resolution_slider_base'] = pygame.Rect(screen_w - 400, 207, 300, 5) # the line
    main_globals['frame_slider_base'] = pygame.Rect(screen_w - 400, 257, 300, 5) # the line
    main_globals['frame_slider'] = pygame.Rect(0, 0, 0, 0) # the thing you grab
    main_globals['resolution_slider'] = pygame.Rect(0, 0, 0, 0) # the thing you grab
    main_globals['apply_button'] = pygame.Rect(0, 0, 0, 0) # apply settings to json

    # mode variables
    main_globals['mode1button'] = pygame.Rect(screen_w * 3 // 4 - 100, screen_h // 2, 200, 50) # left
    main_globals['mode2button'] = pygame.Rect(screen_w * 3 // 4 - 100, screen_h // 2, 200, 50) # right
    main_globals['transition_active'] = False
    main_globals['transition_side'] = 'left' # what side 'in' starts from
    main_globals['transition_progress'] = 0.0
    main_globals['transition_speed'] = 2.2
    main_globals['selected_mode'] = None # swaps to corresponding mode
    main_globals['transition_phase'] = 'in' # in, hold, out
    main_globals['transition_hold_duration'] = 2.0 # time seeing completely black
    main_globals['transition_hold_timer'] = 0.0

    # virtual setup
    main_globals['prev_time'] = pygame.time.get_ticks() / 1000
    main_globals['dt'] = 0
    main_globals['virtual_screen'] = main_globals['screen']
    main_globals['max_fps'] = 0

    # synced settings - resolution
    main_globals['resolution'] = main_globals.get('resolution', (1080, 750))
    resolutions = [
        (1, 1), (50, 50), (200, 200), (420, 800), (1920, 1080), (2560, 1440),
        (3840, 2160), (1280, 720), (1280, 1024), (1600, 900), (1920, 1200),
        (2560, 1600), (800, 600), (1080, 750), (1024, 2048), (670, 410),
    ]
    resolutions.sort()
    main_globals['resolutions'] = resolutions

    closest_index = min(
        range(len(resolutions)),
        key=lambda i: abs(resolutions[i][0] - main_globals['resolution'][0]) + abs(resolutions[i][1] - main_globals['resolution'][1])
    )
    main_globals['resolution_index'] = closest_index
    main_globals['resolution'] = resolutions[closest_index]

    # synced settings - frame cap
    frame_caps = [1, 10, 15, 20, 25, 30, 40, 60, 75, 120, 67, 61, 41, 175]
    frame_caps.sort()
    main_globals['frame_caps'] = frame_caps
    main_globals['frame_cap'] = main_globals.get('max_fps', 60)
    closest_index = min(range(len(frame_caps)), key=lambda i: abs(frame_caps[i] - main_globals['frame_cap']))
    main_globals['frame_cap_index'] = closest_index
    main_globals['frame_cap'] = frame_caps[closest_index]

    # pymunk space
    main_globals['blood_particles'] = []
    main_globals['space'] = None

    # items
    main_globals['selected_item'] = None
    items = {
        # 'item name': {
            # 'description': 'item \ndescription',
            # 'function': lamblabla main gobals: main gobals['function name'](args),
            # 'image': image
        # }

        'fuck': { # test item
            'description': 'item description',
            'function': lambda main_globals: main_globals['player'].effect('heal', 10),
            'image': pygame.image.load("assets/models/items/weapons/katana.png").convert_alpha()
        },

        # health potions
        'small_potion': {
            'description': 'heals you a little',
            'function': lambda main_globals: main_globals['player'].effect('heal', 20),
            'image': pygame.image.load("assets/models/items/consumables/potions/health/potion20.png").convert_alpha()
        },
        'medium_potion': {
            'description': 'heals you a bit',
            'function': lambda main_globals: main_globals['player'].effect('heal', 40),
            'image': pygame.image.load("assets/models/items/consumables/potions/health/potion40.png").convert_alpha()
        },
        'large_potion': {
            'description': 'heals you a lot',
            'function': lambda main_globals: main_globals['player'].effect('heal', 60),
            'image': pygame.image.load("assets/models/items/consumables/potions/health/potion60.png").convert_alpha()
        },

        # crystals
        'crystal_fragments': {
            'description': 'fragments of a crystal, \nyou require 6',
            'function': lambda main_globals: main_globals['use_fragments'](main_globals),
            'image': pygame.image.load("assets/models/items/consumables/crystal/crystalfragments.png").convert_alpha()
        },
        'crystal': {
            'description': 'a crystal',
            'function': lambda main_globals: main_globals['use_crystal'](main_globals),
            'image': pygame.image.load("assets/models/items/consumables/crystal/crystal.png").convert_alpha()
        },

    }
    main_globals['other_consumables'] = [ # consumables you can use in combat: name
            #
        ]

    main_globals['items'] = items

    print("loader1, ", end="")
