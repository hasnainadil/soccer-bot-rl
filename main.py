import pygame
import pymunk
import pymunk.pygame_util
from ball import Ball
from bot import BOT
import constants as const

pygame.init()

def run_sim(space: pymunk.Space, screen: pygame.Surface, draw_options: pymunk.pygame_util.DrawOptions, FPS:int) -> None:
    # setting socres and playing flag
    playing = False
    player_one_score = 0
    player_two_score = 0
    font = pygame.font.Font(None, 36)
    score_text = font.render(str(player_one_score) + " : " + str(player_two_score), True, (255, 255, 255))

    static_body = space.static_body # define static body for friction

    # create soccer ball 
    ball_initial_pos = (screen.get_width()//2, screen.get_height()//2)
    ball_radius = const.BALL_RADIUS
    soccer_ball = Ball(ball_initial_pos, ball_radius, static_body)
    soccer_ball.shape.color = const.BALL_COLOR
    pivot = pymunk.PivotJoint(static_body, soccer_ball.shape.body, (0, 0), (0, 0))
    pivot.max_bias = 0 # disable joint correction
    pivot.max_force = 300 # emulate linear friction 
    space.add(soccer_ball.body, soccer_ball.shape, pivot)

    # create the bot one
    bot_initial_pos = (screen.get_width()//2, screen.get_height()//2 + const.FIELD_HEIGHT//2 - const.BOT_LINE_DIS - const.BOT_HEIGHT//2)
    ps = [(const.BOT_WIDTH//2, const.BOT_HEIGHT//2), (-const.BOT_WIDTH//2, const.BOT_HEIGHT//2), (-const.BOT_WIDTH//2, -const.BOT_HEIGHT//2), (const.BOT_WIDTH//2, -const.BOT_HEIGHT//2)]
    soccer_bot = BOT(bot_initial_pos, ps, space)    
    soccer_bot.shape.color = const.BOT_COLOR_ONE
    pivot = pymunk.PivotJoint(static_body, soccer_bot.shape.body, (0, 0), (0, 0))
    pivot.max_bias = 0 # disable joint correction
    pivot.max_force = 300 # emulate linear friction 
    space.add(soccer_bot.body, soccer_bot.shape, pivot)

    # creating walls around the screen
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, 0)
    wall_left = pymunk.Segment(body, (0, 0), (0, screen.get_height()), 5)
    wall_left.friction = 1
    wall_left.elasticity = 0.95
    space.add(wall_left.body, wall_left)
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, 0)
    wall_top = pymunk.Segment(body, (0, 0), (screen.get_width(), 0), 5)
    wall_top.friction = 1
    wall_top.elasticity = 0.95
    space.add(wall_top.body, wall_top)
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (screen.get_width(), 0)
    wall_right = pymunk.Segment(body, (0, 0), (0, screen.get_height()), 5)
    wall_right.friction = 1
    wall_right.elasticity = 0.95
    space.add(wall_right.body, wall_right)
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, screen.get_height())
    wall_bottom = pymunk.Segment(body, (0, 0), (screen.get_width(), 0), 5)
    wall_bottom.friction = 1
    wall_bottom.elasticity = 0.95
    space.add(wall_bottom.body, wall_bottom)

    #set fps
    clock = pygame.time.Clock()

    #display everything
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                # soccer_bot.shape.body.apply_impulse_at_local_point((0, 1000), (0, 0))
            # if event.type == pygame.KEYUP :
            #     soccer_bot.shape.body.velocity = (0, 0)
        keys = pygame.key.get_pressed()
        soccer_bot.move(keys)
        
        screen.fill(const.SCREEN_BG)
        #draw the field
        pygame.draw.rect(screen, width=1, color=(const.FIELD_LINE_COLOR), rect=(screen.get_width()//2 - const.FIELD_WIDTH//2, screen.get_height()//2 - const.FIELD_HEIGHT//2, const.FIELD_WIDTH, const.FIELD_HEIGHT))
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
        if soccer_ball.shape.body.position.y < screen.get_height()//2 - const.FIELD_HEIGHT//2 and soccer_ball.shape.body.position.x > screen.get_width()//2 - const.GOAL_POST_WIDTH//2 and soccer_ball.shape.body.position.x < screen.get_width()//2 + const.GOAL_POST_WIDTH//2:
            soccer_bot.reset()
            soccer_ball.reset()
            player_one_score += 1
            score_text = font.render(str(player_one_score) + " : " + str(player_two_score), True, (255, 255, 255))
            pygame.draw.rect(screen, width=0, color=(0,0,0), rect=(screen.get_width()//2 - score_text.get_width()//2, screen.get_height()//2 - score_text.get_height()//2, score_text.get_width(), score_text.get_height()))
            screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2 - score_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(1000)
        elif soccer_ball.shape.body.position.y > screen.get_height()//2 + const.FIELD_HEIGHT//2 and soccer_ball.shape.body.position.x > screen.get_width()//2 - const.GOAL_POST_WIDTH//2 and soccer_ball.shape.body.position.x < screen.get_width()//2 + const.GOAL_POST_WIDTH//2:
            soccer_bot.reset()
            soccer_ball.reset()
            player_two_score += 1
            score_text = font.render(str(player_one_score) + " : " + str(player_two_score), True, (255, 255, 255))
            pygame.draw.rect(screen, width=0, color=(0,0,0), rect=(screen.get_width()//2 - score_text.get_width()//2, screen.get_height()//2 - score_text.get_height()//2, score_text.get_width(), score_text.get_height()))
            screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2 - score_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(1000)


        # check if the ball is out of the field
        # if soccer_ball.shape.body.position.x < screen.get_width()//2 - const.FIELD_WIDTH//2 or soccer_ball.shape.body.position.x > screen.get_width()//2 + const.FIELD_WIDTH//2 or soccer_ball.shape.body.position.y < screen.get_height()//2 - const.FIELD_HEIGHT//2 or soccer_ball.shape.body.position.y > screen.get_height()//2 + const.FIELD_HEIGHT//2:
        #     soccer_bot.reset()
        #     soccer_ball.reset()
        #     score_text = font.render(str(player_one_score) + " : " + str(player_two_score), True, (255, 255, 255))
        #     pygame.draw.rect(screen, width=0, color=(0,0,0), rect=(screen.get_width()//2 - score_text.get_width()//2, screen.get_height()//2 - score_text.get_height()//2, score_text.get_width(), score_text.get_height()))
        #     screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2 - score_text.get_height() // 2))
        #     pygame.display.flip()
        #     pygame.time.delay(1000)
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