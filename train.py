from agent import Agent
import constants as const
import ploter

def train():
    agent = Agent(16, 512, 6)
    plot_scores_one = []
    plot_mean_scores_one = []
    plot_scores_two = []
    plot_mean_scores_two = []
    total_score_one = 0
    total_score_two = 0
    record_one = 0
    record_two = 0
    while True:
        state_old_one, state_old_two = agent.get_state()
        # get move
        final_move_one,toward_one, rotation_one = agent.get_action_one(state_old_one)
        final_move_two,toward_two, rotation_two = agent.get_action_two(state_old_two)

        # perform move and get new state
        reward_one, reward_two, done, player_one_score, player_two_score = agent.env.play_step((const.Direction(toward_one), const.Direction
        (rotation_one)), (const.Direction(toward_two), const.Direction(rotation_two)))
        state_new_one, state_new_two = agent.get_state()

        #train short memory one
        agent.train_short_memory_one(state_old_one, final_move_one, reward_one, state_new_one, done)
        #train short memory two
        agent.train_short_memory_two(state_old_two, final_move_two, reward_two, state_new_two, done)

        # remember
        agent.remember_one(state_old_one, final_move_one, reward_one, state_new_one, done)
        agent.remember_two(state_old_two, final_move_two, reward_two, state_new_two, done)