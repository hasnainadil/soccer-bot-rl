import numpy as np
from enum import Enum

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
FIELD_LINE_COLOR = (125, 15, 15)
FIELD_WIDTH = 600
FIELD_HEIGHT = 700
GOAL_POST_WIDTH = 150
GOAL_LINE_COLOR = (255, 255, 255)
BOT_LINE_DIS = 30
BOT_WIDTH = 80
BOT_HEIGHT = 90
BOT_COLOR_ONE = (179, 179, 45,255)
SCREEN_BG = (99, 173, 104)
BALL_RADIUS = 15
BALL_COLOR = (247, 130, 79, 255)


class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    STOP_TOWARDS = 5
    STOP_ROTATION = 6
