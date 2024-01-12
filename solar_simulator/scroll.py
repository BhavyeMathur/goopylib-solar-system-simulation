import math


scale = 0
camera = None


def init(cam):
    global camera

    camera = cam


def scale_from_zoom(zoom):
    return -math.atanh((8 * zoom - 11) / 3)


def zoom_from_scale(s):
    return (3 * math.tanh(-s) + 11) / 8


def get_scale_interpolation_factor():
    return (scale + 4) / 8


def process_scale(s):
    global scale

    scale = s
    camera.zoom = zoom_from_scale(scale)

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
