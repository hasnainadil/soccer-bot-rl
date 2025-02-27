import pymunk
import constants as const
import pygame
import math

class Ball():
    def __init__(self, inial_pos:tuple, radius:int) -> None:
        self.positon = inial_pos
        self.initial_angle = 0
        self.radius = radius
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = self.positon
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.mass = 5
        self.shape.elasticity = 0.90

    def reset(self):
        self.body.position = self.positon
        self.body.angle = self.initial_angle
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0


class BOT():
    def __init__(self, inial_pos:tuple, vertices:list, initial_angle=0) -> None:
        self.initial_pos = inial_pos
        self.initial_angle = initial_angle
        self.vertices = vertices
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = inial_pos
        self.body.angle = initial_angle
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.mass = 5
        self.shape.elasticity = 1
        self.speed = 0
        self.rotation_speed = 0
        self.acceleration = 50
        self.rotation_acceleration = math.pi / 2  # Rotate at pi/2 radians per second^2 (adjust as needed)
        self.model = None

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
    
        
    def move(self, keys):
        max_speed = 500  # Maximum speed (adjust as needed)
        max_rotation_speed = math.pi  # Maximum rotation speed (adjust as needed)

        if keys[pygame.K_DOWN]:
            # Accelerate forward
            self.move_down(max_speed)
        elif keys[pygame.K_UP]:
            # Accelerate backward
            self.move_forward(max_speed)
        else:
            # Decelerate towards 0 speed
            self.stop_towards()

        if keys[pygame.K_RIGHT]:
            # Accelerate left (rotate left)
            self.rotate_right(max_rotation_speed)
        elif keys[pygame.K_LEFT]:
            # Accelerate right (rotate right)
            self.rotate_left(max_rotation_speed)
        else:
            # Decelerate rotation towards 0 rotation speed
            self.stop_rotation()

        # Update body's velocity and angular velocity
        forward_vector = pymunk.Vec2d(0, self.speed).rotated(self.body.angle)
        self.body.velocity = (self.body.velocity + forward_vector) / 2  # Simple averaging for smoothing
        self.body.angular_velocity = self.rotation_speed

    def move_direction(self, direction:const.Direction):
        max_speed = 500
        max_rotation_speed = math.pi
        print(direction)

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
        self.body.position = self.initial_pos
        self.body.angle = self.initial_angle
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
        self.speed = 0
        self.rotation_speed = 0

        
class Wall():
    def __init__(self, body_position:tuple, segmen_start:tuple, segmen_end:tuple, width=2) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (0, 0)
        self.shape = pymunk.Segment(self.body, segmen_start,segmen_end, width)
        self.shape.friction = 1
        self.shape.elasticity = 0.95


#kept if ever needed for bot movement
    # def move(self, keys):
    #     speed = 500
    #     rotation_speed = math.pi  # Rotate at pi radians per second (adjust as needed)

    #     # Reset the body's velocity before applying new values
    #     self.body.velocity = (0, 0)
    #     self.body.angular_velocity = 0

    #     if keys[pygame.K_DOWN]:
    #         # Move forward
    #         forward_vector = pymunk.Vec2d(0, speed).rotated(self.body.angle)
    #         self.body.velocity += forward_vector

    #     if keys[pygame.K_UP]:
    #         # Move backward
    #         backward_vector = pymunk.Vec2d(0, -speed).rotated(self.body.angle)
    #         self.body.velocity += backward_vector

    #     if keys[pygame.K_LEFT]:
    #         # Rotate left
    #         self.body.angular_velocity = -rotation_speed

    #     if keys[pygame.K_RIGHT]:
    #         # Rotate right
    #         self.body.angular_velocity = rotation_speed