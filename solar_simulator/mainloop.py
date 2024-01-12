from __future__ import annotations

import goopylib.imports as gp
import time
import math

import os

PATH = os.path.dirname(os.path.realpath(__file__))

frame = 0
last_refresh = 0
total_scroll = 0

TRAVEL_TIME = 1.5
TRAVEL_EASE = gp.ease_cubic()
travelling_to_body = False

last_follow_body_rotation = 0
last_follow_body_position = (0, 0)
last_follow_body_change = 0
last_follow_body_scale = 1

window: gp.Window
camera: gp.Camera
vignette: gp.Image
background: gp.Image
follow_body: Body


def get_scale_interpolation_factor():
    return (total_scroll + 4) / 8


def process_scale(scale):
    global total_scroll

    total_scroll = scale
    zoom = (3 * math.tanh(-scale) + 11) / 8
    camera.zoom = zoom

    rotation = vignette.rotation
    vignette.rotation = 0
    vignette.set_size(**camera.get_visible_size())
    vignette.rotation = rotation  # TODO fix

    mu = get_scale_interpolation_factor()
    bodies.rescale(mu)
    sunlight.expand(mu)

    if isinstance(follow_body, StationaryBody):
        universe.calculate_dt(mu)


def move_through_space(_, scroll):
    scroll = 1/30 * math.tanh(scroll)  # smoothing the scroll
    process_scale(min(max(total_scroll + scroll, -4), 4))


def increase_dt(state):
    if state == 0:
        return
    universe.DT_MULTIPLIER = min(universe.DT_MULTIPLIER * 1.02, 20)

    if isinstance(follow_body, StationaryBody):
        universe.calculate_dt(get_scale_interpolation_factor())


def decrease_dt(state):
    if state == 0:
        return
    universe.DT_MULTIPLIER = max(universe.DT_MULTIPLIER / 1.02, 0.1)

    if isinstance(follow_body, StationaryBody):
        universe.calculate_dt(get_scale_interpolation_factor())


def update_follow_body(mouse_down):
    global follow_body, travelling_to_body
    global last_follow_body_rotation, last_follow_body_position, last_follow_body_change, last_follow_body_scale

    if mouse_down:
        return

    mouse_pos = window.get_mouse_position()
    for body in Body.instances:
        if body.contains(*mouse_pos):
            if follow_body == body:
                return

            universe.DT = body.follow_dt
            last_follow_body_rotation = camera.rotation
            last_follow_body_position = camera.position
            last_follow_body_scale = total_scroll

            follow_body = body
            travelling_to_body = True

            last_follow_body_change = time.time()
            return

    if follow_body != StationaryBody.instances[0]:
        last_follow_body_rotation = camera.rotation
        last_follow_body_position = camera.position
        last_follow_body_scale = total_scroll
        follow_body = StationaryBody.instances[0]
        travelling_to_body = True

        universe.calculate_dt(get_scale_interpolation_factor())
        last_follow_body_change = time.time()


def travel_to_new_body():
    target_rotation = -follow_body.rotation
    target_position = follow_body.position
    target_scale = follow_body.follow_zoom

    if abs(target_rotation - last_follow_body_rotation) > 180:
        target_rotation = -(360 - target_rotation)

    t = min((time.time() - last_follow_body_change) / TRAVEL_TIME, 1)

    mu = TRAVEL_EASE(t)
    process_scale(target_scale * mu + (1 - mu) * last_follow_body_scale)
    camera.rotation = target_rotation * mu + (1 - mu) * last_follow_body_rotation
    camera.x = target_position[0] * mu + (1 - mu) * last_follow_body_position[0]
    camera.y = target_position[1] * mu + (1 - mu) * last_follow_body_position[1]

    return mu != 1


def mainloop(nstars=5000, sunlight_rings=30):
    global window, camera, frame, last_refresh, vignette, background, follow_body, travelling_to_body

    window = gp.Window(800, 800, "Solar System Simulation")
    window.background = gp.Color("#140010")

    window.scroll_callback = move_through_space
    window.left_click_callback = update_follow_body
    window.set_key_callback(gp.KEY_H, Body.toggle_draw_closest)
    window.set_key_callback(gp.KEY_UP, increase_dt)
    window.set_key_callback(gp.KEY_DOWN, decrease_dt)

    camera = window.get_camera()

    background = gp.Image(f"{PATH}/../assets/background.jpeg", (0, 0), 1200, 1000).draw(window)
    background.transparency = 0.2
    background.z = -0.01

    vignette = gp.Image(f"{PATH}/../assets/vignette.png", (0, 0), 800, 800).draw(window)
    vignette.transparency = 0.99
    vignette.z = 0

    stars.init(nstars, window)
    sunlight.init(sunlight_rings, window)
    Body.draw_all(window)

    follow_body = StationaryBody.instances[0]

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

            if travelling_to_body:
                travelling_to_body = travel_to_new_body()
            else:
                camera.position = follow_body.position
                camera.rotation = -follow_body.rotation

            vignette.position = camera.position  # TODO add methods to make objects follow other objects
            vignette.rotation = -camera.rotation

            background.position = camera.position
            stars.wheel_overhead(*camera.position)

            frame += 1
            last_refresh = time.time()

    gp.terminate()


from . import stars
from . import sunlight
from . import engine as universe
from .body import Body, StationaryBody
from . import body as bodies

sun = StationaryBody((1e9, 0), (0, 0), 1.989e30, 5, "#fada7a", 10000, 1)
