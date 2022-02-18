import sys
import dev
import dat
import numpy as np
import matplotlib.pyplot as plt

def IV2600(filename):

    start, stop, step = 0.05, 10, 0.05

    x = np.arange(start, stop + step * 0.1, step)

    n = len(x)

    for i in range(n): x[i] = round(x[i], 2)

    xstr = str(round(start * 0.001, 4)) + ', '
    xstr = xstr + str(round(stop * 0.001, 4)) + ', '
    xstr = xstr + str(round(step * 0.001, 4)) + ', ' + str(n)

    ksm = dev.ivs()

    ksm.write('reset()')
    ksm.write('smua.source.limitv = 10')
    ksm.write('SweepILinMeasureV(smua, ' + xstr + ')')

    y = ksm.Vread(str(n), 'smua')

    ksm.close()

    dat.save(filename + '-I', x, y)
    dat.plot(filename + '-I', x, y, 5, 4, 0, stop, 1, 1.6, '-', 1)

    for i in range(n): y[i] = round(y[i] / x[i], 6)
    
    dat.save(filename + '-R', x, y)
    dat.plot(filename + '-R', x, y, 5, 6, 0, stop, 0, 10, '-', 0)

def VI2600(filename):

    start, stop, step = -2, 3, 0.01

    x = np.arange(start, stop + step * 0.1, step)

    n = len(x)

    for i in range(n): x[i] = round(x[i], 2)

    xstr = str(start) + ', ' + str(stop) + ', ' + str(step) + ', ' + str(n)

    ksm = dev.ivs()

    ksm.write('reset()')
    ksm.write('smua.source.limiti = 10e-3')
    ksm.write('SweepVLinMeasureI(smua, ' + xstr + ')')

    y = ksm.Iread(str(n), 'smua')

    ksm.close()

    dat.save(filename, x, y)
    dat.plot(filename, x, y, 4, 5, start, stop, min(y), max(y), '-', 1)

def VI2400(filename):

    start, stop, step = -2, 4, 0.1

    x = np.arange(start, stop + step * 0.1, step)

    n = len(x)

    for i in range(n): x[i] = round(x[i], 2)

    ksm = dev.ivs()

    ksm.write('*RST')
    ksm.write(':SENS:FUNC:CONC OFF')
    ksm.write(':SOUR:FUNC VOLT')
    ksm.write(':SENS:FUNC "CURR"')
    ksm.write(':SENS:CURR:PROT 100e-3')
    ksm.write(':SENS:CURR:RANG 10e-3')
    ksm.write(':SOUR:VOLT:START ' + str(start))
    ksm.write(':SOUR:VOLT:STOP ' + str(stop))
    ksm.write(':SOUR:VOLT:STEP ' + str(step))
    ksm.write(':SOUR:VOLT:MODE SWE')
    ksm.write(':SOUR:SWE:RANG AUTO')
    ksm.write(':SOUR:SWE:SPAC LIN')
    ksm.write(':TRIG:COUN ' + str(n))
    ksm.write(':SOUR:DEL 0.01')
    ksm.write(':OUTP ON')

    _, y = ksm.read2400()

    ksm.write(':OUTP OFF')

    ksm.close()

    dat.save(filename, x, y)
    dat.plot(filename, x, y, 4, 5, start, stop, min(y), max(y), '-', 1)

if __name__ == '__main__': 
    
    if sys.argv[1] == 'IV': IV2600(sys.argv[2])
    if sys.argv[1] == 'VI': VI2600(sys.argv[2])
