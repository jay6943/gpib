import cfg
import dev
import time
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


def voltage():
  vir = dev.Agilent_E3831A_power_supply()
  print(vir.query('*IDN?'))

  vir.write('*RST')
  vir.write('INST:COUP:TRIG ALL')
  vir.write('TRIG:SOUR BUS')
  vir.write('TRIG:DEL 5')
  vir.write('INST:SEL P6V')
  vir.write('VOLT:TRIG 0')
  vir.write('OUTP ON')
  vir.write('INIT')
  vir.write('*TRG')
  vir.write('INST:COUP:TRIG NONE')

  vir.close()


def photodide():
  opm = dev.Keysight_81630B_photodiode()

  opm.write('*CLS')
  opm.write('INIT1:CHAN1:CONT 0')
  opm.write('INIT1:CHAN1:IMM')

  for _ in range(10): print(opm.fetch(1, 1))
  for _ in range(10): print(opm.read(1, 1))

  opm.close()


def voa(folder):
  tp = dt.datetime.now()
  fp = f'{cfg.mkdir(folder)}/{tp.strftime('%m-%d-%H%M')}'
  print(fp)

  # vmin, vmax, vstep = 0.4, 1.4, 0.02
  # v = np.round(dat.arange(vmin, vmax, vstep), 3)
  a = [i * 0.1 + 0.5 for i in range(7)]
  b = [(i + 1) * 0.02 + 1.1 for i in range(25)]
  v = np.round(np.array(a + b), 3)
  p = np.zeros_like(v)

  vir = dev.Agilent_E3831A_power_supply()
  opm = dev.Keysight_81630B_photodiode()

  print(vir.query('*IDN?'))
  print(opm.query('*IDN?'))

  vir.write('*RST')
  vir.write('INST P6V')
  vir.write(f'VOLT {v[0]}')
  vir.write('OUTP ON')
  vir.write('INIT')
  opm.write('INIT1:CHAN1:CONT 0')
  opm.write('INIT1:CHAN1:IMM')
  time.sleep(2)

  for i in range(len(v)):
    vir.write(f'VOLT {v[i]}')
    time.sleep(1)
    p[i] = opm.read(1, 1)
    print(v[i], p[i])

  opm.write('INIT1:CHAN1:CONT 1')
  vir.write(f'VOLT {v[0]}')
  vir.write('OUTP OFF')

  vir.close()
  opm.close()

  df = np.array([v, p]).transpose()
  np.savetxt(f'{fp}.dat', df, fmt='%.3f')

  pmin, pmax = np.min(p), np.max(p)
  ex = round(pmax-pmin, 1)

  xt = np.linspace(v[0], v[-1], 11)
  yt = np.linspace(-40, 0, 5)

  plt.figure(dpi=150)
  plt.plot(v, p)
  plt.text(float(v[np.argmin(p)]), pmin-1, f'{ex} dB',
           verticalalignment='top', horizontalalignment='center')
  plt.xlim(xt[0], xt[-1])
  plt.ylim(yt[0], yt[-1])
  plt.xlabel('Voltage (V)')
  plt.ylabel('Output power (dBm)')
  plt.xticks(xt)
  plt.yticks(yt)
  plt.grid()
  plt.savefig(f'{fp}.png')
  plt.show()

  return v, p


def vdraw(folder):
  fp = f'{cfg.mkdir(folder)}/12-05-1047'
  data = np.loadtxt(fp)
  data = data.transpose()
  v, p = data[0], data[1]
  pmin, pmax = np.min(p), np.max(p)
  ex = round(pmax-pmin, 1)

  xt = np.linspace(v[0], v[-1], 11)
  yt = np.linspace(-35, 0, 8)

  plt.figure(dpi=150)
  plt.plot(v, p)
  plt.text(float(v[np.argmin(p)]), pmin-1, f'{ex} dB',
           verticalalignment='top', horizontalalignment='center')
  plt.xlim(xt[0], xt[-1])
  plt.ylim(yt[0], yt[-1])
  plt.xticks(xt)
  plt.yticks(yt)
  plt.grid()
  plt.savefig(f'{fp}.png')


if __name__ == '__main__':
  foldername = 'EI-ICR-WG-R1-TV23-004/voa/t1/'

  voa(foldername)
  # vdraw(foldername)
