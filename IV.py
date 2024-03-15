import dev
import numpy as np


def IV2600():
  start, stop, step = 0.05, 10, 0.05

  x = np.arange(start, stop + step * 0.1, step)
  x = np.round(x, 2)
  n = len(x)

  xstr = str(round(start * 0.001, 4)) + ', '
  xstr = xstr + str(round(stop * 0.001, 4)) + ', '
  xstr = xstr + str(round(step * 0.001, 4)) + ', ' + str(n)

  ksm = dev.ivs()
  ksm.write('reset()')
  ksm.write('smua.source.limitv = 10')
  ksm.write('SweepILinMeasureV(smua, ' + xstr + ')')
  y = ksm.Vread(str(n), 'smua')
  y = np.round(y / x, 6)
  ksm.close()

  return x, y


def VI2600():
  start, stop, step = -2, 3, 0.01

  x = np.arange(start, stop + step * 0.1, step)
  x = np.round(x, 2)
  n = len(x)

  xstr = str(start) + ', ' + str(stop) + ', ' + str(step) + ', ' + str(n)

  ksm = dev.ivs()
  ksm.write('reset()')
  ksm.write('smua.source.limiti = 10e-3')
  ksm.write('SweepVLinMeasureI(smua, ' + xstr + ')')
  y = ksm.Iread(str(n), 'smua')
  ksm.close()

  return x, y


def VI2400():
  start, stop, step = -2, 4, 0.1

  x = np.arange(start, stop + step * 0.1, step)
  x = np.round(x, 2)
  n = len(x)

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

  return x, y

if __name__ == '__main__': print(IV2600())
