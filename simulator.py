from game_env import Game_env
import pygame
import constants as const
import math

screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

env = Game_env(screen=screen, fps=60)
while True:
    env.render()
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #         exit()
    keys = pygame.key.get_pressed()
    # soccer_bot.move(keys)
    if keys[pygame.K_DOWN]:
        # Accelerate forward
        env.soccer_bot_one.move_direction(const.Direction.BACKWARD)
    elif keys[pygame.K_UP]:
        print("up")
        # Accelerate backward
        env.soccer_bot_one.move_direction(const.Direction.FORWARD)
    else:
        # Decelerate towards 0 speed
        env.soccer_bot_one.move_direction(const.Direction.STOP_TOWARDS)
    if keys[pygame.K_RIGHT]:
        # Accelerate left (rotate left)
        env.soccer_bot_one.move_direction(const.Direction.RIGHT)
    elif keys[pygame.K_LEFT]:
        # Accelerate right (rotate right)
        env.soccer_bot_one.move_direction(const.Direction.LEFT)
    else:
        # Decelerate rotation towards 0 rotation speed
        env.soccer_bot_one.move_direction(const.Direction.STOP_ROTATION)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     env.print_state()
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
        #     env.soccer_bot_one.body.position += (0,-10)
        #     env.space.reindex_shapes_for_body(env.soccer_bot_one.body)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
        #     env.soccer_bot_one.body.position += (0,10)
        #     env.space.reindex_shapes_for_body(env.soccer_bot_one.body)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        #     env.soccer_bot_one.body.position += (-10,0)
        #     env.space.reindex_shapes_for_body(env.soccer_bot_one.body)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
        #     env.soccer_bot_one.body.position += (10,0)
        #     env.space.reindex_shapes_for_body(env.soccer_bot_one.body)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        #     env.soccer_ball.body.position += (0,-10)
        #     env.space.reindex_shapes_for_body(env.soccer_ball.body)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        #     env.soccer_ball.body.position += (0,10)
        #     env.space.reindex_shapes_for_body(env.soccer_ball.body)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
        #     env.soccer_ball.body.position += (-10,0)
        #     env.space.reindex_shapes_for_body(env.soccer_ball.body)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        #     env.soccer_ball.body.position += (10,0)
        #     env.space.reindex_shapes_for_body(env.soccer_ball.body)
        # if event.type == pygame.KEYDOWN:
        #     env.get_reward(env.soccer_bot_one, env.soccer_bot_two)