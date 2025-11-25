# for the in game terminal

try:
    import pygame
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

def cmd(main_globals):
    def reset(main_globals):
        main_globals['player'].health = 100
        main_globals['player'].weapons = []
        main_globals['player'].inventory = {}
        main_globals['spawn_set'] = False
        main_globals['player'].wealth = 0
        main_globals['groups_spawned'] = 0
        main_globals['enemy_list'] = []
        main_globals['in_shop'] = False
        main_globals['blood_particles'] = []
        main_globals['money_texts'] = []
        main_globals['facing_left'] = False
        main_globals['is_paused'] = False
        main_globals['inventory_texts'] = []
        main_globals['money_texts'] = []
        for call in main_globals['default_tilemap_calls']:
            eval(call)
        main_globals['rebuild_walkable_mask'](main_globals)
        main_globals['active_tiles'] = []
        main_globals['current_floor'] = 0

    def shell(main_globals, event):
        sections = {
            "branching commands": {
                "weapon": "weapon name",
                "money": "amount",
                "health": "amount",
                "stage": "stage name",
                "inventory": "add/remove, item name+amount",
            },
            "regular commands": {
                "rebuild": "rebuild floor",
                "reset": "reset dungeon",
                "respawn": "respawn player",
                "ccache": "clear data",
            },
            "exit commands": {
                "quit, q, exit, x": "",
            }
        }

        key = getattr(event, "unicode", "")

        # cmd mode
        if not main_globals.get('cmd_active', False):
            sequence = "cmd"
            dttv = main_globals.get('dttv', 0)
            if key.lower() == sequence[dttv]:
                main_globals['dttv'] = dttv + 1
                if main_globals['dttv'] == len(sequence):
                    main_globals['cmd_active'] = True
                    main_globals['is_paused'] = True
                    main_globals['cmd_buffer'] = ""
                    main_globals['waiting_for_input'] = None
                    print("\n> ", end="", flush=True)
                    main_globals['dttv'] = 0
                return
            else:
                main_globals['dttv'] = 0
            return

        waiting = main_globals.get('waiting_for_input')

        # backspace
        if event.key == pygame.K_BACKSPACE:
            if main_globals['cmd_buffer']:
                main_globals['cmd_buffer'] = main_globals['cmd_buffer'][:-1]
                print('\b \b', end="", flush=True)
            return

        # enter
        if event.key == pygame.K_RETURN:
            cmd = main_globals['cmd_buffer'].strip()
            main_globals['cmd_buffer'] = ""

            if waiting:
                value = cmd
                try:
                    if waiting == "inventory_action":
                        action = value.lower()
                        if action in ["a", "add", "+"]:
                            main_globals['waiting_for_input'] = "inventory_add"
                            print(" >>> name, amount: ", end="", flush=True)
                        elif action in ["r", "remove", "-"]:
                            main_globals['waiting_for_input'] = "inventory_remove"
                            print(" >>> name, amount: ", end="", flush=True)
                        else:
                            print("error: invalid action")
                            main_globals['waiting_for_input'] = None
                            print("> ", end="", flush=True)
                        return

                    elif waiting == "inventory_add":
                        parts = value.split(maxsplit=1)
                        if len(parts) == 0:
                            print("error: no item specified")
                        else:
                            item = parts[0]
                            try:
                                amount = int(parts[1]) if len(parts) > 1 else 1
                            except ValueError:
                                print("error: invalid amount")
                                main_globals['waiting_for_input'] = None
                                print("> ", end="", flush=True)
                                return

                            main_globals['player'].inventory[item] = main_globals['player'].inventory.get(item, 0) + amount
                            print(f"\nadded {amount} x {item}")

                        main_globals['waiting_for_input'] = None
                        print("> ", end="", flush=True)
                        return

                    elif waiting == "inventory_remove":
                        parts = value.split(maxsplit=1)
                        if len(parts) == 0:
                            print("error: no item specified")
                        else:
                            item = parts[0]
                            try:
                                amount = int(parts[1]) if len(parts) > 1 else 0
                            except ValueError:
                                print("error: invalid amount")
                                main_globals['waiting_for_input'] = None
                                print("> ", end="", flush=True)
                                return

                            if item not in main_globals['player'].inventory:
                                print(f"\nerror: {item} not in inventory")
                            else:
                                current = main_globals['player'].inventory[item]
                                if amount == 0 or amount >= current:
                                    removed_amount = current
                                    del main_globals['player'].inventory[item]
                                    print(f"\nremoved {removed_amount} {item}")
                                else:
                                    main_globals['player'].inventory[item] = current - amount
                                    print(f"\nremoved {amount} {item}")

                        main_globals['waiting_for_input'] = None
                        print("> ", end="", flush=True)
                        return

                    if waiting == "weapon":
                        if value not in main_globals['weapon_stats']:
                            raise ValueError("invalid")
                        new_weapon = main_globals['Weapon'](value)
                        main_globals['player'].weapon = new_weapon
                        main_globals['player'].weapons = [new_weapon]
                        print(f"\n>> weapon set to {value}")

                    elif waiting == "money":
                        main_globals['give_money'](int(value))
                        print(f"\nmoney set to {value}")

                    elif waiting == "health":
                        main_globals['player'].health = int(value)
                        print(f"\nhealth set to {value}")

                    elif waiting == "stage":
                        main_globals['game_stage'] = value
                        print(f"\nstage set to {value}")

                except Exception:
                    print(f"\nerror: invalid")

                main_globals['waiting_for_input'] = None
                print("> ", end="", flush=True)
                return

            cmd_lower = cmd.lower()
            if cmd_lower in ["quit", "q", "exit", "x"]:
                main_globals['cmd_active'] = False
                main_globals['is_paused'] = False
                print("\nexit")

            elif cmd_lower == "help":
                print()
                for category, cmds in sections.items():
                    print(f"{category}:")
                    for name, desc in cmds.items():
                        print(f"    {name:<10} {desc}")
                    print()
                print("> ", end="", flush=True)

            elif cmd_lower in ["weapon", "money", "health", "stage"]:
                main_globals['waiting_for_input'] = cmd_lower
                prompt = {
                    "weapon": " >> name: ",
                    "money": " >> amount: ",
                    "health": " >> amount: ",
                    "stage": " >> stage name: "
                }[cmd_lower]
                print(prompt, end="", flush=True)

            elif cmd_lower == "rebuild":
                main_globals['remake_floor']()
                print("done\n> ", end="", flush=True)

            elif cmd_lower == "reset":
                main_globals['reset'](main_globals)
                print("done\n> ", end="", flush=True)

            elif cmd_lower == "respawn":
                main_globals['player'].respawn()
                print("done\n> ", end="", flush=True)

            elif cmd_lower == "ccache":
                for i in main_globals['connector_instance'].data:
                    main_globals['save'](main_globals, **{i: main_globals['connector_instance'].default_data[i]})
                print("done\n> ", end="", flush=True)

            elif cmd_lower == "weapon":
                main_globals['waiting_for_input'] = "weapon"
                print(" >> name: ", end="", flush=True)

            elif cmd_lower == "inventory":
                main_globals['waiting_for_input'] = "inventory_action"
                main_globals['current_tab'] = "inventory"
                print(" >> add/remove: ", end="", flush=True)

            # invalid command
            else:
                print("\nerror: invalid command\n> ", end="", flush=True)

        # print characters in terminal
        elif key:
            main_globals['cmd_buffer'] += key
            print(key, end="", flush=True)

    main_globals['shell'] = shell
    main_globals['reset'] = reset
    print("cmd, ", end="")
