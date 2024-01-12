from solar_simulator import *

import os

PATH = os.path.dirname(os.path.realpath(__file__))


mercury = Body((5.7909e10, 0), (0, 47.36e3), 0.33011e24, 3, f"{PATH}/assets/Mercury.png",
               trail_period=40, follow_dt=200, follow_zoom=-4)
venus = Body((108.209e9, 0), (0.0, 35.02e3), 4.8675e24, 5, f"{PATH}/assets/Venus.png",
             trail_period=70, follow_dt=500, follow_zoom=-4)
earth = Body((149.596e9, 0), (0.0, 29.78e3), 5.9724e24, 6, f"{PATH}/assets/Earth.png",
             trail_period=96, follow_dt=800, follow_zoom=-3.8)
mars = Body((227.923e9, 0), (0.0, 24.07e3), 0.64171e24, 4, f"{PATH}/assets/Mars.png",
            trail_period=98.6, follow_dt=1000, follow_zoom=-3.5)
jupiter = Body((778.570e9, 0.0), (0.0, 13e3), 1898.19e24, 12, f"{PATH}/assets/Jupiter.png",
               trail_period=500, follow_dt=5000, follow_zoom=-1.5)
saturn = Body((1433.529e9, 0.0), (0.0, 9.68e3), 568.34e24, 10, f"{PATH}/assets/Saturn.png",
              trail_period=1000, follow_dt=8500, follow_zoom=-0.36)
uranus = Body((2872.463e9, 0.0), (0.0, 6.80e3), 86.813e24, 9, f"{PATH}/assets/Uranus.png",
              trail_period=2500, follow_dt=20000, follow_zoom=1.01)
neptune = Body((4495.060e9, 0.0), (0.0, 5.43e3), 102.413e24, 9.5, f"{PATH}/assets/Neptune.png",
               trail_period=4000, follow_dt=30000, follow_zoom=3.14)

solar_system.mainloop(nstars=10000)
