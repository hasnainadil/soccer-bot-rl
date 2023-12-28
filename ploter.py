import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores_one, scores_two, mean_scores_one, mean_scores_two, games, reward_one, reward_two, player_one_score, player_two_score, cumulative_reward_diff):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training.... \n Game: "+str(games)+" Score: "+str(player_one_score)+"--"+str(player_two_score))
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores_one,label = "Score_one")
    plt.plot(mean_scores_one, label = "Mean_one")
    plt.plot(scores_two, label= "Score_two")
    plt.plot(mean_scores_two,label = "Mean_two")
    plt.plot(reward_one, label="Last step reward bot one")
    plt.plot(reward_two, label="Last step reward bot two")
    plt.plot(cumulative_reward_diff, label="Cumulative reward difference")
    plt.ylim(ymin=0)
    plt.text(len(scores_one)-1, scores_one[-1], str(scores_one[-1]))
    plt.text(len(scores_two)-1, scores_two[-1], str(scores_two[-1]))
    plt.text(len(mean_scores_one)-1, mean_scores_one[-1], str(mean_scores_one[-1]))
    plt.text(len(mean_scores_two)-1, mean_scores_two[-1], str(mean_scores_two[-1]))
    plt.legend()
    plt.pause(.1)