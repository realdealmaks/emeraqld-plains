# for switching the game state
# stsw - stage switcher

def stsw(main_globals):

    def match_state(main_globals, state):
        match state:
            case "in menu":
                main_globals['draw_menu'](main_globals, main_globals['mouse_pos'])
            case "choosing mode" | "in dungeon":
                if state == "choosing mode": # cursed with low fps
                    main_globals['draw_mode_selection'](main_globals, main_globals['mouse_pos'])
                elif state == "in dungeon":
                    main_globals['draw_dungeon'](main_globals, main_globals['player'], main_globals['is_paused'], main_globals['facing_left'])
                    main_globals['draw_hints'](main_globals)
                if main_globals['transition_active']:
                    main_globals['draw_transition'](main_globals, main_globals['screen'])
            case "in settings":
                main_globals['draw_settings'](main_globals, main_globals['mouse_pos'])
            case "dead":
                main_globals['draw_dead'](main_globals, main_globals['mouse_pos'])
            case "in credits":
                main_globals['draw_credits'](main_globals, main_globals['mouse_pos']) # cursed with low fps
            case "shopping":
                main_globals['shop'].draw_shop(main_globals) # should change to shop ui its misleading
            case "in battle pass": # kek # https://cdn.discordapp.com/attachments/773066547525582860/1429558008089804883/speed.gif?ex=6903c225&is=690270a5&hm=e337ff15ddec125110c8135df1c5b8a56ba220bb733b0207d4f5040a3156a4a4&
                main_globals['draw_battle_pass'](main_globals, main_globals['mouse_pos'])

    main_globals['match_state'] = match_state

    print("stsw (stager) file loaded")
