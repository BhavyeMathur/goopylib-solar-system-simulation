from solar_simulator import *

sun = StationaryBody((1e9, 0), (0, 0), 1.989e30, 10, "#edda8e")
mercury = Body((5.7909e10, 0), (0, 47.36e3), 0.33011e24, 3, "#bf8f58")
venus = Body((108.209e9, 0), (0.0, 35.02e3), 4.8675e24, 5, "#bf8f58")
earth = Body((149.596e9, 0), (0.0, 29.78e3), 5.9724e24, 5, "#588dbf")
mars = Body((227.923e9, 0), (0.0, 24.07e3), 0.64171e24, 4, "#bf6158")
jupiter = Body((778.570e9, 0.0), (0.0, 13e3), 1898.19e24, 10, "#bf6158")
saturn = Body((1433.529e9, 0.0), (0.0, 9.68e3), 568.34e24, 9, "#588dbf")
uranus = Body((2872.463e9, 0.0), (0.0, 6.80e3), 86.813e24, 7, "#588dbf")
neptune = Body((4495.060e9, 0.0), (0.0, 5.43e3), 102.413e24, 7.5, "#588dbf")

solar_system.mainloop(stars=8000)
