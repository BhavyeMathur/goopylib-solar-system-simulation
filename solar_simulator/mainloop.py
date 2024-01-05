import goopylib.imports as gp
import time
import math

import os

PATH = os.path.dirname(os.path.realpath(__file__))

frame = 0
last_refresh = 0
total_scroll = 0

next_scroll = None
window: gp.Window


def move_through_space(_, scroll):
    global next_scroll, total_scroll

    scroll = 1/30 * math.tanh(scroll)  # smoothing the scroll
    total_scroll = min(max(total_scroll + scroll, -4), 4)
    window.get_camera().zoom = (3 * math.tanh(-total_scroll) + 11) / 8

    mu = (total_scroll + 4) / 8

    _bodies.rescale(mu)
    _sunlight.expand(mu)
    _universe.calculate_dt(mu)

    if abs(scroll) > 0.001:
        next_scroll = scroll - 0.00005 * (-1 if scroll < 0 else 1)
    else:
        next_scroll = None


def mainloop(stars=8000, sunlight_rings=20):
    global window, frame, last_refresh

    window = gp.Window(800, 800, "Solar System Simulation")
    window.background = gp.Color("#1d1826")
    window.scroll_callback = move_through_space

    # gp.Image(f"{PATH}/../assets/background.jpeg", (0, 0)).draw(window)

    Body.draw_all(window)
    _stars.init(stars, window)
    _sunlight.init(sunlight_rings, window)

    gp.set_buffer_swap_interval(0)
    move_through_space(0, 0)

    while window.is_open():
        gp.update()
        _universe.evolve()

        if time.time() - last_refresh > 0.02:
            _stars.twinkle()
            Body.update_all(frame)
            _sunlight.shine()

            frame += 1
            last_refresh = time.time()

            if next_scroll:
                move_through_space(0, next_scroll)

    gp.terminate()


from . import stars as _stars
from . import sunlight as _sunlight
from . import engine as _universe
from .body import Body
from . import body as _bodies
