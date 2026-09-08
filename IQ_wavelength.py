import cfg
import dev
import time
import numpy as np
import matplotlib.pyplot as plt


def set_wavelength(wavelength):
  lo = dev.Keysight_N7711A_tunalble_laser()
  print(lo.query('*IDN?'))
  lo.write('WAV:AUTO 1')
  lo.write(f'WAV {wavelength}NM')
  lo.close()


def sweep_wavelength():
  lo = dev.Keysight_N7711A_tunalble_laser()
  print(lo.query('*IDN?'))
  lo.write('WAV:AUTO 1')

  wavelength = np.linspace(1530, 1531, 3)

  for k in wavelength:
    lo.write(f'WAV {k:.1f}NM')
    time.sleep(1)
    w = float(lo.query('WAV?')) * 1e9
    print(f'Wavelength = {w} nm')

  lo.close()


def get_data(path):
  dso = dev.Agilent_DSO1014A_oscilloscope(False)
  dso.write('TIM:FORM YT')
  dso.write('SINGLE')
  dso.write(f'TIM:SCAL {100e-6}')

  time.sleep(3)

  m = 4096
  x = dso.getwave(1)
  y = dso.getwave(2)

  dso.write('RUN')
  dso.write('TIM:FORM XY')
  dso.close()

  A = np.arange(float(m * 5)).reshape(5, m)
  B = -x * x

  A[0] = x * y * 2
  A[1] = y * y
  A[2] = x * 2
  A[3] = y * 2
  A[4] = 1

  k = np.dot(B, np.linalg.pinv(A))
  phase = np.arcsin(np.sqrt(1 - k[0] * k[0] / k[1]))
  if k[0] > 0: phase = np.pi - phase
  phase = f'{np.rad2deg(phase):.1f}'

  print(f'Phase difference = {phase} degree')

  plt.figure(dpi=150)
  plt.scatter(x, y, c='b', s=5)
  plt.axis('square')
  plt.title(f'{phase}{cfg.circ}')
  plt.gca().axes.xaxis.set_visible(False)
  plt.gca().axes.yaxis.set_visible(False)
  lim = np.max([np.abs(x), np.abs(y)])
  plt.plot([0, 0], [-lim, lim], 'k:', linewidth='1')
  plt.plot([-lim, lim], [0, 0], 'k:', linewidth='1')
  plt.xlim(-lim, lim)
  plt.ylim(-lim, lim)
  plt.show()


if __name__ == '__main__':
  # set_wavelength(1540)
  get_data('D:/data/SiN/EI-SIN-400-R1-TV26-001/iq')
