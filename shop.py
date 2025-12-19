# this file is mostly unused

import types

def shop(main_globals):

    coefficient = 10 # is that what coefficient means?
    screen = main_globals['screen']

    def check_floor(main_globals, current_floor):
        return current_floor % coefficient == 0

    for name, obj in locals().items():
        if isinstance(obj, (types.FunctionType, type)):
            main_globals[name] = obj

    print("shop, ", end="")