import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(loss_list_one, loss_list_two, loss_list_one_long, loss_list_two_long, epsilons, games, player_one_score, player_two_score):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training.... \n Game: "+str(games)+" Score: "+str(player_one_score)+"--"+str(player_two_score)+" epsilon: "+str(epsilons))
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(loss_list_one, label="Loss_short_one")
    plt.plot(loss_list_two, label="Loss_short_two")
    plt.plot(loss_list_one_long, label="Loss_long_one")
    plt.plot(loss_list_two_long, label="Loss_long_two")
    plt.ylim(ymin=0)
    plt.text(len(loss_list_one)-1, loss_list_one[-1], str(loss_list_one[-1]))
    plt.text(len(loss_list_two)-1, loss_list_two[-1], str(loss_list_two[-1]))
    plt.text(len(loss_list_one_long)-1, loss_list_one_long[-1], str(loss_list_one_long[-1]))
    plt.text(len(loss_list_two_long)-1, loss_list_two_long[-1], str(loss_list_two_long[-1]))
    plt.legend()
    # plt.show(block=False)
    plt.pause(.1)