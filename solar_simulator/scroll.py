import math


scale = 0
camera = None


def init(cam):
    global camera
    camera = cam


def get_scale_interpolation_factor():
    return (scale + 4) / 8


def process_scale(s):
    global scale

    scale = s
    camera.zoom = (3 * math.tanh(-scale) + 11) / 8

    mu = get_scale_interpolation_factor()
    rescale_bodies(mu)
    rescale_sunlight(mu)

    calculate_dt(mu, camera.follow_body)


def on_mouse_scroll(_, ds):
    ds = 1/30 * math.tanh(ds)  # smoothing the scroll
    process_scale(min(max(scale + ds, -4), 4))


from .body import rescale as rescale_bodies
from .sunlight import rescale as rescale_sunlight
from .engine import calculate_dt
