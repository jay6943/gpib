import sys
import dev
import dat
import time

def opm(filename):

    xmin = 10
    xmax = 60
    step = 0.5

    ldc = dev.ldc()
    opm = dev.opm(15)

    opm.write('sens1:chan2:pow:unit 0')
    ldc.value(0)
    voltage = ldc.query('LAS:LDV?')
    ymax = opm.query(1, 1)

    current = xmin
    ldc.value(str(current))
    voltage = ldc.query('LAS:LDV?')
    output = opm.query(1, 1)
    watt = round(current * voltage, 3)

    x, y, v, w = [], [], [], []

    while current < xmax and voltage < 6.7:
        x.append(current)
        y.append(output)
        v.append(voltage)
        w.append(watt)

        print(current, output)

        current += step

        ldc.value(str(current))
        voltage = ldc.query('LAS:LDV?')
        output = opm.query(1, 1)
        watt = round(current * voltage, 3)

    ldc.value(0)
    ldc.off()

    ldc.close()
    opm.close()

    fp = open(dat.getfolder() + filename + '.txt', 'w')

    for i in range(len(x)):
        fp.write(str(x[i]) + '\t')
        fp.write(str(y[i]) + '\t')
        fp.write(str(v[i]) + '\t')
        fp.write(str(w[i]) + '\n')
        y[i] = y[i] - ymax

    fp.close()

def pdl(filename):

    xmin = 10
    xmax = 60
    step = 1

    pdl = dev.pdl()
    ldc = dev.ldc()

    print('initializing...')
    current = xmin
    ldc.value(str(current))
    time.sleep(5)
    voltage = ldc.query('LAS:LDV?')
    pdls, loss = pdl.query()
    voltage = ldc.query('LAS:LDV?')
    watt = round(current * voltage, 3)

    x, y, v, w, p = [], [], [], [], []

    while current < xmax + step and voltage < 6.7:
        x.append(current)
        y.append(loss)
        p.append(pdls)
        v.append(voltage)
        w.append(watt)

        print(current, loss, pdls, voltage, watt)

        current += step
        ldc.value(str(current))
        voltage = ldc.query('LAS:LDV?')
        pdls, loss = pdl.query()
        watt = round(current * voltage, 3)

    ldc.value(0)
    ldc.off()

    ldc.close()
    pdl.close()

    fp = open(dat.getfolder() + filename + '.txt', 'w')

    for i in range(len(x)):
        fp.write(str(x[i]) + '\t')
        fp.write(str(y[i]) + '\t')
        fp.write(str(p[i]) + '\t')
        fp.write(str(v[i]) + '\t')
        fp.write(str(w[i]) + '\n')

    fp.close()

if __name__ == '__main__': pdl(sys.argv[1])
