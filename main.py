# main python script
try:
    import random, pygame, pymunk, time
    from pygame import mixer as mx
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

# initiate things
pygame.init()
mx.init(frequency=44100, size=-16, channels=2, buffer=8192)
screen_h, screen_w = 750, 1080
screen = pygame.display.set_mode((screen_w, screen_h), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_icon(pygame.image.load("assets/models/player/naganou_icon.png"))
resolution = screen_w, screen_h

vfps_max = 175
virtual_dt = 1 / vfps_max
virtual_accumulator = 0
virtual_prev_time = pygame.time.get_ticks() / 1000
virtual_clock = pygame.time.Clock()
virtual_w, virtual_h = 1080, 750
virtual_screen = pygame.Surface((virtual_w, virtual_h))
dt = virtual_clock.tick(vfps_max) / 1000
prev_time = pygame.time.get_ticks() / 1000
max_fps = 60

# pymunk space setup
space = pymunk.Space()
space.gravity = (0, 500)

# this turns all of the main_globals[''] slop into actually non eye burning variables
class DictNamespace:
    def __init__(self, d):
        self._d = d
    def __getattr__(self, k):
        return self._d[k]
    def __setattr__(self, k, v):
        if k == "_d":
            super().__setattr__(k, v)
        else:
            self._d[k] = v
    def __getitem__(self, k):
        return self._d[k]
    def __setitem__(self, k, v):
        self._d[k] = v

main_globals = {
    'screen_w': screen_w, 'screen_h': screen_h, 'screen': screen
}

# import the importer
from masterloader import superloader
main_globals = superloader()

main = DictNamespace(main_globals) # converts some globals
print("ready, ", end="")
# dont use main_globals['🤖'] but instead use main.🤖

# dont change ts diddybludd
main.developer_tools = True
# well obvi unless you are a dev :(
# https://tenor.com/en-GB/view/diddyblud-diddy-einstein-albert-einstein-calc-gif-9528529477851089865


# loads data from json with connector
saved_data = main_globals['connector_instance'].get_data()
for key, value in saved_data.items():
    if key in main_globals:
        main_globals[key] = value
print(f"loaded data: {saved_data}")

# redo getting data because they dont have the same names
frame_caps = main.frame_caps
main.frame_cap = main_globals.get('max_fps', 60)
main.frame_cap_index = min(range(len(frame_caps)), key=lambda i: abs(frame_caps[i] - main.frame_cap))
main.frame_cap = frame_caps[main.frame_cap_index]

resolutions = main.resolutions
main.resolution = main_globals.get('resolution', (1080, 750))
main.resolution_index = min(range(len(resolutions)), key=lambda i: abs(resolutions[i][0] - main.resolution[0]))
main.resolution = resolutions[main.resolution_index]

music_volume = saved_data.get("music", 1)
main.music_volume = music_volume
mx.music.set_volume(music_volume)

# virtual screen setup
current_time = pygame.time.get_ticks() / 1000
main.dt = current_time - main.prev_time
main.prev_time = current_time
main.screen = virtual_screen
main.resolution = resolutions[main.resolution_index]

main.player_gif(main_globals) # loads the player gif

# pass space to globals
main.space = space

time.sleep(0.3)

print(f"started, {"dev" if main.developer_tools else "reg"}")
# loop setup
clock = pygame.time.Clock() # makes some clocks and sets the titles
pygame.display.set_caption(' naganou :)))') # change to naganou? :))) # sure man

# makes the initial walkable surface along with what is made in it
main.walkable_mask = main.make_initial_walkable_surface(main.tilemap, main_globals) 

# calm the fuck down man
for i in range(10):
    time.sleep(0.1) # actually what it does is prevents 5 fps at start
    pygame.event.pump()

# makes some game loops
running = True # https://cdn.discordapp.com/emojis/1234577960414085271.webp?size=96
main.running = running
while main.running:
    main.space.step(main.dt) # physixx step for space particles
    real_mx, real_my = pygame.mouse.get_pos()
    # transform mouse coords to virtual if resolution mismatch
    mouse_pos = pygame.mouse.get_pos()
    main.mouse_pos = (
        real_mx * virtual_w / screen.get_width(),
        real_my * virtual_h / screen.get_height()
    )

    main.input_controller(main_globals) # check inputs

    # update main screen with virtual screen
    current_time = pygame.time.get_ticks() / 1000
    frame_time = current_time - virtual_prev_time
    virtual_prev_time = current_time

    frame_time = min(frame_time, 0.1)
    virtual_accumulator += frame_time
    max_virtual_steps = 5
    steps = 0
    # skip overflow frames ( if fps is below vfps (it always is))
    while virtual_accumulator >= virtual_dt and steps < max_virtual_steps:
        main.dt = virtual_dt
        main.match_state(main_globals, main.game_stage)
        virtual_accumulator -= virtual_dt
        steps += 1

    if main.resolution != resolution:
        resolution = main.resolution
        screen = pygame.display.set_mode(resolution)

    # draw whatever is on virtual screen scaled to real screen
    if main.resolution != resolution: # only if its not original
        resolution = main.resolution
        screen = pygame.display.set_mode(resolution)
        scaled_screen = pygame.transform.scale(main.screen, resolution)
    else:
        scaled_screen = pygame.transform.scale(main.screen, resolution)
    screen.blit(scaled_screen, (0,0))

    loop_fps = clock.tick(main.max_fps)
    pygame.display.flip()

    # debug caption
    if main.developer_tools:
        vfps = int(1 / virtual_dt)
        pygame.display.set_caption(f"fps: {int(clock.get_fps())} / {main.max_fps}, vfps: {vfps}, mouse pos: {pygame.mouse.get_pos()}, vmouse pos: {int(main.mouse_pos[0]), int(main.mouse_pos[1])}, player pos: {main_globals['player'].x, main_globals['player'].y}")

from connector_db import save_db
save_db("data.json", "game_data.db")
print("exiting")
pygame.quit()