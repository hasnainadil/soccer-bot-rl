import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores_one, scores_two, mean_scores_one, mean_scores_two, games):
    display.clear_output(wait=True)
    plt.clf()
    plt.text(.01, .99, "Game: "+str(games), ha='left', va='top', transform=plt.gca().transAxes)
    plt.tight_layout()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores_one, label="Score_one")
    plt.plot(mean_scores_one, label="Mean_one")
    plt.plot(scores_two, label="Score_two")
    plt.plot(mean_scores_two, label="Mean_two")
    plt.ylim(ymin=0)
    plt.text(len(scores_one) - 1, scores_one[-1], str(scores_one[-1]))
    plt.text(len(scores_two) - 1, scores_two[-1], str(scores_two[-1]))
    plt.text(len(mean_scores_one) - 1, mean_scores_one[-1], str(mean_scores_one[-1]))
    plt.text(len(mean_scores_two) - 1, mean_scores_two[-1], str(mean_scores_two[-1]))
    plt.legend()
    plt.pause(0.1)