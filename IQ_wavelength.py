import dev
import time
import numpy as np

def set_wavelength(wavelength):
  lo = dev.Keysight_N7711A_tunalble_laser()
  print(lo.query('*IDN?'))
  lo.write('WAV:AUTO 1')
  lo.write('WAV ' + str(wavelength) + 'NM')
  lo.close()

def sweep_wavelength():
  lo = dev.Keysight_N7711A_tunalble_laser()
  print(lo.query('*IDN?'))
  lo.write('WAV:AUTO 1')

  wavelength = np.linspace(1530, 1531, 3)

  for k in wavelength:
    lo.write('WAV ' + str(round(k, 1)) + 'NM')
    time.sleep(1)
    w = float(lo.query('WAV?')) * 1e9
    print('Wavelength =', w, 'nm')

  lo.close()

def get_data():
  dso = dev.Agilent_DSO1014A_oscilloscope(False)
  dso.write('TIM:FORM YT')
  dso.write('SINGLE')

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
  p = np.arcsin(np.sqrt(1 - k[0] * k[0] / k[1])) * 180 / np.pi

  if k[0] > 0: p = 180 - p

  print('Phase difference =', round(p, 1), 'degree')

if __name__ == '__main__':
  # set_wavelength(1540)
  get_data()
