from __future__ import annotations

import goopylib.imports as gp
import time
import math


frame = 0
last_refresh = 0
total_scroll = 0

window: gp.Window
camera: SolarSystemCamera


def get_scale_interpolation_factor():
    return (total_scroll + 4) / 8


def process_scale(scale):
    global total_scroll

    total_scroll = scale
    zoom = (3 * math.tanh(-scale) + 11) / 8
    camera.zoom = zoom

    mu = get_scale_interpolation_factor()
    bodies.rescale(mu)
    sunlight.expand(mu)

    if camera.follow_body is None:
        universe.calculate_dt(mu)


def on_mouse_scroll(_, scroll):
    scroll = 1/30 * math.tanh(scroll)  # smoothing the scroll
    process_scale(min(max(total_scroll + scroll, -4), 4))


def increase_dt(state):
    if state == 0:
        return
    universe.DT_MULTIPLIER = min(universe.DT_MULTIPLIER * 1.02, 20)

    if camera.follow_body is None:
        universe.calculate_dt(get_scale_interpolation_factor())


def decrease_dt(state):
    if state == 0:
        return
    universe.DT_MULTIPLIER = max(universe.DT_MULTIPLIER / 1.02, 0.1)

    if camera.follow_body is None:
        universe.calculate_dt(get_scale_interpolation_factor())


def update_follow_body(mouse_down):
    if mouse_down:
        return

    mouse_pos = window.get_mouse_position()
    for body in Body.instances:
        if body.contains(*mouse_pos):
            if camera.follow_body == body:
                return

            universe.DT = body.follow_dt
            camera.travel_to(body)
            return

    if camera.follow_body is not None:
        camera.travel_to(None)
        universe.calculate_dt(get_scale_interpolation_factor())


def update_frame():
    global last_refresh, frame

    stars.twinkle()
    sunlight.shine()

    Body.update_all(frame)
    Body.draw_closest_all()

    camera.update()
    stars.wheel_overhead(*camera.position)

    frame += 1
    last_refresh = time.time()


def create_window():
    global window, camera

    window = gp.Window(800, 800, "Solar System Simulation")
    window.background = gp.Color("#140010")

    camera = SolarSystemCamera(window)
    gp.set_buffer_swap_interval(0)

    window.scroll_callback = on_mouse_scroll
    window.left_click_callback = update_follow_body
    window.set_key_callback(gp.KEY_H, Body.toggle_draw_closest)
    window.set_key_callback(gp.KEY_UP, increase_dt)
    window.set_key_callback(gp.KEY_DOWN, decrease_dt)

    process_scale(0)


def universe_is_alive():
    return window.is_open()


from . import stars
from .camera import SolarSystemCamera
from . import sunlight
from . import engine as universe
from .body import Body
from . import body as bodies
