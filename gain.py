import dev
import time
import numpy as np

def spectral():

    current = 400

    ldc = dev.ldc()
    att = dev.att()
    osa = dev.osa(False)

    xmin, xmax, step = 5, 30, 1

    x = np.arange(xmin, xmax + step * 0.1, step)
    y = np.arange(xmin, xmax + step * 0.1, step)

    ldc.value(int(current))
    att.value(xmax)
    osa.write('INIT:CONT OFF')
    osa.write('INIT:IMM')
    time.sleep(2)

    pint = 6

    for i in range(len(x)):
        attenuation = xmax - i * step
        att.value(attenuation)
        osa.write('INIT:IMM')
        osa.write('CALC:MARK:MAX')
        data = osa.query('CALC:MARK:Y?')

        x[i] = pint - float(attenuation)
        y[i] = float(data)

        print(attenuation, x[i], y[i], round(y[i]-x[i], 2))

    ldc.off()
    att.value(xmax)
    osa.write('INIT:CONT ON')

    att.close()
    osa.close()

def current():

    ldc = dev.ldc()
    osa = dev.osa(False)

    xmin = 100
    xmax = 500
    step = 25

    x = np.arange(xmin, xmax + 0.5 * step, step)
    y = np.arange(xmin, xmax + 0.5 * step, step)

    ldc.value(int(xmin))
    osa.write('INIT:CONT OFF')
    osa.write('INIT:IMM')
    time.sleep(2)

    for i in range(len(x)):
        current = xmin + i * step
        ldc.value(int(current))
        osa.write('INIT:IMM')
        osa.write('CALC:MARK:MAX')
        data = osa.query('CALC:MARK:Y?')

        x[i] = current
        y[i] = round(float(data) + 24.0, 3)

        print(x[i], y[i])

    osa.write('INIT:CONT ON')
    ldc.off()
    time.sleep(1)

    osa.close()
    ldc.close()

def opm():

    att = dev.att()
    opm = dev.opm(15)

    xmin = 10
    xmax = 40
    step = 1
    pset = 14
    loss = 3

    x = np.arange(xmin, xmax + 0.5 * step, step)
    y = np.arange(xmin, xmax + 0.5 * step, step)

    opm.dBm(1, 1)
    att.value(xmax)
    time.sleep(2)

    for i in range(len(x)):
        attenuation = xmax - i * step
        att.value(attenuation)
        output = opm.query(1, 1)

        x[i] = float(pset - loss - attenuation)
        y[i] = float(output)

        print(x[i], y[i], y[i]-x[i])

    att.value(xmax)

    att.close()
    opm.close()

if __name__ == '__main__': spectral()
