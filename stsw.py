# stsw - stage switcher
def stsw(main_globals):

    def match_state(main_globals, state):
        match state:
            case "in menu":
                main_globals['draw_menu'](main_globals, main_globals['mouse_pos'])
            case "in dungeon":
                main_globals['draw_dungeon'](main_globals, main_globals['player'], main_globals['is_paused'], main_globals['facing_left'])
                main_globals['draw_hints'](main_globals)
            case "in settings":
                main_globals['draw_settings'](main_globals, main_globals['mouse_pos'])
            case "dead":
                main_globals['draw_dead'](main_globals, main_globals['mouse_pos'])
            case "in credits":
                main_globals['draw_credits'](main_globals, main_globals['mouse_pos'])
            case "shopping":
                main_globals['shop'].draw_shop(main_globals) # should change to shop ui
            case "in battle pass": # kek
                main_globals['draw_battle_pass'](main_globals, main_globals['mouse_pos'])

    main_globals['match_state'] = match_state

    print("stsw (stager) file loaded")