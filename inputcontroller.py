try:
    import random, pygame, webbrowser
    from pygame import mixer as mx
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")


def inputcontroller(main_globals):

    def input_controller(main_globals):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                main_globals['running'] = False

            # key down
            if event.type == pygame.KEYDOWN:

                main_globals['shell'](main_globals, event) # commands

                # movement keys
                if event.key == pygame.K_w:
                    main_globals['moving_up'] = True
                if event.key == pygame.K_s: # up down
                    main_globals['moving_down'] = True

                if event.key == pygame.K_a:
                    main_globals['moving_left'] = True
                    if not main_globals['is_paused']:
                        main_globals['facing_left'] = True
                if event.key == pygame.K_d: # left righ
                    main_globals['moving_right'] = True
                    if not main_globals['is_paused']:
                        main_globals['facing_left'] = False

                # e key
                if event.key == pygame.K_e:
                    main_globals['pressed_e'] = True
                else:
                    main_globals['pressed_e'] = False

                # f key
                if event.key == pygame.K_f:
                    main_globals['pressed_f'] = True
                else: # are we even using this anywhere
                    main_globals['pressed_f'] = False

                # pause
                if event.key == pygame.K_ESCAPE:
                    if main_globals['game_stage'] == "in dungeon":
                        main_globals['selected_item'] = None
                        main_globals['is_paused'] = not main_globals['is_paused']

            # key up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    main_globals['moving_up'] = False
                if event.key == pygame.K_s:
                    main_globals['moving_down'] = False
                if event.key == pygame.K_a:
                    main_globals['moving_left'] = False
                if event.key == pygame.K_d:
                    main_globals['moving_right'] = False

            # mouse down
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                mouse_pos = main_globals['mouse_pos']

                # choosing mode
                if main_globals['game_stage'] == "choosing mode":
                    if main_globals['mode1button'].collidepoint(mouse_pos):
                        main_globals['transition_active'] = True
                        main_globals['transition_side'] = 'left'
                        main_globals['selected_mode'] = 1
                    if main_globals['mode2button'].collidepoint(mouse_pos) and main_globals['has_save_data'](main_globals):
                        main_globals['transition_active'] = True
                        main_globals['transition_side'] = 'right'
                        main_globals['selected_mode'] = 2

                # menu
                if main_globals['game_stage'] == "in menu":
                    if main_globals['play_button'].collidepoint(mouse_pos):
                        main_globals['game_stage'] = "choosing mode"
                    if main_globals['settings_button'].collidepoint(mouse_pos):
                        main_globals['game_stage'] = "in settings"
                    if main_globals['credits_button'].collidepoint(mouse_pos):
                        main_globals['game_stage'] = "in credits"
                    if main_globals['bp_button'].collidepoint(mouse_pos):
                        main_globals['game_stage'] = "in battle pass"
                    if main_globals['stats_button'].collidepoint(mouse_pos):
                        main_globals['game_stage'] = "stats"

                # credits
                if main_globals['game_stage'] == "in credits":
                    if main_globals['to_menu'].collidepoint(mouse_pos):
                        main_globals['game_stage'] = "in menu"

                # settings
                if main_globals['game_stage'] == "in settings":

                    # sliders
                    if main_globals['frame_slider'].collidepoint(mouse_pos):
                        main_globals['dragging_frame_slider'] = True
                    elif main_globals['music_slider'].collidepoint(mouse_pos):
                        main_globals['dragging_music_slider'] = True
                    elif main_globals['resolution_slider'].collidepoint(mouse_pos):
                        main_globals['dragging_resolution_slider'] = True

                    # hints toggle
                    if main_globals['hints_button'].collidepoint(mouse_pos):
                        main_globals['hints_text'] = (
                            "False" if main_globals['hints_text'] == "True" else "True"
                        )
                        main_globals['hints'] = main_globals['hints_text'].split(", ")
                        main_globals['save'](main_globals, hints=main_globals['hints'])

                    # blood toggle
                    if main_globals['blood_button'].collidepoint(mouse_pos):
                        main_globals['blood_text'] = (
                            "False" if main_globals['blood_text'] == "True" else "True"
                        )
                        main_globals['blood'] = main_globals['blood_text'].split(", ")
                        main_globals['save'](main_globals, blood=main_globals['blood'])

                # return / to menu button
                if main_globals['to_menu'].collidepoint(mouse_pos):
                    main_globals['game_stage'] = "in menu"
                    mx.music.pause()

                # battlepass
                if main_globals['game_stage'] == "in battle pass":
                    if main_globals['buy_button'].collidepoint(mouse_pos):
                        webbrowser.open("https://www.youtube.com/channel/UC_zti-S08ZQegAafJw9wPhQ")

                # dungeon combat
                if main_globals['player'] is not None:
                    if main_globals['game_stage'] == "in dungeon":
                        if not main_globals['is_paused']:
                            if main_globals['player'].weapons:
                                main_globals['player'].attack(main_globals)

                # pause menu
                if main_globals['game_stage'] == "in dungeon":
                    if main_globals['is_paused'] and not main_globals['choosing']:

                        for name, rect in main_globals['pause_buttons'].items():
                            if rect.collidepoint(mouse_pos):
                                if name == 'resume':
                                    main_globals['is_paused'] = False
                                elif name == 'inventory':
                                    main_globals['current_tab'] = 'inventory'
                                elif name == 'weapon':
                                    main_globals['current_tab'] = 'weapon'
                                elif name == 'quit':
                                    main_globals['game_stage'] = "in menu"
                                    main_globals['reset'](main_globals)
                                    """
                                    main_globals['running'] = False
                                    pygame.quit()
                                    print("quit")
                                    """

                        # selecting inventory items
                        if main_globals['current_tab'] == 'inventory':
                            for item_name, rect in main_globals.get('inventory_items_rects', {}).items():
                                if rect.collidepoint(mouse_pos):
                                    main_globals['selected_item'] = item_name

            # mouse up
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                main_globals['dragging_frame_slider'] = False
                main_globals['dragging_music_slider'] = False
                main_globals['dragging_resolution_slider'] = False

            # pass mouse to globals
            main_globals['mouse_pressed'] = pygame.mouse.get_pressed()[0]

        # idle / hint timer
        if main_globals['game_stage'] == "in dungeon":

            keys = pygame.key.get_pressed()
            if any(keys):
                main_globals['last_input_time'] = pygame.time.get_ticks() / 1000

            if main_globals['mouse_pressed']:
                main_globals['last_input_time'] = pygame.time.get_ticks() / 1000

            current_time = pygame.time.get_ticks() / 1000
            main_globals['idle_time'] = current_time - main_globals['last_input_time']

        else:
            main_globals['last_input_time'] = 0

    main_globals['input_controller'] = input_controller
    print("incon, ", end="")
