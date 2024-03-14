import dat
import dev
import time
import Standa
import numpy as np
import matplotlib.pyplot as plt


def fiber_align(ports):
  for i in ports:
    print(Standa.title[i])
    axis = Standa.Stage(i)
    axis.find_max(0, 64)
    axis.close()


def axis_move(address, steps, ports):
  axis = Standa.Stage(address)
  axis.shift_on(steps, 0)
  axis.close()

  fiber_align(ports)


def save_spectrum(filename):
  print(filename, end=' ... ')
  osa = dev.Yokogawa_AQ6370D_oscilloscope(False)
  osa.timeout = 50000
  osa.write(':INIT:SMOD SING')
  osa.write(':INIT:IMM')
  x = osa.query(':TRAC:DATA:X? TRA')
  y = osa.query(':TRAC:DATA:Y? TRA')
  time.sleep(2)
  osa.write(':INIT:SMOD REP')
  osa.write(':INIT:IMM')
  osa.close()

  x = x.replace('\n', '').split(',')
  y = y.replace('\n', '').split(',')
  x = np.array(x).astype(float) * 1e9
  y = np.array(y).astype(float)
  x = np.round(x, 9)
  y = np.round(y, 9)

  data = np.array([x, y])
  np.savetxt(filename + '.dat', data.transpose(), fmt='%.3f')

  plt.figure(dpi=150)
  plt.plot(x, y)
  plt.xlabel('Wavelength (nm)')
  plt.ylabel('Output (dBm)')
  plt.xlim(1500, 1600)
  plt.ylim(-80, -20)
  plt.grid()
  plt.savefig(filename + '.png')
  plt.close()

  print('done.')


def PolarER(filename):
  y1 = np.loadtxt(filename + '-1-o.dat')
  y2 = np.loadtxt(filename + '-2-o.dat')

  y1 = y1.transpose()
  y2 = y2.transpose()

  x = y1[0]
  y = y1[1] - y2[1]

  data = np.array([x, y])
  np.savetxt(filename + '-o.dat', data.transpose(), fmt='%.3f')

  plt.figure(dpi=150)
  plt.plot(x, y, label='PER')
  plt.plot(y1[0], y1[1] + 50, label='Port 1')
  plt.plot(y2[0], y2[1] + 50, label='Port 2')
  plt.xlabel('Wavelength (nm)')
  plt.ylabel('Output (dBm)')
  plt.xlim(1500, 1600)
  plt.ylim(-30, 30)
  plt.legend()
  plt.grid()
  plt.savefig(filename + '-o.png')
  plt.close()

def operation():
  folder = dat.get_folder()
  for i in range(17):
    # filename = folder + '/pbs-53-' + str(50 - i * 2)
    filename = folder + '/pbs-53-' + str(18 + i * 2)
    if i > 0: axis_move(0, -80, [2, 3, 5, 6])
    save_spectrum(filename + '-1-o')
    axis_move(5, 80, [5, 6])
    save_spectrum(filename + '-2-o')
    axis_move(5, -80, [])
    PolarER(filename)
  # axis_move(0, -80, [2, 3, 5, 6])


if __name__ == '__main__': operation()
