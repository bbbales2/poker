#%%

import numpy
import matplotlib.pyplot as plt

#%%
money = []
with open('/home/bbales2/poker/project_acpc_server/test1.log') as f:
    for line in f:
        if line[0:5] == 'STATE':
            m, ps = line.split(':')[-2:]

            m = m.split('|')
            ps = ps.split('|')
            if ps[0] == 'p1':
                money.append(int(m[0]))
            else:
                money.append(int(m[1]))

money = numpy.cumsum(money)
plt.plot(money)
plt.plot(numpy.zeros(len(money)))

#%%
import subprocess
import itertools
import shutil
import random
import json

players = ['joao5', 'clifford2', 'clifford', 'gerard', 'fred', 'fred1000', 'fred2', 'derf', 'joao', 'joao3', 'joao4', 'fred3']

output = []

for p1, p2 in [('joao5', 'fred2')]:#itertools.combinations_with_replacement(players, 2):#
    match = "{0}vs{1}".format(p1, p2)

    money = []

    with open('/home/bbales2/poker/project_acpc_server/{0}.log'.format(match)) as f:
        for line in f:
            if line[0:5] == 'STATE':
                m, ps = line.split(':')[-2:]

                m = m.split('|')
                ps = ps.split('|')
                if ps[0] == 'p1':
                    money.append(int(m[0]))
                else:
                    money.append(int(m[1]))

    money2 = numpy.cumsum(money)

    print match, money[-1] / (10000 * 20.0)
    plt.plot(numpy.zeros(len(money2)), 'r', linewidth = 6)
    plt.plot(range(1, len(money2) + 1), money2 / 20, 'b', linewidth = 6)
    plt.title("{0} vs {1}".format(p1.capitalize(), p2.capitalize()), fontsize = 44)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.tick_params(axis='both', which='minor', labelsize=20)
    plt.yticks(rotation = 45)
    #plt.ylim((-1000, 4000))
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(14.5, 10.5)
    plt.xlabel('Hand #', fontsize = 36)
    plt.ylabel('{0}\'s money (big blinds)'.format(p1.capitalize()), fontsize = 36)
    plt.show()

    mean = numpy.mean(money)

    print match, numpy.mean(money) / 20.0, numpy.abs(mean / numpy.std(money))

    #1/0
