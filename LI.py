import sys
import dev
import dat
import time
import numpy as np

def scan(filename):

    start = 0
    stop = 60
    step = 1

    ldc = dev.ldc()
    opm = dev.opm(20)

    ldc.value(int(start))
    opm.mW(1, 1)
    time.sleep(3)

    x = np.arange(start, stop + step * 0.1, step)
    y = np.arange(start, stop + step * 0.1, step)
    v = np.arange(start, stop + step * 0.1, step)

    for i in range(len(x)):
        current = start + i * step
        ldc.value(current)
        v[i] = ldc.volt()
        x[i] = float(current)
        y[i] = opm.query(1, 1) * 1e6

        if x[i] < 0: x[i] = 0

        print(x[i], y[i], v[i])

    ldc.value(0)
    ldc.off()
    opm.dBm(1, 1)

    ldc.close()
    opm.close()

    fp = open(dat.getfolder() + filename + '.txt', 'w')

    for i in range(len(x)):
        fp.write(str(x[i]) + '\t')
        fp.write(str(y[i]) + '\t')
        fp.write(str(v[i]) + '\n')

    fp.close()

if __name__ == '__main__': scan(sys.argv[1])
