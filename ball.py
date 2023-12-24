import pymunk

class Ball():
    def __init__(self, inial_pos:tuple, radius:int, static_body:pymunk.space) -> None:
        self.positon = inial_pos
        self.initial_angle = 0
        self.radius = radius
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = self.positon
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.mass = 5
        self.shape.elasticity = 0.8

    def reset(self):
        self.body.position = self.positon
        self.body.angle = self.initial_angle
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0