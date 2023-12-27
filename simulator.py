from game_env import Game_env
import pygame
import constants as const
import math

screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

env = Game_env(screen=screen, fps=60)
while True:
    done, ending_reward_one, ending_reward_two = env.render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:

            keys = pygame.key.get_pressed()
            # soccer_bot.move(keys)
            if keys[pygame.K_DOWN]:
                # Accelerate forward
                env.play_step((const.Direction.BACKWARD, const.Direction.STOP_ROTATION),(const.Direction.STOP_TOWARDS, const.Direction.STOP_ROTATION))
            elif keys[pygame.K_UP]:
                # Accelerate backward
                env.play_step((const.Direction.FORWARD, const.Direction.STOP_ROTATION),(const.Direction.STOP_TOWARDS, const.Direction.STOP_ROTATION))
            else:
                # Decelerate towards 0 speed
                env.soccer_bot_one.move_direction(const.Direction.STOP_TOWARDS)
            if keys[pygame.K_RIGHT]:
                # Accelerate left (rotate left)
                env.play_step((const.Direction.STOP_TOWARDS, const.Direction.RIGHT),(const.Direction.STOP_TOWARDS, const.Direction.STOP_ROTATION))
            elif keys[pygame.K_LEFT]:
                # Accelerate right (rotate right)
                env.play_step((const.Direction.STOP_TOWARDS, const.Direction.LEFT),(const.Direction.STOP_TOWARDS, const.Direction.STOP_ROTATION))
            else:
                # Decelerate rotation towards 0 rotation speed
                env.soccer_bot_one.move_direction(const.Direction.STOP_ROTATION)

            if keys[pygame.K_w]:
                # Accelerate forward
                env.play_step((const.Direction.STOP_TOWARDS, const.Direction.STOP_ROTATION),(const.Direction.FORWARD, const.Direction.STOP_ROTATION))
            elif keys[pygame.K_s]:
                env.play_step((const.Direction.STOP_TOWARDS, const.Direction.STOP_ROTATION),(const.Direction.BACKWARD, const.Direction.STOP_ROTATION))
            else:
                # Decelerate towards 0 speed
                env.soccer_bot_two.move_direction(const.Direction.STOP_TOWARDS)
            if keys[pygame.K_d]:
                env.play_step((const.Direction.STOP_TOWARDS, const.Direction.STOP_ROTATION),(const.Direction.STOP_TOWARDS, const.Direction.RIGHT))
            elif keys[pygame.K_a]:
                env.play_step((const.Direction.STOP_TOWARDS, const.Direction.STOP_ROTATION),(const.Direction.STOP_TOWARDS, const.Direction.LEFT))
            else:
                # Decelerate rotation towards 0 rotation speed
                env.soccer_bot_two.move_direction(const.Direction.STOP_ROTATION)

    if done:
        env.reset()
        print("Ending reward one:", ending_reward_one, "Ending reward two:", ending_reward_two)

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