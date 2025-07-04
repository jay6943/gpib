import dev
import numpy as np


def IV2600():
  start, stop, step = 0.05, 10, 0.05

  x = np.arange(start, stop + step * 0.1, step)
  x = np.round(x, 2)
  n = len(x)

  xstr = f'{start * 0.001:.4f}, {stop * 0.001:.4f}, {step * 0.001:.4f}, {n}'

  iv = dev.Keithley()
  iv.write('reset()')
  iv.write('smua.source.limitv = 10')
  iv.write(f'SweepILinMeasureV(smua, {xstr})')
  y = iv.Vread(str(n), 'smua')
  y = np.round(y / x, 6)
  iv.close()

  return x, y


def VI2600():
  start, stop, step = -2, 3, 0.01

  x = np.arange(start, stop + step * 0.1, step)
  x = np.round(x, 2)
  n = len(x)

  vi = dev.Keithley()
  vi.write('reset()')
  vi.write('smua.source.limiti = 10e-3')
  vi.write(f'SweepVLinMeasureI(smua, {start}, {stop}, {step}, {n})')
  y = vi.Iread(str(n), 'smua')
  vi.close()

  return x, y


def VI2400():
  start, stop, step = -2, 4, 0.1

  x = np.arange(start, stop + step * 0.1, step)
  x = np.round(x, 2)
  n = len(x)

  iv = dev.Keithley()
  iv.write('*RST')
  iv.write(':SENS:FUNC:CONC OFF')
  iv.write(':SOUR:FUNC VOLT')
  iv.write(':SENS:FUNC "CURR"')
  iv.write(':SENS:CURR:PROT 100e-3')
  iv.write(':SENS:CURR:RANG 10e-3')
  iv.write(f':SOUR:VOLT:START {start}')
  iv.write(f':SOUR:VOLT:STOP {stop}')
  iv.write(f':SOUR:VOLT:STEP {step}')
  iv.write(':SOUR:VOLT:MODE SWE')
  iv.write(':SOUR:SWE:RANG AUTO')
  iv.write(':SOUR:SWE:SPAC LIN')
  iv.write(f':TRIG:COUN {n}')
  iv.write(':SOUR:DEL 0.01')
  iv.write(':OUTP ON')
  _, y = iv.read2400()
  iv.write(':OUTP OFF')
  iv.close()

  return x, y


if __name__ == '__main__': print(IV2600())
