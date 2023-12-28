import pymunk
import random
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
        self.body.position = (self.positon[0]+random.randint(-200, 200), self.positon[1])
        self.body.angle = self.initial_angle
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
