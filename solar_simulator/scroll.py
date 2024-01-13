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
    bodies.rescale(mu)
    sunlight.rescale(mu)
    universe.recalculate_dt(mu)


def on_mouse_scroll(_, ds):
    ds = 1/30 * math.tanh(ds)  # smoothing the scroll
    process_scale(min(max(scale + ds, -4), 4))


from . import body as bodies
from . import sunlight
from . import engine as universe
