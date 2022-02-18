import sys
import dat
import dev
import time
import matplotlib.pyplot as plt

x, y = [], []

opm = dev.opm(15)

for i in range(20):

    x.append(i)
    y.append(opm.query(1, 1))

    time.sleep(0.2)

    plt.cla()
    plt.plot(x, y)
    plt.grid()
    plt.pause(0.1)

plt.show()

opm.close()