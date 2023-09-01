import dev
import time
import numpy as np

def set_wavelength(wavelength):
  lo = dev.Keysight_N7711A_tunalble_laser()
  print(lo.query('*IDN?'))
  lo.write('WAV ' + str(wavelength) + 'NM')
  lo.close()

def sweep_wavelength():
  lo = dev.Keysight_N7711A_tunalble_laser()
  print(lo.query('*IDN?'))

  wavelength = np.linspace(1530, 1531, 3)

  for k in wavelength:
    lo.write('WAV ' + str(round(k, 1)) + 'NM')
    time.sleep(1)
    w = float(lo.query('WAV?')) * 1e9
    print('Wavelength =', w, 'nm')
  lo.close()

if __name__ == '__main__':
  set_wavelength(1540)
