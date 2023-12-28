from collections import deque
import torch
import numpy as np
from game_env import Game_env
import constants as const
import pygame
import math
from model import Linear_QNet, QTrainer
import random
import os

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self,input_size, hidden_size, output_size):
        self.n_games = 0
        self.epsilon_one = 1 # randomness
        self.epsilon_two = 1
        self.gamma = 0.9
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.env = Game_env(screen=self.screen, fps=60) #create game environment

        self.env.soccer_bot_one.model = Linear_QNet(input_size, hidden_size, output_size)
        # model_path = os.path.join('./model', file_name)
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
        # print("Training long memory")
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
        towards = None
        rotation = None
        self.epsilon_one = 1 - self.env.episode_count*0.01
        self.epsilon_one = max(self.epsilon_one, 0.3)
        explore = np.random.choice([True, False], p=[self.epsilon_one, 1-self.epsilon_one])
        final_move = np.zeros(6)
        if explore:
            # print("random")
            towards = np.random.choice([0, 1, 2],p=[0.4, 0.35, 0.25])
            final_move[towards] = 1
            rotation = random.randint(3, 5)
            final_move[rotation] = 1
        else:
            # print("Predicted")
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.env.soccer_bot_one.model(state0)
            prediction = prediction.detach().numpy()
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
        self.epsilon_two -= self.env.episode_count*0.01
        self.epsilon_two = max(self.epsilon_two, 0.3)
        explore = np.random.choice([True, False], p=[self.epsilon_two, 1-self.epsilon_two])
        final_move = np.zeros(6)
        if explore:
            towards = np.random.choice([0, 1, 2],p=[0.4, 0.35, 0.25])
            final_move[towards] = 1
            rotation = random.randint(3, 5)
            final_move[rotation] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.env.soccer_bot_two.model(state0)
            prediction = prediction.detach().numpy()
            towards, rotation = np.split(prediction, 2)
            towards = np.argmax(towards)
            rotation = np.argmax(rotation) + 3
            final_move[towards] = 1
            final_move[rotation] = 1

        return final_move, towards, rotation