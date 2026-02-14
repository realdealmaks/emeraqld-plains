# for switching the game state
# stsw - stage switcher

try:
    import pygame
except ImportError as e:
    print(f"missing module {e}")

def stsw(main_globals):

    def match_state(main_globals, state):
        match state:

            case "in menu":
                main_globals['draw_menu'](main_globals, main_globals['mouse_pos'])
                main_globals['musicswitcher'](main_globals, 3)

            case "choosing mode" | "in dungeon":

                if state == "choosing mode":
                    main_globals['draw_mode_selection'](main_globals, main_globals['mouse_pos'])

                elif state == "in dungeon":
                    if main_globals['textures_ready']: # wait for tile textures
                        main_globals['draw_dungeon'](main_globals, main_globals['player'], main_globals['is_paused'], main_globals['facing_left'])
                        main_globals['draw_hints'](main_globals)

                    else: # show texture progress
                        main_globals['draw_texturing_progress'](main_globals)

                    if main_globals.get('draw_autosave_spinner'):
                        main_globals['draw_autosave_spinner'](main_globals)

                if main_globals['transition_active']: # transition to dungeon
                    main_globals['transition_to_dungeon'](main_globals, main_globals['screen'])

            case "in settings":
                main_globals['draw_settings'](main_globals, main_globals['mouse_pos'])
                main_globals['musicswitcher'](main_globals, 4)

            case "stats":
                main_globals['draw_stats'](main_globals)

            case "dead":
                main_globals['draw_dead'](main_globals, main_globals['mouse_pos'])

            case "in credits":
                main_globals['draw_credits'](main_globals, main_globals['mouse_pos']) # cursed with low fps
                main_globals['musicswitcher'](main_globals, 5)

            case "in battle pass": # kek # https://cdn.discordapp.com/attachments/773066547525582860/1429558008089804883/speed.gif?ex=6903c225&is=690270a5&hm=e337ff15ddec125110c8135df1c5b8a56ba220bb733b0207d4f5040a3156a4a4&
                main_globals['draw_battle_pass'](main_globals, main_globals['mouse_pos'])

    main_globals['match_state'] = match_state

    print("stager, ", end = "")
