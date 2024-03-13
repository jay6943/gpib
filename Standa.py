import dev
import matplotlib.pyplot as plt
import libximc.highlevel as ximc

port = [5, 12, 10, 14, 11, 9, 13, 15]
edge = [20000, 800, 800, 800, 800, 800, 800, 1300]
title = ['linear', 'Xin', 'Yin', 'Zin', 'Xout', 'Yout', 'Zout', 'vertical']
stop = 100


class photodiode:
  def __init__(self):
    self.pd = dev.Keysight_81630B_photodiode()
    self.pd.write('*CLS')
    self.pd.write('INIT1:CHAN1:CONT 0')
    self.pd.write('INIT1:CHAN1:IMM')

  def read(self):
    return self.pd.read(1, 1)

  def close(self):
    self.pd.write('INIT1:CHAN1:CONT 1')
    self.pd.close()


class Stage:
  def __init__(self, address):
    self.address = address
    self.port = port[address]
    self.edge = edge[address]

    self.device = ximc.Axis(r'xi-com:\\.\COM' + str(port[address]))

  def get_position(self):
    self.device.open_device()
    position = str(self.device.get_position()).split()
    self.device.close_device()

    return [position[1], position[3]]

  def get_speed(self):
    self.device.open_device()
    m = self.device.get_move_settings()
    self.device.close_device()

    return str(m.Speed)

  def set_speed(self, speed):
    if speed < 1: speed = 1
    if speed > 2000: speed = 2000

    self.device.open_device()
    m = self.device.get_move_settings()
    m.Speed = speed
    self.device.set_move_settings(m)
    self.device.close_device()

  def set_zero(self):
    self.device.open_device()
    self.device.command_zero()
    self.device.close_device()

  def get_edges(self):
    self.device.open_device()
    edges = str(self.device.get_edges_settings()).split()
    self.device.close_device()

    return [edges[5], edges[9]]

  def go_home(self):
    self.set_speed(1000)
    self.device.open_device()
    self.device.command_home()
    self.device.command_wait_for_stop(stop)
    self.device.close_device()

  def move_to(self, there, microsteps):
    self.set_speed(abs(there - int(self.get_position()[0])) * 2)
    self.device.open_device()
    self.device.command_move(there, microsteps)
    self.device.command_wait_for_stop(stop)
    self.device.close_device()

  def shift_on(self, steps, microsteps):
    self.set_speed(abs(steps) * 2)
    self.device.open_device()
    self.device.command_movr(steps, microsteps)
    self.device.command_wait_for_stop(stop)
    self.device.close_device()

  def scanner(self, steps, microsteps, show):
    x, y, a, b = [i for i in range(33)], [], [], []

    pd = photodiode()

    start = self.get_position()
    self.shift_on(-2, 0)
    for i in x:
      position = self.get_position()
      power = pd.read()
      y.append(power)
      a.append(position[0])
      b.append(position[1])
      print(i, position, power)
      self.shift_on(steps, microsteps)
    imax = y.index(max(y))
    self.move_to(int(start[0]), int(start[1]))

    pd.close()

    if show:
      plt.figure(dpi=120)
      plt.plot(x, y)
      plt.xlabel('Axis position')
      plt.ylabel('Measured power (dBm)')
      plt.grid()
      plt.savefig('../data/scanning.png')
      plt.show()

    return a[imax], b[imax]

  def go_scan_max(self, steps, microsteps):
    steps, microsteps = self.scanner(steps, microsteps, 0)
    self.move_to(int(steps), int(microsteps))

    return steps, microsteps


if __name__ == '__main__':
  axis = Stage(0)
  print(axis.get_position())
