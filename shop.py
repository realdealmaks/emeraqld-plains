import types

def shop(main_globals):

    coefficient = 10 # is that what coefficient means?
    screen = main_globals['screen']

    def check_floor(main_globals, current_floor):
        return current_floor % coefficient == 0

    def draw(main_globals):
        screen.blit(main_globals['shopbase'], (0, 0))
        # etc

    for name, obj in locals().items():
        if isinstance(obj, (types.FunctionType, type)):
            main_globals[name] = obj

    print("shop, ", end="")