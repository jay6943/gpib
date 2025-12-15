import cfg
import dev
import time
import numpy as np
import datetime as dt
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
  iv.write('SOUR:CURR:RANG 0.1')
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


def set_voa(mA):
  pd = dev.Keysight_81630B_photodiode()
  iv = dev.Keithley_2450()
  iv.write('*RST')
  iv.write(':SENS:FUNC "VOLT"')
  iv.write(':SENS:VOLT:RANG:AUTO ON')
  iv.write(':SENS:VOLT:RSEN ON')
  iv.write(':SOUR:FUNC CURR')
  iv.write(':SOUR:CURR:RANG 1')
  iv.write(':SOUR:CURR:VLIM 10')
  iv.write(':OUTP ON')
  iv.write(f':SOUR:CURR {np.round(mA * 0.001, 3)}')
  time.sleep(1)
  print(float(iv.query(':READ?')), 'V')
  print(float(pd.read(1, 1)), 'dBm')
  # iv.write(':OUTP OFF')
  iv.close()
  pd.close()


def voa(filname):
  c = np.linspace(10, 300, 30)
  d = np.linspace(301, 310, 10)
  x = np.unique(np.concatenate((c, d)))
  y = np.zeros_like(x)
  v = np.zeros_like(x)

  iv = dev.Keithley_2450()
  iv.write('*RST')
  iv.write(':SENS:FUNC "VOLT"')
  iv.write(':SENS:VOLT:RANG:AUTO ON')
  iv.write(':SENS:VOLT:RSEN ON')
  iv.write(':SOUR:FUNC CURR')
  iv.write(':SOUR:CURR:RANG 1')
  iv.write(':SOUR:CURR:VLIM 10')
  iv.write(':OUTP ON')

  pd = dev.Keysight_81630B_photodiode()
  for i, current in enumerate(x):
    iv.write(f':SOUR:CURR {np.round(x[i] * 0.001, 3)}')
    v[i] = float(iv.query(':READ?'))
    time.sleep(0.4)
    y[i] = pd.read(1, 1)
    print(f'{x[i]:3.0f} mA, {y[i]:10.3f} dBm, {v[i]:6.3f} V')
  pd.close()

  iv.write(':OUTP OFF')
  iv.close()

  data = np.array([x, y, v]).transpose()
  np.savetxt(f'{filname}.dat', data)
  plt.figure(figsize=(10, 6))
  plt.plot(x * v, y)
  plt.xlabel('Power (mW)')
  plt.ylabel('Output power (dBm)')
  plt.grid()
  plt.savefig(f'{filname}_watt.png')
  plt.close()
  plt.figure(figsize=(10, 6))
  plt.plot(x, y)
  plt.xlabel('Current (mA)')
  plt.ylabel('Output power (dBm)')
  plt.grid()
  plt.savefig(f'{filname}_current.png')
  plt.show()


if __name__ == '__main__':
  # set_voa(0)
  at = dt.datetime.now()
  voa(f'{cfg.path}/voa/10w_{at.strftime('%H%M%S')}')
