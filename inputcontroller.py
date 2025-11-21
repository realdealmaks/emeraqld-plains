try:
    import random, pygame, pymunk, time
    from pygame import mixer as mx
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

def inputcontroller(main_globals):
    def input_controller(main_globals):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() # https://cdn.discordapp.com/emojis/1389247646593581206.webp?size=96

            # key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: 
                    main_globals['moving_up'] = True
                if event.key == pygame.K_s: 
                    main_globals['moving_down'] = True
                if event.key == pygame.K_a:
                    main_globals['moving_left'] = True
                    if not main_globals['is_paused']:
                        main_globals['facing_left'] = True
                if event.key == pygame.K_d: 
                    main_globals['moving_right'] = True
                    if not main_globals['is_paused']:
                        main_globals['facing_left'] = False
                if event.key == pygame.K_e:
                    main_globals['pressed_e'] = True
                else:
                    main_globals['pressed_e'] = False
                if event.key == pygame.K_f:
                    main_globals['pressed_f'] = True
                else:
                    main_globals['pressed_f'] = False
                if event.key == pygame.K_ESCAPE:
                    if main_globals['is_paused'] == False: main_globals['is_paused'] = True
                    else: main_globals['is_paused'] = False

                # testing binds
                if main_globals['developer_tools'] == True:
                    if event.key == pygame.K_m:
                        if main_globals['game_stage'] == "in dungeon":
                            mx.music.pause()
                            main_globals['game_stage'] = "in menu"
                    if main_globals['game_stage'] == "in dungeon":
                        if event.key == pygame.K_h:
                            main_globals['player'].damaged(10)
                        if event.key == pygame.K_p:
                            main_globals['game_stage'] = "dead"
                        if event.key == pygame.K_y:
                            rand1 = random.randint(0, 9)
                            rand2 = random.randint(0, 9)
                            main_globals['update_tile'](main_globals, rand1, rand2, 99)
                            main_globals['update_tile'](main_globals, rand1 + 1, rand2, 2)
                            main_globals['camera_x'], main_globals['camera_y'] = main_globals['get_camera_offset'](main_globals, main_globals['player'], main_globals['tile_size'])
                            main_globals['spawn_weapons'](main_globals)
                        if event.key == pygame.K_r:
                            main_globals['player'].respawn()
                        if event.key == pygame.K_o:
                            main_globals['player'].locked = not main_globals['player'].locked
                            print(f"is locked {main_globals['player'].locked}")
                        if event.key == pygame.K_b:
                            if not main_globals['in_shop']:
                                main_globals['in_shop'] = True # just now for debugging use match state when actually doing the thing
                                main_globals['game_stage'] = "shopping"
                                print("in shop")
                            else:
                                main_globals['in_shop'] = False
                                main_globals['game_stage'] = "in dungeon"
                                print("dih")

            # keys releases
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w: main_globals['moving_up'] = False
                if event.key == pygame.K_s: main_globals['moving_down'] = False
                if event.key == pygame.K_a: main_globals['moving_left'] = False
                if event.key == pygame.K_d: main_globals['moving_right'] = False

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if main_globals['game_stage'] == "choosing mode":
                        if main_globals['mode1button'].collidepoint(main_globals['mouse_pos']):
                            main_globals['transition_active'] = True
                            main_globals['transition_side'] = 'left'
                            main_globals['selected_mode'] = 1
                        if main_globals['mode2button'].collidepoint(main_globals['mouse_pos']):
                            main_globals['transition_active'] = True
                            main_globals['transition_side'] = 'right'
                            main_globals['selected_mode'] = 2
                    if main_globals['game_stage'] == "in menu": # IF IN MENU # really?
                        if main_globals['play_button'].collidepoint(main_globals['mouse_pos']):
                            main_globals['game_stage'] = "choosing mode"
                        if main_globals['settings_button'].collidepoint(main_globals['mouse_pos']):
                            main_globals['game_stage'] = "in settings"
                        if main_globals['credits_button'].collidepoint(main_globals['mouse_pos']):
                            main_globals['game_stage'] = "in credits"
                        if main_globals['bp_button'].collidepoint(main_globals['mouse_pos']):
                            main_globals['game_stage'] = "in battle pass"
                    if main_globals['game_stage'] == "in credits": # IF IN CREDITS
                        if main_globals['to_menu'].collidepoint(main_globals['mouse_pos']):
                            main_globals['game_stage'] = "in menu"
                    if main_globals['game_stage'] == "in settings": # IF IN SETTINGS
                        if main_globals['frame_slider'].collidepoint(main_globals['mouse_pos']):
                            main_globals['dragging_frame_slider'] = True
                        elif main_globals['music_slider'].collidepoint(main_globals['mouse_pos']):
                            main_globals['dragging_music_slider'] = True
                        elif main_globals['resolution_slider'].collidepoint(main_globals['mouse_pos']):
                            main_globals['dragging_resolution_slider'] = True
                        if main_globals['hints_button'].collidepoint(main_globals['mouse_pos']):
                            if main_globals['hints_text'] == "True":
                                main_globals['hints_text'] = "False"
                                print("hints disabled")
                            else: 
                                main_globals['hints_text'] = "True"
                                print("hints reenabled")
                        if main_globals['to_menu'].collidepoint(main_globals['mouse_pos']):
                            main_globals['game_stage'] = "in menu"
                    if main_globals['game_stage'] == "dead": # IF DEAD
                        if main_globals['to_menu'].collidepoint(main_globals['mouse_pos']):
                            main_globals['game_stage'] = "in menu"
                            mx.music.pause()
                    if main_globals['game_stage'] == "in battle pass": # kek
                        if main_globals['to_menu'].collidepoint(main_globals['mouse_pos']):
                            pygame.quit()
                    if main_globals['player'] is not None:
                        if main_globals['game_stage'] == "in dungeon":
                            if main_globals['player'].weapons != []:
                                main_globals['player'].attack(main_globals)
                                # print("player attacked") annoys me that it says it even if its on cd so i moved it

            main_globals['mouse_pressed'] = pygame.mouse.get_pressed()[0] # hi

            # mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    main_globals['dragging_frame_slider'] = False
                    main_globals['dragging_music_slider'] = False
                    main_globals['dragging_resolution_slider'] = False

    main_globals['input_controller'] = input_controller
    print("incon, ", )