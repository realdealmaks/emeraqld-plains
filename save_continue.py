# save_continue.py

import threading, pygame, types
from connector_db import save_db
from player import player

def save_continue(main_globals):

    def save_game_state(main_globals):
        player = main_globals['player']

        tilemap = main_globals.get('tilemap', [])
        tilemap_calls = main_globals['generate_update_tile_calls'](tilemap)


        weapon_names = []
        if player.weapons:
            for weapon in player.weapons:
                weapon_names.append(weapon.name)

        save_data = {
            "last_position": [player.x, player.y],
            "last_health": player.health,
            "last_wealth": player.wealth,
            "last_inventory": player.inventory.copy(),
            "last_weapons": weapon_names,
            "last_floor": main_globals.get('current_floor', 0),
            "last_tilemap_calls": tilemap_calls,
        }

        main_globals['save'](main_globals, **save_data)

    def load_game_state(main_globals):
        connector = main_globals['connector_instance']
        data = connector.get_data()
        main_globals['loading_save'] = True

        if not has_save_data(main_globals):
            print("no save data")
            return False

        player = main_globals['player']

        # restore tilemap
        calls = data.get('last_tilemap_calls', [])
        for call in calls:
            try:
                exec(call)
            except Exception as e:
                print(f"error executing: {call}, {e}")
        main_globals['rebuild_walkable_mask'](main_globals)

        # restore player pos
        pos = data.get('last_position', [0, 0])
        player.x, player.y = pos[0], pos[1]
        player.health = data.get('last_health', 100)
        player.wealth = data.get('last_wealth', 0)
        player.inventory = data.get('last_inventory', {}).copy()
        player.rect.topleft = (player.x, player.y)

        main_globals['active_tiles'] = []

        weapon_names = data.get('last_weapons', [])
        for weapon_name in weapon_names:
            weapon = main_globals['Weapon'](weapon_name)
            player.weapons.append(weapon)

        # restore stats
        main_globals['current_floor'] = data.get('last_floor', 0)

        print("loaded")
        main_globals['loading_save'] = False
        return True

    def has_save_data(main_globals):
        connector = main_globals['connector_instance']
        data = connector.get_data()

        return (
            data.get('last_health', 0) > 0 or
            data.get('last_wealth', 0) > 0 or
            len(data.get('last_inventory', {})) > 0
        )

    def clear_save_data(main_globals):
        save_data = {
            "last_position": [0, 0],
            "last_health": 0,
            "last_wealth": 0,
            "last_inventory": {},
            "last_weapons": [],
            "last_floor": 0,
            "last_tilemap_calls": [],
        }
        main_globals['save'](main_globals, **save_data)

    def auto_save(main_globals): # autosave
        if main_globals.get('autosaving'):
            return

        def save_task():
            main_globals['autosaving'] = True
            main_globals['spinner_active'] = True
            main_globals['autosave_start_time'] = pygame.time.get_ticks()

            save_game_state(main_globals)

            save_db("data.json", "game_data.db")

            main_globals['autosave_finished'] = True
            print("auto saved, ", end="")

        main_globals['autosave_finished'] = False
        threading.Thread(target=save_task, daemon=True).start()

    for name, obj in locals().items():
        if isinstance(obj, (types.FunctionType, type)):
            main_globals[name] = obj

    print("save_continue, ", end="")
