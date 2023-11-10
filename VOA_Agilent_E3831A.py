import cfg
import dev
import dat
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
  fp = cfg.mkdir(folder) + tp.strftime('%H%M%S')
  print(fp)

  vmin, vmax, vstep = 0, 1.5, 0.02
  v = dat.arange(vmin, vmax, vstep)
  p = np.zeros_like(v)

  vir = dev.Agilent_E3831A_power_supply()
  opm = dev.Keysight_81630B_photodiode()

  print(vir.query('*IDN?'))
  print(opm.query('*IDN?'))

  vir.write('*RST')
  vir.write('INST P6V')
  vir.write('VOLT ' + str(round(vmin, 3)))
  vir.write('OUTP ON')
  vir.write('INIT')
  opm.write('INIT1:CHAN1:CONT 0')
  opm.write('INIT1:CHAN1:IMM')

  for i in range(len(v)):
    v[i] = round(v[i], 3)
    vir.write('VOLT ' + str(v[i]))
    time.sleep(1)
    p[i] = opm.read(1, 1)
    print(v[i], p[i])

  opm.write('INIT1:CHAN1:CONT 1')
  vir.write('VOLT ' + str(round(vmin, 3)))
  vir.write('OUTP OFF')

  vir.close()
  opm.close()

  df = np.array([v, p]).transpose()
  np.savetxt(fp + '.dat', df, fmt='%.3f')

  xt = np.linspace(v[0], v[-1], 5)
  yt = np.linspace(-30, 0, 7)

  plt.figure(dpi=150)
  plt.plot(v, p)
  plt.xlim(xt[0], xt[-1])
  plt.ylim(yt[0], yt[-1])
  plt.xticks(xt)
  plt.yticks(yt)
  plt.grid()
  plt.savefig(fp + '.png')

  return v, p


if __name__ == '__main__':
  voa('EI-ICR-WG-R1-TV23-004/voa/t1/')
