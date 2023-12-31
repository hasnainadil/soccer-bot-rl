from collections import deque
import torch
import numpy as np
from game_env import Game_env
import constants as const
import pygame
from model import Linear_QNet, QTrainer
import random
import os

MAX_MEMORY = 100_000
BATCH_SIZE = 1000

def get_direction_labeled(action: int):
    if action == 0:
        #up
        return (const.Direction.FORWARD, const.Direction.STOP_ROTATION)
    elif action == 1:
        #up right
        return (const.Direction.FORWARD, const.Direction.RIGHT)
    elif action == 2:
        #right
        return (const.Direction.STOP_TOWARDS, const.Direction.RIGHT)
    elif action == 3:
        #down right
        return (const.Direction.BACKWARD, const.Direction.RIGHT)
    elif action == 4:
        #down
        return (const.Direction.BACKWARD, const.Direction.STOP_ROTATION)
    elif action == 5:
        #down left
        return (const.Direction.BACKWARD, const.Direction.LEFT)
    elif action == 6:
        #left
        return (const.Direction.STOP_TOWARDS, const.Direction.LEFT)
    elif action == 7:
        #up left
        return (const.Direction.FORWARD, const.Direction.LEFT)

class Agent:
    def __init__(self,input_size, hidden_size, output_size, epsilon, min_epsilon, decay_rate, gamma, learning_rate):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.decay_rate = decay_rate
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.env = Game_env(screen=self.screen, fps=60) #create game environment

        self.env.soccer_bot_one.model = Linear_QNet(input_size, hidden_size, output_size)
        if os.path.exists("model/bot_one_model.pth"):
            print("Loading model one")
            self.env.soccer_bot_one.model.load_state_dict(torch.load("model/bot_one_model.pth"))
            self.env.soccer_bot_one.model.train()

        self.env.soccer_bot_one.trainer = QTrainer(self.env.soccer_bot_one.model, lr=self.learning_rate, gamma=self.gamma)
        
        self.env.soccer_bot_two.model = Linear_QNet(input_size, hidden_size, output_size)
        if os.path.exists("model/bot_two_model.pth"):
            print("Loading model two ")
            self.env.soccer_bot_two.model.load_state_dict(torch.load("model/bot_two_model.pth"))
            self.env.soccer_bot_two.model.train()
        self.env.soccer_bot_two.trainer = QTrainer(self.env.soccer_bot_two.model, lr=self.learning_rate, gamma=self.gamma)
        
        self.env.soccer_bot_one.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.env.soccer_bot_two.memory = deque(maxlen=MAX_MEMORY)

    def update_epsilon(self):
        self.epsilon = max(1 * np.exp(-self.env.episode_count * self.decay_rate), self.min_epsilon)

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
        return self.env.soccer_bot_one.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_long_memory_two(self):
        if len(self.env.soccer_bot_two.memory) > BATCH_SIZE:
            minibatch = random.sample(self.env.soccer_bot_two.memory, BATCH_SIZE)
        else:
            minibatch = self.env.soccer_bot_two.memory

        states, actions, rewards, next_states, dones = zip(*minibatch)
        return self.env.soccer_bot_two.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory_one(self, state, action, reward, next_state, done):
        return self.env.soccer_bot_one.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory_two(self, state, action, reward, next_state, done):
        return self.env.soccer_bot_two.trainer.train_step(state, action, reward, next_state, done)

    def get_state(self):
        return self.env.get_state()

    def get_action_one(self, state) -> tuple:
        # random moves: tradeoff exploration / exploitation
        explore = np.random.choice([True, False], p=[self.epsilon, 1-self.epsilon])
        final_move = np.zeros(self.output_size)
        if explore:
            # print("random")
            direction = np.random.randint(0, 7)
            final_move[direction] = 1
            return final_move, get_direction_labeled(direction)
        else:
            # print("Predicted")
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.env.soccer_bot_one.model(state0)
            prediction = prediction.detach().numpy()
            direction = np.argmax(prediction)
            final_move[direction] = 1
            return final_move, get_direction_labeled(direction) 

    def get_action_two(self, state) -> tuple:
        # random moves: tradeoff exploration / exploitation
        explore = np.random.choice([True, False], p=[self.epsilon, 1-self.epsilon])
        final_move = np.zeros(self.output_size)
        if explore:
            # print("random")
            direction = np.random.randint(0, 7)
            final_move[direction] = 1
            return final_move, get_direction_labeled(direction)
        else:
            # print("Predicted")
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.env.soccer_bot_two.model(state0)
            prediction = prediction.detach().numpy()
            direction = np.argmax(prediction)
            final_move[direction] = 1
            return final_move, get_direction_labeled(direction)
