from game_env import Game_env
import pygame
import constants as const
import math

screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

env = Game_env(screen=screen, fps=60)
env.create_ball((screen.get_width()//2, screen.get_height()//2), const.BALL_RADIUS,const.BALL_COLOR)
env.create_bot_one((screen.get_width()//2, screen.get_height()//2 + const.FIELD_HEIGHT//2 - const.BOT_LINE_DIS - const.BOT_HEIGHT//2),const.BOT_COLOR_ONE, 0)
env.create_bot_two((screen.get_width()//2, screen.get_height()//2 - const.FIELD_HEIGHT//2 + const.BOT_LINE_DIS + const.BOT_HEIGHT//2),const.BOT_COLOR_TWO, math.pi)

while True:
    env.render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            env.print_state()