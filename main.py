import goopylib.imports as gp
from solar_simulator import *
import time

window = gp.Window(800, 800, "Solar System Simulation")
gp.set_buffer_swap_interval(0)
window.background = gp.Color("#1d1826")

sun = StationaryBody((0, 0), 1.989e30, 20, "#edda8e")
mercury = Body((5.7909e10, 0), (0, 47.36e3), 0.33011e24, 3, "#bf8f58")
venus = Body((108.209e9, 0), (0.0, 35.02e3), 4.8675e24, 5, "#bf8f58")
earth = Body((149.596e9, 0), (0.0, 29.78e3), 5.9724e24, 5, "#588dbf")
mars = Body((227.923e9, 0), (0.0, 24.07e3), 0.64171e24, 4, "#bf6158")
jupiter = Body((778.570e9, 0.0), (0.0, 13e3), 1898.19e24, 10, "#bf6158")
saturn = Body((1433.529e9, 0.0), (0.0, 9.68e3), 568.34e24, 9, "#588dbf")
uranus = Body((2872.463e9, 0.0), (0.0, 6.80e3), 86.813e24, 7, "#588dbf")
neptune = Body((4495.060e9, 0.0), (0.0, 5.43e3), 102.413e24, 7.5, "#588dbf")

planets.init(window)
stars.init(8000, window)
sunlight.init(20, window)

last_refresh = 0
next_scroll = None


def move_through_space(_, scroll):
    global next_scroll

    scroll = max(-0.3, min(0.3, scroll))

    planets.approach(scroll)
    sunlight.expand(planets.mu)
    universe.time_dilate(planets.mu)

    if abs(scroll) > 0.001:
        next_scroll = scroll - 0.00005 * np.sign(scroll)
    else:
        next_scroll = None


window.scroll_callback = move_through_space
move_through_space(0, 0)

while window.is_open():
    gp.update()

    universe.evolve()

    if time.time() - last_refresh > 0.02:
        stars.twinkle()
        sunlight.shine()
        last_refresh = time.time()
        planets.orbit()

        if next_scroll:
            move_through_space(0, next_scroll)

gp.terminate()
