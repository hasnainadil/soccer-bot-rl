from collections import deque
import torch
import numpy as np
from game_env import Game_env
import constants as const
import pygame
import math
from model import Linear_QNet, QTrainer
import random

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self,input_size, hidden_size, output_size):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.env = Game_env(screen=self.screen, fps=60) #create game environment

        #create ball and bots
        self.env.create_ball((self.screen.get_width()//2, self.screen.get_height()//2), const.BALL_RADIUS,const.BALL_COLOR)
        self.env.create_bot_one((self.screen.get_width()//2, self.screen.get_height()//2 + const.FIELD_HEIGHT//2 - const.BOT_LINE_DIS - const.BOT_HEIGHT//2),const.BOT_COLOR_ONE, 0)
        self.env.create_bot_two((self.screen.get_width()//2, self.screen.get_height()//2 - const.FIELD_HEIGHT//2 + const.BOT_LINE_DIS + const.BOT_HEIGHT//2),const.BOT_COLOR_TWO, math.pi)

        self.env.soccer_bot_one.model = Linear_QNet(input_size, hidden_size, output_size)
        self.env.soccer_bot_one.trainer = QTrainer(self.env.soccer_bot_one.model, lr=LR, gamma=self.gamma)
        self.env.soccer_bot_two.model = Linear_QNet(input_size, hidden_size, output_size)
        self.env.soccer_bot_two.trainer = QTrainer(self.env.soccer_bot_two.model, lr=LR, gamma=self.gamma)
        self.env.soccer_bot_one.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.env.soccer_bot_two.memory = deque(maxlen=MAX_MEMORY)

    def remember_one(self, state, action, reward, next_state, done):
        self.env.soccer_bot_one.memory.append((state, action, reward, next_state, done))
    
    def remember_two(self, state, action, reward, next_state, done):
        self.env.soccer_bot_two.memory.append((state, action, reward, next_state, done))

    def train_long_memory_one(self):
        if len(self.env.soccer_bot_one.memory) > BATCH_SIZE:
            minibatch = random.sample(self.env.soccer_bot_one.memory, BATCH_SIZE)
        else:
            minibatch = self.env.soccer_bot_one.memory

        states, actions, rewards, next_states, dones = zip(*minibatch)
        self.env.soccer_bot_one.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_long_memory_two(self):
        if len(self.env.soccer_bot_two.memory) > BATCH_SIZE:
            minibatch = random.sample(self.env.soccer_bot_two.memory, BATCH_SIZE)
        else:
            minibatch = self.env.soccer_bot_two.memory

        states, actions, rewards, next_states, dones = zip(*minibatch)
        self.env.soccer_bot_two.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory_one(self, state, action, reward, next_state, done):
        self.env.soccer_bot_one.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory_two(self, state, action, reward, next_state, done):
        self.env.soccer_bot_two.trainer.train_step(state, action, reward, next_state, done)

    def get_state(self):
        return self.env.get_state()

    def get_action_one(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 50 - self.n_games*0.1
        towards = None
        rotation = None
        self.epsilon = max(self.epsilon, 0)
        final_move = np.zeros(6)
        if random.randint(0, 200) < self.epsilon:
            towards = random.randint(0, 2)
            final_move[towards] = 1
            rotation = random.randint(3, 5)
            final_move[rotation] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.env.soccer_bot_one.model(state0).numpy()
            towards, rotation = np.split(prediction, 2)
            towards = np.argmax(towards)
            rotation = np.argmax(rotation) + 3
            final_move[towards] = 1
            final_move[rotation] = 1

        return final_move, towards, rotation

    def get_action_two(self, state):
        # random moves: tradeoff exploration / exploitation
        towards = None
        rotation = None
        self.epsilon = 50 - self.n_games*0.1
        self.epsilon = max(self.epsilon, 0)
        final_move = np.zeros(6)
        if random.randint(0, 200) < self.epsilon:
            towards = random.randint(0, 2)
            final_move[towards] = 1
            rotation = random.randint(3, 5)
            final_move[rotation] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.env.soccer_bot_two.model(state0).numpy()
            towards, rotation = np.split(prediction, 2)
            towards = np.argmax(towards)
            rotation = np.argmax(rotation) + 3
            final_move[towards] = 1
            final_move[rotation] = 1

        return final_move, towards, rotation
    

        