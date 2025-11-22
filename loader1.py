# this file is for variables

import pygame

def loader1(main_globals):
    # player variables
    main_globals['spawn_set'] = False
    main_globals['can_move_x'] = True
    main_globals['can_move_y'] = True
    main_globals['moving_up'] = False
    main_globals['moving_down'] = False
    main_globals['moving_left'] = False
    main_globals['moving_right'] = False
    main_globals['player_size'] = 50
    main_globals['current_frame'] = 0
    main_globals['frame_timer'] = 0
    main_globals['frame_delay'] = 50
    main_globals['facing_left'] = False
    main_globals['frames'] = []
    main_globals['pressed_e'] = False
    main_globals['pressed_f'] = False
    main_globals['spawn_x'] = 0
    main_globals['spawn_y'] = 0

    # weapon variables
    main_globals['Weapon'] = None
    main_globals['attack_counter'] = 0
    main_globals['weapons_on_map'] = []
    main_globals['dual_wields'] = ["katana"]

    # dungeon variables
    main_globals['tilemap'] = [
        [0, 0, 0, 0, 88, 0, 0, 0, 0, 0], # 0 = void
        [0, 99, 1, 2, 98, 0, 0, 0, 0, 0], # 1 = empty
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 99 = spawn tile
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 88 = shop tile
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 2 = weapon tile
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 3 = enemy tile
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 98 = end tile
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    main_globals['walkable_tiles'] = [1, 2, 3, 4, 99, 88, 98]
    main_globals['in_shop'] = False
    main_globals['tile_size'] = 600
    main_globals['tile_offset'] = 50
    main_globals['is_paused'] = False
    main_globals['money_texts'] = []
    main_globals['current_floor'] = 0
    main_globals['best_floor'] = None
    main_globals['groups_cleared'] = 0
    main_globals['deaths'] = 0
    main_globals['enemies_killed'] = 0
    main_globals['total_enemies_killed'] = 0
    main_globals['most_groups_cleared'] = None
    main_globals['most_enemies_killed'] = None
    main_globals['richest_player'] = None
    main_globals['total_deaths'] = None
    main_globals['active_tiles'] = []
    main_globals['tabs'] = {
        'player_stats': 'draw_pause_stats',
        'buttons': 'draw_pause_buttons',
        'weapon_stats': 'weapon_info',
        'inventory': 'draw_inventory',
        'settings': 'draw_settings',
    }

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
    main_globals['enemy_list'] = []
    main_globals['enemy_spawn_x'] = 0
    main_globals['enemy_spawn_y'] = 0

    # menu variables
    main_globals['menu_bg_x'] = main_globals['screen_w']
    main_globals['dragging_music_slider'] = False
    main_globals['dragging_resolution_slider'] = False
    main_globals['dragging_frame_slider'] = False
    main_globals['menu_bg_can_animate'] = True
    main_globals['flash_alpha'] = 0
    main_globals['flash_active'] = False
    main_globals['flash_speed'] = 1
    main_globals['mode1_scale'] = 1.0
    main_globals['mode2_scale'] = 1.0
    main_globals['mode1_dim'] = 150
    main_globals['mode2_dim'] = 150
    main_globals['mode1_btn_size'] = [200, 50]
    main_globals['mode2_btn_size'] = [200, 50]

    # game variables
    main_globals['game_stage'] = ""
    main_globals['font'] = pygame.font.Font("assets/font/editundo.ttf", 48)
    main_globals['developer_tools'] = True
    main_globals['mouse_pressed'] = pygame.mouse.get_pressed()[0]
    main_globals['match'] = None
    main_globals['interact_distance'] = 75
    main_globals['currently_playing_index'] = 0
    main_globals['blood_text'] = "True"
    main_globals['blood'] = main_globals['blood_text'].split(", ")
    main_globals['dttv'] = 0
    main_globals['cmd_active'] = False
    main_globals['cmd_buffer'] = "" # collects inputs

    # hint variables
    main_globals['hint_alpha'] = 0
    main_globals['idle_time'] = 0
    main_globals['idle_threshold'] = 5
    main_globals['last_input_time'] = 0
    main_globals['hint_fade_duration'] = 0.5
    main_globals['hints_text'] = "True"
    main_globals['hints'] = main_globals['hints_text'].split(", ")

    # button variables
    screen_w, screen_h = main_globals['screen_w'], main_globals['screen_h']

    main_globals['music_slider'] = pygame.Rect(screen_w - 400, 100, 300, 20)
    main_globals['play_button'] = pygame.Rect(50, screen_h - 150, 200, 100)
    main_globals['settings_button'] = pygame.Rect(50, screen_h - 300, 200, 100)
    main_globals['credits_button'] = pygame.Rect(50, screen_h - 450, 200, 100)
    main_globals['bp_button'] = pygame.Rect(50, screen_h - 600, 200, 100)
    main_globals['to_menu'] = pygame.Rect(screen_w - 120, screen_h - 120, 65, 65)
    main_globals['buy_button'] = pygame.Rect(20, screen_h - 150, 200, 100)
    main_globals['hints_button'] = pygame.Rect(screen_w - 400, 143, 75, 35)
    main_globals['blood_button'] = pygame.Rect(screen_w - 400, 293, 75, 35)
    main_globals['resolution_slider_base'] = pygame.Rect(screen_w - 400, 207, 300, 5)
    main_globals['frame_slider_base'] = pygame.Rect(screen_w - 400, 257, 300, 5)
    main_globals['frame_slider'] = pygame.Rect(0, 0, 0, 0)
    main_globals['resolution_slider'] = pygame.Rect(0, 0, 0, 0)
    main_globals['apply_button'] = pygame.Rect(0, 0, 0, 0)

    # mode variables
    main_globals['mode1button'] = pygame.Rect(screen_w * 3 // 4 - 100, screen_h // 2, 200, 50)
    main_globals['mode2button'] = pygame.Rect(screen_w * 3 // 4 - 100, screen_h // 2, 200, 50)
    main_globals['transition_active'] = False
    main_globals['transition_side'] = 'left'
    main_globals['transition_progress'] = 0.0
    main_globals['transition_speed'] = 2.2
    main_globals['selected_mode'] = None
    main_globals['transition_phase'] = 'in'
    main_globals['transition_hold_duration'] = 2.0
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
        (2560, 1600), (800, 600), (1080, 750), (1024, 2048)
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
    frame_caps = [1, 10, 15, 20, 25, 30, 40, 60, 75, 120]
    frame_caps.sort()
    main_globals['frame_caps'] = frame_caps
    main_globals['frame_cap'] = main_globals.get('max_fps', 60)
    closest_index = min(range(len(frame_caps)), key=lambda i: abs(frame_caps[i] - main_globals['frame_cap']))
    main_globals['frame_cap_index'] = closest_index
    main_globals['frame_cap'] = frame_caps[closest_index]

    # pymunk space
    main_globals['blood_particles'] = []
    main_globals['space'] = None

    print("loader1, ", end="")
