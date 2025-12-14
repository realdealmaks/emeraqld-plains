# speedloader for testings
try:
    import importlib.util, threading, pygame, time
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

def superloader():
    def load_into_globals(filepath):
        spec = importlib.util.spec_from_file_location("module_name", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        globals().update(module.__dict__)
        return module

    start_time = time.time()

    # pre defines some variables
    screen_w, screen_h = 1080, 750
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.HWSURFACE | pygame.DOUBLEBUF)
    main_globals = {}
    main_globals = {
        'screen_w': screen_w, 'screen_h': screen_h, 'screen': screen
    }

    last_context = "preparing"
    loading_step = 0
    loading_steps = 0
    bar_risen = False
    bar_h = 0
    splash_alpha = 0
    text_alpha = 0
    text_faded = False
    bar_color = (0, 170, 0)
    fade_out = False
    splash_image = pygame.image.load("assets/useful images/splashimage.jpg").convert_alpha()
    loading_icon = pygame.image.load("assets/useful images/save.png")
    loading_icon = pygame.transform.scale2x(loading_icon)

    def draw_loading_screen(step, total, context):
        nonlocal bar_risen, bar_h, splash_alpha, bar_color, last_context, text_alpha, text_faded, fade_out, screen, screen_w, screen_h

        if context is not None:
            last_context = context
        else:
            context = last_context

        screen.fill((0, 0, 0))
        splash_image.set_alpha(splash_alpha)
        screen.blit(splash_image, (screen_w // 2 - splash_image.get_width() // 2, screen_h // 2 - splash_image.get_height() // 2))

        if not fade_out and splash_alpha < 255:
            splash_alpha += 5
            if splash_alpha > 255:
                splash_alpha = 255

        if fade_out and splash_alpha > 0:
            splash_alpha -= 5
            if splash_alpha < 0:
                splash_alpha = 0

        bar_w = screen_w
        target_bar_h = 20

        if not fade_out and not bar_risen and bar_h < target_bar_h:
            bar_h += 2
            if bar_h >= target_bar_h:
                bar_h = target_bar_h
                bar_risen = True

        if fade_out and bar_h > 0:
            bar_h -= 2
            if bar_h < 0:
                bar_h = 0

        if not fade_out and bar_risen and not text_faded:
            text_alpha += 5
            if text_alpha >= 255:
                text_alpha = 255
                text_faded = True

        if fade_out:
            if text_alpha > 0:
                text_alpha -= 5
                if text_alpha < 0:
                    text_alpha = 0

        pygame.draw.rect(screen, (80, 80, 80), (0, screen_h - bar_h, bar_w, target_bar_h))
        pygame.draw.rect(screen, bar_color, (0, screen_h - bar_h, (bar_w / total) * step if total else 0, target_bar_h))

        angle = (pygame.time.get_ticks() // 5) % 360
        rotated_icon = pygame.transform.rotate(loading_icon, angle)
        rotated_rect = rotated_icon.get_rect(center=(50, screen_h - 70))
        rotated_icon.set_alpha(text_alpha)
        screen.blit(rotated_icon, rotated_rect.topleft)

        temp_font = pygame.font.Font("assets/font/editundo.ttf", 34)
        display_text = f"loading {context}..." if context not in ("preparing", "finalizing") else context
        text = temp_font.render(display_text, True, (255, 255, 255))
        text_rect = text.get_rect(topleft=(loading_icon.get_width() + 20, screen_h - 60))
        text.set_alpha(text_alpha)
        screen.blit(text, text_rect)

        pygame.display.flip()

    # modules to load
    modules_to_load = [
        ("stsw", "stager"),
        ("loader1", "variables"),
        ("connector", "data"),
        ("loader2", "assets"),
        ("ui", "ui"),
        ("weapons", "logic"),
        ("loader3", "logic"),
        ("shop", "logic"),
        ("dungeon", "logic"),
        ("player", "logic"),
        ("enemy", "logic"),
        ("inputcontroller", "controller"),
        ("cmd", "tools"),
    ]
    loading_steps = len(modules_to_load)

    loading_done = False
    loading_error = None
    loaded_modules = []

    print("loading: ", end="")

    def loader():
        nonlocal loading_done, loading_error, loaded_modules, loading_step, last_context

        try:
            for idx, (mod_name, context) in enumerate(modules_to_load, start=1):
                loading_step = idx
                last_context = context

                # load module into globals
                mod = load_into_globals(f"{mod_name}.py")
                loaded_modules.append((mod, mod_name))

                loader_func = getattr(mod, mod_name, None)
                if loader_func:
                    loader_func(main_globals)

            loading_done = True
        except Exception as e:
            loading_error = e
            loading_done = True

    draw_loading_screen(0, loading_steps, last_context)
    pygame.event.pump()

    thread = threading.Thread(target=loader, daemon=True)
    thread.start()

    while not loading_done:
        draw_loading_screen(loading_step, loading_steps, last_context)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

    if loading_error:
        raise loading_error

    fade_out = True
    while splash_alpha > 0:
        draw_loading_screen(loading_step, loading_steps, "finalizing")

    main_globals['game_stage'] = "in menu"
    total_time = time.time() - start_time
    print(f"took {total_time:.2f} seconds to load")
    return main_globals
