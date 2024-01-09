import goopylib.imports as gp
import time
import math

import os

PATH = os.path.dirname(os.path.realpath(__file__))

frame = 0
last_refresh = 0
total_scroll = 0

window: gp.Window
camera: gp.Camera
vignette: gp.Image


def get_scale_interpolation_factor():
    return (total_scroll + 4) / 8


def move_through_space(_, scroll):
    global total_scroll

    scroll = 1/30 * math.tanh(scroll)  # smoothing the scroll
    total_scroll = min(max(total_scroll + scroll, -4), 4)
    zoom = (3 * math.tanh(-total_scroll) + 11) / 8

    camera.zoom = zoom
    vignette.set_size(**camera.get_visible_size())

    mu = get_scale_interpolation_factor()
    bodies.rescale(mu)
    sunlight.expand(mu)
    universe.calculate_dt(mu)


def increase_dt(state):
    if state == 0:
        return
    universe.DT_MULTIPLIER = min(universe.DT_MULTIPLIER * 1.02, 20)
    universe.calculate_dt(get_scale_interpolation_factor())


def decrease_dt(state):
    if state == 0:
        return
    universe.DT_MULTIPLIER = max(universe.DT_MULTIPLIER / 1.02, 0.1)
    universe.calculate_dt(get_scale_interpolation_factor())


def mainloop(nstars=5000, sunlight_rings=20):
    global window, camera, frame, last_refresh, vignette

    window = gp.Window(800, 800, "Solar System Simulation")
    window.background = gp.Color("#240140")

    window.scroll_callback = move_through_space
    window.set_key_callback(gp.KEY_H, Body.toggle_draw_closest)
    window.set_key_callback(gp.KEY_UP, increase_dt)
    window.set_key_callback(gp.KEY_DOWN, decrease_dt)

    camera = window.get_camera()

    background = gp.Image(f"{PATH}/../assets/background.jpeg", (0, 0), 800, 800).draw(window)
    background.set_transparency(0.3)
    background.z = -1

    vignette = gp.Image(f"{PATH}/../assets/vignette.png", (0, 0), 800, 800).draw(window)
    vignette.set_transparency(0.9)

    stars.init(nstars, window)
    sunlight.init(sunlight_rings, window)
    Body.draw_all(window)

    move_through_space(0, 0)
    gp.set_buffer_swap_interval(0)

    while window.is_open():
        gp.update()
        universe.evolve()

        if time.time() - last_refresh > 0.03:
            stars.twinkle()
            sunlight.shine()

            Body.update_all(frame)
            Body.draw_closest_all()

            frame += 1
            last_refresh = time.time()

    gp.terminate()


from . import stars
from . import sunlight
from . import engine as universe
from .body import Body
from . import body as bodies
