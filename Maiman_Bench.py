import dev
import numpy as np
import matplotlib.pyplot as plt


def test():
    mbl = dev.Maiman_Laser_TEC()
    # mbl.write('curr:value 1')
    # mbl.write('dev:start on')
    # mbl.write('dur:value 1')
    # mbl.write('freq:value 0')
    # mbl.write('tec:temp:value 25')
    mbl.write('dev:blo:ign')
    # print(mbl.read('block?'))
    # print(mbl.read('tec:temp:real?'))
    mbl.close()


def laser(filname):
  x = np.linspace(1, 100, 100)
  y = np.zeros_like(x)
  v = np.zeros_like(x)

  iv = dev.Maiman_Laser_TEC()
  iv.write('*RST')
  iv.write(f'curr:value {np.round(x[0], 3)}')
  iv.write('dev:start on')

  pd = dev.Keysight_81630B_photodiode()
  pd.mW(1, 1)
  for i in range(len(x)):
    iv.write(f'curr:value {np.round(x[i], 3)}')
    v[i] = float(iv.read('volt:real?'))
    y[i] = pd.fetch(1, 1) * 1e6
    x[i] = float(iv.read('curr:real?'))
    print(f'{x[i]:.3f} mA, {y[i]:.6f} uW, {v[i]:.3f} V')
  pd.dBm(1, 1)
  pd.close()

  iv.write('dev:start off')
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
  # laser('D:/data/SOA/3SOA010-3/LIV_real')
  test()
