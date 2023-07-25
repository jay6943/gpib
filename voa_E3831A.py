import sys
import dev
import dat
import time
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

def volt():
  vir = dev.Agilent_E3831A_power_supply()

  vir.write('*RST')
  vir.write('INST:COUP:TRIG ALL')
  vir.write('TRIG:SOUR BUS')
  vir.write('TRIG:DEL 5')
  vir.write('INST:SEL P6V')
  vir.write('VOLT:TRIG 1')
  vir.write('OUTP ON')
  vir.write('INIT')
  vir.write('*TRG')
  vir.write('INST:COUP:TRIG NONE')

  vir.close()

def pd():
  opm = dev.opm(20)

  opm.write('*CLS')
  opm.write('INIT1:CHAN1:CONT 0')
  opm.write('INIT1:CHAN1:IMM')

  for _ in range(10): print(opm.query(1, 1))
  for _ in range(10): print(opm.read(1, 1))

  opm.close()

def voa(folder):
  vmin, vmax, vstep = 0, 4, 0.1
  v = dat.arange(vmin, vmax, vstep)
  p = np.zeros_like(v)

  vir = dev.Agilent_E3831A_power_supply()
  opm = dev.opm(20)

  vir.write('*RST')
  vir.write('INST P6V')
  vir.write('VOLT ' + str(round(vmin,1)))
  vir.write('OUTP ON')
  vir.write('INIT')
  opm.write('INIT1:CHAN1:CONT 0')
  opm.write('INIT1:CHAN1:IMM')

  for i in range(len(v)):
    v[i] = round(v[i],1)
    vir.write('VOLT ' + str(v[i]))
    time.sleep(1)
    p[i] = opm.read(1, 1)
    print(v[i], ',', p[i])

  opm.write('INIT1:CHAN1:CONT 1')
  vir.write('VOLT ' + str(round(vmin,1)))
  vir.write('OUTP OFF')

  vir.close()
  opm.close()

  filename = folder + dt.datetime.now().strftime('%H%M%S')
  np.savetxt(filename + '.txt', np.array([v, p]).transpose(), fmt='%.3f')

  xt = np.linspace(v[0], v[-1], 5)
  yt = np.linspace(-30, 0, 7)

  plt.figure(dpi=150)
  plt.plot(v, p)
  plt.xlim(xt[0], xt[-1])
  plt.ylim(yt[0], yt[-1])
  plt.xticks(xt)
  plt.yticks(yt)
  plt.grid()
  plt.savefig(filename + '.png')

  return v, p

if __name__ == '__main__':
  voa('../../data/SIN/EI-ICR-WG-R1-TV22-012/voa/')
