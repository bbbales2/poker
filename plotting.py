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