import pymunk
import constants as const
import pygame
import math

class Wall():
    def __init__(self, body_position:tuple, segmen_start:tuple, segmen_end:tuple, width=2) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (0, 0)
        self.shape = pymunk.Segment(self.body, segmen_start,segmen_end, width)
        self.shape.friction = 1
        self.shape.elasticity = 0.95