import pymunk
import constants as const
import random
import numpy as np
import math

class BOT():
    def __init__(self, inial_pos:tuple, vertices:list, initial_angle=0) -> None:
        self.initial_pos = inial_pos
        self.initial_angle = initial_angle
        self.vertices = vertices
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = inial_pos
        self.body.angle = initial_angle
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.mass = 50
        self.shape.elasticity = 0.1
        self.speed = 0
        self.rotation_speed = 0
        self.acceleration = 50
        self.rotation_acceleration = math.pi / 2  # Rotate at pi/2 radians per second^2 (adjust as needed)
        self.model = None
        self.trainer = None
        self.memory = None

    def move_down(self,max_speed):
        self.speed = min(self.speed + self.acceleration, max_speed)
    def move_forward(self,max_speed):
        self.speed = max(self.speed - self.acceleration, -max_speed)
    def stop_towards(self):
        self.speed = 0 if abs(self.speed) < self.acceleration else self.speed - self.acceleration * (self.speed / abs(self.speed))
    def rotate_right(self,max_rotation_speed):
        self.rotation_speed = min(self.rotation_speed + self.rotation_acceleration, max_rotation_speed)
    def rotate_left(self,max_rotation_speed):
        self.rotation_speed = max(self.rotation_speed - self.rotation_acceleration, -max_rotation_speed)
    def stop_rotation(self):
        self.rotation_speed = 0 if abs(self.rotation_speed) < self.rotation_acceleration else self.rotation_speed - self.rotation_acceleration * (self.rotation_speed / abs(self.rotation_speed))

    def move_direction(self, direction:const.Direction):
        max_speed = 500
        max_rotation_speed = math.pi

        if direction == const.Direction.FORWARD:
            self.move_forward(max_speed)
        elif direction == const.Direction.BACKWARD:
            self.move_down(max_speed)
        elif direction == const.Direction.STOP_TOWARDS:
            self.stop_towards()
        if direction == const.Direction.LEFT:
            self.rotate_left(max_rotation_speed)
        elif direction == const.Direction.RIGHT:
            self.rotate_right(max_rotation_speed)
        elif direction == const.Direction.STOP_ROTATION:
            self.stop_rotation()

        # Update body's velocity and angular velocity
        forward_vector = pymunk.Vec2d(0, self.speed).rotated(self.body.angle)
        self.body.velocity = (self.body.velocity + forward_vector) / 2  # Simple averaging for smoothing
        self.body.angular_velocity = self.rotation_speed

    def reset(self):
        self.body.position = (self.initial_pos[0]+random.randint(-200, 200), self.initial_pos[1]+random.randint(0, 100))
        self.body.angle = self.initial_angle + random.uniform(-math.pi/2 , math.pi/2) * np.random.choice([2,1,0],p=[0.25,0.25,0.5])
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
        self.speed = 0
        self.rotation_speed = 0
