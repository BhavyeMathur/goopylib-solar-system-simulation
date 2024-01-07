from solar_simulator import *

import os

PATH = os.path.dirname(os.path.realpath(__file__))


sun = StationaryBody((1e9, 0), (0, 0), 1.989e30, 5, "#fada7a")
mercury = Body((5.7909e10, 0), (0, 47.36e3), 0.33011e24, 3, f"{PATH}/assets/Mercury.png", 40)
venus = Body((108.209e9, 0), (0.0, 35.02e3), 4.8675e24, 5, f"{PATH}/assets/Venus.png", 40)
earth = Body((149.596e9, 0), (0.0, 29.78e3), 5.9724e24, 5, f"{PATH}/assets/Earth.png", 96)
mars = Body((227.923e9, 0), (0.0, 24.07e3), 0.64171e24, 4, f"{PATH}/assets/Mars.png", 98.6)
jupiter = Body((778.570e9, 0.0), (0.0, 13e3), 1898.19e24, 10, f"{PATH}/assets/Jupiter.png", 500)
saturn = Body((1433.529e9, 0.0), (0.0, 9.68e3), 568.34e24, 9, f"{PATH}/assets/Saturn.png", 1000)
uranus = Body((2872.463e9, 0.0), (0.0, 6.80e3), 86.813e24, 7, f"{PATH}/assets/Uranus.png", 2500)
neptune = Body((4495.060e9, 0.0), (0.0, 5.43e3), 102.413e24, 7.5, f"{PATH}/assets/Neptune.png", 4000)

solar_system.mainloop(nstars=8000)
