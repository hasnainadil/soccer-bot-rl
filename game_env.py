import constants as const 
import pymunk, pymunk.pygame_util
import pygame
import math
from objects import Ball, BOT, Wall
import numpy as np

def true_y(pos_y, screen_height):
    return screen_height - pos_y

def true_x(pos_x):
    return pos_x

def true_pos(pos:tuple, screen_height):
    return (true_x(pos[0]), true_y(pos[1], screen_height))

def get_direction(ball_pos:tuple, bot_pos:tuple, bot_angle:float)->tuple:
    direction = (ball_pos[0] - bot_pos[0], ball_pos[1] - bot_pos[1])
    direction = (direction[0] * math.cos(bot_angle) - direction[1] * math.sin(bot_angle), direction[0] * math.sin(bot_angle) + direction[1] * math.cos(bot_angle))
    direction = (round(direction[0], 2), round(direction[1], 2))
    ball_relative_pos = np.zeros(4) #[left, right, up, down]
    if direction[0] > 0:
        ball_relative_pos[1] = 1
    elif direction[0] < 0:
        ball_relative_pos[0] = 1
    if direction[1] > 0:
        ball_relative_pos[2] = 1
    elif direction[1] < 0:
        ball_relative_pos[3] = 1
    return ball_relative_pos


