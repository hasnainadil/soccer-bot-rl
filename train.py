from agent import Agent
from ploter import plot

def train():
    agent = Agent(12, 512, 8,epsilon=1, min_epsilon=0.05, decay_rate=0.1, gamma=0.9, learning_rate=0.01)
    plot_scores_one = []
    plot_mean_scores_one = []
    plot_scores_two = []
    plot_mean_scores_two = []
    total_score_one = 0
    reward_one = 0
    reward_two = 0
    epsilons = []
    reward_list_one = []
    reward_list_two = []
    cumulative_reward_diff = []
    cumulative_reward_one = 0
    cumulative_reward_two = 0
    loss_list_one = []
    loss_list_two = []
    loss_list_one_long = []
    loss_list_two_long = []
    loss_one = 0
    loss_two = 0
    step_count = 0
    total_score_two = 0
    totat_reward_player_one = 0
    totat_reward_player_two = 0
    record_one = 0
    record_two = 0
    state_old_one, state_old_two = agent.get_state()
    while True:
        #render ui        
        # get old state
        # get 
        step_count += 1
        final_move_one, action_one = agent.get_action_one(state_old_one)
        final_move_two, action_two = agent.get_action_two(state_old_two)
        
        # perform move and get new state
        reward_one, reward_two, player_one_score, player_two_score, state_new_one, state_new_two, done = agent.env.play_step(action_one=action_one, action_two=action_two)
        
        #train short memory one
        loss_one += agent.train_short_memory_one(state_old_one, final_move_one, reward_one, state_new_one, done)
        #train short memory two
        loss_two += agent.train_short_memory_two(state_old_two, final_move_two, reward_two, state_new_two, done)

        # remember
        agent.remember_one(state_old_one, final_move_one, reward_one, state_new_one, done)
        agent.remember_two(state_old_two, final_move_two, reward_two, state_new_two, done)
        cumulative_reward_one += reward_one
        cumulative_reward_two += reward_two
        state_old_one = state_new_one
        state_old_two = state_new_two

        if done:
            agent.env.reset()
            agent.update_epsilon()
            state_old_one, state_old_two = agent.get_state()

            # train long memory, plot result
            loss_long_one = agent.train_long_memory_one()
            loss_list_one_long.append(loss_long_one/10)
            loss_long_two = agent.train_long_memory_two()
            loss_list_two_long.append(loss_long_two/10)
            loss_list_one.append(loss_one*0.1/step_count)
            loss_list_two.append(loss_two*0.1/step_count)
            loss_one = 0
            loss_two = 0
            step_count = 0

            if player_one_score > record_one:
                record_one = player_one_score

            if player_two_score > record_two:
                record_two = player_two_score

            agent.env.soccer_bot_one.model.save("bot_one_model.pth")
            agent.env.soccer_bot_two.model.save("bot_two_model.pth")

            cumulative_reward_diff.append(cumulative_reward_one - cumulative_reward_two)

            print("Cumulative Reward One: ", cumulative_reward_one)
            print("Cumulative Reward Two: ", cumulative_reward_two)
            print('Game', agent.env.episode_count, 'Player One Score', player_one_score, 'Player Two Score', player_two_score, 'Record:', record_one,"--", record_two)

            plot_scores_one.append(player_one_score)
            plot_scores_two.append(player_two_score)
            # reward_list_one.append(reward_one/10)
            # reward_list_two.append(reward_two/10)
            totat_reward_player_one += reward_one
            totat_reward_player_two += reward_two
            epsilons.append(agent.epsilon)
            reward_list_one.append(totat_reward_player_one*0.1/agent.env.episode_count)
            reward_list_two.append(totat_reward_player_two*0.1/agent.env.episode_count)
            total_score_one += player_one_score
            total_score_two += player_two_score
            mean_score_one = total_score_one / agent.env.episode_count
            mean_score_two = total_score_two / agent.env.episode_count
            plot_mean_scores_one.append(mean_score_one)
            plot_mean_scores_two.append(mean_score_two)
            plot(loss_list_one, loss_list_two, loss_list_one_long, loss_list_two_long, agent.epsilon*100, agent.env.episode_count, player_one_score, player_two_score)

if __name__ == '__main__':
    import sys
    sys.exit(train())