from __future__ import annotations

import goopylib.imports as gp
import time

from . body import Body

TRAVEL_TIME = 1.5
TRAVEL_EASE = gp.ease_cubic()


class SolarSystemCamera(gp.Camera):
    def __init__(self, window):
        self._camera = window.get_camera()

        self.background = gp.Image("assets/background.jpeg", (0, 0), 1200, 1000).draw(window)
        self.background.transparency = 0.2
        self.background.z = -0.01

        self.vignette = gp.Image("assets/vignette.png", (0, 0), 800, 800).draw(window)
        self.vignette.transparency = 0.99
        
        self.follow_body: Body | None = None
        self.is_travelling = False

    @gp.Camera.position.setter
    def position(self, value) -> None:
        self._camera.position = value
        self.vignette.position = value
        self.background.position = value

    @gp.Camera.x.setter
    def x(self, value) -> None:
        self._camera.x = value
        self.vignette.x = value
        self.background.x = value

    @gp.Camera.y.setter
    def y(self, value) -> None:
        self._camera.y = value
        self.vignette.y = value
        self.background.y = value

    @gp.Camera.rotation.setter
    def rotation(self, angle: float) -> None:
        self._camera.rotation = angle
        self.vignette.rotation = -angle

    @gp.Camera.zoom.setter
    def zoom(self, value: float) -> None:
        self._camera.zoom = value

        rotation = self.vignette.rotation
        self.vignette.rotation = 0
        self.vignette.set_size(**self.get_visible_size())
        self.vignette.rotation = rotation  # TODO image should not require rotation to 0 for this to work
        
    def follow(self, other):
        self.position = other.position
        self.rotation = -other.rotation
        
    def travel(self):
        if self.follow_body is None:
            target_rotation = 0
            target_position = (0, 0)
            target_scale = 1
        else:
            target_rotation = -self.follow_body.rotation
            target_position = self.follow_body.position
            target_scale = self.follow_body.follow_zoom

        if abs(target_rotation - self.travel_start_rotation) > 180:
            target_rotation = -(360 - target_rotation)

        mu = (time.time() - self.travel_start) / TRAVEL_TIME
        mu = TRAVEL_EASE(min(mu, 1))

        scroll.process_scale(target_scale * mu + (1 - mu) * self.travel_start_scale)

        self.rotation = target_rotation * mu + (1 - mu) * self.travel_start_rotation
        # TODO add goopylib interpolation functions
        self.x = target_position[0] * mu + (1 - mu) * self.travel_start_position[0]
        self.y = target_position[1] * mu + (1 - mu) * self.travel_start_position[1]

        self.is_travelling = mu != 1
    
    def travel_to(self, other):
        self.travel_start_rotation = self.rotation
        self.travel_start_position = self.position
        self.travel_start_scale = scroll.scale
        
        self.follow_body = other
        self.is_travelling = True
        self.travel_start = time.time()
        
    def update(self):
        if self.is_travelling:
            self.travel()
        elif self.follow_body is not None:
            self.follow(self.follow_body)


from . import scroll
