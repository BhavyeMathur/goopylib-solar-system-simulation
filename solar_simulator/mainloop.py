from __future__ import annotations

import goopylib.imports as gp


frame = 0

window: gp.Window
camera: SolarSystemCamera


def update_follow_body(mouse_down):
    if mouse_down:
        return

    mouse_pos = window.get_mouse_position()
    other = None

    for body in Body.instances:
        if body.contains(*mouse_pos):
            if isinstance(body, StationaryBody):
                break
            if camera.follow_body == body:
                return

            other = body
            break

    camera.travel_to(other)
    universe.recalculate_dt()


def update_frame():
    global frame

    stars.twinkle()
    sunlight.shine()
    planets.orbit()
    camera.update()

    if camera.follow_body is not None or camera.is_travelling:
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
    window.set_key_callback(gp.KEY_UP, universe.increase_dt)
    window.set_key_callback(gp.KEY_DOWN, universe.decrease_dt)

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