class Game_env():
    def __init__(self, screen:pygame.Surface, fps:int) -> None:
        pygame.init()
        self.space = pymunk.Space()
        self.player_one_score = 0
        self.player_two_score = 0
        self.static_body = self.space.static_body
        self.soccer_ball = None
        self.soccer_bot_one = None
        self.soccer_bot_two = None
        self.ball_relative_pos_one = None
        self.ball_relative_pos_two = None
        self.target_post_relative_pos_one = None
        self.target_post_relative_pos_two = None
        self.own_goal_relative_pos_one = None
        self.own_goal_relative_pos_two = None
        self.bot_one_state = None
        self.bot_two_state = None
        self.screen = screen
        self.FPS = fps
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        # creating wall around the field
        wall_left = Wall((0,0),(screen.get_width()//2 - const.FIELD_WIDTH//2, screen.get_height()//2 - const.FIELD_HEIGHT//2), (screen.get_width()//2 - const.FIELD_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), 2)
        self.space.add(wall_left.body, wall_left.shape)
        
        wall_right = Wall((0,0), (screen.get_width()//2 + const.FIELD_WIDTH//2, screen.get_height()//2 - const.FIELD_HEIGHT//2), (screen.get_width()//2 + const.FIELD_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), 2)
        self.space.add(wall_right.body, wall_right.shape)
        
        wall_bottom_left = Wall((0,0), (screen.get_width()//2 - const.FIELD_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), (screen.get_width()//2 - const.GOAL_POST_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), 2)
        self.space.add(wall_bottom_left.body, wall_bottom_left.shape)
        wall_bottom_right = Wall((0,0), (screen.get_width()//2 + const.FIELD_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), (screen.get_width()//2 + const.GOAL_POST_WIDTH//2 , screen.get_height()//2+ const.FIELD_HEIGHT//2), 2)

        self.space.add(wall_bottom_right.body, wall_bottom_right.shape)
        wall_top_left = Wall((0,0), (screen.get_width()//2 - const.FIELD_WIDTH//2 , screen.get_height()//2- const.FIELD_HEIGHT//2), (screen.get_width()//2 - const.GOAL_POST_WIDTH//2 , screen.get_height()//2- const.FIELD_HEIGHT//2), 2)
        self.space.add(wall_top_left.body, wall_top_left.shape)
        
        wall_top_right = Wall((0,0), (screen.get_width()//2 + const.FIELD_WIDTH//2 , screen.get_height()//2 - const.FIELD_HEIGHT//2), (screen.get_width()//2 + const.GOAL_POST_WIDTH//2 , screen.get_height()//2 - const.FIELD_HEIGHT//2), 2)
        self.space.add(wall_top_right.body, wall_top_right.shape)

    def create_ball(self, initial_pos:tuple, radius:int, color:tuple) -> None:
        self.soccer_ball = Ball(initial_pos, radius)
        self.soccer_ball.shape.color = color
        pivot = pymunk.PivotJoint(self.static_body, self.soccer_ball.shape.body, (0, 0), (0, 0))
        pivot.max_bias = 0 # disable joint correction
        pivot.max_force = const.BALL_FRICTION_FORCE # emulate linear friction 
        self.space.add(self.soccer_ball.body, self.soccer_ball.shape, pivot)

    def create_bot_one(self,initial_pos:tuple, color:tuple, initial_angle=0):
        vertices = [(const.BOT_WIDTH//2, const.BOT_HEIGHT//2), (-const.BOT_WIDTH//2, const.BOT_HEIGHT//2), (-const.BOT_WIDTH//2, -const.BOT_HEIGHT//2), (const.BOT_WIDTH//2, -const.BOT_HEIGHT//2)] 
        self.soccer_bot_one = BOT(initial_pos, vertices, initial_angle)
        self.soccer_bot_one.shape.color = color
        pivot = pymunk.PivotJoint(self.static_body, self.soccer_bot_one.shape.body, (0, 0), (0, 0))
        pivot.max_bias = 0
        pivot.max_force = const.BOT_FRICTION_FORCE
        self.space.add(self.soccer_bot_one.body, self.soccer_bot_one.shape, pivot)
    
    def create_bot_two(self,initial_pos:tuple, color:tuple, initial_angle=math.pi):
        vertices = [(const.BOT_WIDTH//2, const.BOT_HEIGHT//2), (-const.BOT_WIDTH//2, const.BOT_HEIGHT//2), (-const.BOT_WIDTH//2, -const.BOT_HEIGHT//2), (const.BOT_WIDTH//2, -const.BOT_HEIGHT//2)] 
        self.soccer_bot_two = BOT(initial_pos, vertices, initial_angle)
        self.soccer_bot_two.shape.color = color
        pivot = pymunk.PivotJoint(self.static_body, self.soccer_bot_two.shape.body, (0, 0), (0, 0))
        pivot.max_bias = 0
        pivot.max_force = const.BOT_FRICTION_FORCE
        self.space.add(self.soccer_bot_two.body, self.soccer_bot_two.shape, pivot)

    def reset(self):
        if self.soccer_ball is not None:
            self.soccer_ball.reset()
        if self.soccer_bot_one is not None:
            self.soccer_bot_one.reset()
        if self.soccer_bot_two is not None:
            self.soccer_bot_two.reset()

    def get_ball_reward(self, bot:BOT, opponent:BOT) -> int:
        # get side zone id
        side_zone_id = 0
        reward_one = 0
        reward_two = 0
        if (self.soccer_ball.body.position.x < self.screen.get_width()//2 - 
        const.FIELD_WIDTH//2 + const.FIELD_HEIGHT//4) or (self.soccer_ball.body.position.x > self.screen.get_width()//2 + const.FIELD_WIDTH//2 - const.FIELD_HEIGHT//4):
            side_zone_id = -1

        # get vertical zone id
        vertical_zone_id = 0
        if (self.soccer_ball.body.position.y < self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + const.FIELD_HEIGHT//6):
            vertical_zone_id = 3
        elif (self.soccer_ball.body.position.y < self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 2*const.FIELD_HEIGHT//6):
            vertical_zone_id = 2
        elif (self.soccer_ball.body.position.y < self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 3*const.FIELD_HEIGHT//6):
            vertical_zone_id = 1
        elif (self.soccer_ball.body.position.y < self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 4*const.FIELD_HEIGHT//6):
            vertical_zone_id = -1
        elif (self.soccer_ball.body.position.y < self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 5*const.FIELD_HEIGHT//6):
            vertical_zone_id = -2
        else:
            vertical_zone_id = -3
        
        if vertical_zone_id == -3 and side_zone_id == 0:
            reward_one += -200
            reward_two += 200

        # get distance from ball to bot
        distance_bot_one = math.sqrt((self.soccer_ball.body.position.x - bot.shape.body.position.x)**2 + (self.soccer_ball.body.position.y - bot.shape.body.position.y)**2)
        distance_bot_two = math.sqrt((self.soccer_ball.body.position.x - opponent.shape.body.position.x)**2 + (self.soccer_ball.body.position.y - opponent.shape.body.position.y)**2)
        # rewards are based on position on the field(vertical zone and side zone) and distance from ball to bot
        reward_one += const.BASE_REWARD*10 * (1/distance_bot_one - 1/distance_bot_two)
        reward_two += const.BASE_REWARD*10 * (1/distance_bot_two - 1/distance_bot_one)
        reward_one += side_zone_id * const.BASE_REWARD
        reward_two += side_zone_id * const.BASE_REWARD
        reward_one += vertical_zone_id * const.BASE_REWARD
        reward_two += (-1)*vertical_zone_id * const.BASE_REWARD # opponent vertical zone id is negative of bot vertical zone id
        return (reward_one, reward_two)

        
    def score_reset(self):
        self.player_two_score = 0
        self.player_one_score = 0

    def step(self, action_one:tuple=None, action_two:tuple=None):
        #logic bots movement and state change
        if self.soccer_bot_one is not None:
            towards,rotation = action_one
            self.soccer_bot_one.move_direction(towards)
            self.soccer_bot_one.rotate(rotation)
            reward_one = self.get_ball_reward(self.soccer_bot_one, self.soccer_bot_two)

    # get state of both the bots
    def get_state(self):
        # ball and two post position relative to bot one
        if((self.soccer_bot_one == None and self.soccer_bot_two == None) or self.soccer_ball == None):
            return None
        if self.soccer_bot_one is not None :
            self.ball_relative_pos_one = get_direction(true_pos(self.soccer_ball.shape.body.position, self.screen.get_height()), true_pos(self.soccer_bot_one.shape.body.position, self.screen.get_height()), self.soccer_bot_one.shape.body.angle)

            self.target_post_relative_pos_one = get_direction(true_pos((self.screen.get_width()//2, self.screen.get_height()//2 - const.FIELD_HEIGHT//2), self.screen.get_height()), true_pos(self.soccer_bot_one.shape.body.position, self.screen.get_height()), self.soccer_bot_one.shape.body.angle)

            self.own_goal_relative_pos_one = get_direction(true_pos((self.screen.get_width()//2, self.screen.get_height()//2 + const.FIELD_HEIGHT//2), self.screen.get_height()), true_pos(self.soccer_bot_one.shape.body.position, self.screen.get_height()), self.soccer_bot_one.shape.body.angle)

            self.bot_one_state = np.concatenate((self.ball_relative_pos_one, self.target_post_relative_pos_one, self.own_goal_relative_pos_one))

        # ball and two post position relative to bot two
        if self.soccer_bot_two is not None :
            self.ball_relative_pos_two = get_direction(true_pos(self.soccer_ball.shape.body.position, self.screen.get_height()), true_pos(self.soccer_bot_two.shape.body.position, self.screen.get_height()), self.soccer_bot_two.shape.body.angle)

            self.target_post_relative_pos_two = get_direction(true_pos((self.screen.get_width()//2, self.screen.get_height()//2 + const.FIELD_HEIGHT//2), self.screen.get_height()), true_pos(self.soccer_bot_two.shape.body.position, self.screen.get_height()), self.soccer_bot_two.shape.body.angle)

            self.own_goal_relative_pos_two = get_direction(true_pos((self.screen.get_width()//2, self.screen.get_height()//2 - const.FIELD_HEIGHT//2), self.screen.get_height()), true_pos(self.soccer_bot_two.shape.body.position, self.screen.get_height()), self.soccer_bot_two.shape.body.angle)
            
            self.bot_two_state = np.concatenate((self.ball_relative_pos_two, self.target_post_relative_pos_two, self.own_goal_relative_pos_two))


        # return state
        return self.bot_one_state, self.bot_two_state

    def check_goal_top(self) -> bool:
        return self.soccer_ball.shape.body.position.y < self.screen.get_height()//2 - const.FIELD_HEIGHT//2 and self.soccer_ball.shape.body.position.x > self.screen.get_width()//2 - const.GOAL_POST_WIDTH//2 and self.soccer_ball.shape.body.position.x < self.screen.get_width()//2 + const.GOAL_POST_WIDTH//2

    def check_goal_bottom(self) -> bool:
        return self.soccer_ball.shape.body.position.y > self.screen.get_height()//2 + const.FIELD_HEIGHT//2 and self.soccer_ball.shape.body.position.x > self.screen.get_width()//2 - const.GOAL_POST_WIDTH//2 and self.soccer_ball.shape.body.position.x < self.screen.get_width()//2 + const.GOAL_POST_WIDTH//2
    
    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(str(self.player_one_score) + " : " + str(self.player_two_score), True, (255, 255, 255))
        pygame.draw.rect(self.screen, width=0, color=(0,0,0), rect=(self.screen.get_width()//2 - score_text.get_width()//2, self.screen.get_height()//2 - score_text.get_height()//2, score_text.get_width(), score_text.get_height()))
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, self.screen.get_height() // 2 - score_text.get_height() // 2))
        pygame.display.flip()

    def print_state(self):
        self.get_state()
        print("Position array format: [left, right, up, down]")
        print("Ball Relative Position to bot one:", self.ball_relative_pos_one)
        print("Target Post Relative Position to bot one:", self.target_post_relative_pos_one)
        print("Own Goal Relative Position to bot one:", self.own_goal_relative_pos_one)
        print("Bot State one:", self.bot_one_state)
        print("Ball Relative Position to bot two:", self.ball_relative_pos_two)
        print("Target Post Relative Position to bot two:", self.target_post_relative_pos_two)
        print("Own Goal Relative Position to bot two:", self.own_goal_relative_pos_two)
        print("Bot State two:", self.bot_two_state)
        
    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # draw background
        self.screen.fill(const.SCREEN_BG)

        # draw goal line
        pygame.draw.line(self.screen, width=3, color=(const.GOAL_LINE_COLOR), start_pos=(self.screen.get_width()//2 - const.GOAL_POST_WIDTH//2, self.screen.get_height()//2 - const.FIELD_HEIGHT//2), end_pos=(self.screen.get_width()//2 + const.GOAL_POST_WIDTH//2, self.screen.get_height()//2 - const.FIELD_HEIGHT//2))
        pygame.draw.line(self.screen, width=3, color=(const.GOAL_LINE_COLOR), start_pos=(self.screen.get_width()//2 - const.GOAL_POST_WIDTH//2, self.screen.get_height()//2 + const.FIELD_HEIGHT//2), end_pos=(self.screen.get_width()//2 + const.GOAL_POST_WIDTH//2, self.screen.get_height()//2 + const.FIELD_HEIGHT//2))
        #draw middle line 
        pygame.draw.line(self.screen, width=1, color=(const.FIELD_LINE_COLOR), start_pos=(self.screen.get_width()//2 - const.FIELD_WIDTH//2, self.screen.get_height()//2 ), end_pos=(self.screen.get_width()//2 + const.FIELD_WIDTH//2, self.screen.get_height()//2 ))     

        # divide the field in diffrent zones
        # devide the field in 3 zones vertically
        pygame.draw.line(self.screen, width=1, color=(const.FIELD_LINE_COLOR), start_pos=(self.screen.get_width()//2 - const.FIELD_HEIGHT//2 + const.FIELD_HEIGHT//4 , self.screen.get_height()//2 - const.FIELD_HEIGHT//2 ), end_pos=(self.screen.get_width()//2 - const.FIELD_HEIGHT//2 + const.FIELD_HEIGHT//4, self.screen.get_height()//2 + const.FIELD_HEIGHT//2 ))
        
        pygame.draw.line(self.screen, width=1, color=(const.FIELD_LINE_COLOR), start_pos=(self.screen.get_width()//2 + const.FIELD_HEIGHT//2 - const.FIELD_HEIGHT//4 , self.screen.get_height()//2 - const.FIELD_HEIGHT//2 ), end_pos=(self.screen.get_width()//2 + const.FIELD_HEIGHT//2 - const.FIELD_HEIGHT//4, self.screen.get_height()//2 + const.FIELD_HEIGHT//2 ))

        # divide the field in 5 zones horizontally
        pygame.draw.line(self.screen, width=1, color=(const.FIELD_LINE_COLOR), start_pos=(self.screen.get_width()//2 - const.FIELD_WIDTH//2 , self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + const.FIELD_HEIGHT//6), end_pos=(self.screen.get_width()//2 + const.FIELD_WIDTH//2, self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + const.FIELD_HEIGHT//6))
        pygame.draw.line(self.screen, width=1, color=(const.FIELD_LINE_COLOR), start_pos=(self.screen.get_width()//2 - const.FIELD_WIDTH//2 , self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 2*const.FIELD_HEIGHT//6), end_pos=(self.screen.get_width()//2 + const.FIELD_WIDTH//2, self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 2*const.FIELD_HEIGHT//6))

        pygame.draw.line(self.screen, width=1, color=(const.FIELD_LINE_COLOR), start_pos=(self.screen.get_width()//2 - const.FIELD_WIDTH//2 , self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 4*const.FIELD_HEIGHT//6), end_pos=(self.screen.get_width()//2 + const.FIELD_WIDTH//2, self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 4*const.FIELD_HEIGHT//6))
        pygame.draw.line(self.screen, width=1, color=(const.FIELD_LINE_COLOR), start_pos=(self.screen.get_width()//2 - const.FIELD_WIDTH//2 , self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 5*const.FIELD_HEIGHT//6), end_pos=(self.screen.get_width()//2 + const.FIELD_WIDTH//2, self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + 5*const.FIELD_HEIGHT//6))

        
        #update the space
        self.space.step(1/self.FPS)
        self.clock.tick(self.FPS)
        self.space.debug_draw(self.draw_options)

        if self.check_goal_top():
            self.soccer_bot.reset()
            self.soccer_ball.reset()
            self.player_one_score += 1
            self.display_score(self.screen, self.player_one_score, self.player_two_score)
            pygame.time.delay(1000)
        elif self.check_goal_bottom():
            self.soccer_bot.reset()
            self.soccer_ball.reset()
            self.player_two_score += 1
            self.display_score(self.screen, self.player_one_score, self.player_two_score)
            pygame.time.delay(1000)
        
        pygame.display.flip()
        
