import dev
import numpy as np
import matplotlib.pyplot as plt


def test():
  ld = dev.Thorlabs_ITC_8052()
  # ld.write('*RST')
  # print(ld.query('*IDN?'))
  # ld.write(':tec on')
  # ld.write(':ild:start 0.01')
  ld.write(':ild:set 0.04')
  ld.write(':laser on')
  # print(ld.query(':temp:set?'))
  # print(ld.query(':ild:set?'))
  # print(ld.read(':vld:act?'))
  ld.close()


def laser(filname):
  x = np.linspace(1, 100, 100)
  y = np.zeros_like(x)
  v = np.zeros_like(x)

  ld = dev.Thorlabs_ITC_8052()
  ld.write(f':ild:set {np.round(x[0] * 0.001, 3)}')
  ld.write(':laser on')

  pd = dev.Keysight_81630B_photodiode()
  pd.mW(1, 1)
  for i, current in enumerate(x):
    ld.write(f':ild:set {np.round(x[i] * 0.001, 3)}')
    v[i] = ld.read(':vld:act?')
    y[i] = pd.fetch(1, 1) * 1e6
    print(f'{x[i]:.0f} mA, {y[i]:.6f} uW, {v[i]:.3f} V')
  pd.dBm(1, 1)
  pd.close()

  ld.write(':laser off')
  ld.close()

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
  test()
  # laser('D:/data/SOA/3SOA010-3/thorlabs_no_delay')
