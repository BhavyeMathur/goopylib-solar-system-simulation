from __future__ import annotations

import goopylib.imports as gp


frame = 0
total_scroll = 0

window: gp.Window
camera: SolarSystemCamera


def increase_dt(state):
    if state == 0:
        return
    universe.DT_MULTIPLIER = min(universe.DT_MULTIPLIER * 1.1, 20)
    universe.calculate_dt(scroll.get_scale_interpolation_factor(), camera.follow_body)


def decrease_dt(state):
    if state == 0:
        return
    universe.DT_MULTIPLIER = max(universe.DT_MULTIPLIER / 1.1, 0.1)
    universe.calculate_dt(scroll.get_scale_interpolation_factor(), camera.follow_body)


def update_follow_body(mouse_down):
    if mouse_down:
        return

    mouse_pos = window.get_mouse_position()
    for body in Body.instances:
        if body.contains(*mouse_pos):
            if (camera.follow_body == body) or isinstance(body, StationaryBody):
                return

            camera.travel_to(body)
            universe.calculate_dt(scroll.get_scale_interpolation_factor(), camera.follow_body)
            return

    if camera.follow_body is not None:
        camera.travel_to(None)
        universe.calculate_dt(scroll.get_scale_interpolation_factor(), camera.follow_body)


def update_frame():
    global frame

    stars.twinkle()
    sunlight.shine()
    planets.orbit()

    camera.update()
    if camera.is_travelling or camera.follow_body is not None:
        stars.wheel_overhead(*camera.position)

    frame += 1


def create_universe(nstars=5000, sunlight_rings=20):
    global window, camera

    window = gp.Window(800, 800, "Solar System Simulation")
    window.background = gp.Color("#140010")

    camera = SolarSystemCamera(window)
    gp.set_buffer_swap_interval(0)

    window.scroll_callback = scroll.on_mouse_scroll
    window.left_click_callback = update_follow_body
    window.set_key_callback(gp.KEY_H, closest_planet.toggle_draw_closest)
    window.set_key_callback(gp.KEY_UP, increase_dt)
    window.set_key_callback(gp.KEY_DOWN, decrease_dt)

    stars.init(nstars)
    sunlight.init(sunlight_rings)
    planets.init()
    universe.init()

    scroll.init(camera)
    scroll.process_scale(0)


def universe_is_alive():
    return window.is_open()


from .body import Body, StationaryBody
from .camera import SolarSystemCamera

from . import stars
from . import sunlight
from . import engine as universe
from . import scroll
from . import body as planets
from . import closest_planet
