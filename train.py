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
        #render ui
        agent.env.render()

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

        if done:
            # train long memory, plot result
            agent.env.reset()
            agent.n_games += 1
            agent.train_long_memory_one()
            agent.train_long_memory_two()

            if player_one_score > record_one:
                record_one = player_one_score
                agent.env.soccer_bot_one.model.save()

            if player_two_score > record_two:
                record_two = player_two_score
                agent.env.soccer_bot_two.model.save()

            print('Game', agent.n_games, 'Player One Score', player_one_score, 'Player Two Score', player_two_score, 'Record:', record_one,"--", record_two)

            plot_scores_one.append(player_one_score)
            plot_scores_two.append(player_two_score)
            total_score_one += player_one_score
            total_score_two += player_two_score
            mean_score_one = total_score_one / agent.n_games
            mean_score_two = total_score_two / agent.n_games
            plot_mean_scores_one.append(mean_score_one)
            plot_mean_scores_two.append(mean_score_two)
            ploter.plot(plot_scores_one, plot_mean_scores_one, plot_scores_two, plot_mean_scores_two)

if __name__ == '__main__':
    import sys
    sys.exit(train())