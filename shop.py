# this file is mostly unused, for shop things check tile update loop at tile 88

import types

def shop(main_globals):

    coefficient = 3 # is that what coefficient means? # not sure buddy
    screen = main_globals['screen']

    def check_floor(main_globals, current_floor):
        return current_floor % coefficient == 0

    for name, obj in locals().items():
        if isinstance(obj, (types.FunctionType, type)):
            main_globals[name] = obj

    print("shop, ", end="")