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
camera: gp.Camera
vignette: gp.Image


def get_scale_interpolation_factor():
    return (total_scroll + 4) / 8


def move_through_space(_, scroll):
    global next_scroll, total_scroll

    scroll = 1/30 * math.tanh(scroll)  # smoothing the scroll
    total_scroll = min(max(total_scroll + scroll, -4), 4)
    zoom = (3 * math.tanh(-total_scroll) + 11) / 8

    camera.zoom = zoom
    vignette.set_size(**camera.get_visible_size())

    mu = get_scale_interpolation_factor()

    _bodies.rescale(mu)
    _sunlight.expand(mu)
    _universe.calculate_dt(mu)

    if abs(scroll) > 0.001:
        next_scroll = scroll - 0.00005 * (-1 if scroll < 0 else 1)
    else:
        next_scroll = None


def mainloop(stars=8000, sunlight_rings=20):
    global window, camera, frame, last_refresh, vignette

    window = gp.Window(800, 800, "Solar System Simulation")
    window.background = gp.Color("#1d1826")
    window.scroll_callback = move_through_space

    camera = window.get_camera()

    # gp.Image(f"{PATH}/../assets/background.jpeg", (0, 0)).draw(window)

    vignette = gp.Image(f"{PATH}/../assets/vignette.png", (0, 0), 800, 800).draw(window)

    _stars.init(stars, window)
    _sunlight.init(sunlight_rings, window)
    Body.draw_all(window)

    gp.set_buffer_swap_interval(0)
    move_through_space(0, 0)

    while window.is_open():
        gp.update()
        _universe.evolve()

        if time.time() - last_refresh > 0.02:
            _stars.twinkle()
            _sunlight.shine()
            Body.update_all(frame)

            if next_scroll:
                move_through_space(0, next_scroll)

            if window.check_key(gp.KEY_UP):
                _universe.DT_MULTIPLIER = min(_universe.DT_MULTIPLIER * 1.01, 20)
                _universe.calculate_dt(get_scale_interpolation_factor())

            elif window.check_key(gp.KEY_DOWN):
                _universe.DT_MULTIPLIER = max(_universe.DT_MULTIPLIER / 1.01, 0.1)
                _universe.calculate_dt(get_scale_interpolation_factor())

            frame += 1
            last_refresh = time.time()

    gp.terminate()


from . import stars as _stars
from . import sunlight as _sunlight
from . import engine as _universe
from .body import Body
from . import body as _bodies
