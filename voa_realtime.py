import sys
import dat
import dev
import time
import numpy as np
import matplotlib.pyplot as plt

star = 0
stop = 1
step = 0.1

v = np.arange(star, stop + step * 0.1, step)
x = []
y = []

dcp = dev.dcp()
opm = dev.ando()

dcp.write('APPL P25V, ' + str(star) + ', 1.0')
dcp.write('OUTP ON')

for i in range(len(v)):

    v[i] = round(v[i], 1)

    dcp.write('APPL P25V, ' + str(v[i]) + ', 1.0')

    time.sleep(0.5)

    a, b = opm.query()

    x.append(v[i])
    y.append(b)

    plt.cla()
    plt.plot(x, y)
    plt.grid()
    plt.pause(0.1)

plt.show()

dcp.write('APPL P25V, ' + str(star) + ', 1.0')
dcp.write('OUTP OFF')

dat.save(dat.getfolder() + '/voa.txt', x, y)

opm.close()
dcp.close()
