import cfg
import dev
import dat
import time
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as ani

tp = dt.datetime.now()
fp = cfg.mkdir('EI-ICR-WG-R1-TV23-004/voa/t1/') + tp.strftime('%m-%d-%H%M')
print(fp)

vmin, vmax, vstep = 0, 0.1, 0.02
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


def animate(i):
  vir.write('VOLT ' + str(v[i]))
  time.sleep(1)
  p[i] = opm.read(1, 1)
  print(v[i], p[i])
  plt.cla()
  plt.plot(v[:i], p[:i])

volt = ani.FuncAnimation(plt.gcf(), animate, frames=200, interval=100)
plt.show()

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
