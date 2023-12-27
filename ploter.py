import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores_one, scores_two, mean_scores_one, mean_scores_two):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores_one)
    plt.plot(mean_scores_two)
    plt.plot(scores_two)
    plt.plot(mean_scores_one)
    plt.ylim(ymin=0)
    plt.text(len(scores_one)-1, scores_one[-1], str(scores_one[-1]))
    plt.text(len(scores_two)-1, scores_two[-1], str(scores_two[-1]))
    plt.text(len(mean_scores_one)-1, mean_scores_one[-1], str(mean_scores_one[-1]))
    plt.text(len(mean_scores_two)-1, mean_scores_two[-1], str(mean_scores_two[-1]))
    plt.show(block=False)
    plt.pause(.1)
