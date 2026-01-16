# main python script
try:
    import random, pygame, pymunk, time
    from pygame import mixer as mx
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")
    raise e

# initiate things
pygame.init()
mx.init(frequency=44100, size=-16, channels=8, buffer=512)
screen_w, screen_h = 1080, 750
screen = pygame.display.set_mode((screen_w, screen_h), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_icon(pygame.image.load("assets/models/player/naganou_icon.png"))
resolution = screen_w, screen_h

# fps shit for virtual shit
vfps_max = 175
virtual_dt = 1 / vfps_max
virtual_accumulator = 0 # overflow frames
virtual_prev_time = pygame.time.get_ticks() / 1000
virtual_clock = pygame.time.Clock()
virtual_w, virtual_h = 1080, 750
virtual_screen = pygame.Surface((virtual_w, virtual_h))
dt = virtual_clock.tick(vfps_max) / 1000 # time passed since last frame
prev_time = pygame.time.get_ticks() / 1000
max_fps = 60

# pymunk space setup
space = pymunk.Space()
space.gravity = (0, 500)

# import the importer
from masterloader import superloader
main_globals = superloader() # load with the importer

print("ready, ", end="")


# dont change ts diddybludd
main_globals['developer_tools'] = True
# well obvi unless you are a dev ;(
# https://tenor.com/en-GB/view/diddyblud-diddy-einstein-albert-einstein-calc-gif-9528529477851089865


# loads data from json with connector
saved_data = main_globals['connector_instance'].get_data()
for key, value in saved_data.items():
    if key in main_globals:
        main_globals[key] = value
print(f"loaded data: {saved_data}")

# redo getting some data because they dont have the same names
frame_caps = main_globals['frame_caps']
main_globals['frame_cap'] = main_globals.get('max_fps', 60)
main_globals['frame_cap_index'] = min(range(len(frame_caps)), key=lambda i: abs(frame_caps[i] - main_globals['frame_cap']))
main_globals['frame_cap'] = frame_caps[main_globals['frame_cap_index']]

resolutions = main_globals['resolutions']
main_globals['resolution'] = main_globals.get('resolution', (1080, 750))
main_globals['resolution_index'] = min(range(len(resolutions)), key=lambda i: abs(resolutions[i][0] - main_globals['resolution'][0]))
main_globals['resolution'] = resolutions[main_globals['resolution_index']]

music_volume = saved_data.get("music", 1)
main_globals['music_volume'] = music_volume
mx.music.set_volume(music_volume)

# virtual screen setup into globales
current_time = pygame.time.get_ticks() / 1000
main_globals['dt'] = current_time - main_globals['prev_time']
main_globals['prev_time'] = current_time
main_globals['screen'] = virtual_screen # globals screen = virtual, here local = real
main_globals['resolution'] = resolutions[main_globals['resolution_index']]

main_globals['player_gif'](main_globals) # loads the player gif

# pass space to globals
main_globals['space'] = space

print(f"started, {"developer" if main_globals['developer_tools'] else "regular"}")
# loop setup
clock = pygame.time.Clock() # makes some clocks and sets the titles
pygame.display.set_caption('Naganou') # change to naganou? :))) # sure man

# makes the initial walkable surface along with what is made in it
main_globals['walkable_mask'] = main_globals['make_initial_walkable_surface'](main_globals['tilemap'], main_globals) 

# calm the fuck down man
for i in range(10):
    time.sleep(0.1) # actually what it does is warm up pytish
    pygame.event.pump()

# makes some game loops
running = True # https://cdn.discordapp.com/emojis/1234577960414085271.webp?size=96
main_globals['running'] = running
while main_globals['running']:
    main_globals['space'].step(main_globals['dt']) # physixx step for space particles
    real_mx, real_my = pygame.mouse.get_pos()
    # transform mouse coords to virtual if resolution mismatch
    mouse_pos = pygame.mouse.get_pos()
    main_globals['mouse_pos'] = (
        real_mx * virtual_w / screen.get_width(),
        real_my * virtual_h / screen.get_height()
    )

    main_globals['input_controller'](main_globals) # check inputs

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
        main_globals['dt'] = virtual_dt
        main_globals['match_state'](main_globals, main_globals['game_stage'])
        virtual_accumulator -= virtual_dt
        steps += 1

    # draw whatever is on virtual screen scaled to real screen
    if main_globals['resolution'] != resolution:
        resolution = main_globals['resolution']
        screen = pygame.display.set_mode(resolution)

    scaled_screen = pygame.transform.scale(main_globals['screen'], resolution)
    screen.blit(scaled_screen, (0,0))

    loop_fps = clock.tick(main_globals['max_fps'])
    pygame.display.flip()

    # debug caption
    if main_globals['developer_tools'] and pygame.time.get_ticks() % 100 == 0:
        vfps = int(1 / virtual_dt)
        pygame.display.set_caption(f"fps: {int(clock.get_fps())} / {main_globals['max_fps']}, vfps: {vfps}, mouse pos: {pygame.mouse.get_pos()}, vmouse pos: {int(main_globals['mouse_pos'][0]), int(main_globals['mouse_pos'][1])}, player pos: {main_globals['player'].x, main_globals['player'].y}")

print("exiting")
pygame.quit()