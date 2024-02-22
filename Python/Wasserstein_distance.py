import matplotlib.pyplot as plt
plt.style.use('ggplot')

import persim
import os
import matplotlib.pyplot as plt
import ripser

def wasserstein(X, X2):
    P1 = ripser.ripser(X)['dgms'][1]
    P2 = ripser.ripser(X2)['dgms'][1]

    plt.clf()

    distance_bottleneck, matching = persim.bottleneck(P1, P2, matching=True)

    persim.bottleneck_matching(P1, P2, matching, labels=['PD($S_1$)', 'PD($S_2$)'])
    plt.title("Distance {:.3f}".format(distance_bottleneck))

    path = os.getcwd() + '/match.png'
    plt.savefig(path)

    return [P1, P2]
