import goopylib.imports as gp
import time

frame = 0
last_refresh = 0
next_scroll = None


def move_through_space(_, scroll):
    global next_scroll

    scroll = max(-0.3, min(0.3, scroll))

    _planets.approach(scroll)
    _sunlight.expand(_planets.mu)
    _universe.calculate_dt(_planets.mu)

    if abs(scroll) > 0.001:
        next_scroll = scroll - 0.00005 * (-1 if scroll < 0 else 1)
    else:
        next_scroll = None


def mainloop(stars=8000, sunlight_rings=20):
    window = gp.Window(800, 800, "Solar System Simulation")
    window.background = gp.Color("#1d1826")
    window.scroll_callback = move_through_space

    _planets.init(window)
    _stars.init(stars, window)
    _sunlight.init(sunlight_rings, window)

    gp.set_buffer_swap_interval(0)
    move_through_space(0, 0)

    while window.is_open():
        gp.update()
        update()

    gp.terminate()


def update():
    global frame, last_refresh

    _universe.evolve()

    if time.time() - last_refresh > 0.02:
        _stars.twinkle()
        _sunlight.shine()
        _planets.orbit()

        if next_scroll:
            move_through_space(0, next_scroll)

        frame += 1
        last_refresh = time.time()


from . import stars as _stars
from . import sunlight as _sunlight
from . import engine as _universe
from . import renderer as _planets
