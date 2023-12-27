import math
import pygame
import pymunk
import pymunk.pygame_util
from objects import Ball, BOT, Wall
import constants as const

pygame.init()

def check_goal_top(soccer_ball:Ball, screen:pygame.Surface) -> bool:
    return soccer_ball.shape.body.position.y < screen.get_height()//2 - const.FIELD_HEIGHT//2 and soccer_ball.shape.body.position.x > screen.get_width()//2 - const.GOAL_POST_WIDTH//2 and soccer_ball.shape.body.position.x < screen.get_width()//2 + const.GOAL_POST_WIDTH//2

def check_goal_bottom(soccer_ball:Ball, screen:pygame.Surface) -> bool:
    return soccer_ball.shape.body.position.y > screen.get_height()//2 + const.FIELD_HEIGHT//2 and soccer_ball.shape.body.position.x > screen.get_width()//2 - const.GOAL_POST_WIDTH//2 and soccer_ball.shape.body.position.x < screen.get_width()//2 + const.GOAL_POST_WIDTH//2

def display_score(screen:pygame.Surface, player_one_score:int, player_two_score:int)->None:
    font = pygame.font.Font(None, 36)
    score_text = font.render(str(player_one_score) + " : " + str(player_two_score), True, (255, 255, 255))
    pygame.draw.rect(screen, width=0, color=(0,0,0), rect=(screen.get_width()//2 - score_text.get_width()//2, screen.get_height()//2 - score_text.get_height()//2, score_text.get_width(), score_text.get_height()))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2 - score_text.get_height() // 2))
    pygame.display.flip()

def run_sim(space: pymunk.Space, screen: pygame.Surface, draw_options: pymunk.pygame_util.DrawOptions, FPS:int) -> None:
    # setting socres and playing flag
    player_one_score = 0
    player_two_score = 0

    static_body = space.static_body # define static body for friction

    # create soccer ball 
    ball_initial_pos = (screen.get_width()//2, screen.get_height()//2)
    ball_radius = const.BALL_RADIUS
    soccer_ball = Ball(ball_initial_pos, ball_radius)
    soccer_ball.shape.color = const.BALL_COLOR
    pivot = pymunk.PivotJoint(static_body, soccer_ball.shape.body, (0, 0), (0, 0))
    pivot.max_bias = 0 # disable joint correction
    pivot.max_force = 50 # emulate linear friction 
    space.add(soccer_ball.body, soccer_ball.shape, pivot)

    # create the bot one
    bot_initial_pos = (screen.get_width()//2, screen.get_height()//2 + const.FIELD_HEIGHT//2 - const.BOT_LINE_DIS - const.BOT_HEIGHT//2)
    ps = [(const.BOT_WIDTH//2, const.BOT_HEIGHT//2), (-const.BOT_WIDTH//2, const.BOT_HEIGHT//2), (-const.BOT_WIDTH//2, -const.BOT_HEIGHT//2), (const.BOT_WIDTH//2, -const.BOT_HEIGHT//2)]
    soccer_bot = BOT(bot_initial_pos, ps, 0)    
    soccer_bot.shape.color = const.BOT_COLOR_ONE
    pivot = pymunk.PivotJoint(static_body, soccer_bot.shape.body, (0, 0), (0, 0))
    pivot.max_bias = 0 # disable joint correction
    pivot.max_force = 300 # emulate linear friction 
    space.add(soccer_bot.body, soccer_bot.shape, pivot)

    # creating walls around the field
    wall_left = Wall((0,0),(screen.get_width()//2 - const.FIELD_WIDTH//2, screen.get_height()//2 - const.FIELD_HEIGHT//2), (screen.get_width()//2 - const.FIELD_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), 2)
    space.add(wall_left.body, wall_left.shape)
    
    wall_right = Wall((0,0), (screen.get_width()//2 + const.FIELD_WIDTH//2, screen.get_height()//2 - const.FIELD_HEIGHT//2), (screen.get_width()//2 + const.FIELD_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), 2)
    space.add(wall_right.body, wall_right.shape)
    
    wall_bottom_left = Wall((0,0), (screen.get_width()//2 - const.FIELD_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), (screen.get_width()//2 - const.GOAL_POST_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), 2)
    space.add(wall_bottom_left.body, wall_bottom_left.shape)
    wall_bottom_right = Wall((0,0), (screen.get_width()//2 + const.FIELD_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), (screen.get_width()//2 + const.GOAL_POST_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), 2)

    space.add(wall_bottom_right.body, wall_bottom_right.shape)
    wall_top_left = Wall((0,0), (screen.get_width()//2 - const.FIELD_WIDTH//2 , screen.get_height()//2- const.FIELD_HEIGHT//2), (screen.get_width()//2 - const.GOAL_POST_WIDTH//2 , screen.get_height()//2- const.FIELD_HEIGHT//2), 2)
    space.add(wall_top_left.body, wall_top_left.shape)
    
    wall_top_right = Wall((0,0), (screen.get_width()//2 + const.FIELD_WIDTH//2 , screen.get_height()//2 - const.FIELD_HEIGHT//2), (screen.get_width()//2 + const.GOAL_POST_WIDTH//2 , screen.get_height()//2 - const.FIELD_HEIGHT//2), 2)
    space.add(wall_top_right.body, wall_top_right.shape)

    #set fps
    clock = pygame.time.Clock()

    #display everything
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        keys = pygame.key.get_pressed()
        # soccer_bot.move(keys)
        if keys[pygame.K_DOWN]:
            # Accelerate forward
            soccer_bot.move_direction(const.Direction.BACKWARD)
        elif keys[pygame.K_UP]:
            # Accelerate backward
            soccer_bot.move_direction(const.Direction.FORWARD)
        else:
            # Decelerate towards 0 speed
            soccer_bot.move_direction(const.Direction.STOP_TOWARDS)

        if keys[pygame.K_RIGHT]:
            # Accelerate left (rotate left)
            soccer_bot.move_direction(const.Direction.RIGHT)
        elif keys[pygame.K_LEFT]:
            # Accelerate right (rotate right)
            soccer_bot.move_direction(const.Direction.LEFT)
        else:
            # Decelerate rotation towards 0 rotation speed
            soccer_bot.move_direction(const.Direction.STOP_ROTATION)
        
        screen.fill(const.SCREEN_BG)
        #draw the goal posts
        pygame.draw.line(screen, width=3, color=(const.GOAL_LINE_COLOR), start_pos=(screen.get_width()//2 - const.GOAL_POST_WIDTH//2, screen.get_height()//2 - const.FIELD_HEIGHT//2), end_pos=(screen.get_width()//2 + const.GOAL_POST_WIDTH//2, screen.get_height()//2 - const.FIELD_HEIGHT//2))
        pygame.draw.line(screen, width=3, color=(const.GOAL_LINE_COLOR), start_pos=(screen.get_width()//2 - const.GOAL_POST_WIDTH//2, screen.get_height()//2 + const.FIELD_HEIGHT//2), end_pos=(screen.get_width()//2 + const.GOAL_POST_WIDTH//2, screen.get_height()//2 + const.FIELD_HEIGHT//2))
        #draw middle line 
        pygame.draw.line(screen, width=1, color=(const.FIELD_LINE_COLOR), start_pos=(screen.get_width()//2 - const.FIELD_WIDTH//2, screen.get_height()//2 ), end_pos=(screen.get_width()//2 + const.FIELD_WIDTH//2, screen.get_height()//2 ))      
        #update the space
        space.step(1/FPS)
        clock.tick(FPS)
        space.debug_draw(draw_options)


        #check for score 
        #if ball crosses the goal line then add score to the player
        if check_goal_top(soccer_ball, screen):
            soccer_bot.reset()
            soccer_ball.reset()
            player_one_score += 1
            display_score(screen, player_one_score, player_two_score)
            pygame.time.delay(1000)
        elif check_goal_bottom(soccer_ball, screen):
            soccer_bot.reset()
            soccer_ball.reset()
            player_two_score += 1
            display_score(screen, player_one_score, player_two_score)
            pygame.time.delay(1000)

        pygame.display.flip()

def main():
    # define screen and space and everything
    screen_shape = (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screen_shape)
    space = pymunk.Space()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    FPS = 60
    run_sim(space, screen, draw_options, FPS)


if __name__ == "__main__":
    import sys

    sys.exit(main())