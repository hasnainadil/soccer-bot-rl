from objects import Ball, BOT
import pymunk 
import pygame
import pymunk.pygame_util
import numpy as np
import constants as const
import math

def true_y(pos_y, screen_height):
    return screen_height - pos_y

def true_x(pos_x):
    return pos_x

def true_pos(pos:tuple, screen_height):
    return (true_x(pos[0]), true_y(pos[1], screen_height))

def get_direction(ball_pos:tuple, bot_pos:tuple, bot_angle:float)->tuple:
    direction = (ball_pos[0] - bot_pos[0], ball_pos[1] - bot_pos[1])
    direction = (direction[0] * math.cos(bot_angle) - direction[1] * math.sin(bot_angle), direction[0] * math.sin(bot_angle) + direction[1] * math.cos(bot_angle))
    return (round(direction[0], 2), round(direction[1], 2))
def label_direction(directions:tuple)-> list:
    l=[]
    if directions[0] > 0:
        l.append("right")
    elif directions[0] < 0:
        l.append("left")
    else:
        l.append("none")
    if directions[1] > 0:
        l.append("up")
    elif directions[1] < 0:
        l.append("down")
    else:
        l.append("none")
    return l

def sim():
    pygame.init()
    screen = pygame.display.set_mode((800, 700))
    space = pymunk.Space()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    fps = 60
    clock = pygame.time.Clock()
    static_body = space.static_body # define static body for friction
    ball_initial_pos = (screen.get_width()//2, screen.get_height()//2)
    ball_radius = 20
    soccer_ball = Ball(ball_initial_pos, ball_radius)
    pivot = pymunk.PivotJoint(static_body, soccer_ball.shape.body, (0, 0), (0, 0))
    pivot.max_bias = 0 # disable joint correction
    pivot.max_force = 50 # emulate linear friction 
    space.add(soccer_ball.body, soccer_ball.shape, pivot)
    bot_initial_pos = true_pos((0,0),screen.get_height())
    ps = [(50, 50), (-50, 50), (-50, -50), (50, -50)]
    soccer_bot = BOT(bot_initial_pos, ps, initial_angle=0)
    pivot = pymunk.PivotJoint(static_body, soccer_bot.shape.body, (0, 0), (0, 0))
    pivot.max_bias = 0 # disable joint correction
    pivot.max_force = 300 # emulate linear friction

    space.add(soccer_bot.body, soccer_bot.shape)
    print("Ball positional details:",soccer_ball.shape.body.position, soccer_ball.shape.body.angle)
    print("Bot positional details:",soccer_bot.shape.body.position, soccer_bot.shape.body.angle)
    directions =  get_direction(true_pos(soccer_ball.shape.body.position,screen_height=screen.get_height()), true_pos(soccer_bot.shape.body.position,screen_height=screen.get_height()), soccer_bot.shape.body.angle)
    print("Directions:",label_direction(directions))



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                soccer_bot.body.angle += math.pi/8
                space.reindex_shapes_for_body(soccer_bot.body)
                print("Bot positional details:",soccer_bot.shape.body.position, soccer_bot.shape.body.angle)
                print("Directions:",label_direction(get_direction(true_pos(soccer_ball.shape.body.position,screen_height=screen.get_height()), true_pos(soccer_bot.shape.body.position,screen_height=screen.get_height()), soccer_bot.shape.body.angle)))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                soccer_bot.body.angle -= math.pi/8
                space.reindex_shapes_for_body(soccer_bot.body)
                print("Bot positional details:",soccer_bot.shape.body.position, soccer_bot.shape.body.angle)
                print("Directions:",label_direction(get_direction(true_pos(soccer_ball.shape.body.position,screen_height=screen.get_height()), true_pos(soccer_bot.shape.body.position,screen_height=screen.get_height()), soccer_bot.shape.body.angle)))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                soccer_bot.body.position = (soccer_bot.body.position[0], soccer_bot.body.position[1] - 10)
                space.reindex_shapes_for_body(soccer_bot.body)
                print("Bot positional details:",soccer_bot.shape.body.position, soccer_bot.shape.body.angle)
                print("Directions:",label_direction(get_direction(true_pos(soccer_ball.shape.body.position,screen_height=screen.get_height()), true_pos(soccer_bot.shape.body.position,screen_height=screen.get_height()), soccer_bot.shape.body.angle)))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                soccer_bot.body.position = (soccer_bot.body.position[0], soccer_bot.body.position[1] + 10)
                space.reindex_shapes_for_body(soccer_bot.body)
                print("Bot positional details:",soccer_bot.shape.body.position, soccer_bot.shape.body.angle)
                print("Directions:",label_direction(get_direction(true_pos(soccer_ball.shape.body.position,screen_height=screen.get_height()), true_pos(soccer_bot.shape.body.position,screen_height=screen.get_height()), soccer_bot.shape.body.angle)))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                soccer_bot.body.position = (soccer_bot.body.position[0] - 10, soccer_bot.body.position[1])
                space.reindex_shapes_for_body(soccer_bot.body)
                print("Bot positional details:",soccer_bot.shape.body.position, soccer_bot.shape.body.angle)
                print("Directions:",label_direction(get_direction(true_pos(soccer_ball.shape.body.position,screen_height=screen.get_height()), true_pos(soccer_bot.shape.body.position,screen_height=screen.get_height()), soccer_bot.shape.body.angle)))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                soccer_bot.body.position = (soccer_bot.body.position[0] + 10, soccer_bot.body.position[1])
                space.reindex_shapes_for_body(soccer_bot.body)
                print("Bot positional details:",soccer_bot.shape.body.position, soccer_bot.shape.body.angle)
                print("Directions:",label_direction(get_direction(true_pos(soccer_ball.shape.body.position,screen_height=screen.get_height()), true_pos(soccer_bot.shape.body.position,screen_height=screen.get_height()), soccer_bot.shape.body.angle)))


        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        pygame.display.flip()


if __name__ == "__main__":
    a = np.array([1,2,3])
    b = np.array([4,5,6])
    c = np.concatenate((a,b))
    d,e = np.split(c,2)
    print(d,e)

    # # print(c)
    # sim()
