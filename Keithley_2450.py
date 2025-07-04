import dev
import time
import numpy as np
import matplotlib.pyplot as plt


def sweep():
  start = 1 * 0.001
  stop = 10 * 0.001
  step = 1 * 0.001
  num = int(round((stop - start) / step)) + 1

  iv = dev.Keithley_2450()
  print(iv.query('*IDN?'))
  iv.write('*RST')
  iv.write('SENS:FUNC "VOLT"')
  iv.write('SENS:VOLT:RANG:AUTO ON')
  iv.write('SENS:VOLT:RSEN ON')
  iv.write('SOUR:FUNC CURR')
  iv.write('SOUR:CURR:RANGE 0.1')
  iv.write('SOUR:CURR:VLIM 10')
  iv.write(f'SOUR:SWE:CURR:LIN {start}, {stop}, {num}, 0.1')
  iv.write('INIT')
  iv.write('*WAI')
  iv.write(f'TRAC:DATA? 1, {num}, "defbuffer1", SOUR, READ')
  iv.close()


def injection():
  iv = dev.Keithley_2450()
  print(iv.query('*IDN?'))
  iv.write('*RST')
  iv.write('SENS:FUNC "VOLT"')
  iv.write('SENS:VOLT:RANG:AUTO ON')
  iv.write('SENS:VOLT:RSEN ON')
  iv.write('SOUR:FUNC CURR')
  iv.write('SOUR:CURR:RANG 0.1')
  iv.write('SOUR:CURR:VLIM 10')
  iv.write('SOUR:CURR 0.05')
  iv.write('OUTP ON')
  data = iv.query('READ?')
  iv.write('OUTP OFF')
  iv.close()

  print(data, len(data))


def detector():
  pd = dev.Keysight_81630B_photodiode()
  for _ in range(10):
    print(pd.fetch(1, 1))
  pd.close()


def laser(filname):
  x = np.linspace(1, 100, 100)
  y = np.zeros_like(x)
  v = np.zeros_like(x)

  iv = dev.Keithley_2450()
  iv.write('*RST')
  iv.write(':SENS:FUNC "VOLT"')
  iv.write(':SENS:VOLT:RANG:AUTO ON')
  iv.write(':SENS:VOLT:RSEN ON')
  iv.write(':SOUR:FUNC CURR')
  iv.write(':SOUR:CURR:RANG 0.1')
  iv.write(':SOUR:CURR:VLIM 10')
  iv.write(':OUTP ON')

  pd = dev.Keysight_81630B_photodiode()
  pd.mW(1, 1)
  for i, current in enumerate(x):
    iv.write(f':SOUR:CURR {np.round(x[i] * 0.001, 3)}')
    v[i] = float(iv.query(':READ?'))
    time.sleep(0.4)
    y[i] = pd.fetch(1, 1) * 1e6
    print(f'{x[i]:.0f} mA, {y[i]:.6f} uW, {v[i]:.3f} V')
  pd.dBm(1, 1)
  pd.close()

  iv.write(':OUTP OFF')
  iv.close()

  data = np.array([x, y, v]).transpose()
  np.savetxt(f'{filname}.dat', data)

  plt.figure(figsize=(10, 6))
  plt.plot(x, y)
  plt.xlabel('Current (mA)')
  plt.ylabel(r'Output power ($\mu$W)')
  plt.grid()
  plt.savefig(f'{filname}.png')
  plt.show()


if __name__ == '__main__':
  laser('D:/data/SOA/3SOA010-3/LI')
