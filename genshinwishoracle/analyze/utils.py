
import base64
from .models import *
from io import BytesIO
from matplotlib import pyplot 
import numpy

def bar_graph_for_statistics(solution, banner_type,statistics_type, numwishes, pity, guaranteed,fate_points) ->str:
    if statistics_type == "calcprobability":
        return bar_graph_for_calcprobability(solution,banner_type,numwishes, pity, guaranteed,fate_points)
    elif statistics_type == "calcnumwishes":
        return ""
    return ""

def bar_graph_for_calcprobability(solution, banner_type, numwishes, pity, guaranteed, fate_points) -> str:
    values = [float(solution[key]) for key in solution.keys()]
    pyplot.switch_backend('AGG')
    fig, ax = pyplot.subplots(figsize=(10, 6))
    guaranteed_text = "with" if guaranteed else "without"
    if banner_type == "character":
        x_labels = ["X"]
        for i in range(0,7):
            x_labels.append("C"+str(i))
        fig.suptitle('Wish Probability Breakdown for: {} Wishes, {} Pity, {} Guaranteed'.format(numwishes, pity, guaranteed_text))
        fig.supylabel('Portion Resuling in Specified Constellation')
    elif banner_type == "weapon":
        x_labels = ["X"]
        for i in range(1,6):
            x_labels.append("R"+str(i))
        fig.suptitle('Wish Probability Breakdown for: {} Wishes, {} Pity, {} Guaranteed, {} Fate Points'.format(numwishes, pity, guaranteed_text, fate_points))
        fig.supylabel('Portion Resuling in Specified Refinement')

    bars= pyplot.bar(x_labels , values)
    ax.bar_label(bars)
    min_ylim = -0.1
    max_ylim = 1.1
    pyplot.ylim(min_ylim,max_ylim)
    pyplot.tight_layout()

    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph