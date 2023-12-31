import numpy as np
from game_env import Game_env
import pygame
import constants as const
import matplotlib.pyplot as plt
from IPython import display
import os

plt.ion()

def reduce_state(a): # #[left, right, up, down] #[left, right, up, down] #[left, right, up, down] #[left, right, up, down]
  reduced = np.zeros(9)
  for i in range(3):
    if a[4*i + 1] == 1 and a[4*i + 2] == 0 and a[4*i + 3] == 0:
      reduced[3*i + 0] = 0 
      reduced[3*i + 1] = 0 
      reduced[3*i + 2] = 0
    elif a[4*i + 1] == 1 and a[4*i + 2] == 1 : 
      reduced[3*i + 0] = 1
      reduced[3*i + 1] = 0 
      reduced[3*i + 2] = 0
    elif a[4*i + 2] == 1 and a[4*i + 1] == 0 and a[4*i + 0] == 0 : 
      reduced[3*i + 0] = 0
      reduced[3*i + 1] = 1 
      reduced[3*i + 2] = 0
    elif a[4*i + 2] == 1 and a[4*i + 0] == 1 : 
      reduced[3*i + 0] = 1
      reduced[3*i + 1] = 1 
      reduced[3*i + 2] = 0
    elif a[4*i + 0] == 1 and a[4*i + 2] == 0 and a[4*i + 3] == 0 : 
      reduced[3*i + 0] = 0
      reduced[3*i + 1] = 0 
      reduced[3*i + 2] = 1
    elif a[4*i + 3] == 1 and a[4*i + 0] == 1 : 
      reduced[3*i + 0] = 1
      reduced[3*i + 1] = 0 
      reduced[3*i + 2] = 1
    elif a[4*i + 3] == 1 and a[4*i + 1] == 0 and a[4*i + 0] == 0 : 
      reduced[3*i + 0] = 0
      reduced[3*i + 1] = 1 
      reduced[3*i + 2] = 1
    elif a[4*i + 1] == 1 and a[4*i + 3] == 1 : 
      reduced[3*i + 0] = 1
      reduced[3*i + 1] = 1 
      reduced[3*i + 2] = 1 
    
  return reduced
    
def plot(scores_one, scores_two, games, reward_one, reward_two, player_one_score, player_two_score):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training.... \n Game: "+str(games)+" Score: "+str(player_one_score)+"--"+str(player_two_score))
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores_one,label = "Score_one")
    plt.plot(scores_two, label= "Score_two")
    plt.plot(reward_one, label="mean reward bot one")
    plt.plot(reward_two, label="mean reward bot two")
    plt.ylim(ymin=0)
    plt.text(len(scores_one)-1, scores_one[-1], str(scores_one[-1]))
    plt.text(len(scores_two)-1, scores_two[-1], str(scores_two[-1]))
    plt.text(len(reward_one)-1, reward_one[-1], str(reward_one[-1]))
    plt.text(len(reward_two)-1, reward_two[-1], str(reward_two[-1]))
    plt.legend()
    plt.pause(.1)

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

def train_classic(env):
    binary_array = np.array([1,1,1,1,1,1,1,1,1])
    max_state_number = np.dot(binary_array, 2**np.arange(len(binary_array))[::-1]) + 1
    action_size = 8 # 8 possible actions( 8 directions )
    file_path = "classic_model/q_tables.npz"

    if os.path.exists(file_path) :
      npz = np.load(file_path)
      env.soccer_bot_one.model = npz["arr_0"]
      env.soccer_bot_two.model = npz["arr_1"]
      print("Previous table loaded")
    else:
      env.soccer_bot_one.model = np.zeros((max_state_number,action_size))
      env.soccer_bot_two.model = np.zeros((max_state_number,action_size))

    learning_rate = 0.01
    gamme = 0.9
    max_epsilon = 1.0
    epsilon = max_epsilon/3
    min_epsilon = 0.1
    decay_rate = 0.06
    total_reward_one = 0
    total_reward_two = 0
    rewards_list_one = []
    rewards_list_two = []
    score_list_one = []
    score_list_two = []
    player_one_score = 0
    player_two_score = 0
    episode_count = 0
    action_one = 0
    action_two = 0
    step_count = 0
    state_old_one, state_old_two = env.get_state()
    state_old_one = reduce_state(state_old_one)
    state_old_two = reduce_state(state_old_two)
    state_old_one = np.dot(state_old_one, 2**np.arange(len(state_old_one))[::-1])
    state_old_one = int(state_old_one)
    state_old_two = np.dot(state_old_two, 2**np.arange(len(state_old_two))[::-1])
    state_old_two = int(state_old_two)

    while True:
        step_count += 1
        explore = np.random.choice([True, False], p=[epsilon, 1-epsilon])

        if explore:
            action_one = np.random.randint(0, action_size - 1)
            action_two = np.random.randint(0, action_size - 1)
        else:
            action_one = np.argmax(env.soccer_bot_one.model[state_old_one, : ])
            action_two = np.argmax(env.soccer_bot_two.model[state_old_two, : ])

        action_one = int(action_one)
        action_two = int(action_two)
        reward_one, reward_two, player_one_score, player_two_score, state_new_one, state_new_two, done = env.play_step(get_direction_labeled(action_one),get_direction_labeled(action_two))
        state_new_one = reduce_state(state_new_one)
        state_new_two = reduce_state(state_new_two)
        state_new_one = np.dot(state_new_one, 2**np.arange(len(state_new_one))[::-1])
        state_new_two = np.dot(state_new_two, 2**np.arange(len(state_new_two))[::-1])
        state_new_one = int(state_new_one)
        state_new_two = int(state_new_two)

        # qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma * np.max(qtable[new_state, :]) - qtable[state, action])
        env.soccer_bot_one.model[state_old_one, action_one] = (1 - learning_rate)*env.soccer_bot_one.model[state_old_one, action_one] + learning_rate * (reward_one + gamme * np.max(env.soccer_bot_one.model[state_new_one, :]) - env.soccer_bot_one.model[state_old_one, action_one])
        env.soccer_bot_two.model[state_old_two, action_two] = (1 - learning_rate)*env.soccer_bot_two.model[state_old_two, action_two] + learning_rate * (reward_two + gamme * np.max(env.soccer_bot_two.model[state_new_two, :]) - env.soccer_bot_two.model[state_old_two, action_two])
        state_old_one = state_new_one
        state_old_two = state_new_two

        total_reward_one += reward_one
        total_reward_two += reward_two

        if done:
            episode_count += 1
            np.savez('classic_model/q_tables.npz', env.soccer_bot_one.model, env.soccer_bot_two.model)
            env.reset()
            if episode_count > 1500:
              break
            epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode_count)

            score_list_one.append(player_one_score)
            score_list_two.append(player_two_score)
            rewards_list_one.append(total_reward_one/10000)
            rewards_list_two.append(total_reward_two/10000)
            total_reward_one = 0
            total_reward_two = 0
            step_count = 0

            print("Episode: ", episode_count, "Player One Score: ", player_one_score, "Player Two Score: ", player_two_score, "Epsilon: ", epsilon)
            plot(score_list_one, score_list_two, episode_count, rewards_list_one, rewards_list_two, player_one_score, player_two_score)

if __name__ == "__main__":
    import sys
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    env = Game_env(screen=screen, fps= 120)
    sys.exit(train_classic(env))