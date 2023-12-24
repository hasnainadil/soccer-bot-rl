import pymunk
import constants as const
import pygame
import math

class BOT():
    def __init__(self, inial_pos:tuple, vertices:list,static_body) -> None:
        self.initial_pos = inial_pos
        self.initial_angle = 0
        self.vertices = vertices
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = inial_pos
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.mass = 5
        self.shape.elasticity = 0.8
        self.speed = 0
        self.rotation_speed = 0
        self.acceleration = 50
        self.rotation_acceleration = math.pi / 2  # Rotate at pi/2 radians per second^2 (adjust as needed)

    # def apply_velocity_to_vertices(self, velocities):
    #     # Make sure the number of vertices matches the number of velocities
    #     assert len(self.vertices) == len(velocities)
    #     self.body.velocity = (0, 0)

    #     for i, vertex in enumerate(self.vertices):
    #         # Set the velocity of each vertex using apply_impulse_at_local_point
    #         impulse = self.body.mass * pymunk.Vec2d(*velocities[i])
    #         self.body.apply_impulse_at_local_point(impulse, vertex)
        
    def move(self, keys):
        max_speed = 500  # Maximum speed (adjust as needed)
        max_rotation_speed = math.pi  # Maximum rotation speed (adjust as needed)

        if keys[pygame.K_DOWN]:
            # Accelerate forward
            self.speed = min(self.speed + self.acceleration, max_speed)
        elif keys[pygame.K_UP]:
            # Accelerate backward
            self.speed = max(self.speed - self.acceleration, -max_speed)
        else:
            # Decelerate towards 0 speed
            self.speed = 0 if abs(self.speed) < self.acceleration else self.speed - self.acceleration * (self.speed / abs(self.speed))

        if keys[pygame.K_RIGHT]:
            # Accelerate left (rotate left)
            self.rotation_speed = min(self.rotation_speed + self.rotation_acceleration, max_rotation_speed)
        elif keys[pygame.K_LEFT]:
            # Accelerate right (rotate right)
            self.rotation_speed = max(self.rotation_speed - self.rotation_acceleration, -max_rotation_speed)
        else:
            # Decelerate rotation towards 0 rotation speed
            self.rotation_speed = 0 if abs(self.rotation_speed) < self.rotation_acceleration else self.rotation_speed - self.rotation_acceleration * (self.rotation_speed / abs(self.rotation_speed))

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
